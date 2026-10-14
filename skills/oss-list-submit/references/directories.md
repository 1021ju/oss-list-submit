# 目录站 / 发布站清单（awesome 列表之外）

**上次整体核实：2026-10-14。** 来源有三：Ahrefs 查 9 个同类开源项目的外链（5 个大项目、4 个小项目），GrokBot 在 X 上找真人经验帖，再由 agent 逐站打开核实（只看不提交）。

- **rel 列**：抽一个站上已收录项目的页面，看指向官网或 GitHub 的链接。`follow` 表示没有 nofollow。这是单页抽样，免费档和付费档可能不一样。
- **未核实**：站点挡了脚本访问（Cloudflare 人机验证）。提交时由用户在浏览器里过验证，agent 顺便把这一行补全。
- **用之前**：超过 3 个月没核实的行，先打开提交页确认还在、还免费。发现变化就改这份文件，并把核实日期更新掉。

## 1. 所有开源项目都提

| 站点 | 提交入口 | 费用 | 登录 | rel | 备注 |
|---|---|---|---|---|---|
| Hacker News · Show HN | news.ycombinator.com/submit（规则：/showhn.html） | 免费 | HN 账号 | follow | 要能直接下载或试用，作者要在帖子里回复。新号容易被限流。上首页才有量 |
| DevHunt | devhunt.org（Submit → 登录） | 免费；广告 $149/周 | GitHub / Google | follow | 专做开发者工具，有 Open Source 分类。X 上有人反馈比其他发布板效果明显 |
| PeerPush | peerpush.com/submit | 免费档排在付费用户后面；$39 起 | 要账号 | follow | 输入网址后自动生成草稿，审核后上线 |
| AlternativeTo | alternativeto.net | 自称免费 | 要账号 | 未核实 | 有 Open Source 标签，按“X 的替代品”挂靠 |
| SourceForge | sourceforge.net（Import from GitHub） | 免费 | 要账号 | 未核实 | 能从 GitHub 一键导入镜像 |
| OpenAlternative | openalternative.co/submit | 未核实 | 未核实 | 未核实 | 只收能对标某个商业产品的开源项目 |
| SaaSHub | saashub.com/submit | 免费，可选付费 | 未核实 | 未核实 | X 上多次被列为“有效果” |

## 2. 中文渠道（主要带曝光和 star）

| 站点 | 提交入口 | 备注 |
|---|---|---|
| 阮一峰《科技爱好者周刊》 | github.com/ruanyf/weekly/issues，标题写【开源自荐】 | 免费，编辑挑选，不保证收录 |
| HelloGitHub | hellogithub.com 里的“提交项目”，或 github.com/521xueweihan/HelloGitHub/issues | 每月 28 日出刊，偏好有趣、入门级的项目 |
| V2EX 分享创造 | v2ex.com/go/create | 免费，要账号 |
| 开源中国 | oschina.net/project/new（入口未核实） | |
| GeekNews（韩国） | news.hada.io/write，Show 栏目 | 要用韩语写摘要 |

## 3. AI / agent 类项目加提

| 站点 | 提交入口 | 费用 | 登录 | rel | 备注 |
|---|---|---|---|---|---|
| agentindex.app | agentindex.app/submit | 免费 | **不用登录** | follow | 只要 GitHub 仓库链接，人工审核。门槛最低 |
| FutureTools | futuretools.io/submit-a-tool | 免费 | 不用登录（有验证码） | 未查 | 人工审核，定价选项里有 Open Source |
| AI Agents Listing | aiagentslisting.com/submit | 免费，但要挂徽章 | 邮箱 | 挂着徽章就是 follow | 徽章放在 README 或网站上，会定期检查，撤掉就降级。**挂徽章前先问作者** |
| Dang AI | dang.ai/pricing → Submit | 免费要回链、审核 4 周；$49 免回链 | 邮箱 | 未查 | 伪免费 |
| AI Agent Store | aiagentstore.ai/new-agent | 收录费用未写 | 要登录 | nofollow | 优先级低 |
| Aixploria | aixploria.com/en/add-ai/ | 免费档未确认 | 未查 | 未查 | 优先级低 |
| There's An AI For That / Toolify / Futurepedia | 各站 /submit | **通常付费**（帖子里说约 $49 / $99 / $247） | — | 未核实 | 按需付费，零元任务不做 |

