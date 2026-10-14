# -*- coding: utf-8 -*-
"""Check every GitHub PR/issue in the submissions tracker and notify on changes.

Tracker:  ~/.oss-list-submit/submissions.csv   (header = references/tracker-template.csv)
State:    ~/.oss-list-submit/state.json
Config:   ~/.oss-list-submit/config            (optional, KEY=VALUE lines)
          NOTIFY_WEBHOOK=<飞书/Lark 或 Slack incoming webhook URL>

Usage: python3 watch_submissions.py [--dry-run]
Only needs python3 (stdlib) and a logged-in `gh`.
"""
import csv
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

HOME = os.environ.get("OSS_LIST_SUBMIT_HOME") or os.path.expanduser("~/.oss-list-submit")
TRACKER = os.path.join(HOME, "submissions.csv")
STATE = os.path.join(HOME, "state.json")
CONFIG = os.path.join(HOME, "config")
LOG = os.path.join(HOME, "watch.log")
LINK_RE = re.compile(r"https://github\.com/([^/\s]+)/([^/\s]+)/(pull|issues)/(\d+)")
DRY = "--dry-run" in sys.argv


def log(msg):
    line = "%s %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), msg)
    print(line)
    if not DRY:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def gh_json(args):
    out = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[:300])
    return json.loads(out.stdout)


def readme_has(list_repo, needle):
    out = subprocess.run(
        ["gh", "api", "repos/%s/readme" % list_repo, "-H", "Accept: application/vnd.github.raw"],
        capture_output=True, text=True)
    return out.returncode == 0 and needle.lower() in out.stdout.lower()


def load_config():
    cfg = {}
    if os.path.exists(CONFIG):
        for line in open(CONFIG, encoding="utf-8"):
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    return cfg


def notify(title, body, cfg):
    log("[通知] %s | %s" % (title, body))
    if DRY:
        return
    if sys.platform == "darwin":
        script = 'display notification %s with title %s' % (json.dumps(body), json.dumps(title))
        subprocess.run(["osascript", "-e", script], capture_output=True)
    elif shutil.which("notify-send"):
        subprocess.run(["notify-send", title, body], capture_output=True)
    hook = cfg.get("NOTIFY_WEBHOOK")
    if hook:
        text = "%s\n%s" % (title, body)
        if "feishu" in hook or "larksuite" in hook:
            payload = {"msg_type": "text", "content": {"text": text}}
        else:
            payload = {"text": text}
        req = urllib.request.Request(hook, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=15).read()
        except Exception as e:  # webhook 失败不影响本地通知
            log("webhook 发送失败: %s" % e)


def check(row):
    """Return (snapshot dict, our repo needle) for one tracker row, or None if no GitHub link."""
    m = LINK_RE.search(row.get("PR或表单回执链接", ""))
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
    target = row.get("指向的URL", "")
    needle = re.sub(r"^https?://(www\.)?", "", target).rstrip("/") or url
    return snap, needle


def main():
    if not os.path.exists(TRACKER):
        print("没有找到提交记录 %s，先按 skill 第 6 步记录提交。" % TRACKER)
        return
    cfg = load_config()
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    with open(TRACKER, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    today = datetime.date.today().isoformat()
    changed = False

    for row in rows:
        try:
            got = check(row)
        except Exception as e:
            log("查询失败 %s: %s" % (row.get("PR或表单回执链接", ""), e))
            continue
        if not got:
            continue
        snap, needle = got
        old = state.get(snap["url"])
        name = "%s（%s）" % (snap["list"], row.get("项目", ""))
        if old is None:
            # 第一次见到：还开着就只记基线；已经合并/关闭的照常走下面的通知和状态更新
            old = {"state": "OPEN", "others": snap["others"]}
            if snap["state"] == "OPEN":
                state[snap["url"]] = snap
                continue

        if snap["state"] != old["state"]:
            if snap["state"] == "MERGED" or (snap["kind"] == "issues" and snap["state"] == "CLOSED"
                                            and snap["reason"] == "COMPLETED"):
                listed = readme_has(snap["list"], needle)
                status = "已上线" if listed else "已合并（README 里还没找到条目）"
                notify("🎉 " + ("PR 已合并" if snap["kind"] == "pull" else "issue 已处理"),
                       "%s → %s\n%s" % (name, status, snap["url"]), cfg)
            elif snap["state"] == "CLOSED":
                status = "被拒（关闭未合并）"
                notify("PR/issue 被关闭", "%s 没有被收录，去看看原因\n%s" % (name, snap["url"]), cfg)
            else:
                status = row.get("状态", "")
            if status and row.get("状态") != status:
                row["状态"], row["复核日期"], changed = status, today, True
        elif snap["others"] > old.get("others", 0):
            notify("维护者回复了", "%s 有新的回复或 review，记得回\n%s" % (name, snap["url"]), cfg)
        state[snap["url"]] = snap

    if DRY:
        log("dry-run：检查完成，没有写入任何文件")
        return
    json.dump(state, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if changed:
        with open(TRACKER, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    os.makedirs(HOME, exist_ok=True)
    main()
