# Directory / launch site list (outside awesome lists)

**Last full verification: 2026-10-14.** Three sources: Ahrefs backlink data for 9 similar open-source projects (5 large, 4 small), first-hand experience posts on X found by GrokBot, and the agent opening and checking each site (looking only, not submitting).

- **rel column**: taken from one page of a project already listed on the site, looking at the link to the website or GitHub. `follow` means no nofollow. This is a single-page sample; free and paid tiers may differ.
- **Unverified**: the site blocks script access (Cloudflare bot check). When submitting, the user passes the check in the browser and the agent fills in the row while it's there.
- **Before use**: for rows not verified in over 3 months, first open the submission page to confirm it still exists and is still free. If anything changed, update this file and the verification date.

## 1. Submit for every open-source project

| Site | Submission page | Cost | Login | rel | Notes |
|---|---|---|---|---|---|
| Hacker News · Show HN | news.ycombinator.com/submit (rules: /showhn.html) | Free | HN account | follow | Must be downloadable or tryable directly, and the author must reply in the thread. New accounts often get rate-limited. Traffic only comes if it reaches the front page |
| DevHunt | devhunt.org (Submit → log in) | Free; ads $149/week | GitHub / Google | follow | Focused on developer tools, has an Open Source category. People on X report it works noticeably better than other launch boards |
| PeerPush | peerpush.com/submit | Free tier is queued behind paid users; from $39 | Account required | follow | Enter a URL and it drafts the listing automatically; goes live after review |
| AlternativeTo | alternativeto.net | Claims to be free | Account required | Unverified | Has an Open Source tag; listed as "alternative to X" |
| SourceForge | sourceforge.net (Import from GitHub) | Free | Account required | Unverified | Can mirror from GitHub in one click |
| OpenAlternative | openalternative.co/submit | Unverified | Unverified | Unverified | Only accepts open-source projects that are an alternative to a specific commercial product |
| SaaSHub | saashub.com/submit | Free, optional paid | Unverified | Unverified | Listed several times on X as "it works" |

## 2. Chinese channels (mainly for exposure and stars)

