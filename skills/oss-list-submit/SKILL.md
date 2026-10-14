---
name: oss-list-submit
description: Use when someone wants to promote a company open-source GitHub project by getting it into awesome-xxx lists, MCP/agent registries, developer directories or free backlink sites; or asks "submit to awesome list", "list my repo", "get more stars", "提交 awesome 列表", "开源项目推广", "上列表", "外链目录".
---

# Getting an open-source project onto lists / backlink submissions

Reply to the user in the language they write in; write submissions in the language each platform uses.

Submit one open-source project to the awesome lists, registries and directories that fit it, and record the real status of each one. **The agent finds channels, screens them, writes drafts and verifies results; PRs and forms are submitted with the project author's own account.**

## Tool mapping (one skill for Claude Code / Codex / Cursor)

| Need | Claude Code | Codex | Cursor |
|---|---|---|---|
| GitHub queries, opening PRs, scheduled watcher | `gh` CLI | `gh` CLI | `gh` CLI |
| Opening directory sites, filling forms, checking `href` | Claude in Chrome extension | Codex's built-in browser use, or another installed browser plugin (such as [Tabgent](https://github.com/FibonaAI/tabgent)) | Cursor's built-in browser tools (if enabled) |

For reading public pages and checking `href`, plain `curl` also works.

This skill does not depend on any paid SEO tool or API key. Before starting, confirm three things: whether `gh` works, whether there is network access, and whether there is a browser tool that **can click and fill forms** (one that can only search or read pages does not count). Without a browser tool that can fill forms, only write the copy for directories and let a person fill them in.

## Three hard rules

1. **No bulk submissions on someone's behalf.** Do not use a company bot or shared account to open PRs on many lists in a short time. Maintainers treat this as spam and close the PRs or even block the account, and the whole organization suffers afterward. Many lists explicitly reject automated/AI-generated PRs. Open only one PR per list, submitted through the author's own `gh` login, or hand the draft to the author to open by hand; no more than 3–5 per day from the same account. The same applies if the user asks to "submit everything today": explain why, save the rest as drafts, and continue another day.
2. **Decide where the link points first.** A link to `github.com/...` adds authority to GitHub, not directly to the company domain. Awesome lists by convention link to the repo, so do that. For directories and registries that allow a website field, prefer the project page on the company domain (for example `<company domain>/oss/<slug>`); if there is no project page, use the repo and note in the report "this backlink does not benefit the company domain".
3. **Submitted ≠ live.** An opened PR or a sent form is recorded only as "submitted". Record it as "live" only when the PR is merged and the entry is visible in the list, or the directory page is publicly reachable and its `href` points to the right place.

## Workflow

### 1. Project profile (read existing info first, then ask for what's missing)

Repo URL, one-line positioning (≤ 15 English words), category (MCP server / agent / CLI / library + language), star count, first commit date, license, whether the company domain has a project page, and the submitter's GitHub account.

Repo age, star count and license are entry requirements for many lists:

```bash
O=<owner>; P=<repo>
gh api repos/$O/$P --jq '{stars:.stargazers_count, license:.license.spdx_id, homepage, topics, private}'
gh api -i "repos/$O/$P/commits?per_page=1" | grep -i '^link:'      # take page=N from rel="last"
gh api "repos/$O/$P/commits?per_page=1&page=N" --jq '.[0].commit.committer.date'   # first commit date
gh api users/$O --jq .blog                                          # organization website (organizations also use the users/ endpoint)
```

**Pre-check: is the repo ready to submit right now?**
- **Hard blockers** (repo not public, no license, no install instructions): tell the author what to add, do only read-only research and drafts, and do not submit.
- **Easy fixes** (old wording like private / WIP left in the README, no topics, no homepage set): list them for the author and suggest fixing before submitting; if the author says not to fix them, you can continue.

### 2. Find awesome lists and check activity

Use `gh search repos "awesome <category keyword>" --sort stars` plus the seed lists in `references/channels.md`. Check each of the following for every candidate list. If any check fails, skip the list and write down why:

