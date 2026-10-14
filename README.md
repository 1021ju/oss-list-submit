# oss-list-submit

帮开源项目找到对口的 awesome 列表、MCP registry 和开发者目录站：检查准入门槛，写好提交草稿，PR 合并时通知你。适用于 Claude Code、Codex 和 Cursor。

## 安装（一行）

```bash
npx skills add <OWNER>/oss-list-submit -g -a '*' -y
```

这行命令会把 skill 装到本机所有支持的 agent 里（Claude Code、Codex、Cursor 等）。只想装到某一个，就把 `-a '*'` 换成 `-a claude-code`、`-a codex` 或 `-a cursor`。

更新：`npx skills update oss-list-submit`

**前置条件**：Node.js（用来运行 npx）、[`gh`](https://cli.github.com/)，并且已经执行过 `gh auth login`。不需要任何付费工具或 API key。

## 怎么用

在 agent 里直接说：

> 帮我把 https://github.com/<org>/<repo> 提交到对口的 awesome 列表和目录站

agent 会按这个顺序做：

1. **建项目底稿**：star 数、仓龄、license、类别、公司官网上有没有项目页。
2. **找列表、查门槛**：列表是否归档、最近有没有合并、PR 积压多少、只收 PR 还是只收 issue，以及 CONTRIBUTING 和 CI 里的硬门槛、是否已经有人提过。
3. **照每个列表的格式写草稿**：条目、PR 或 issue 正文。
4. **筛外链目录站**，过五项检查：价格、领域、有没有人专门搜这个站、近 7 天新页面有没有收录、同行有没有用。
5. **你用自己的账号提交**。agent 不会用 bot 账号批量提交。
6. **记录到 `~/.oss-list-submit/submissions.csv`**。
7. **（可选）装定时监听**：PR 合并、被关闭或维护者回复时，弹系统通知，也可以同时推到飞书或 Slack 群。

## 为什么不让 agent 直接批量提 PR

awesome 列表的维护者会把短时间内的批量 PR 当成 spam，可能直接 block 账号，整个组织都会受牵连。由作者本人提交、每个列表一个 PR，通过率高得多。
