# -*- coding: utf-8 -*-
"""Build a pre-filled GitHub "new issue" link. Whoever opens it and clicks Submit owns the issue.

Usage:
  python3 issue_link.py <owner/list> fields.json
fields.json: {"template": "resource.yml", "title": "...", "<issue-form field id>": "...", ...}
Field ids come from the list's .github/ISSUE_TEMPLATE/*.yml (the `id:` of each input/textarea).
Checkboxes cannot be pre-filled on purpose: the submitter ticks them.
Without a template, use "body" for the issue text.
"""
import json
import sys
import urllib.parse

MAX_URL = 8000  # 浏览器/GitHub 对超长 URL 不可靠，超过就把长字段缩短

repo, path = sys.argv[1], sys.argv[2]
fields = json.load(open(path, encoding="utf-8"))
url = "https://github.com/%s/issues/new?%s" % (
    repo, urllib.parse.urlencode(fields, quote_via=urllib.parse.quote))
if len(url) > MAX_URL:
    sys.exit("链接长度 %d 超过 %d，缩短描述类字段后重试" % (len(url), MAX_URL))
print(url)