```bash
L=<owner/list>; R=<our repo name>
gh repo view $L --json isArchived                                              # archived? (pushedAt includes pushes to any branch, so it is not a maintenance signal)
gh api "repos/$L/commits?per_page=1" --jq '.[0].commit.committer.date'         # last commit on the default branch (for a list repo this is basically the last merge)
gh api "search/issues?q=repo:$L+is:pr+is:merged+merged:>=<date 90 days ago>&per_page=1" --jq .total_count  # PRs merged in the last 90 days
gh api "search/issues?q=repo:$L+is:pr+is:open&per_page=1" --jq .total_count      # real number of open PRs (gh pr list -L truncates)
gh pr list -R $L --state open --search "sort:created-asc" -L 1 --json createdAt --jq '.[0].createdAt'  # oldest open PR
gh api "repos/$L/contents/.github/workflows" --jq '.[].name'   # Not Found (HTTP 404) = no CI; retry on 403, rate limits or other errors, don't treat them as "no CI". If there are workflows, read each YAML file and the scripts/configs it references
gh api repos/$L/contents/README.md -H "Accept: application/vnd.github.raw" > /tmp/list-readme.md && { grep -i $R /tmp/list-readme.md || echo "not in README"; }  # duplicate check in README (the raw header is required above 1MB); large files sometimes cut off mid-download (unexpected EOF), which won't falsely report "not in README", so just retry. If the list is split across several files, check those files too
gh search prs --repo $L $R --json number,state,author; gh search issues --repo $L $R --json number,state  # duplicate check on existing PRs/issues
```

