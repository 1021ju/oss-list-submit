# oss-list-submit

帮开源项目找到对口的 awesome 列表、MCP registry 和开发者目录站：检查准入门槛，写好提交草稿，PR 合并时通知你。适用于 Claude Code、Codex 和 Cursor。

## 安装

**通用（推荐）**：一行命令同时装进 Claude Code、Codex、Cursor，需要本机有 Node.js。

```bash
npx skills add 1021ju/oss-list-submit -g -a '*' -y
```

更新用 `npx skills update oss-list-submit`。只想装到某一个，把 `-a '*'` 换成 `-a claude-code`、`-a codex` 或 `-a cursor`。

**没有 Node，就用各自的原生方式：**

| 工具 | 怎么装 |
|---|---|
| Claude Code | 在 Claude Code 里输入 `/plugin install oss-list-submit --marketplace 1021ju/oss-list-submit` |
| Codex | 对 Codex 说：`$skill-installer install https://github.com/1021ju/oss-list-submit/tree/main/skills/oss-list-submit` |
| Cursor | 用上面的通用命令 |

两种方式只选一种，同时用会在 Claude Code 里出现两份同名 skill。

**前置条件**：安装并登录 [`gh`](https://cli.github.com/)（`gh auth login`）。不需要任何付费工具或 API key。

可选：agent 有浏览器能力（Claude in Chrome、Codex 自带的 browser use、Cursor 浏览器工具）时，目录站由 agent 代填，没有就给你列好文案自己粘贴。装了 `terminal-notifier`（`brew install terminal-notifier`），合并通知点一下就能打开 PR。

## 怎么用

在 agent 里直接说：

> 帮我把 https://github.com/<org>/<repo> 提交到对口的 awesome 列表和目录站

agent 会按这个顺序做：

1. **建项目底稿**：star 数、仓龄、license、类别、公司官网上有没有项目页。
2. **找列表、查门槛**：列表是否归档、最近有没有合并、PR 积压多少、只收 PR 还是只收 issue，以及 CONTRIBUTING 和 CI 里的硬门槛、是否已经有人提过。
3. **照每个列表的格式写草稿**：条目、PR 或 issue 正文、目录站表单、发帖文案，都按内置的去 AI 腔规则写。
4. **筛外链目录站**，过五项检查：价格、领域、有没有人专门搜这个站、近 7 天新页面有没有收录、同行有没有用。
5. **你用自己的账号提交**。agent 不会用 bot 账号批量提交。
6. **记录到 `~/.oss-list-submit/submissions.csv`**。
7. **（可选）装定时监听**：本机系统定时任务，每 6 小时查一次，PR 合并、被关闭或维护者回复时弹系统通知。agent 关着也照常运行。

## 为什么不让 agent 直接批量提 PR

awesome 列表的维护者会把短时间内的批量 PR 当成 spam，可能直接 block 账号，整个组织都会受牵连。由作者本人提交、每个列表一个 PR，通过率高得多。
