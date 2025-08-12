from env import DEBUG

def log(msg, data = None, ignore_debug=False):
    if not ignore_debug and not DEBUG:
        return

    if data:
        print(msg, data)
    else:
        print(msg)