| Check | When it fails |
|---|---|
| Archived | `isArchived: true` → skip |
| Maintained | Last commit more than 90 days ago and no PRs merged in the last 90 days → skip. If 0 PRs were merged in 90 days but there are recent commits (the maintainer may push directly), note it and tell the author |
| Submission channel | First confirm whether the list accepts outside PRs: read CONTRIBUTING and the issue templates. Some lists take only issues (outside PRs get blocked). Write the draft for whatever channel it actually uses. If both PRs and forms are open, pick the one CONTRIBUTING recommends; if it doesn't say, pick a PR so progress is visible |
| Backlog | Not a reason to skip on its own. Tell the author the count and the oldest date as they are, and don't convert that into "it will take N days". If the oldest open PR is more than six months old and almost all recent merges are the maintainer's own PRs, write "likely won't get through" and let the author decide whether to submit. For issue-only lists, look at the issue queue |
| Entry requirements | CONTRIBUTING, PR/issue templates, and the scripts and configs CI references (don't go by file names alone). If requirements for stars, repo age, license, badges, manifests and so on aren't met, skip and write "can submit after adding X". If the requirement is vague (for example "no very new projects"), give the author the exact wording and let them decide |
| Fit | Put it in the same section where similar projects are listed; if there is no suitable section, skip. Don't force it in |
| Duplicate | Already in the README, or there is already an open PR/issue (no matter who opened it) → skip. Don't submit twice |

This step only checks and reports. Changing our own repo (adding topics, editing the README, adding badges, etc.) is a separate action, so ask the author first.

### 3. Draft awesome entries

Copy the **format** of the list's existing entries exactly: link style, description length, ending punctuation, emoji and badges. **Don't copy the wording**: if neighboring entries use marketing words like "AI-powered", ours still follows the "Copy rules" at the end. Formats the list explicitly requires (for example, the separator must be a dash) follow the list, which takes priority over our punctuation rules. Choose icons for language, deployment method and so on based on what the repo actually does; if you don't know, check, don't guess.

- **Section**: when similar projects are spread across several sections, pick the one closest to what ours does, explain why in the draft, and let the author confirm.
- **Insertion point**: if the section is sorted alphabetically, insert alphabetically; if it isn't sorted, add at the end.
- **PR template**: fill in the title and body from the template, and go through each checkbox one by one. Only tick ones that are true; never tick them all.
- **Follow the list's rules on AI**: if the list explicitly rejects AI-generated PRs or descriptions, ask the author to write the description themselves before submitting, or skip. Submitting with the author's account does not exempt it. If the list has a specific label or channel for AI-assisted submissions, mark it as required.

Write a separate draft for each list. For issue-only lists, follow their issue template, mark the confirmation items according to whether they're true, and show the submitter which ones are ticked in the batch confirmation in step 5:

```
List: <owner/repo>  Section: <section>  Insert at: <between which two entries>
Entry: - [name](url) - Description.
PR title: ...
PR body: ...
```

### 4. Backlinks / directories: screen them first

**Start with `references/directories.md`**: it is a verified, tiered list. Pick tiers by project type. Tier 1 is for every project, but wait to post Show HN until the project installs with one command or can be tried online and the README is clear; skip it before then. AI/agent, MCP and skill projects add the matching tiers; Chinese channels depend on whether the team wants them; launch-day channels are as needed. For rows marked "unverified", fill them in while submitting; for rows not verified in over 3 months, first confirm the submission page still exists. With no browser and no way to see the form, write copy for the common fields (name, one-line intro, full description, URL, category, tags, logo, screenshots) and note "fields depend on the actual form".

For new sites not on the list, ignore DR (Domain Rating) and run only the five checks below. Mark anything you can't check as "not checked"; it does not count as a pass. Add sites that pass to `directories.md`:

| Check | How to check | Criteria |
|---|---|---|
| Price | Open the submission page | What the free option includes; list expedited, featured and paid listings separately. A zero-budget task does not get upgraded to paid |
| Topic fit | Look at similar entries on the site | It has developer, AI or open-source tool categories, and our project doesn't look out of place there |
| Do people search for the site by name | `curl -s "https://suggestqueries.google.com/complete/search?client=firefox&q=<site name>"` (Google autocomplete, no key needed) | Brand searches like "site name + reviews / login / alternative / submit" in the suggestions point toward a real site; if it only suggests the site name itself or unrelated terms, be more careful. This is a weak signal: small real sites may have no suggestions, so don't reject a site on this alone |
| Are new pages from the last 7 days indexed | `site:<domain>` with Google's "Past week" filter, or search for a recently listed entry page | If new pages get indexed within a week, our entry has a chance to be seen |
| Do similar projects use it | Search the directory for 1–2 good similar open-source projects by name, or look for "Featured on" badges in their READMEs | If similar projects are listed there, the channel is credible |

Also, after an entry goes live, record the link's `rel`. `nofollow` is not a failure; just record it as is. `noopener noreferrer` is not the same as `nofollow`.

### 5. Submitting (always with the submitter's own GitHub account)

First run `gh api user --jq .login` to see who is logged in on this machine:

- Logged in as the submitter account recorded in step 1 → Method A.
- `gh` not installed, not logged in, or logged in as someone other than the submitter → ask first, for example: "Do you want to log in to your own GitHub? Once you're logged in I can submit these for you, so you won't have to click each link." If the user agrees, have them run `gh auth login` (in Claude Code they can type `! gh auth login`) and approve in the browser, then use Method A. If the user doesn't want to log in, or the agent runs in the cloud and can only use its own account → Method B.

**A. Local `gh` is logged in to the submitter's own account: confirm the batch once, then the agent submits everything**

1. Show the user the whole batch of PRs/issues at once: list, section, exact entry text, title and body, which confirmation items are ticked, and which ones go out today. Once the user says yes, start and don't ask about each one again. The approval covers only this batch; new lists need separate confirmation.
2. The agent submits them one by one:
   - Lists that take PRs: `gh repo fork <list> --clone=false`, create a branch in the fork, change that one line, then `gh pr create -R <list>`.
   - Issue-only lists: `gh issue create -R <list>`; if the list uses an issue form, build the body from the form fields.
3. No more than 3–5 per day. Mark the rest as "draft" in the tracker, and continue when the user next says "continue submitting". After each submission, write the link into the step 6 tracker.
4. **Only stop and ask when stuck**, for example: a CLA needs signing; a CI check fails and can't be fixed with a simple format change; a maintainer or bot asks for information only the author has; fork or submission permission errors; a fresh duplicate check right before submitting shows someone else already submitted it. Fix what you can fix yourself (wrong format, wrong sort order) and keep going; don't stop.
5. When done, give the user a summary: what was submitted (with links), which ones stopped at which step, and why.

**B. No `gh`, or logged in as someone other than the submitter (for example a cloud agent like Fleet using its own account)**

Don't submit with the agent's account. Send the submitter links instead:
- **Issue-only lists**: send a pre-filled issue link. The submitter opens it, checks it over, ticks the confirmation items in the template, and clicks Create to submit. The issue belongs to whoever opened the link. To generate it:
  ```bash
  python3 <this skill's directory>/scripts/issue_link.py <owner/list> fields.json
  ```
  The field names in `fields.json` come from the `id` of each item in the list's `.github/ISSUE_TEMPLATE/*.yml`, plus `template` and `title`. Checkboxes are left unfilled on purpose; the submitter must tick them.
- **Lists that take PRs**: GitHub can't pre-fill file changes through a link, so send the web edit link `https://github.com/<list>/edit/<default branch>/README.md`, tell them "paste this line at line N, between these two entries", and include the PR title and body. When they open it, GitHub forks automatically; they paste, click Propose changes, then Create pull request. It takes about a minute.
- Ask the submitter to send back the link after submitting, and the agent records it. If they don't, find it with the search commands in step 6.

**Directories: the agent submits with the browser tool; the person only handles logins.**

- Before starting, show the user the sites that passed step 4. After the user approves this batch, the agent opens each submission page, fills in the form, uploads the logo or screenshots, and submits. Approved sites don't need to be asked about one by one; sites outside the batch, or paid ones, need separate approval.
- When you hit sign-up, login, email verification or a CAPTCHA, stop and ask the user to finish it in the browser, then continue. While waiting, move on to the next site instead of getting stuck. The agent does not create accounts for people and does not type passwords.
- For the URL field, prefer the project page on the company website; if there isn't one, use the repo. Rewrite the description for each site's audience; don't reuse one paragraph everywhere.
- After submitting, open the public page or dashboard and check the actual `href` of the product name, description and URL fields. Anything under review is marked "submitted"; only entries visible on the public page with a correct link count as "live".
- With no browser tool that can click and fill forms (for example pure CLI, or read-only page access), list the sites and the content to fill in for the user to do themselves.
- Never write passwords, tokens or verification codes into the tracker or logs.

### 6. Tracking

Record one row per submission in `~/.oss-list-submit/submissions.csv` (header in `references/tracker-template.csv`; if the file doesn't exist, copy that first). The step 7 watcher script reads this file, so the `receipt_url` column must contain the full PR/issue link. If the team also has a shared sheet, record in both.

If Method B (sending links) was used and the submitter didn't send back the link, find it with the commands below. The search index lags, so a fresh submission may not show up yet; not finding it doesn't mean it wasn't submitted:

```bash
gh search prs "<owner>/<repo>" --json url,author,state ; gh search issues "<owner>/<repo>" --json url,author,state
gh search prs --repo <list> <repo name> --json url,author,state    # global search misses some; search again with --repo for each list you submitted to
gh search prs "<repo name> in:title" --json url,author,state      # links in some PR bodies aren't indexed, so search titles too; check by hand that results are our project
```

Use only these statuses: `draft` / `submitted` / `live` / `rejected (reason)` / `skipped (reason)`. When reporting, count each status separately. **Don't report the number submitted as the number of new backlinks.**

### 7. Install the scheduled watcher (after PRs/issues are submitted)

First ask the user whether to install it (it runs a scheduled task on their machine). If they agree, run:

```bash
bash <this skill's directory>/scripts/install_watch.sh        # checks every 6 hours by default; --uninstall to remove
```

- macOS uses launchd and Linux uses crontab. It only needs `python3` and a logged-in `gh`. It is a built-in system scheduler that doesn't rely on Claude Code, Codex or Cursor: it keeps checking on schedule after the agent is closed or the computer restarts. Don't switch to the agent's own scheduling features; most of them only run while a session is open.
- If `terminal-notifier` is installed (`brew install terminal-notifier`, optional), clicking a notification opens the PR. Otherwise it uses the system's built-in notification, which shows "Script Editor" and doesn't open anything when clicked.
- It shows a system notification when it detects: a PR merged, an issue resolved, a PR/issue closed, or a new maintainer reply or review. After a merge it reads the list's README to confirm the entry really appears, then changes the status to "live".
- To check right away: `python3 <this skill's directory>/scripts/watch_submissions.py`; add `--dry-run` to look without writing.
- When you get a "maintainer replied" notification, reply soon. PRs whose maintainers asked for changes and got no response usually get closed.

Directory forms have no PR to watch, so check them by hand once after a week: is the page live, and what are the `href` and `rel`?

## Copy rules (all text that goes out: entries, PR / issue bodies, directory forms, Show HN / V2EX posts)

Maintainers and directory reviewers get a lot of AI-generated submissions every day, and readers spot AI-sounding text right away. Once they notice, they close it or scroll past.

**Applies to all text:**
- **Banned words**: revolutionary, seamless, powerful, cutting-edge, game-changing, next-gen, ultimate, effortless, supercharge, unlock, leverage, robust, best-in-class, empower, elevate, streamline, harness, delve, comprehensive, innovative, transform, in today's fast-paced world. For Chinese copy, the same goes for: 赋能、颠覆、一站式、极致、全方位、助力. When you want to use one, write what the project actually does instead.
- **Write concrete actions, not adjectives**: "reads the current tab and fills forms" beats "powerful browser automation".
- **Write only facts that can be verified**: star counts need a date; never make up user counts, downloads or case studies. If it's still early, say early preview.
- **Punctuation and format**: at most one em dash (—) per submission (unless the list format requires it); no exclamation marks; no emoji as bullet points; no piles of hashtags.
- **Don't list things in threes**: don't force features or benefits into groups of three. Write as many as there actually are.
- **Mix sentence lengths**: don't write three sentences in a row with the same length and structure.

**Write separately for each platform; don't copy and paste:**
- Before writing, read 2–3 similar entries or posts on that platform and note the angle they take, their length and tone, then write the same way. For example, awesome-mcp lists care about "which tools it connects to", AI tool directories care about "what it can do for you", Show HN cares about "why you built it and how", and V2EX and newsletter self-submissions are in Chinese and more casual.
- The same fact can appear on several platforms, but rewrite the sentences, especially the opening one.
- When done, compare the whole batch side by side: if any two share a full identical sentence, change it.

**By context:**
- **Awesome list entries**: one sentence saying what it does; copy the length and sentence pattern of neighboring entries.
- **PR / issue bodies**: 3–5 sentences of your own explanation (the checklist the template requires is filled in as given and doesn't count), covering what was added, which section and why, and the submitter's relationship to the project (for example "I'm on the team behind X"). Don't write "I'm excited to share".
- **Directory forms**: the one-line intro (tagline) says "who it's for and what it does", not a slogan; rewrite the full description for each site's audience so each one differs; pick only categories and tags that truly fit.
- **Show HN / V2EX / newsletter self-submissions**: first person, sounding like a real person (use contractions: I'm / it's / don't); open by saying directly what you built and why; mention one real limitation or unsolved problem; no headings or bold; don't open with "As a developer, I…". Show the user before posting.

When done, review each piece: does it share a full sentence with drafts for other platforms? Any banned words? Any made-up numbers? Could this paragraph describe any project? If so, rewrite it with specific details.

## Common mistakes

| Mistake | What to do instead |
|---|---|
| Using a bot account to open PRs on 20 lists at once | Use the submitter's own account, confirm the batch once, submit 3–5 per day over several days; cloud agents only send pre-filled links |
| Picking backlink sites by DR from high to low | Run only the five checks in step 4; high DR doesn't mean a good fit or that anyone reads it |
| Putting the GitHub repo in directory forms | If the company has a project page, use that |
| Making up your own entry format | Copy neighboring entries and insert alphabetically |
| Using the same description on every list | Rewrite it for each list's style and length |
| Counting a PR as done once it's opened | It's live only when merged and the entry is visible in the README; use the step 7 watcher or check by hand regularly |
| Forcing it into a section that doesn't fit | Skip and write down why |
