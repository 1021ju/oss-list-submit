# 候选渠道（种子清单）

awesome 列表的种子清单。每个列表都要按 SKILL.md 第 2 步重新检查，状态以检查当天为准。

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
| Codex / 浏览器 agent（2026-10-14 实测） | milisp/awesome-codex-cli（只收 issue，要求有真实 Codex 集成和采用证据）、RoggeOhta/awesome-codex-cli（积压约 300 个 PR）、hashgraph-online/awesome-codex-plugins（必须有 `.codex-plugin/plugin.json`，且扫描分 ≥80）、ianwieds/awesome-browser-agents（CI 要求 ≥10 star）、e2b-dev/awesome-ai-agents（PR 积压近千，最老的放了两年）。themeselection/best-chrome-extensions 已经 200 天没合并，而且要求 Chrome Web Store 链接。tabgent 还提交过：steel-dev/awesome-web-agents、supernalintelligence/Awesome-Gui-Agents、jqueryscript/awesome-codex（issue）、ichangyou/awesome-codex |
| 语言生态 | awesome-python / awesome-go / awesome-rust / awesome-nodejs 等（门槛通常更高，看 CONTRIBUTING） |
| 自托管 / 替代品 | awesome-selfhosted（对 license 和部署方式有要求） |

## 其他渠道

awesome 列表以外的目录站、registry、中文渠道、发布日渠道，统一放在 `directories.md`（已经核实过，分好层）。
