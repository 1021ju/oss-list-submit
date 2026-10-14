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

MAX_URL = 8000  # browsers/GitHub are unreliable with very long URLs; shorten long fields if over this

repo, path = sys.argv[1], sys.argv[2]
fields = json.load(open(path, encoding="utf-8"))
url = "https://github.com/%s/issues/new?%s" % (
    repo, urllib.parse.urlencode(fields, quote_via=urllib.parse.quote))
if len(url) > MAX_URL:
    sys.exit("Link length %d exceeds %d; shorten the description fields and retry" % (len(url), MAX_URL))
print(url)
