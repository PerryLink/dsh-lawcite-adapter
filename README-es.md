# dsh-lawcite-adapter — Verificación de citas de artículos legales y de los elementos del documento jurídico

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-lawcite-adapter` lee un inventario de citas de artículos legales —la cabecera del documento más una fila por cita— y comprueba la verificabilidad y los elementos documentales de ese propio inventario: que cada cita indique la ley y el número de artículo, que el número de artículo siga la forma china, que se haya transcrito el texto citado, que el estado de vigencia provenga de su propio vocabulario, que la cita indique dónde se usa y qué argumenta, que la cabecera del documento declare su título y su tipo, que los números de cita no se repitan y que no sobreviva ningún marcador de plantilla en la columna del texto citado. No verifica que una ley exista, que esté vigente, que no haya sido modificada o derogada, ni que se aplique al caso.

## Cómo se ve la salida

![Terminal demo of dsh-lawcite-adapter: real output over its LC-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-lawcite-adapter/main/docs/assets/dsh-lawcite-adapter-demo.png)

Salida real de este plugin sobre su propio fixture de prueba `LC-001` — no es un montaje. El paquete de reglas no inventa citas, así que cada hallazgo nombra la cláusula aplicada y advierte que su texto no se obtuvo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fila lleva el número de artículo pero deja vacío el nombre de la ley. ¿Se informa? | Sí. `LC-001` exige el nombre de la ley y el número de artículo (`lawName`, `articleNo`) en cada fila e informa de la fila a la que le falta uno de los dos. Comprueba que estén escritos, no que la ley o el artículo existan: no incluye ninguna base de datos normativa ni la consulta. |
| El número de artículo figura como `第 577 条` o como `第12条第3款`. ¿Pasa la comprobación? | `LC-002` compara `articleNo` con `^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$`, de modo que tanto la forma con espacios `第 577 条` como la mixta `第12条第3款` se informan. Solo comprueba la forma del número, nada sobre si el artículo existe; el número de párrafo o de inciso va en su propia columna, así que `第12条` se escribe en `articleNo`. El `pattern` se puede ajustar a su estilo interno. |
| En una fila la columna del texto citado está vacía y en otra todavía dice `【待补充】`. ¿Se detectan ambos casos? | Sí, con dos reglas. `LC-003` exige que `quotedText` esté transcrito en cada fila; `LC-008` informa de la fila cuyo `quotedText` aún contiene un término de plantilla (`【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, `示例`). Ninguna compara el texto con la ley: `LC-003` comprueba que la cita esté presente, `LC-008` solo que no quede marcador alguno. 「略」 no figura entre los términos, así que `……（略）` es una abreviación normal y pasa. |
| El informe muestra `LC-004` como `skipped` en lugar de aprobado. ¿Por qué? | Porque la lista `values` de `LC-004` viene vacía, es decir, el vocabulario del estado de vigencia no está configurado, y la regla se informa en `skipped` en vez de pasar en silencio. Al llenar `values` con su propio vocabulario (por ejemplo `现行有效`, `已修订`, `已废止`), `LC-004` comprueba que `effectiveStatus` figure en esa lista. Comprueba la pertenencia a su lista, no que el estado registrado corresponda a los hechos. |
| Las filas indican la ley y transcriben el texto, pero no dicen dónde se usa la cita ni qué argumenta, y la cabecera no da el tipo de documento. ¿Se informa? | Sí. `LC-005` exige `usage` y `purpose` en cada fila de cita e informa de la fila que deja ambos vacíos; no juzga si la cita sostiene realmente ese argumento. `LC-006` exige que la cabecera declare `documentTitle` y `documentType`, y no juzga si el tipo se eligió correctamente. |
| El mismo artículo se cita en dos secciones y ambas filas llevan el número de cita 3. ¿Es un hallazgo? | Sí. `LC-007` informa de un `citationNo` repetido dentro del inventario, porque un número repetido impide que las notas localicen cada cita. Citar la misma disposición en varias secciones es normal: dé a cada cita su propio número. La regla no juzga si es adecuado citar dos veces la misma disposición. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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
