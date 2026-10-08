# dsh-lawcite-adapter

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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-lawcite-adapter
dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-lawcite-adapter
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-lawcite-adapter contributors.