| Site | Submission page | Notes |
|---|---|---|
| 阮一峰《科技爱好者周刊》 (Ruan Yifeng's Tech Enthusiast Weekly) | github.com/ruanyf/weekly/issues, with 【开源自荐】 ("open-source self-recommendation") in the title | Free, chosen by the editor, inclusion not guaranteed |
| HelloGitHub | "提交项目" ("Submit project") on hellogithub.com, or github.com/521xueweihan/HelloGitHub/issues | Published on the 28th of each month; prefers fun, beginner-friendly projects |
| V2EX 分享创造 ("Share & Create" node) | v2ex.com/go/create | Free, account required |
| 开源中国 (OSChina) | oschina.net/project/new (submission page unverified) | |
| GeekNews (Korea) | news.hada.io/write, Show section | Summary must be written in Korean |

## 3. Add for AI / agent projects

| Site | Submission page | Cost | Login | rel | Notes |
|---|---|---|---|---|---|
| agentindex.app | agentindex.app/submit | Free | **No login** | follow | Only needs the GitHub repo link; reviewed by a person. Lowest barrier |
| FutureTools | futuretools.io/submit-a-tool | Free | No login (has CAPTCHA) | Not checked | Reviewed by a person; pricing options include Open Source |
| AI Agents Listing | aiagentslisting.com/submit | Free, but requires a badge | Email | follow as long as the badge is up | The badge goes in the README or on the website and is checked regularly; removing it gets you downgraded. **Ask the author before adding the badge** |
| Dang AI | dang.ai/pricing → Submit | Free requires a backlink and 4-week review; $49 without backlink | Email | Not checked | Not really free |
| AI Agent Store | aiagentstore.ai/new-agent | Listing cost not stated | Login required | nofollow | Low priority |
| Aixploria | aixploria.com/en/add-ai/ | Free tier unconfirmed | Not checked | Not checked | Low priority |
| There's An AI For That / Toolify / Futurepedia | /submit on each site | **Usually paid** (posts mention about $49 / $99 / $247) | — | Unverified | Pay only if needed; skip for zero-budget tasks |

## 4. Add for MCP servers (submit to the official Registry first; other sites sync from it)

| Site | Submission page | Cost | Login | rel | Notes |
|---|---|---|---|---|---|
| Official MCP Registry | `mcp-publisher` CLI, docs at modelcontextprotocol.io/registry/quickstart | Free | GitHub | — | The package must be published to npm or another registry first. Still in preview |
| Smithery | smithery.ai/servers/new | Free | Email / Google / GitHub | follow | |
| Glama | Add Server on glama.ai | Free; Boost $49/month | Not checked | follow when linking to GitHub, nofollow when linking to the website | punkpeye/awesome-mcp-servers requires new entries to carry a Glama badge |
| LobeHub | `lhm` CLI, docs at lobehub.com/publish-mcp/skill.md | Free | OIDC, must verify GitHub ownership | follow | All 5 large similar projects are on it |
| MCP Market | mcpmarket.com/submit | Free queue 4–6 weeks; $29 for live within 24 hours | Email only | follow | Also accepts agent skills |
| mcpservers.org | mcpservers.org/submit | Free, 2-week review; dofollow only at $39 | Not checked | Free version probably nofollow | |
| mcptoplist.com | No submission; scraped from the registries; can be claimed with GitHub | Free | GitHub | follow | |
| PulseMCP / mcp.so / Cursor Directory | Each site's submission page | Unverified | Unverified | Unverified | Often included in MCP launch checklists on X |

## 5. Add for Claude skills / plugins / libraries

| Site | How to get listed | Notes |
|---|---|---|
| SkillsMP | **No submission**: have a SKILL.md in the repo and add the topic `claude-skills` or `claude-code-skill`; it syncs daily | DR 68, follow |
| SkillsLLM | skillsllm.com/submit | follow. The pricing page is rendered by JS and couldn't be read |
| Anthropic official plugin directory | claude.com/docs/directory/publish → platform.claude.com/plugins/submissions | Requires a paid Claude plan; each one is reviewed by Anthropic. Not a backlink site, but it is the official channel |
| Context7 | context7.com/add-library, paste the public repo link | Lets AI coding assistants find your docs. Suits libraries, frameworks and SDKs; doesn't count as an SEO backlink |
| claudemarketplaces.com | No submission, scraped only (sources: skills.sh, GitHub, MCP registry) | Claims 380k monthly visitors |

## 6. Launch-day channels (as needed)

Only do these when the project has a UI to demo and the team can rally a group of people on launch day. Don't submit otherwise.

| Site | Notes |
|---|---|
| Product Hunt | Traffic only comes from reaching the top few spots (real cases: #4 brought 930 visitors and 60+ signups; one that didn't make it got 52 visitors and 0 signups). Links are mostly nofollow. For open-source developer tools, do Show HN first |
| Peerlist Launchpad / Fazier / MicroLaunch / Uneed / BetaList | Fazier's free tier requires a backlink and a 30-day queue; MicroLaunch free tier unconfirmed; people report Uneed's paid sponsorship had no effect at all; BetaList free has a 4–6 week queue |

## 7. Appears automatically, no submission needed

DeepWiki (5 of the 9 similar projects checked have one, dofollow), trendshift.io, ossinsight.io, star-history.com, newreleases.io, plus many GitHub aggregator sites with single-digit DR. For Chrome extensions, chrome-stats.com and extpose.com only show it after it's on the Chrome Web Store.

## 8. Don't touch

- **Bulk directory submission services** ("submit to 100–300 sites at once"): many people on X report most are dead links or not really free.
- **devtoolsdir.com**: sells "DR Booster" backlink packages, looks like a link farm, and requires the website to have DR ≥ 10.
- **eliteai.tools**: all listing links are nofollow (even GitHub), and it sells guest posts.
- **TLDR / AlphaSignal**: no free submission channel, ads only.
- **SaaStr AI Agents Directory**: audience is B2B sales, not a fit.
- **opensource-observer/oss-directory**: display pages require login to view, no backlink value.
