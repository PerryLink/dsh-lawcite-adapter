# dsh-lawcite-adapter — Verificação de citações de artigos legais e dos elementos do documento jurídico

`dsh-lawcite-adapter` lê um inventário de citações de artigos legais —o cabeçalho do documento mais uma linha por citação— e verifica a verificabilidade e os elementos documentais desse próprio inventário: se cada citação indica a lei e o número do artigo, se o número do artigo segue a forma chinesa, se o texto citado foi transcrito, se a situação de vigência vem do seu próprio vocabulário, se a citação indica onde é usada e o que argumenta, se o cabeçalho do documento declara o título e o tipo, se os números de citação não se repetem e se não resta nenhum marcador de modelo na coluna do texto citado. Não verifica se uma lei existe, se está em vigor, se não foi alterada ou revogada, nem se se aplica ao caso.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha traz o número do artigo, mas o nome da lei está em branco. Isso é reportado? | Sim. `LC-001` exige o nome da lei e o número do artigo (`lawName`, `articleNo`) em cada linha e reporta a linha à qual falta um dos dois. Verifica que estejam escritos, não que a lei ou o artigo exista: não inclui nenhuma base de dados normativa nem a consulta. |
| O número do artigo está escrito `第 577 条` ou `第12条第3款`. Isso passa? | `LC-002` compara `articleNo` com `^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$`, portanto tanto a forma com espaços `第 577 条` como a forma mista `第12条第3款` são reportadas. Verifica apenas a forma do número, nada sobre a existência do artigo; o número do parágrafo ou do inciso vai na sua própria coluna, pelo que `第12条` se escreve em `articleNo`. O `pattern` pode ser ajustado ao seu estilo interno. |
| Numa linha a coluna do texto citado está vazia e noutra ainda diz `【待补充】`. Ambos os casos são detetados? | Sim, por duas regras. `LC-003` exige que `quotedText` seja transcrito em cada linha; `LC-008` reporta a linha cujo `quotedText` ainda contém um termo de modelo (`【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, `示例`). Nenhuma compara o texto com a lei: `LC-003` verifica que a citação esteja presente, `LC-008` apenas que não reste qualquer marcador. 「略」 não consta dos termos, pelo que `……（略）` é uma abreviação normal e passa. |
| O relatório mostra `LC-004` como `skipped` em vez de aprovado. Porquê? | Porque a lista `values` de `LC-004` vem vazia, ou seja, o vocabulário da situação de vigência não está configurado, e a regra reporta-se em `skipped` em vez de passar em silêncio. Ao preencher `values` com o seu próprio vocabulário (por exemplo `现行有效`, `已修订`, `已废止`), `LC-004` passa a verificar se `effectiveStatus` consta dessa lista. Verifica a pertença à sua lista, não se o estado registado corresponde aos factos. |
| As linhas indicam a lei e transcrevem o texto, mas não dizem onde a citação é usada nem o que argumenta, e o cabeçalho não indica o tipo de documento. Isso é reportado? | Sim. `LC-005` exige `usage` e `purpose` em cada linha de citação e reporta a linha que deixa ambos em branco; não julga se a citação sustenta realmente esse argumento. `LC-006` exige que o cabeçalho declare `documentTitle` e `documentType`, e não julga se o tipo foi escolhido corretamente. |
| O mesmo artigo é citado em duas secções e ambas as linhas levam o número de citação 3. Isso é um achado? | Sim. `LC-007` reporta um `citationNo` repetido dentro do inventário, porque um número repetido impede que as notas localizem cada citação. Citar a mesma disposição em várias secções é normal: dê a cada citação o seu próprio número. A regra não julga se é adequado citar duas vezes a mesma disposição. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-lawcite-adapter
dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-lawcite-adapter
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-lawcite-adapter contributors.
