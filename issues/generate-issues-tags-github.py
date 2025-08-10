#!/usr/bin/env python3
"""
Generate (and update) GitHub labels from issues/tags.json.

Usage:
  python issues/generate-issues-tags-github.py --repo owner/repo [--token <token>] [--tags-file issues/tags.json] [--base-url https://api.github.com] [--dry-run] [--no-update]

Environment variables:
  GITHUB_TOKEN   Personal access token (if --token not provided)
  GITHUB_REPO    Default owner/repo (if --repo not provided)
  GITHUB_API_URL Base API URL (default https://api.github.com)

Notes:
  - Idempotent: creates missing labels; by default updates color/description if they differ.
  - Use --no-update to only create missing labels and skip updates.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, List, Optional, Tuple


def debug(msg: str):
    print(msg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create/update GitHub labels from a JSON file")
    parser.add_argument("--repo", "-r", default=os.getenv("GITHUB_REPO"), help="GitHub repository in the form owner/repo")
    parser.add_argument("--token", "-t", default=os.getenv("GITHUB_TOKEN"), help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--tags-file", default="issues/tags.json", help="Path to tags JSON file")
    parser.add_argument(
        "--base-url",
        default=os.getenv("GITHUB_API_URL", "https://api.github.com"),
        help="Base GitHub API URL",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not perform changes, just print actions")
    parser.add_argument("--no-update", action="store_true", help="Do not update existing labels (only create missing)")
    return parser.parse_args()


def load_tags(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("tags.json must contain a list of label objects")
    # Basic validation
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Label entry at index {i} must be an object")
        for key in ("name", "color"):
            if key not in item:
                raise ValueError(f"Label entry at index {i} missing required key: {key}")
        # Normalize color (GitHub expects hex without #)
        color = item["color"].lstrip("#").lower()
        if len(color) not in (6, 3):
            raise ValueError(f"Invalid color '{item['color']}' for label '{item.get('name')}'")
        item["color"] = color
    return data


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


def get_all_labels(base_url: str, repo: str, token: str) -> Dict[str, Dict[str, str]]:
    """Return existing labels as a dict keyed by lowercased name."""
    labels: Dict[str, Dict[str, str]] = {}
    url = f"{base_url}/repos/{repo}/labels?per_page=100"
    while url:
        status, payload, headers = http_request("GET", url, token)
        if status != 200:
            raise RuntimeError(f"Failed to list labels ({status}): {payload}")
        for item in payload:
            name = item.get("name", "")
            if not name:
                continue
            labels[name.lower()] = {
                "name": name,
                "color": item.get("color", ""),
                "description": item.get("description") or "",
            }
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
    return labels


def create_label(base_url: str, repo: str, token: str, name: str, color: str, description: str, dry_run: bool) -> bool:
    if dry_run:
        debug(f"[DRY-RUN] Create label: name='{name}', color='{color}', description='{description}'")
        return True
    status, payload, _ = http_request(
        "POST",
        f"{base_url}/repos/{repo}/labels",
        token,
        {"name": name, "color": color, "description": description or None},
    )
    if status in (200, 201):
        return True
    # 422 could be validation error
    debug(f"Failed to create label '{name}' (status {status}): {payload}")
    return False


def update_label(base_url: str, repo: str, token: str, current_name: str, color: str, description: str, dry_run: bool) -> bool:
    if dry_run:
        debug(f"[DRY-RUN] Update label: name='{current_name}', color='{color}', description='{description}'")
        return True
    status, payload, _ = http_request(
        "PATCH",
        f"{base_url}/repos/{repo}/labels/{urllib.parse.quote(current_name, safe='')}",
        token,
        {"color": color, "description": description or None},
    )
    if status in (200, 201):
        return True
    debug(f"Failed to update label '{current_name}' (status {status}): {payload}")
    return False


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

    try:
        desired = load_tags(args.tags_file)
    except Exception as e:
        print(f"Error loading tags file '{args.tags_file}': {e}", file=sys.stderr)
        return 2

    try:
        existing = get_all_labels(base_url, repo, token)
    except Exception as e:
        print(f"Error fetching existing labels: {e}", file=sys.stderr)
        return 2

    created = 0
    updated = 0
    skipped = 0

    for item in desired:
        name = item["name"]
        color = item["color"].lower().lstrip("#")
        description = item.get("description") or ""

        key = name.lower()
        if key not in existing:
            ok = create_label(base_url, repo, token, name, color, description, args.dry_run)
            if ok:
                created += 1
        else:
            if args.no_update:
                skipped += 1
                continue
            current = existing[key]
            needs_update = (current.get("color", "").lower() != color) or (
                (current.get("description") or "") != description
            )
            if needs_update:
                ok = update_label(base_url, repo, token, current["name"], color, description, args.dry_run)
                if ok:
                    updated += 1
            else:
                skipped += 1

    print(f"Done. created={created}, updated={updated}, skipped={skipped}")
    if args.dry_run:
        print("Note: dry-run was enabled; no changes were made.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
