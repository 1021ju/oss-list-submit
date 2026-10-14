---
name: oss-list-submit
description: Use when someone wants to promote a company open-source GitHub project by getting it into awesome-xxx lists, MCP/agent registries, developer directories or free backlink sites; or asks "提交 awesome 列表"、"开源项目推广"、"上列表"、"外链目录"、"submit to awesome list"、"list my repo"、"get more stars".
---

# 开源项目上列表 / 外链提交

把一个开源项目提交到对口的 awesome 列表、registry 和目录站，并记录每一条的真实状态。**agent 负责找渠道、筛选、写草稿和核验；PR 和表单由项目作者本人的账号提交。**

## 工具对照（Claude Code / Codex / Cursor 同一份 skill）

| 需要 | Claude Code | Codex | Cursor |
|---|---|---|---|
| GitHub 查询、开 PR、定时监听 | `gh` CLI | `gh` CLI | `gh` CLI |
| 打开目录站、填表、核验 `href` | Claude in Chrome 扩展 | Codex 自带的 browser use，或装了的其他浏览器插件（如 [Tabgent](https://github.com/FibonaAI/tabgent)） | Cursor 自带的浏览器工具（如果开启了） |

读公开页、查 `href` 也可以直接用 `curl`。

这个 skill 不依赖任何付费 SEO 工具或 API key。开始前先确认三件事：`gh` 能不能用、能不能联网、有没有**能点击和填表**的浏览器工具（只能搜索或读网页的不算）。没有能填表的浏览器工具时，目录站只出文案，由人去填。

## 三条硬规则

1. **不批量代提。** 不用公司 bot 或共享账号在短时间内向多个列表开 PR。维护者会把这当 spam 关掉甚至 block，之后整个组织都受牵连。很多列表明文拒收自动/AI 生成的 PR。每个列表只开一个 PR，由作者本人的 `gh` 登录态提交，或把草稿交给作者手动开；同一个账号每天不超过 3–5 个。用户要求“今天全部提完”也一样：说明原因，超出的存成草稿，改天接着提。
2. **先定链接指向哪里。** 指向 `github.com/...` 的链接给 GitHub 涨权重，不直接给公司域名加分。awesome 列表按惯例链 repo，照办。目录站、registry 允许填 website 的，优先填公司域名上的项目页（如 `<公司域名>/oss/<slug>`）；没有项目页就填 repo，并在报告里注明“这条外链不给公司域名”。
3. **已提交 ≠ 已上线。** PR 已开、表单已交只记为“已提交”。PR 合并且列表里能看到条目、目录页公开可访问且 `href` 指向正确，才记为“已上线”。

## 流程

### 1. 项目底稿（先读已有信息，缺的再问）

repo URL、一句话定位（≤ 15 词英文）、类别（MCP server / agent / CLI / 库 + 语言）、star 数、首次提交日期、license、公司域名上有没有项目页、提交人的 GitHub 账号。

仓龄、star 数和 license 是很多列表的准入门槛：

```bash
O=<owner>; P=<repo>
gh api repos/$O/$P --jq '{stars:.stargazers_count, license:.license.spdx_id, homepage, topics, private}'
gh api -i "repos/$O/$P/commits?per_page=1" | grep -i '^link:'      # 取 rel="last" 的 page=N
gh api "repos/$O/$P/commits?per_page=1&page=N" --jq '.[0].commit.committer.date'   # 首次提交日期
gh api users/$O --jq .blog                                          # 组织官网（组织也用 users/ 接口）
```

**预检：repo 现在能不能拿出去提。**
- **硬阻塞**（repo 没公开、没有 license、没有安装说明）：告诉作者要补什么，只做只读调研和草稿，不提交。
- **能顺手修的**（README 里残留 private / WIP 之类的旧说法、没有 topics、没填 homepage）：列给作者，建议先修再提；作者说不修也可以继续。

### 2. 找 awesome 列表并检查活跃度

用 `gh search repos "awesome <类别关键词>" --sort stars` 加上 `references/channels.md` 里的种子列表。每个候选列表都要查以下几项，任何一项不过就跳过，并记下原因：

```bash
L=<owner/list>; R=<我们的repo名>
gh repo view $L --json isArchived                                              # 是否归档（pushedAt 含任何分支的 push，不能当维护信号）
gh api "repos/$L/commits?per_page=1" --jq '.[0].commit.committer.date'         # 默认分支最后一次提交（列表仓库基本等于最后一次合并）
gh api "search/issues?q=repo:$L+is:pr+is:merged+merged:>=<90天前的日期>&per_page=1" --jq .total_count  # 近 90 天合并了几个 PR
gh api "search/issues?q=repo:$L+is:pr+is:open&per_page=1" --jq .total_count      # open PR 的真实数量（gh pr list -L 会截断）
gh pr list -R $L --state open --search "sort:created-asc" -L 1 --json createdAt --jq '.[0].createdAt'  # 最老的 open PR
gh api "repos/$L/contents/.github/workflows" --jq '.[].name'   # 报 Not Found (HTTP 404) = 没配 CI；403、限流等其他报错要重试，不能当成没有。有的话逐个读 YAML 和它引用的脚本/配置
gh api repos/$L/contents/README.md -H "Accept: application/vnd.github.raw" > /tmp/list-readme.md && { grep -i $R /tmp/list-readme.md || echo "README 里没有"; }  # README 查重（超过 1MB 时必须加 raw 头）；大文件偶尔下载到一半断掉（报 unexpected EOF），这时不会误报“没有”，重试即可。列表拆成多个文件的，要连同那些文件一起查
gh search prs --repo $L $R --json number,state,author; gh search issues --repo $L $R --json number,state  # 已开的 PR/issue 查重
```

| 检查项 | 不过的情况 |
|---|---|
| 归档 | `isArchived: true` → 跳过 |
| 维护 | 最后一次提交在 90 天以前，且近 90 天没有合并任何 PR → 跳过。近 90 天合并数为 0 但最近有提交（可能是维护者直接 push），记下来告诉作者 |
| 提交入口 | 先确认这个列表收不收外部 PR：读 CONTRIBUTING 和 issue 模板，有些列表只收 issue（外部开 PR 会被拦）。按它的实际入口出草稿。PR 和表单都开放时，选 CONTRIBUTING 推荐的那个；没写就选 PR，进度看得见 |
| 积压 | 本身不作为跳过理由，把数量和最老日期如实告诉作者，不要折算成“要等几天”。如果最老的 open PR 超过半年，而且近期合并的几乎都是维护者自己的 PR，就写明“大概率排不进去”，由作者决定提不提。只收 issue 的列表，看的是 issue 队列 |
| 准入门槛 | CONTRIBUTING、PR/issue 模板、CI 引用的脚本和配置（不能只看文件名）。star、仓龄、license、徽章、manifest 等要求不满足就跳过，并写明“补齐什么之后可以提”。只写了模糊门槛（比如“不收太新的项目”）的，把原话给作者，由作者判断 |
| 对口 | 同类项目放在哪个分类，我们就放哪个；找不到合适的分类就跳过，不要硬塞 |
| 重复 | README 已收录，或者已经有 open 的 PR/issue（不管是谁开的）→ 跳过，不要重复提 |

这一步只做检查和报告。修改我们自己的 repo（补 topics、改 README、加徽章等）属于另外的动作，要先问作者。

### 3. 写 awesome 条目草稿

严格照抄该列表现有条目的**格式**：链接写法、描述长度、句尾标点、emoji 和徽章。**措辞不照抄**：相邻条目用了 “AI-powered” 这类营销词，我们的条目照样按文末“文案规则”写。列表明文规定的格式（比如分隔符必须用破折号）照列表的来，它优先于我们的标点规则。语言、部署方式这类图标按 repo 的实际情况选，不知道就查，不要猜。

- **分类**：同类项目分散在几个分类时，选和我们功能最接近的那一个，草稿里写明理由，让作者确认。
- **插入位置**：分类本身按字母序排，就按字母序插；分类本身没排序，就加在末尾。
- **PR 模板**：标题和正文按模板填，要勾选的项逐项核对，属实的才勾，不能直接全勾。
- **对方关于 AI 的规定照办**：列表明文拒收 AI 生成的 PR 或描述，就请作者自己写描述再提，或者跳过；用作者账号提交不等于豁免。列表给 AI 辅助的提交设了专门的标记或通道，就按要求标上。

每个列表单独出一份草稿。只收 issue 的列表就按它的 issue 模板写，模板里的确认项按属实与否标好，在第 5 步的批量确认里让提交人看到勾了哪些：

```
列表: <owner/repo>  分类: <section>  插入位置: <在哪两条之间>
条目: - [name](url) - Description.
PR 标题: ...
PR 正文: ...
```

### 4. 外链 / 目录站：先过筛选关

**先看 `references/directories.md`**：这是已经核实过、分好层的清单。按项目类型选层：第 1 层是所有项目都考虑的，但 Show HN 要等项目能一条命令装好或在线试用、README 写清楚了再发，这之前先跳过；AI/agent、MCP、skill 类项目再加对应的层；中文渠道看团队需不需要；发布日渠道按需。清单里标“未核实”的行，提交时顺便补全；超过 3 个月没核实的行，先确认提交页还在。没有浏览器、看不到表单时，按通用字段出文案（名称、一句话介绍、详细描述、网址、分类、标签、Logo、截图），注明“字段以实际表单为准”。

清单之外新发现的站，不看 DR（站点权重分），只过下面五项。查不到的项标“未查”，不能当作通过。通过的站补进 `directories.md`：

| 检查项 | 怎么查 | 判据 |
|---|---|---|
| 价格 | 打开提交页 | 免费入口包含哪些内容；加急、置顶、付费收录单独列出。零元任务不升级成付费 |
| 领域 | 看站内同类条目 | 有开发者、AI 或开源工具类目，而且我们的项目放进去不突兀 |
| 有没有人专门搜这个站 | `curl -s "https://suggestqueries.google.com/complete/search?client=firefox&q=<站名>"`（Google 搜索联想，不需要 key） | 联想词里出现“站名 + reviews / login / alternative / submit”这类品牌搜索，偏向是真站；只联想出站名本身或无关词，要多留个心眼。这是弱信号，小众真站也可能没有联想，不能单凭这一项否决 |
| 近 7 天新页面有没有收录 | `site:<domain>` 配合 Google 的“过去一周”筛选，或抽一条最近收录的条目页去搜 | 新页面一周内能被收录，我们的条目才有机会被看到 |
| 同行有没有用 | 在目录站里搜 1–2 个同类优秀开源项目的名字；或者看同行 README 里的 “Featured on” 徽章 | 同行在这里有条目，说明渠道可信 |

另外，上线后要记录链接的 `rel`。`nofollow` 不代表失败，只是如实记下来；`noopener noreferrer` 不等于 `nofollow`。

### 5. 提交（永远用提交人自己的 GitHub 账号）

先运行 `gh api user --jq .login`，看本机登录的是谁：

- 登录的就是第 1 步记下的提交人账号 → 方式 A。
- 没装 `gh`、没登录，或登录的不是提交人本人 → 先问一句：“要不要登录你自己的 GitHub？登录后我直接帮你提，不用一个个点链接。”用户同意，就让用户运行 `gh auth login`（Claude Code 里可以输入 `! gh auth login`），在浏览器里点授权，然后走方式 A。用户不想登录，或者 agent 跑在云端、只能用 agent 自己的账号 → 方式 B。

**A. 本机 `gh` 已登录提交人自己的账号：批量确认一次，然后 agent 自己提完**

1. 把这一批要提的 PR/issue 一次列给用户：列表、分类、条目原文、标题和正文、勾了哪些确认项、今天提哪几个。用户点头后就开始，不再逐条问。批准的范围只有这一批，新增的列表要另外确认。
2. agent 逐个提交：
   - 收 PR 的列表：`gh repo fork <list> --clone=false`，在 fork 里建分支，改那一行，然后 `gh pr create -R <list>`。
   - 只收 issue 的列表：`gh issue create -R <list>`；如果用的是 issue 表单，就按表单字段拼好正文。
3. 每天不超过 3–5 个。超出的在记录里标“草稿”，用户下次说“继续提交”就接着提。每提完一个就把链接写进第 6 步的记录。
4. **只有卡住才停下来问**，比如：要签 CLA；CI 检查失败，而且不是改一下格式就能修好的；维护者或 bot 要求提供只有作者知道的信息；fork 或提交权限报错；提交前重新查重，发现别人已经提了。能自己修的（格式不对、排序错位）修好继续，不要停。
5. 提完给用户一个汇总：提了哪些（附链接）、哪些停在哪一步、为什么。

**B. 没有 `gh`，或者登录的不是提交人本人（比如 Fleet 等云端 agent 用的是 agent 自己的账号）**

不要用 agent 的账号提交，改为给提交人发链接：
- **只收 issue 的列表**：发一个已经预填好内容的 issue 链接。提交人点开，检查一遍，勾选模板里的确认项，点 Create 就提交了。这个 issue 属于点开链接的人自己的账号。生成方法：
  ```bash
  python3 <本 skill 目录>/scripts/issue_link.py <owner/list> fields.json
  ```
  `fields.json` 的字段名取自列表 `.github/ISSUE_TEMPLATE/*.yml` 里每一项的 `id`，再加上 `template` 和 `title`。勾选框故意不预填，必须由提交人自己勾。
- **收 PR 的列表**：GitHub 不支持通过链接预填文件改动，只能发 `https://github.com/<list>/edit/<默认分支>/README.md` 这个网页编辑链接，同时告诉对方“在第几行、哪两条之间粘贴这一行”，并附上 PR 标题和正文。点开后 GitHub 会自动 fork，粘贴后点 Propose changes，再点 Create pull request，大约一分钟。
- 请提交人把提交后的链接发回来，agent 写进记录。没发回来的，用第 6 步的搜索命令找。

**目录站：agent 用浏览器工具自己提交，人只负责登录。**

- 开始前把通过第 4 步筛选的站点列给用户，用户批准这一批后，agent 逐个打开提交页，自己填表、上传 Logo 或截图、提交。批准过的站点不用每个再问一遍，超出这批的、要付费的，要另外问。
- 遇到注册、登录、邮箱验证、验证码，停下来请用户在浏览器里完成，完成后 agent 接着往下做。等用户的时候先去做下一个站，不要卡住。agent 不替人注册账号，也不输入密码。
- 网址字段优先填公司官网上的项目页，没有就填 repo。描述要按每个站的受众改写，不要全部用同一段。
- 提交后打开公开页或后台，核对产品名、描述、网址字段实际的 `href`。审核中的标记为“已提交”，公开页能看到且链接正确的才算“已上线”。
- 没有能点击和填表的浏览器工具（比如纯 CLI，或只能读网页），就把站点和要填的内容列给用户，让用户自己去填。
- 密码、token、验证码一律不写进表格或日志。

### 6. 记录

每一个提交动作记一行，写进 `~/.oss-list-submit/submissions.csv`（表头见 `references/tracker-template.csv`，文件不存在就先拷一份）。第 7 步的监听脚本读的就是这个文件，所以“PR或表单回执链接”一栏要填完整的 PR/issue 链接。团队另有共享表的话，两边都记。

用了方式 B（发链接）、提交人又没把链接发回来的，用下面的命令找。搜索索引有延迟，刚提交的可能搜不到，搜不到不等于没提交：

```bash
gh search prs "<owner>/<repo>" --json url,author,state ; gh search issues "<owner>/<repo>" --json url,author,state
gh search prs --repo <list> <repo名> --json url,author,state    # 全局搜会漏，对每个提过的列表再按 --repo 搜一遍
gh search prs "<repo名> in:title" --json url,author,state      # 有些 PR 正文里的链接没被索引，标题再搜一遍；结果要人工确认是不是我们的项目
```

状态只用这几种：`草稿` / `已提交` / `已上线` / `被拒（原因）` / `跳过（原因）`。汇报时把各状态分开计数。**不要把已提交的数量说成新增外链数。**

### 7. 装定时监听（提交完 PR/issue 后）

先问用户要不要装（它会在本机常驻一个定时任务）。同意后运行：

```bash
bash <本 skill 目录>/scripts/install_watch.sh        # 默认每 6 小时检查一次；--uninstall 卸载
```

- macOS 用 launchd，Linux 用 crontab，只依赖 `python3` 和已登录的 `gh`。它是系统自带的定时任务，不靠 Claude Code、Codex 或 Cursor：agent 关了、电脑重启后照样按时检查。不要改用 agent 自己的定时功能，那些大多要会话开着才跑。
- 本机装了 `terminal-notifier`（`brew install terminal-notifier`，可选）时，点通知直接打开对应的 PR；没装就用系统自带方式弹，通知上会显示“脚本编辑器”，点了不会跳转。
- 检测到这些变化时，会弹系统通知：PR 合并、issue 被处理、PR/issue 被关闭、维护者有新回复或 review。合并之后它会去读列表的 README，确认条目真的出现了，再把状态改成“已上线”。
- 想马上查一次：`python3 <本 skill 目录>/scripts/watch_submissions.py`，加 `--dry-run` 就只看不写。
- 收到“维护者回复了”要尽快回。维护者提了修改意见没人理，PR 通常会被直接关掉。

目录站的表单没有 PR 可以监听，一周后手动复查一次：页面有没有上线，`href` 和 `rel` 是什么。

## 文案规则（所有要发出去的文字：条目、PR / issue 正文、目录站表单、Show HN / V2EX 帖子）

维护者和目录站审核每天都收到大量 AI 生成的提交，读者一眼就能认出 AI 腔，看出来就直接关掉或划走。

**所有文字都适用：**
- **禁用词**：revolutionary、seamless、powerful、cutting-edge、game-changing、next-gen、ultimate、effortless、supercharge、unlock、leverage、robust、best-in-class、empower、elevate、streamline、harness、delve、comprehensive、innovative、transform、in today's fast-paced world；中文同理：赋能、颠覆、一站式、极致、全方位、助力。想用的时候换成具体做了什么。
- **写具体动作，不写形容词**：“reads the current tab and fills forms” 胜过 “powerful browser automation”。
- **只写能核实的事实**：star 数要带日期；没有的用户数、下载量、案例一律不编。还在早期就写 early preview。
- **标点和格式**：每条提交里破折号（—）最多一个（列表格式规定的除外）；不用感叹号；不用 emoji 当列表符号；不堆 hashtag。
- **别三个三个地列**：特性、优点不要凑成三条一组，有几条写几条。
- **句子长短要混着来**，不要连着三句一样长、一样的结构。

**按场景：**
- **awesome 列表条目**：一句话说清它做什么，长度和句式照抄相邻条目。
- **PR / issue 正文**：自己写的说明部分 3–5 句（模板要求的 checklist 照填，不算在内），写加了什么、放在哪个分类以及理由、提交人和项目的关系（比如 “I'm on the team behind X”）。不写 “I'm excited to share”。
- **目录站表单**：一句话介绍（tagline）写“给谁、做什么”，不写口号；详细描述按这个站的受众改写，每个站不一样；分类和标签只选真对口的。
- **Show HN / V2EX / 周刊自荐**：用第一人称、像人说话（用缩写 I'm / it's / don't），开头直接说做了什么、为什么做；写一个真实的限制或还没解决的问题；不用标题和加粗，不以 “As a developer, I…” 开头。发之前给用户过目。

写完逐条自查一遍：有没有禁用词？有没有编出来的数字？是不是任何项目都能套用这段话？能套用就加具体细节重写。

## 常见错误

| 错误 | 正确做法 |
|---|---|
| 用 bot 账号一次给 20 个列表开 PR | 用提交人自己的账号，整批确认一次，每天 3–5 个分几天提；云端 agent 只发预填链接 |
| 按 DR 从高到低挑外链站 | 只过第 4 步的五项筛选，DR 高不等于对口，也不等于有人看 |
| 目录站填的是 GitHub repo | 有公司项目页就填项目页 |
| 条目格式自己发挥 | 照抄相邻条目，按字母序插入 |
| 所有列表用同一句描述 | 按每个列表的风格和长度改写 |
| PR 开了就算完成 | 合并且 README 里能看到条目才算上线；用第 7 步的监听或定期手动查 |
| 往不对口的分类硬塞 | 跳过，并写下原因 |
