# 候选渠道（种子清单）

这份清单只是起点，不能直接当结论用。站点是否还活着、提交入口、是否免费、链接是否 nofollow，都要在当天打开页面确认。外链类站点要先过 SKILL.md 第 4 步的筛选关。清单里的状态是 2026-10 整理时的印象，没有逐条核验。

## A. awesome 列表（GitHub PR，链接指向 repo）

按项目类别搜，不要只用下面这几个：

```bash
gh search repos "awesome mcp" --sort stars -L 20
gh search repos "awesome <语言或领域>" --sort stars -L 20
```

| 类别 | 种子 |
|---|---|
| MCP server | punkpeye/awesome-mcp-servers（2026-10-14 实测：仍有合并，没有 star 门槛；CI 要求新条目带 Glama 评分徽章，所以先上 Glama。open PR 有 2.8k 个，最老的从 2025-12 开到现在，要做好长期排队的准备）。appcypher/awesome-mcp-servers 已归档，不要提 |
| Claude / agent / skill | 搜 `awesome claude`、`awesome claude-code`、`awesome ai-agents`、`awesome claude skills` |
| Codex / 浏览器 agent（2026-10-14 实测） | milisp/awesome-codex-cli（只收 issue，要求有真实 Codex 集成和采用证据）、RoggeOhta/awesome-codex-cli（积压约 300 个 PR）、hashgraph-online/awesome-codex-plugins（必须有 `.codex-plugin/plugin.json`，且扫描分 ≥80）、ianwieds/awesome-browser-agents（CI 要求 ≥10 star）、e2b-dev/awesome-ai-agents（PR 积压近千，最老的放了两年）。themeselection/best-chrome-extensions 已经 200 天没合并，而且要求 Chrome Web Store 链接 |
| 语言生态 | awesome-python / awesome-go / awesome-rust / awesome-nodejs 等（门槛通常更高，看 CONTRIBUTING） |
| 自托管 / 替代品 | awesome-selfhosted（对 license 和部署方式有要求） |

## B. MCP / agent registry（大多自助提交，可填 website）

官方 MCP Registry（registry.modelcontextprotocol.io，通过 CLI 发布）、Glama、Smithery、mcp.so、PulseMCP。只有 MCP 类项目才提交。

## C. 开发者 / 开源目录（可填 website，适合放公司项目页）

| 站点 | 说明 |
|---|---|
| OpenAlternative | 开源替代品目录，项目需要能对标某个商业产品 |
| AlternativeTo | 以“X 的替代品”的方式挂靠 |
| SaaSHub / LibHunt | LibHunt 会聚合 awesome 列表，有了 GitHub 收录后可能自动出现 |
| DevHunt | 开发者工具的发布榜 |
| Product Hunt | 发布日渠道，只适合有界面、能演示的项目；准备工作按 marketing-skills:launch |

## D. 中文渠道（主要带来曝光和 star，不是外链）

HelloGitHub（在它的 GitHub repo 提 issue 自荐）、阮一峰《科技爱好者周刊》（在 ruanyf/weekly 提 issue）、V2EX 的“分享创造”节点、掘金、即刻。

## E. 发布日社区（带 star，按发布节奏集中在同一天发）

Show HN（要有技术亮点，泛泛的发布帖会被 flag）、对口的 subreddit（先看版规里的自推规定）、X。这些属于发布动作，不进外链台账；台账里只记“已发”和帖子链接。

## 不要碰

- 收费的“批量提交 100 个目录”服务。
- 搜站名没有任何品牌联想词、什么类目都收、满页付费位的目录站。
- 和项目领域无关的站，不管 DR 多高。
