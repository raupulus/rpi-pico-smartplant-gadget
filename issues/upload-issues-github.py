#!/usr/bin/env python3
"""
Upload GitHub issues from JSON files in issues/json/.

Usage:
  python issues/upload-issues-github.py --repo owner/repo [--token <token>] [--issues-dir issues/json] [--base-url https://api.github.com] [--dry-run] [--force-create]

Environment variables:
  GITHUB_TOKEN   Personal access token (if --token not provided)
  GITHUB_REPO    Default owner/repo (if --repo not provided)
  GITHUB_API_URL Base API URL (default https://api.github.com)

Notes:
  - By default, the script attempts to avoid duplicates by skipping files whose title already exists in the repository (state=all).
  - Labels: Only existing repository labels are used by default. Unknown labels in the JSON are ignored to keep a small curated set.
    - A small mapping is applied: "documentation" -> "docs".
    - If the JSON contains a "status" field (e.g., "todo"), a label "status:<value>" is added if it exists on the repo.
  - Use --force-create to create issues even if one with the same title exists (may create duplicates).
  - Use --dry-run to preview actions without making API calls.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Tuple


# ------------------------ Helpers ------------------------

def http_request(method: str, url: str, token: str, data: Optional[dict] = None) -> Tuple[int, dict, dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "smartplant-scripts/1.0",
        "Authorization": f"Bearer {token}",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.getcode()
            resp_body = resp.read().decode("utf-8")
            try:
                payload = json.loads(resp_body) if resp_body else {}
            except json.JSONDecodeError:
                payload = {}
            return status, payload, dict(resp.headers)
    except urllib.error.HTTPError as e:
        resp_body = e.read().decode("utf-8")
        try:
            payload = json.loads(resp_body) if resp_body else {}
        except json.JSONDecodeError:
            payload = {"message": resp_body}
        return e.code, payload, dict(e.headers or {})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload issues to GitHub from JSON files")
    parser.add_argument("--repo", "-r", default=os.getenv("GITHUB_REPO"), help="GitHub repository in the form owner/repo")
    parser.add_argument("--token", "-t", default=os.getenv("GITHUB_TOKEN"), help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--issues-dir", default="issues/json", help="Directory containing issue JSON files")
    parser.add_argument(
        "--base-url",
        default=os.getenv("GITHUB_API_URL", "https://api.github.com"),
        help="Base GitHub API URL",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not perform changes, just print actions")
    parser.add_argument(
        "--force-create",
        action="store_true",
        help="Create issues even if there is an existing one with the same title",
    )
    parser.add_argument(
        "--create-missing-labels",
        action="store_true",
        help="Create labels that are referenced in JSON but not present in the repository",
    )
    return parser.parse_args()


# ------------------------ GitHub Data Fetch ------------------------

def get_existing_labels(base_url: str, repo: str, token: str) -> Dict[str, str]:
    """Return existing labels as dict mapping lowercased name -> canonical name."""
    result: Dict[str, str] = {}
    url = f"{base_url}/repos/{repo}/labels?per_page=100"
    while url:
        status, payload, headers = http_request("GET", url, token)
        if status != 200:
            raise RuntimeError(f"Failed to list labels ({status}): {payload}")
        for item in payload:
            name = item.get("name", "")
            if name:
                result[name.lower()] = name
        link = headers.get("Link")
        next_url = None
        if link:
            parts = [p.strip() for p in link.split(",")]
            for p in parts:
                if 'rel="next"' in p:
                    start = p.find("<")
                    end = p.find(">")
                    if start != -1 and end != -1:
                        next_url = p[start + 1 : end]
                        break
        url = next_url
    return result


def get_existing_issues_titles(base_url: str, repo: str, token: str) -> Dict[str, int]:
    """Return dict mapping lowercased title -> issue_number for state=all (open+closed)."""
    titles: Dict[str, int] = {}
    page = 1
    while True:
        url = f"{base_url}/repos/{repo}/issues?state=all&per_page=100&page={page}"
        status, payload, _ = http_request("GET", url, token)
        if status != 200:
            raise RuntimeError(f"Failed to list issues ({status}): {payload}")
        if not payload:
            break
        for item in payload:
            # Skip PRs (issues API returns PRs too when state=all)
            if "pull_request" in item:
                continue
            title = (item.get("title") or "").strip()
            number = item.get("number")
            if title and isinstance(number, int):
                titles[title.lower()] = number
        page += 1
    return titles


# ------------------------ Issue Composition ------------------------

def map_labels(raw_labels: List[str], status_value: Optional[str], existing_label_map: Dict[str, str]) -> List[str]:
    """Map JSON labels to repo labels using a minimal curated set.

    - Map 'documentation' -> 'docs'
    - Add 'status:<value>' if provided and exists
    - Include only labels that exist in the repository (case-insensitive)
    """
    mapped: List[str] = []
    for l in raw_labels or []:
        if not l:
            continue
        name = l
        if l.lower() == "documentation":
            name = "docs"
        canonical = existing_label_map.get(name.lower())
        if canonical and canonical not in mapped:
            mapped.append(canonical)
    if status_value:
        status_label = f"status:{status_value.strip().lower()}"
        canonical = existing_label_map.get(status_label.lower())
        if canonical and canonical not in mapped:
            mapped.append(canonical)
    return mapped


def compose_body(issue: dict) -> str:
    body = issue.get("body") or ""
    parts = [body.strip()]

    ac = issue.get("acceptance_criteria") or []
    if isinstance(ac, list) and ac:
        parts.append("\n\n### Acceptance criteria\n")
        for item in ac:
            parts.append(f"- {item}")

    tasks = issue.get("tasks") or []
    if isinstance(tasks, list) and tasks:
        parts.append("\n\n### Tasks\n")
        for t in tasks:
            if isinstance(t, dict):
                desc = t.get("description") or ""
                done = t.get("done") is True
                checkbox = "[x]" if done else "[ ]"
                parts.append(f"- {checkbox} {desc}")
            else:
                parts.append(f"- [ ] {t}")

    meta_bits = []
    if issue.get("priority"):
        meta_bits.append(f"priority: {issue.get('priority')}")
    if issue.get("status"):
        meta_bits.append(f"status: {issue.get('status')}")
    if meta_bits:
        parts.append("\n\n_" + ", ".join(meta_bits) + "_")

    return "\n".join(parts).strip()


# ------------------------ Main ------------------------

def main() -> int:
    args = parse_args()
    repo = args.repo
    token = args.token
    base_url = args.base_url.rstrip("/")

    if not repo:
        print("Error: --repo or GITHUB_REPO is required (owner/repo)", file=sys.stderr)
        return 2
    if not token:
        print("Error: --token or GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    # Load existing labels and issues for idempotency and label filtering
    try:
        existing_labels = get_existing_labels(base_url, repo, token)
    except Exception as e:
        print(f"Error fetching labels: {e}", file=sys.stderr)
        return 2

    try:
        existing_issues = {} if args.force_create else get_existing_issues_titles(base_url, repo, token)
    except Exception as e:
        print(f"Error fetching existing issues: {e}", file=sys.stderr)
        return 2

    # Read issue files
    files = sorted(glob.glob(os.path.join(args.issues_dir, "*.json")))
    if not files:
        print(f"No issue files found in {args.issues_dir}")
        return 0

    created = 0
    skipped = 0
    errors = 0

    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                issue = json.load(f)
        except Exception as e:
            print(f"Error reading '{path}': {e}", file=sys.stderr)
            errors += 1
            continue

        title = (issue.get("title") or "").strip()
        if not title:
            print(f"Skipping '{path}': missing title", file=sys.stderr)
            skipped += 1
            continue

        if not args.force_create and title.lower() in existing_issues:
            print(f"Skip existing issue (same title): {title}")
            skipped += 1
            continue

        body = compose_body(issue)

        raw_labels = issue.get("labels") or []
        status_value = (issue.get("status") or "").strip().lower() or None

        # Build desired label names (apply small mapping)
        desired_label_names: List[str] = []
        for l in raw_labels:
            if not l:
                continue
            name = "docs" if str(l).lower() == "documentation" else str(l)
            if name not in desired_label_names:
                desired_label_names.append(name)
        if status_value:
            status_label = f"status:{status_value}"
            if status_label not in desired_label_names:
                desired_label_names.append(status_label)

        # Resolve labels to canonical names; optionally create missing
        labels: List[str] = []
        for name in desired_label_names:
            canonical = existing_labels.get(name.lower())
            if canonical:
                if canonical not in labels:
                    labels.append(canonical)
                continue
            if args.create_missing_labels:
                ok = create_label(base_url, repo, token, name, color="ededed", description="", dry_run=args.dry_run)
                if ok:
                    existing_labels[name.lower()] = name
                    labels.append(name)

        payload = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels

        if args.dry_run:
            print(f"[DRY-RUN] Would create issue: title='{title}', labels={labels}, file={os.path.basename(path)}")
            created += 1
            continue

        status, resp, _ = http_request("POST", f"{base_url}/repos/{repo}/issues", token, payload)
        if status in (200, 201):
            number = resp.get("number")
            print(f"Created issue #{number}: {title}")
            created += 1
            # Track to avoid dupes in same run
            existing_issues[title.lower()] = number or 0
        else:
            print(f"Error creating issue from '{path}' (status {status}): {resp}", file=sys.stderr)
            errors += 1

    print(f"Done. created={created}, skipped={skipped}, errors={errors}")
    if args.dry_run:
        print("Note: dry-run was enabled; no changes were made.")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())


# ------------------------ Label Creation Helper ------------------------

def create_label(base_url: str, repo: str, token: str, name: str, color: str = "ededed", description: str = "", dry_run: bool = False) -> bool:
    if dry_run:
        print(f"[DRY-RUN] Would create label: name='{name}', color='{color}', description='{description}'")
        return True
    status, payload, _ = http_request(
        "POST",
        f"{base_url}/repos/{repo}/labels",
        token,
        {"name": name, "color": color, "description": description or None},
    )
    if status in (200, 201):
        return True
    print(f"Failed to create label '{name}' (status {status}): {payload}", file=sys.stderr)
    return False
