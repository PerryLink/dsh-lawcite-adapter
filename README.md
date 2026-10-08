# dsh-lawcite-adapter — Statute citation and legal document element check

`dsh-lawcite-adapter` reads one statute-citation inventory — the document header plus one row per citation — and checks that inventory's own verifiability and document elements: that each citation states its law and article number, that the article number follows the Chinese form, that a direct quotation has been transcribed into the quotation column, that the power status comes from your own vocabulary, that the citation states where it is used and what it argues, that the document header names its title and type, that citation numbers are not repeated, and that no unreplaced placeholder survives in the quotation column. It does not verify that a statute exists, that it is currently in force, that it has not been amended or repealed, or that it applies to the case.

## What it answers

| You ask | What it answers |
|---|---|
| A citation row carries an article number but the law name is blank. Is that reported? | Yes. `LC-001` requires the law name and the article number (`lawName`, `articleNo`) on every row and reports the row that leaves either one blank. It checks that they are written, not that the statute or the article exists: it holds no statute database and does not query one. |
| The article number is written `第 577 条`, or `第12条第3款`. Will it pass? | `LC-002` matches `articleNo` against `^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$`, so the spaced form `第 577 条` and the mixed form `第12条第3款` are both reported. It checks the form of the number only, nothing about whether the article exists; a paragraph or item number belongs in its own column, so `第12条` goes in `articleNo`. The `pattern` is adjustable to your house style. |
| One row's quotation column is empty and another still reads `【待补充】`. Are both caught? | Yes, by two rules. `LC-003` requires `quotedText` to be transcribed on every row; `LC-008` reports the row whose `quotedText` still contains a template term (`【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, `示例`). Neither compares the text with the statute: `LC-003` checks that a quotation is present, `LC-008` only that no placeholder survives. 「略」 is deliberately absent from the terms, so `……（略）` is a normal abridgement and passes. |
| The report shows `LC-004` as `skipped` instead of passing. Why? | Because `LC-004`'s `values` list ships empty, meaning the power-status vocabulary is not configured, so the rule reports itself in `skipped` rather than passing silently. Fill `values` with your own vocabulary (for example `现行有效`, `已修订`, `已废止`) and `LC-004` then checks that `effectiveStatus` is on that list. It checks membership in your list, not whether the recorded status matches the facts. |
| The rows name the law and quote it, but say nothing about where the citation is used or what it argues, and the header gives no document type. Is that reported? | Yes. `LC-005` requires `usage` and `purpose` on every citation row and reports a row that leaves both blank; it does not judge whether the citation really supports that argument. `LC-006` requires the header to declare `documentTitle` and `documentType`, and does not judge whether the type was chosen correctly. |
| The same article is cited in two sections and both rows carry citation number 3. Is that a finding? | Yes. `LC-007` reports a `citationNo` that repeats inside the inventory, because a repeated number stops the footnotes from locating each citation. Citing the same provision in several sections is normal: give each citation its own number. The rule does not judge whether citing the same provision twice is appropriate. |

## Standards it follows

| Document | Number | Cited by rules |
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

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a long submission use `ptc` |

## What it does

Registers the `lawcite_adapter` tool. It reads one citation inventory — the document header plus one row per
citation — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `LC-001` | the law name and article number are stated | info | local |
| `LC-002` | the article number follows the Chinese form | info | local |
| `LC-003` | a direct quotation is transcribed | info | local |
| `LC-004` | the power status comes from your vocabulary (off by default) | info | local |
| `LC-005` | the citation states its location and purpose | info | local |
| `LC-006` | the document names its title and type | info | local |
| `LC-007` | citation numbers are unique | info | local |
| `LC-008` | the quotation column holds no unreplaced placeholder | info | local |
## Install

```sh
dsh plugin --profile <name> add dsh-lawcite-adapter
dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `LC-002` `pattern` — the article number's shape, `第[〇零一二三四五六七八九十百千0-9]+条` plus an optional
  `之一`, by default. Adjust it if your house style writes numbers differently.
- `LC-004` `values` — your power-status vocabulary, e.g. `[现行有效, 已修订, 已废止, 尚未生效]`. Empty means no
  check, and **no statute's current status is built in either**.
- `LC-008` `terms` — the placeholders to look for. 「略」 is deliberately absent: `……（略）` is a normal way to
  abridge a long quotation.

## Material format

The tool accepts JSON or YAML:

```yaml
documentTitle: 某某买卖合同纠纷起诉状
documentType: 民事起诉状
author: 王律师
draftedAt: 2026-05-12
rows:
  - { 序号: '1', 法律法规名称: 《中华人民共和国民法典》, 条号: 第五百七十七条,
      引用原文: 当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。,
      引用位置: 第 2 部分 诉讼请求的事实与理由（第三段）,
      论证作用: 作为被告违约责任请求权的法律依据,
      效力状态: 现行有效, 版本说明: 2020 年 5 月 28 日通过，2021 年 1 月 1 日施行, 引用格式: 脚注① }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the inventory's own
column names are kept, so a finding names the column it read. Article numbers may use Chinese or Arabic numerals;
a spaced Arabic form like `第 577 条` is reported so the house style stays consistent.

## Rule sources

Rule data lives in `rules/lawcite-adapter.yaml`. Its header explains that the plugin holds no statute database and
verifies neither existence nor validity, and each rule's `note` repeats the part that matters for that rule. The
load-time guard still requires a document, clause, excerpt and source per rule, and still forbids a
principle-derived or locally configured check from being `error`.

## Troubleshooting

- **It passed a citation to a repealed statute.** By design: it checks that the citation is *verifiable*, never
  that it is *correct*. Verifying needs the national database, which the plugin does not query.
- **`LC-003` passed a quotation that is not what the statute says.** It checks that a quotation is *present*.
  Comparing it against the statute is the verification step it deliberately omits.
- **`LC-002` fires on a form I consider acceptable.** Adjust `pattern` to your house style. Note that paragraph
  and item numbers belong in their own columns here, so `第 12 条第 3 款` should put `第 12 条` in the article
  column.
- **`LC-004` never runs.** Its vocabulary is empty, and no statute's status is built in.
- **`LC-007` fires on one article cited twice.** Citing the same provision in several sections is normal — give
  each citation its own number, or the footnotes cannot locate them apart.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-lawcite-adapter@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-lawcite-adapter   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and the
check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-lawcite-adapter contributors.
