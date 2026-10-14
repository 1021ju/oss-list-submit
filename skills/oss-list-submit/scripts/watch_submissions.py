# -*- coding: utf-8 -*-
"""Check every GitHub PR/issue in the submissions tracker and notify on changes.

Tracker:  ~/.oss-list-submit/submissions.csv   (header = references/tracker-template.csv)
State:    ~/.oss-list-submit/state.json

Usage: python3 watch_submissions.py [--dry-run]
Only needs python3 (stdlib) and a logged-in `gh`.
"""
import csv
import datetime
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys

HOME = os.environ.get("OSS_LIST_SUBMIT_HOME") or os.path.expanduser("~/.oss-list-submit")
TRACKER = os.path.join(HOME, "submissions.csv")
STATE = os.path.join(HOME, "state.json")
LOG = os.path.join(HOME, "watch.log")
LINK_RE = re.compile(r"https://github\.com/([^/\s]+)/([^/\s]+)/(pull|issues)/(\d+)")
DRY = "--dry-run" in sys.argv
TIMEOUT = 120  # seconds per gh / notifier call, so a stalled call can't hang the scheduled run
PENDING = "merged (entry not found in README yet)"


def log(msg):
    line = "%s %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), msg)
    print(line)
    if not DRY:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def gh_json(args):
    out = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=TIMEOUT)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[:300])
    return json.loads(out.stdout)


def readme_has(list_repo, needle):
    out = subprocess.run(
        ["gh", "api", "repos/%s/readme" % list_repo, "-H", "Accept: application/vnd.github.raw"],
        capture_output=True, timeout=TIMEOUT)
    text = out.stdout.decode("utf-8", "replace")
    return out.returncode == 0 and needle.lower() in text.lower()


def write_atomic(path, write):
    """Write to a temp file and rename, so an interrupted run never leaves a half-written file."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig" if path.endswith(".csv") else "utf-8", newline="") as f:
        write(f)
    os.replace(tmp, path)


def load_state():
    if not os.path.exists(STATE):
        return {}
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except ValueError:
        log("state.json is unreadable, starting a fresh baseline")
        return {}


def notify(title, body, url):
    log("[notify] %s | %s" % (title, body))
    if DRY:
        return
    if shutil.which("terminal-notifier"):  # optional: clicking the notification opens the PR
        subprocess.run(["terminal-notifier", "-title", title, "-message", body, "-open", url],
                       capture_output=True, timeout=TIMEOUT)
    elif sys.platform == "darwin":
        script = 'display notification %s with title %s' % (json.dumps(body), json.dumps(title))
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=TIMEOUT)
    elif shutil.which("notify-send"):
        subprocess.run(["notify-send", title, body], capture_output=True, timeout=TIMEOUT)


def check(row):
    """Return (snapshot dict, our repo needle) for one tracker row, or None if no GitHub link."""
    m = LINK_RE.search(row.get("receipt_url", ""))
    if not m:
        return None
    owner, repo, kind, num = m.groups()
    url = m.group(0)
    if kind == "pull":
        d = gh_json(["pr", "view", url, "--json", "state,mergedAt,author,comments,reviews"])
    else:
        d = gh_json(["issue", "view", url, "--json", "state,stateReason,author,comments"])
    me = d["author"]["login"]
    others = [c for c in d.get("comments", []) + d.get("reviews", [])
              if (c.get("author") or {}).get("login") != me]
    snap = {"url": url, "list": "%s/%s" % (owner, repo), "kind": kind,
            "state": d["state"], "reason": d.get("stateReason") or "",
            "others": len(others)}
    target = row.get("target_url", "")
    needle = re.sub(r"^https?://(www\.)?", "", target).rstrip("/")  # "" = can't check the README
    return snap, needle


def listed_status(snap, needle):
    if not needle:
        return "merged (target_url is empty, check the README by hand)"
    return "live" if readme_has(snap["list"], needle) else PENDING


def process(row, state, today):
    """Handle one tracker row. Returns True if the row's status changed."""
    got = check(row)
    if not got:
        return False
    snap, needle = got
    old = state.get(snap["url"])
    who = row.get("submitter", "")
    name = "%s (%s%s)" % (snap["list"], row.get("project", ""), ", submitter " + who if who else "")
    if old is None:
        # First time seen: if still open, just record a baseline; if already merged/closed, go through the notification and status update below as usual
        old = {"state": "OPEN", "others": snap["others"]}
        if snap["state"] == "OPEN":
            state[snap["url"]] = snap
            return False

    accepted = snap["state"] == "MERGED" or (snap["kind"] == "issues" and snap["state"] == "CLOSED"
                                             and snap["reason"] == "COMPLETED")
    status = None
    if snap["state"] != old["state"]:
        if accepted:
            status = listed_status(snap, needle)
            notify("🎉 " + ("PR merged" if snap["kind"] == "pull" else "Issue resolved"),
                   "%s → %s\n%s" % (name, status, snap["url"]), snap["url"])
        elif snap["state"] == "CLOSED":
            status = "rejected (closed without merging)"
            notify("PR/issue closed", "%s was not accepted, check why\n%s" % (name, snap["url"]), snap["url"])
    elif accepted and row.get("status") == PENDING:
        # Many lists regenerate the README some time after the merge: keep checking until the entry shows up
        if listed_status(snap, needle) == "live":
            status = "live"
            notify("Entry is live", "%s now shows the entry in its README\n%s" % (name, snap["url"]), snap["url"])
    elif snap["others"] > old.get("others", 0):
        notify("Maintainer replied", "%s has a new reply or review, remember to respond\n%s" % (name, snap["url"]), snap["url"])
    state[snap["url"]] = snap
    if status and row.get("status") != status:
        row["status"], row["checked_on"] = status, today
        return True
    return False


def main():
    if not os.path.exists(TRACKER):
        print("Tracker %s not found. Record submissions first (skill step 6)." % TRACKER)
        return
    state = load_state()
    with open(TRACKER, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    today = datetime.date.today().isoformat()
    changed = False

    for row in rows:
        try:
            changed = process(row, state, today) or changed
        except Exception as e:  # one bad row must not stop the others or lose their updates
            log("Check failed %s: %s" % (row.get("receipt_url", ""), e))

    if DRY:
        log("dry-run: check finished, no files written")
        return
    write_atomic(STATE, lambda f: json.dump(state, f, ensure_ascii=False, indent=1))
    if changed:
        def write_rows(f):
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        write_atomic(TRACKER, write_rows)


if __name__ == "__main__":
    os.makedirs(HOME, exist_ok=True)
    lock = open(os.path.join(HOME, "watch.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit("Another check is still running, skipping this one")
    main()
