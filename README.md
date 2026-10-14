# oss-list-submit

Helps an open-source project find the right awesome lists, MCP registries and developer directories: it checks entry requirements, writes submission drafts, and notifies you when a PR is merged. Works with Claude Code, Codex and Cursor.

## Install

**Universal (recommended)**: one command installs it into Claude Code, Codex and Cursor at once. Requires Node.js on your machine.

```bash
npx skills add 1021ju/oss-list-submit -g -a '*' -y
```

Update with `npx skills update oss-list-submit`. To install into just one tool, replace `-a '*'` with `-a claude-code`, `-a codex` or `-a cursor`.

**No Node? Use each tool's native method:**

| Tool | How to install |
|---|---|
| Claude Code | In Claude Code, type `/plugin install oss-list-submit --marketplace 1021ju/oss-list-submit` |
| Codex | Tell Codex: `$skill-installer install https://github.com/1021ju/oss-list-submit/tree/main/skills/oss-list-submit` |
| Cursor | Use the universal command above |

Pick only one method. Using both gives you two skills with the same name in Claude Code.

**Prerequisite**: install and log in to [`gh`](https://cli.github.com/) (`gh auth login`). No paid tools or API keys needed.

Optional: if the agent has a browser tool (Claude in Chrome, Codex's built-in browser use, Cursor's browser tools), it fills in directory forms for you. Without one, it lists the copy for you to paste yourself. If you install `terminal-notifier` (`brew install terminal-notifier`), clicking a merge notification opens the PR.

## How to use

Just tell the agent:

> Submit https://github.com/<org>/<repo> to the awesome lists and directories that fit it

The agent works in this order:

1. **Builds a project profile**: star count, repo age, license, category, and whether the company website has a page for the project.
2. **Finds lists and checks requirements**: whether the list is archived, whether anything was merged recently, how big the PR backlog is, whether it takes only PRs or only issues, the hard requirements in CONTRIBUTING and CI, and whether someone already submitted the project.
3. **Writes drafts in each list's format**: entries, PR or issue bodies, directory forms and posts, all following the built-in rules against AI-sounding copy.
4. **Screens backlink directories** with five checks: price, topic fit, whether people search for the site by name, whether new pages from the last 7 days are indexed, and whether similar projects use it.
5. **Submits with your own account**: if `gh` is logged in on your machine, you look over the batch of drafts once and say yes, then the agent submits them all and only comes back to you if it gets stuck. If you'd rather not log in, it gives you pre-filled links to open and submit. The agent never uses a bot account.
6. **Records everything in `~/.oss-list-submit/submissions.csv`**.
7. **(Optional) Installs a scheduled watcher**: a system scheduled task on your machine that checks every 6 hours and shows a system notification when a PR is merged, closed, or a maintainer replies. It keeps running when the agent is closed.

## Why only 3–5 per day

Maintainers of awesome lists treat a burst of PRs as spam and may block the account outright, and the whole organization can suffer for it. Using the author's own account, one PR per list, spread over several days, gets far more accepted.
