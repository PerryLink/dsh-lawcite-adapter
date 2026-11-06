<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-lawcite-adapter-hero-en-dark.webp">
  <img src="docs/assets/dsh-lawcite-adapter-hero-en-light.webp" width="100%" alt="dsh-lawcite-adapter: à esquerda, o nome do plugin, o lema em duas linhas e o limite (sem base de dados normativa, sem veredito, sem alterar o original); à direita, um inventário de citações —cabeçalho do documento e duas linhas, com lawName e articleNo vazios na linha 1 e um marcador não substituído em quotedText na linha 2— ao lado da lista de diferenças: achados LC-001 e LC-008, e LC-004 em skipped porque values não está configurado; o rodapé indica apenas diferenças, sem veredito, o original nunca é modificado.">
</picture>

# dsh-lawcite-adapter

**Confere cada citação de um documento jurídico —nome da lei, número do artigo, transcrição, status de vigência e elementos do documento— e devolve uma lista do que está inconsistente, onde e o que corrigir.**

Um verificador de citações para o DeepSeek Harness, feito para advogados, jurídico e redatores de documentos: o pacote de regras declara o fundamento de cada verificação, lista apenas diferenças literais, não decide conformidade, não atribui responsabilidade e nunca altera o original.

[Instalar](#instalação-em-três-passos) · [Configuração](#configuração) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidade)
[![npm](https://img.shields.io/npm/v/dsh-lawcite-adapter?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-lawcite-adapter)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-lawcite-adapter/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-lawcite-adapter/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidade)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-lawcite-adapter?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-lawcite-adapter/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-lawcite-adapter?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-lawcite-adapter)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-lawcite-adapter?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-lawcite-adapter?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-lawcite-adapter/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-lawcite-adapter)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-lawcite-adapter)

```sh
dsh plugin --profile <name> add dsh-lawcite-adapter
```

</div>

<sub>Plugin da comunidade, sem vínculo com a DeepSeek. Repositório canônico: <https://github.com/PerryLink/dsh-lawcite-adapter> (o Gitee é um espelho).</sub>

## O que é

O `dsh-lawcite-adapter` lê um inventário de citações —o cabeçalho do documento mais uma linha por citação— e confere o que esse inventário permite decidir de forma mecânica: se cada citação indica a lei e o número do artigo, se o número segue a forma chinesa, se a citação literal foi transcrita na coluna própria, se o status de vigência vem do seu vocabulário, se a citação indica onde é usada e o que sustenta, se o cabeçalho declara título e tipo de documento, se os números de citação se repetem e se sobrou algum marcador de modelo não substituído na coluna de citação literal. Você entrega o material original (uma tabela, um registro ou um documento; o Excel pode ser convertido antes para JSON/YAML, inclusive no chat quando a plataforma permite) e ele devolve uma lista de diferenças. Não verifica se uma lei existe, se está vigente, se foi alterada ou revogada, nem se se aplica ao caso. Não decide conformidade, não atribui responsabilidade, não substitui quem revisa e nunca altera o original.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-lawcite-adapter-flow-v5-dark.svg">
  <img src="docs/assets/dsh-lawcite-adapter-flow-v5-light.svg" width="100%" alt="Estrutura do dsh-lawcite-adapter: o cabeçalho e os sete campos de uma linha de citações que as regras leem são dispostos como colunas; cada regra aparece sob os campos que lê —LC-001 presenceAny (lawName e articleNo), LC-002 pattern, LC-003 presence e LC-008 containsAny (quotedText), LC-004 enum (effectiveStatus), LC-005 presenceAny (usage e purpose), LC-006 headerPresence (cabeçalho), LC-007 unique (citationNo)—. Na execução real do exemplo LC-001-unsafe.json, LC-001 produz um achado (linha 1, lawName e articleNo vazios), LC-004 não é executada porque values está sem configuração e entra em skipped, e as outras seis regras não produzem diferenças e não entram em nenhuma lista. O relatório traz error 0 / warn 0 / info 1, issueCount 1 e skippedCount 1; uma faixa separada mantém visível o limite: existência da norma, vigência, alteração ou revogação, aplicabilidade, conformidade e responsabilidade não são verificadas. Apenas diferenças, sem veredito, o original nunca é modificado.">
</picture>

## Instalação em três passos

1. **Instalar**:

   ```sh
   dsh plugin --profile <name> add dsh-lawcite-adapter
   ```

   Também é possível buscá-lo no WorkBuddy / Coze como «Documents and Governance Check Suite» (o conjunto completo; esta verificação é uma parte; disponibilidade conforme catálogo).

2. **Configuração mínima** (funciona como está):

   ```yaml
   - insert:
       - id: dsh-lawcite-adapter
         name: dsh-lawcite-adapter
   ```

   Todos os parâmetros ficam no esquema Schemastery de `src/config.ts` e os padrões funcionam sem ajuste; os limites de cada regra ficam no pacote de regras em `rules/`.

3. **Conferir que monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
   ```

   Depois rode o exemplo incluído (cerca de um minuto):

   ```sh
   node samples/quickstart/run.mjs --check
   ```

   A entrada do exemplo está em `samples/quickstart/input/`, a saída esperada em `samples/quickstart/expected/result.json` e uma execução capturada em `docs/assets/quickstart.png`.

**Desinstalar**: `dsh plugin --profile <name> remove dsh-lawcite-adapter` (ou remova a linha do patch do perfil).

<details>
<summary>Instalar pelo mercado do DSH Desktop</summary>

Todos os plugins PerryLink estão no mercado embutido do DSH Desktop: **Mercado → Fontes → Adicionar fonte → cole** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ selecione**. A instalação continua passando pela checagem de identidade npm do mercado e pela sua confirmação.

</details>

## Capacidades principais

O plugin registra a ferramenta `lawcite_adapter`: lê um inventário de citações (cabeçalho do documento mais uma linha por citação), aplica um pacote de regras versionado e devolve um relatório estruturado.

- **O pacote de regras é dado, não código** — cada regra fica em `rules/lawcite-adapter.yaml`; trocar o arquivo troca o conjunto de regras sem tocar em TypeScript, e o pacote é validado na carga, não presumido.
- **A gravidade segue a evidência** — uma regra apoiada na configuração da sua instituição (`institutional-configuration`) fica no máximo em `info`; uma apoiada em princípio geral (`derived-from-principle`) fica no máximo em `warn`; nenhuma pode ser declarada `error` (há teste que exige isso). As oito regras atuais são `institutional-configuration` em `info`.
- **Lista vazia nunca é «tudo certo»** — toda verificação que não pôde rodar se declara em `skipped` com o motivo, e uma regra cuja lista exigida está sem configuração se declara em `skipped` em vez de passar em silêncio (a lista `values` da `LC-004` vem vazia).
- **Sem julgamento** — o relatório lista diferenças e nunca se pronuncia sobre conformidade, responsabilidade ou acerto; um guarda de redação obriga o relatório a trazer sempre o aviso legal.
- **Fundamento conforme obtido** — cada regra traz documento, número, descrição da cláusula, trecho literal e URL de leitura; o trecho precisa ser citação real de pelo menos oito caracteres. Quando o texto literal não foi obtido, o próprio trecho diz isso e a regra é marcada como derivada de princípio ou configurada pela instituição: nunca se apresenta uma paráfrase como citação.

```text
inventário de citações (cabeçalho · uma linha por citação) ──lawcite_adapter──▶ pacote LC-001…LC-008 ──▶ relatório (findings + skipped)
        ▲                                                                                                        │
        └──────────────────────────────── o original nunca é alterado ──────────────────────────────────────────┘
```

### As regras em resumo

| Regra | Confere | Gravidade | Tipo de fundamento |
|---|---|---|---|
| `LC-001` | indicam-se o nome da lei e o número do artigo | info | local |
| `LC-002` | o número do artigo segue a forma chinesa | info | local |
| `LC-003` | a citação literal está transcrita | info | local |
| `LC-004` | o status de vigência vem do seu vocabulário (desligada por padrão) | info | local |
| `LC-005` | a citação indica onde é usada e o que sustenta | info | local |
| `LC-006` | o documento declara título e tipo | info | local |
| `LC-007` | os números de citação são únicos | info | local |
| `LC-008` | a coluna de citação literal não guarda marcadores não substituídos | info | local |

A `LC-004` vem com a lista de valores vazia, então se declara em `skipped` até você configurá-la: nunca passa em silêncio.

### Exemplos

Estes são os pontos de entrada reais do plugin; instale uma vez e chame um deles.

**Saída detalhada** — ferramenta `lawcite_adapter`, entrada:

```json
{"documentTitle":"某某买卖合同纠纷起诉状","documentType":"民事起诉状","rows":[{"法律法规名称":"","条号":"","引用原文":"当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"}]}
```

Saída:

```json
{
  "id": "dsh-lawcite-adapter.LC-001.de09b5a6",
  "ruleId": "LC-001",
  "severity": "info",
  "locator": {
    "row": 1,
    "field": "lawName"
  },
  "found": "第 1 行 lawName、articleNo 都为空",
  "expected": "lawName、articleNo 至少应填写一项"
}
```

*Observed from `dsh-lawcite-adapter/tests/fixtures/LC-001/LC-001-unsafe.json`*

É a **saída real** do plugin para o próprio fixture `LC-001`, não uma ilustração. O pacote de regras nunca fabrica citação, então cada achado informa tanto o fundamento de que foi lido quanto o fato de o texto desse fundamento não ter sido obtido nesta rodada.

### O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha traz número de artigo, mas o nome da lei está vazio. Isso é reportado? | Sim. A `LC-001` exige o nome da lei e o número do artigo (`lawName`, `articleNo`) em cada linha e reporta a linha que deixa qualquer um dos dois vazio. Confere se estão escritos, não se a lei ou o artigo existe: não embute base normativa nem a consulta. |
| O número do artigo é escrito com espaço dentro, ou com um número de parágrafo anexado. Vai passar? | A `LC-002` compara `articleNo` com o padrão ancorado documentado em «Formato do material», então tanto a forma com espaço quanto a forma mista são reportadas. Confere só a forma do número, nada sobre a existência do artigo; parágrafo e inciso vão em coluna própria, então a coluna do artigo guarda apenas a parte do artigo. O `pattern` é ajustável ao seu padrão interno. |
| A coluna de citação literal de uma linha está vazia e outra ainda guarda um marcador de modelo. As duas são pegas? | Sim, por duas regras. A `LC-003` exige `quotedText` transcrito em cada linha; a `LC-008` reporta a linha cujo `quotedText` ainda contém termo de modelo (a lista de fábrica cobre colchetes e chaves de modelo, um marcador de xis e os avisos usuais de «preencher»; a lista exata está documentada no pacote de regras). Nenhuma compara o texto com a lei: a `LC-003` confere se a citação existe, a `LC-008` só que não sobrou marcador. O marcador de abreviação está deliberadamente ausente, então um corte normal de citação longa passa. |
| O relatório mostra a `LC-004` como `skipped` em vez de aprovada. Por quê? | Porque a lista `values` da `LC-004` vem vazia, ou seja, o vocabulário de status de vigência não está configurado, então a regra se declara em `skipped` em vez de passar em silêncio. Preencha `values` com o seu vocabulário (por exemplo os termos locais de vigente, alterada, revogada) e a `LC-004` passa a conferir se `effectiveStatus` está nessa lista. Confere a pertinência à sua lista, não se o status registrado corresponde aos fatos. |
| As linhas nomeiam a lei e a citam, mas não dizem onde a citação é usada nem o que sustenta, e o cabeçalho não traz o tipo de documento. Isso é reportado? | Sim. A `LC-005` exige `usage` e `purpose` em cada linha de citação e reporta a linha que deixa os dois em branco; não julga se a citação realmente sustenta aquele argumento. A `LC-006` exige que o cabeçalho declare `documentTitle` e `documentType`, e não julga se o tipo foi escolhido corretamente. |
| O mesmo artigo é citado em duas seções e as duas linhas levam o número de citação 3. É um achado? | Sim. A `LC-007` reporta o `citationNo` que se repete dentro do inventário, porque número repetido impede as notas de rodapé de localizar cada citação. Citar a mesma disposição em várias seções é normal: dê a cada citação o seu número. A regra não julga se citar duas vezes a mesma disposição é adequado. |

## Configuração

Todos os parâmetros ficam no esquema Schemastery de `src/config.ts`, então podem ser alterados pelo `cordis.yml` sem editar código; os limites de cada regra ficam no pacote de regras em `rules/`. As cinco chaves abaixo são a lista completa; os parâmetros de regra vêm depois.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regra que deixam de rodar; cada um aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Rodar só estes ids de regra; vazio roda todas |
| `skipNotes` | string | `""` | Nota anexada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de timeout cooperativo da ferramenta |

Parâmetros de regra que vale conhecer:

- `LC-002` `pattern` — a forma do número do artigo: por padrão a marca de artigo com um numeral chinês ou árabe e um sufixo opcional de subartigo. Ajuste o padrão se o seu estilo interno escreve os números de outro modo.
- `LC-004` `values` — seu vocabulário de status de vigência, p. ex. `[vigente, alterada, revogada, ainda não vigente]`. Vazio significa que não há verificação, e também não há nenhum status normativo embutido.
- `LC-008` `terms` — os marcadores procurados. O marcador de abreviação está deliberadamente ausente: encurtar uma citação longa com reticências é uma forma normal de abreviá-la.

Exemplo de sobrescrita no patch do seu perfil:

```yaml
- insert:
    - id: dsh-lawcite-adapter
      name: dsh-lawcite-adapter
      config:
        onlyRules: [LC-001, LC-002, LC-008]
        skipNotes: manual interno da instituição, edição 2026
```

## FAQ

<details>
<summary>Meu material é alterado ou enviado para algum lugar?</summary>

Não. A ferramenta apenas lê o texto JSON/YAML que você entrega e **nunca altera o original**; o plugin é ESM puro, sem código nativo, **sem rede e sem chamada a modelo** (ver Compatibilidade), então o material não sai da sua máquina.

</details>

<details>
<summary>Sem vocabulário de status de vigência configurado, algo passa em silêncio?</summary>

Não. A lista `values` da `LC-004` vem vazia, e uma regra cuja lista está sem configuração se declara em `skipped` com o motivo, então uma lista de diferenças vazia nunca é lida como «não falta nada». Depois de preenchida, a regra só confere se o valor registrado está na sua lista, não se corresponde aos fatos.

</details>

<details>
<summary>Ele consegue verificar se uma lei existe ou está vigente?</summary>

Não. O plugin não embute base normativa nem a consulta; confere se a citação deixou os elementos necessários para verificá-la: a lei, o artigo, a citação literal, o status de vigência e a finalidade. Confirmar que uma lei ou um artigo existe, está vigente ou não foi alterado ou revogado exige a base nacional de leis e regulamentos e os fatos do caso, o que é trabalho de um profissional do Direito. Ver «Normas que segue».

</details>

<details>
<summary>O plugin instala, mas a ferramenta nunca aparece. E agora?</summary>

Confira se `main` resolve para `lib/index.mjs` e se `pnpm run build` o gerou; um `main` errado faz o carregador pular a entrada em silêncio.

</details>

<details>
<summary>Dá conta de um documento longo ou de um diretório inteiro em lote?</summary>

A ferramenta funciona nos modos `native` e `ptc`; para um lote sobre um diretório use `ptc`, assim o custo do esquema é pago uma vez. Toda a aritmética é de relógio de parede sobre as strings de entrada, sem conversão de fuso horário.

</details>

## Normas que segue

O pacote de regras declara um fundamento para cada verificação. A tabela traz os documentos e números que as oito regras carregam hoje; todos os fundamentos são configuração da instituição e todas as regras estão em `info`.

| Documento | Número | Regras que o citam |
|---|---|---|
| Critério de revisão de documentos jurídicos da instituição (configuração própria) — antes atribuído à Lei de Legislação da RPC; verificou-se que seu artigo 65 é cláusula de técnica legislativa | Sem norma uniforme (o fundamento é o critério próprio de gestão de citações da instituição) — o texto da segunda alteração de 2023 da Lei de Legislação foi verificado e esta regra não a cita | LC-001 |
| Critério de revisão de documentos jurídicos da instituição (configuração própria) — antes atribuído à GB/T 9704—2012, verificada como norma de leiaute | GB/T 9704—2012 (texto da cláusula não obtido nesta rodada) | LC-002, LC-003, LC-005, LC-006, LC-007, LC-008 |
| Medidas de revisão de documentos jurídicos da instituição (configuração própria) | Sem norma uniforme (o fundamento é o critério próprio de status de vigência da instituição) | LC-004 |

Títulos originais dos documentos citados:

```text
《中华人民共和国立法法》 2023 年第二次修正
《党政机关公文格式》 GB/T 9704—2012
本机构法律文书审查口径（本机构配置）
本机构法律文书审查办法（本机构配置）
```

**Limite:** este plugin confere um **inventário de citações** quanto a verificabilidade e elementos do documento: se cada citação nomeia sua lei e seu artigo, se o número do artigo segue a forma chinesa, se a citação literal está transcrita, se o status de vigência vem do seu vocabulário, se a citação indica onde é usada e o que sustenta, se o documento declara título e tipo, se os números de citação são únicos e se não sobrou marcador. **Não** verifica se uma lei existe, se está vigente, se não foi alterada ou revogada, nem se se aplica ao caso.

> ### ⚠️ Este plugin não consulta base de dados normativa — e esse é o ponto
>
> **Ele não consegue encontrar o erro mais grave: a citação de uma lei ou de um artigo que não existe ou que foi revogado.** Confirmar isso exige a base nacional de leis e regulamentos e os fatos do caso, o que é trabalho de um profissional do Direito. O que o plugin confere é se a citação deixou os elementos necessários para verificá-la: a lei, o artigo, o texto citado, o status de vigência e a finalidade.
>
> Esse limite está escrito no cabeçalho do pacote, nas notas da `LC-001`, da `LC-003` e da `LC-004`, e na seção de resolução de problemas. Leia antes de agir com base em qualquer achado: **um relatório limpo deste plugin não afirma que as citações estão corretas.**
>
> A `LC-002` confere a *forma* do número do artigo —a marca de artigo com um numeral chinês ou árabe e um sufixo opcional de subartigo— e nada sobre a existência do artigo. A `LC-003` confere se a citação foi transcrita, não se a transcrição corresponde à lei. O vocabulário de status de vigência da `LC-004` vem **vazio** porque também não há embutido o status atual de nenhuma lei.
>
> **Cada `excerpt` do pacote de regras diz, com todas as letras, que o texto da cláusula não foi obtido.** O regime está na Lei de Legislação da RPC, na GB/T 9704—2012 e nas regras de revisão de documentos jurídicos de cada instituição. A passagem de verificação não conseguiu recuperar o texto literal, então o pacote declara a lacuna no próprio campo `excerpt` e mantém cada regra em `warn` ou `info`. **Quando os textos estiverem em mãos, substitua cada `excerpt` pela cláusula real e eleve `kind` para `direct`.**
>
> ⚠️ **Um fundamento foi corrigido em vez de completado.** Verificou-se capítulo a capítulo que a GB/T 9704—2012 é norma de **leiaute**: papel, composição, encadernação, posição dos elementos do documento e formulários de modelo. **Ela não contém nenhuma disposição sobre gestão de citações.** Seis regras tinham sido penduradas nela mesmo assim («toda citação deve nomear o instrumento e o artigo», «a citação literal deve ser transcrita», etc.). Essas seis agora declaram como fundamento **a prática de revisão de documentos jurídicos da própria instituição**, são classificadas **`institutional-configuration`** e por isso ficam em **`info`** em vez de `warn`. Deixá-las em `warn` enquanto a própria nota diz «leia como prática da instituição» seria contraditório.
>
> **A `LC-001` foi corrigida depois, do mesmo modo.** Ela citava a Lei de Legislação. Essa lei foi obtida na íntegra e de fato contém uma disposição de numeração: o artigo 65 organiza uma lei em partes, capítulos, seções, artigos, parágrafos, incisos e alíneas conforme o conteúdo, com regras de numeração e autorização ao órgão de trabalho do Comitê Permanente da Assembleia Popular Nacional para redigir normas de técnica legislativa. Mas isso regula **como uma lei é redigida e numerada**; não diz nada sobre como um documento oficial cita uma lei existente. Então a `LC-001` se junta às outras sete: **as oito regras deste pacote agora declaram como fundamento a prática de revisão da própria instituição e são classificadas `institutional-configuration` em `info`.** Ver `rules/evidence/clause-verification-basis-mismatch.md`.

## Formato do material

A ferramenta aceita JSON ou YAML:

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

Os nomes de coluna são comparados sem diferenciar maiúsculas e ignorando espaços, sublinhados e hífens; os nomes próprios do inventário são preservados, então um achado nomeia a coluna que leu. Os números de artigo aceitam algarismos chineses ou árabes; uma forma árabe com espaço é reportada para manter o padrão interno coerente:

```text
Padrão da LC-002 (por padrão): ^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$

第577条          ✓ passa na LC-002
第12条之一        ✓ passa na LC-002
第 577 条        ✗ reportado: o número do artigo contém espaço
第12条第3款       ✗ reportado: ponha 第12条 na coluna do artigo e o parágrafo à parte
```

Os campos de cabeçalho (`documentTitle`, `documentType`, `author`, `draftedAt` etc.) são opcionais na camada de leitura e validados pelo motor de verificação, então um material parcialmente exportado produz diferenças de «campo ausente» em vez de travar a ferramenta.

## Fontes das regras

Os dados das regras ficam em `rules/lawcite-adapter.yaml`, separados do código. Cada regra traz documento, número, cláusula descrita na numeração própria da fonte, trecho literal e URL de leitura. O carregador exige que o trecho seja citação real de pelo menos oito caracteres, e que uma verificação apoiada em princípio geral (`derived-from-principle`, teto `warn`) ou em política local (`institutional-configuration`, teto `info`) **nunca** possa ser declarada `error`. Um pacote que exagera o fundamento falha na carga em vez de produzir um relatório que pareça sólido.

⚠️ Todos os trechos deste pacote declaram que o texto da cláusula não foi obtido: a passagem de verificação não conseguiu recuperá-lo, então as oito regras se apoiam no critério de revisão da própria instituição, são classificadas `institutional-configuration` e ficam em `info`. **Isso não enfraquece a exigência: é recusar registrar peso sobre um documento que não o carrega.**

O relatório completo de verificação de cláusulas —a enumeração capítulo a capítulo do escopo da GB/T 9704—2012, as fontes verificadas e descartadas e a conclusão de que «o fundamento não coincide com o objeto»— está em `rules/evidence/clause-verification-basis-mismatch.md`.

## Compatibilidade

| Superfície | Status |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado que aceita tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` é declarado como `>=0.2.1-0 <0.3.0` e aplicado pelo host desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada a modelo) |
| Modo de ferramenta | Funciona em `native` e `ptc`; para lote sobre um diretório use `ptc` |

## Resolução de problemas

- **Aprovou uma citação de lei revogada.** Por projeto: confere se a citação é *verificável*, nunca se é *correta*. Verificar exige a base nacional, que o plugin não consulta.
- **A `LC-003` aprovou uma citação que não corresponde à lei.** Confere se a citação está *presente*. Compará-la com a lei é o passo de verificação que ela deliberadamente omite.
- **A `LC-002` acusa uma forma que considero aceitável.** Ajuste `pattern` ao seu padrão interno. Aqui parágrafos e incisos vão em colunas próprias, então um valor misto deve guardar só a parte do artigo na coluna dele.
- **A `LC-004` nunca roda.** O vocabulário está vazio e não há embutido o status de nenhuma lei.
- **A `LC-007` acusa um artigo citado duas vezes.** Citar a mesma disposição em várias seções é normal: dê a cada citação o seu número, ou as notas de rodapé não conseguirão separá-las.
- **Uma regra não rodou.** Veja o array `skipped`: ele nomeia o id da regra e o motivo.
- **O leitor recusa o material.** Não encontrou nenhuma das colunas de citação conhecidas (nome da lei, número do artigo, citação literal); preencha como descrito em «Formato do material» e rode de novo.
- **O plugin instala, mas a ferramenta nunca aparece.** Confira se `main` resolve para `lib/index.mjs` e se `pnpm run build` o gerou; um `main` errado faz o carregador pular a entrada em silêncio.
- **`dsh plugin add` recusa o pacote por incompatibilidade.** A faixa de peers cobre `0.1.x` e `0.2.x`; se o seu runtime estiver fora, conceda isenção explícita: `dsh plugin --profile <name> allow-version dsh-lawcite-adapter@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` informa `manifest-peers` como falho.** O verificador estático compara com uma faixa de peers fixa anterior à linha 0.2. O runtime aplica a compatibilidade na instalação, então a faixa declarada é a correta; é um problema conhecido do `dsh-plugin-dev`.
- **Os horários parecem deslocados.** Toda a aritmética é de relógio de parede sobre as strings de entrada, sem conversão de fuso horário.

## Ecossistema e qualidade

- [Espelho no Gitee](https://gitee.com/perrylink/dsh-lawcite-adapter) (espelho sincronizado; o GitHub é a referência)
- [Página do plugin no dshfind](https://dshfind.com/plugins/PerryLink/dsh-lawcite-adapter) (instalações e classificação)
- [Relatório do OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-lawcite-adapter) (gerado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (publicado)
- [Base de conhecimento do ecossistema: escolher um verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice completo da família: 62 verificadores e plugins gerais)

## Desenvolvimento

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, fixtures pareados por regra (tests/fixtures/<RULE>/)
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes   # coerência dos README em cinco idiomas
node ../scripts/sync-shared.mjs dsh-lawcite-adapter   # atualiza src/shared a partir de ../_shared
```

O plugin é orientado por dados: `src/model.ts` declara a forma da tabela, o kit compartilhado fornece o leitor e o motor de verificação, e o pacote de regras declara cada verificação. O pacote de regras é dado, não código: editar `rules/*.yaml` troca o conjunto de regras sem tocar em TypeScript; o pacote é validado na carga, não presumido. As imagens do README são geradas por programa por [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow): o hero é um conjunto de quatro webp (zh/en × claro/escuro) e o diagrama estrutural é SVG escrito à mão (claro + escuro, mapa de colunas campo × regra).

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `lawcite`

## Família e agradecimentos

Este projeto faz parte da família de plugins do DeepSeek Harness mantida por [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Se este plugin for útil, **uma estrela** não desbloqueia nada, mas ajuda a próxima pessoa a encontrá-lo.

- [@PerryLink](https://github.com/PerryLink) — criador e mantenedor: a ferramenta `lawcite_adapter`, o pacote de regras com fundamento declarado em cada verificação e seu registro de verificação de cláusulas, e a documentação em cinco idiomas.

<details>
<summary>Expandir todos os plugins</summary>

| Plugin | Status |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver o README do repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 APOSENTADO (repo arquivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 APOSENTADO (repo arquivado) |

</details>

## Licença

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-lawcite-adapter contributors

<p align="center"><sub>Apache-2.0 · Plugin da comunidade, sem vínculo com a DeepSeek.</sub></p>