## 4. MCP server 加提（先提官方 Registry，其他站会从那里同步）

| 站点 | 提交入口 | 费用 | 登录 | rel | 备注 |
|---|---|---|---|---|---|
| 官方 MCP Registry | `mcp-publisher` CLI，文档 modelcontextprotocol.io/registry/quickstart | 免费 | GitHub | — | 要先把包发到 npm 等仓库。目前还是 preview 版 |
| Smithery | smithery.ai/servers/new | 免费 | 邮箱 / Google / GitHub | follow | |
| Glama | glama.ai 的 Add Server | 免费；Boost $49/月 | 未查 | 链 GitHub 的是 follow，链官网的是 nofollow | punkpeye/awesome-mcp-servers 要求新条目带 Glama 徽章 |
| LobeHub | `lhm` CLI，文档 lobehub.com/publish-mcp/skill.md | 免费 | OIDC，要验证 GitHub 所有权 | follow | 同类 5 个大项目都在上面 |
| MCP Market | mcpmarket.com/submit | 免费排队 4–6 周；$29 24 小时上线 | 只要邮箱 | follow | 也收 agent skills |
| mcpservers.org | mcpservers.org/submit | 免费，2 周审核；$39 才给 dofollow | 未查 | 免费版大概率 nofollow | |
| mcptoplist.com | 不用提交，从各 registry 抓取；可以用 GitHub 认领 | 免费 | GitHub | follow | |
| PulseMCP / mcp.so / Cursor Directory | 各站提交页 | 未核实 | 未核实 | 未核实 | X 上常被列进 MCP 发布清单 |

## 5. Claude skill / plugin / 库类加提

| 站点 | 怎么上 | 备注 |
|---|---|---|
| SkillsMP | **不用提交**：仓库里有 SKILL.md，并加上 topic `claude-skills` 或 `claude-code-skill`，每天自动同步 | DR 68，follow |
| SkillsLLM | skillsllm.com/submit | follow。费用页由 JS 渲染，没读到 |
| Anthropic 官方插件目录 | claude.com/docs/directory/publish → platform.claude.com/plugins/submissions | 要有付费 Claude 套餐，官方逐个审核。不是外链站，但这是官方入口 |
| Context7 | context7.com/add-library，贴公开仓库链接 | 让 AI 编码助手能检索到你的文档。适合库、框架、SDK，不算 SEO 外链 |
| claudemarketplaces.com | 不能提交，只能被抓取（来源：skills.sh、GitHub、MCP registry） | 自称月访客 38 万 |

## 6. 发布日渠道（按需）

只有在项目有界面可以演示、团队能在发布当天动员一批人时才做。平时不提。

| 站点 | 说明 |
|---|---|
| Product Hunt | 冲进前几名才有量（真人案例：第 4 名带来 930 访客、60+ 注册；没冲上去的 52 访客、0 注册）。链接基本是 nofollow。开源开发者工具优先发 Show HN |
| Peerlist Launchpad / Fazier / MicroLaunch / Uneed / BetaList | Fazier 免费档要回链、排队 30 天；MicroLaunch 免费档未确认；Uneed 的付费赞助有人反馈完全没效果；BetaList 免费要排 4–6 周 |

## 7. 自动出现，不用提交

DeepWiki（查过的 9 个同类项目里有 5 个都有，dofollow）、trendshift.io、ossinsight.io、star-history.com、newreleases.io，以及大量 DR 个位数的 GitHub 聚合站。Chrome 扩展类的 chrome-stats.com、extpose.com 要先上架 Chrome Web Store 才会出现。

## 8. 不要碰

- **批量目录提交服务**（“一次提交 100–300 个站”）：X 上多人反馈大部分是死链或伪免费。
- **devtoolsdir.com**：卖“DR Booster”外链套餐，像外链农场，而且要求网站 DR ≥ 10。
- **eliteai.tools**：收录链接全是 nofollow（连 GitHub 也是），还卖 guest post。
- **TLDR / AlphaSignal**：没有免费投稿入口，只有广告。
- **SaaStr AI Agents Directory**：受众是 B2B 销售，不对口。
- **opensource-observer/oss-directory**：展示页要登录才能看，没有外链价值。
