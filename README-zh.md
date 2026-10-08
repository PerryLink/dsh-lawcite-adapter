# dsh-lawcite-adapter — 法条引用与文书要素核对

`dsh-lawcite-adapter` 读取一份法条引用清单——表头加每处引用一行——核对这份清单自身的可核验性与文书要素：每处引用是否写明法律名称与条号、条号是否写成规范的中文形式、是否抄录了引用原文、效力状态是否取自本机构配置的取值、是否写明引用位置与论证作用、文书表头是否声明标题与文书类型、引用编号是否重复、引用原文栏是否残留未替换的占位符。它不核验法条是否真实存在、是否现行有效、是否已被修订或废止、是否适用于本案。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 某处引用填了条号，法律名称栏却是空的，会被报出吗？ | 会。`LC-001` 要求每处引用都写明法律名称与条号（`lawName`、`articleNo`），缺其一即报出该行。它只核对是否写明，不核验该法律或该条号是否存在——本插件不含法规库，也不查询法规库。 |
| 条号写成 `第 577 条`，或者写成 `第12条第3款`，能通过吗？ | `LC-002` 用 `^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$` 匹配 `articleNo`，因此带空格的 `第 577 条` 与混写的 `第12条第3款` 都会被报出。它只核对条号本身的形式，不核对条号是否存在；款、项应单列一栏，故 `第12条` 填在 `articleNo`。`pattern` 可按本机构口径调整。 |
| 某行的引用原文栏是空的，另一行还写着 `【待补充】`，两种情况都能查出来吗？ | 能，两条规则各管一头。`LC-003` 要求每行都抄录引用原文（`quotedText`）；`LC-008` 报出 `quotedText` 仍含模板用语的行（出厂 `terms` 为 `【`、`】`、`{{`、`}}`、`XXX`、`xxx`、`待填`、`待补充`、`TBD`、`todo`、`示例`）。两条都不与法条原文比对：`LC-003` 只核对是否抄录，`LC-008` 只核对是否残留占位符。`terms` 不含「略」，故 `……（略）` 属于正常省略写法。 |
| 报告里 `LC-004` 显示为 `skipped` 而不是通过，为什么？ | 因为 `LC-004` 的 `values` 出厂为空，表示效力状态口径尚未配置，本条报告「无法执行」而不是静默通过。把 `values` 填成本机构的取值（如 `现行有效`、`已修订`、`已废止`）后，`LC-004` 才核对 `effectiveStatus` 是否在册；在册与否之外，它不核验所填状态是否与事实相符。 |
| 各行写了法律名称也抄了原文，却没写引用位置与论证作用，表头也没写文书类型，会被报出吗？ | 会。`LC-005` 要求每处引用写明引用位置与论证作用（`usage`、`purpose`），两者都空即报出该行；它不判断该引用是否真的支持该论点。`LC-006` 要求表头声明文书标题与文书类型（`documentTitle`、`documentType`），它不判断类型选得对不对。 |
| 同一条法条在两章里各引一次，两行的引用编号都填了 3，会被报出吗？ | 会。`LC-007` 报出清单内重复的引用编号（`citationNo`），因为编号重复会让脚注无法准确定位到具体那处引用。同一法条在不同章节多次引用属于正常情形：给每处引用各自的编号即可。它不判断重复引用同一条法条是否恰当。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 本机构法律文书审查口径（本机构配置）—— 原挂《中华人民共和国立法法》，已核实其第六十五条为立法技术条款 | 无统一标准（本条依据为本机构配置的引用管理口径）—— ⚠️ 《立法法》2023 年第二次修正文本已核实，本条不引用该法 | LC-001 |
| 本机构法律文书审查口径（本机构配置）—— 原挂《党政机关公文格式》GB/T 9704—2012，已核实为版式标准 | GB/T 9704—2012（本次未取得条文） | LC-002, LC-003, LC-005, LC-006, LC-007, LC-008 |
| 本机构法律文书审查办法（本机构配置） | 无统一标准（本条依据为本机构配置的效力口径） | LC-004 |

**Boundary:** this plugin checks a **法条引用清单** for verifiability and document elements — that each citation
names its law and article, that the article number follows the Chinese form, that a direct quotation is
transcribed, that the power status comes from your vocabulary, that the citation states where it is used and what
it argues, that the document names its title and type, that citation numbers are unique, and that no placeholder
survives. It does **not** verify that a statute exists, that it is currently in force, that it has not been amended
or repealed, or that it applies to the case.

> ### ⚠️ This plugin does not query a statute database — and that is the point
>
> **It cannot find the most consequential error: a citation to a statute or article that does not exist, or that
> has been repealed.** Confirming that requires the national laws-and-regulations database and the facts of the
> case, which is a legal professional's work. What this plugin checks is whether a citation left behind the
> elements needed to verify it — the law, the article, the quoted text, the power status, the purpose.
>
> That boundary is stated in the pack's header, in `LC-001`'s, `LC-003`'s and `LC-004`'s notes, and in the
> troubleshooting section. Read it before acting on any finding: **a clean report from this plugin is not a
> statement that the citations are correct.**
>
> `LC-002` checks the article number's *form* — `第X条` in Chinese or Arabic numerals, allowing `第X条之一` —
> and nothing about whether the article exists. `LC-003` checks that a quotation is transcribed, not that the
> transcription matches the statute. `LC-004`'s power-status vocabulary ships **empty** because no statute's
> current status is built in either.
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The regime
> lives in 《中华人民共和国立法法》, GB/T 9704—2012 and each institution's legal-document review rules. The
> verification pass could not retrieve verbatim clause text, so the pack states the gap in the `excerpt` field
> itself and keeps every rule at `warn` or `info`. **When the texts are in hand, replace each `excerpt` with the
> real clause and raise `kind` to `direct`.**
>
> ⚠️ **One basis was corrected rather than completed.** GB/T 9704—2012《党政机关公文格式》 was verified chapter by
> chapter to be a **layout** standard — paper, typesetting, binding, the placement of document elements and the
> specimen forms. **It contains no provision about citation management at all.** Six rules had been hung on it
> anyway ("every citation must name the instrument and the article", "a direct quotation must be transcribed",
> and so on). Those six now declare **the institution's own legal-document review practice** as their basis, are
> rated **`institutional-configuration`**, and therefore sit at **`info`** rather than `warn`. Leaving them at
> `warn` while their own note says "read this as the institution's practice" would have contradicted itself.
>
> **`LC-001` was then corrected the same way.** It cited 《中华人民共和国立法法》. That statute was obtained in
> full and does contain a numbering provision — 第六十五条: 「法律根据内容需要，可以分编、章、节、条、款、项、目」，with
> numbering rules and an authorisation for the NPC Standing Committee's working body to draft legislative
> technique rules. But that governs **how a law is itself drafted and numbered**; it says nothing about how an
> official document cites an existing law. So `LC-001` joins the other seven: **all eight rules in this pack now
> declare the institution's own review practice as their basis and are rated `institutional-configuration` at
> `info`.** See `rules/evidence/clause-verification-basis-mismatch.md`.

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-lawcite-adapter
dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-lawcite-adapter
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-lawcite-adapter contributors.
