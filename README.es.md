<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-lawcite-adapter-hero-en-dark.webp">
  <img src="docs/assets/dsh-lawcite-adapter-hero-en-light.webp" width="100%" alt="dsh-lawcite-adapter: a la izquierda, el nombre del plugin, el lema en dos líneas y el límite (sin base de datos normativa, sin veredicto, sin editar el original); a la derecha, un inventario de citas —cabecera del documento y dos filas, con lawName y articleNo vacíos en la fila 1 y un marcador sin sustituir en quotedText de la fila 2— junto a la lista de diferencias: hallazgos LC-001 y LC-008, y LC-004 en skipped porque values no está configurado; el pie indica solo diferencias, sin veredicto, el original nunca se modifica.">
</picture>

# dsh-lawcite-adapter

**Verifica cada cita de un documento jurídico —nombre de la ley, número de artículo, transcripción, estado de vigencia y elementos del documento— y devuelve una lista de qué es inconsistente, dónde y qué corregir.**

Un verificador de citas para DeepSeek Harness, pensado para abogados, asesoría jurídica y redactores de documentos: el paquete de reglas declara su fundamento en cada comprobación, solo enumera diferencias literales, no dictamina cumplimiento, no atribuye responsabilidad y nunca modifica el original.

[Instalar](#instalación-en-tres-pasos) · [Configuración](#configuración) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidad)
[![npm](https://img.shields.io/npm/v/dsh-lawcite-adapter?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-lawcite-adapter)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-lawcite-adapter/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-lawcite-adapter/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidad)

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

<sub>Complemento comunitario, sin relación con DeepSeek. Repositorio canónico: <https://github.com/PerryLink/dsh-lawcite-adapter> (Gitee es un espejo).</sub>

## Qué es

`dsh-lawcite-adapter` lee un inventario de citas —la cabecera del documento más una fila por cita— y comprueba lo que ese inventario puede verificarse de forma mecánica: que cada cita indique la ley y el número de artículo, que el número siga la forma china, que se haya transcrito la cita literal en su columna, que el estado de vigencia provenga de tu propio vocabulario, que la cita indique dónde se usa y qué sostiene, que la cabecera declare el título y el tipo de documento, que los números de cita no se repitan y que no quede ningún marcador de plantilla sin sustituir en la columna de cita literal. Tú entregas el material original (una tabla, un registro o un documento; Excel puede convertirse antes a JSON/YAML, también en el chat si la plataforma lo admite) y él devuelve una lista de diferencias. No verifica que una ley exista, esté vigente, no haya sido modificada o derogada, ni que se aplique al caso. No dictamina cumplimiento, no atribuye responsabilidad, no sustituye a quien revisa y nunca modifica el original.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-lawcite-adapter-flow-v5-dark.svg">
  <img src="docs/assets/dsh-lawcite-adapter-flow-v5-light.svg" width="100%" alt="Estructura de dsh-lawcite-adapter: la cabecera y los siete campos de una fila de citas que leen las reglas se disponen como columnas; cada regla aparece bajo los campos que lee —LC-001 presenceAny (lawName y articleNo), LC-002 pattern, LC-003 presence y LC-008 containsAny (quotedText), LC-004 enum (effectiveStatus), LC-005 presenceAny (usage y purpose), LC-006 headerPresence (cabecera), LC-007 unique (citationNo)—. En la ejecución real del ejemplo LC-001-unsafe.json, LC-001 produce un hallazgo (fila 1, lawName y articleNo vacíos), LC-004 no se ejecuta porque values está sin configurar y se registra en skipped, y las otras seis reglas no producen diferencias y no entran en ninguna lista. El informe lleva error 0 / warn 0 / info 1, issueCount 1 y skippedCount 1; una franja aparte mantiene visible el límite: existencia de la norma, vigencia, modificación o derogación, aplicabilidad, cumplimiento y responsabilidad no se comprueban. Solo diferencias, sin veredicto, el original nunca se modifica.">
</picture>

## Instalación en tres pasos

1. **Instalar**:

   ```sh
   dsh plugin --profile <name> add dsh-lawcite-adapter
   ```

   También puedes buscarlo en WorkBuddy / Coze como «Documents and Governance Check Suite» (el conjunto completo; esta comprobación es una parte; disponibilidad según catálogo).

2. **Configuración mínima** (funciona tal cual):

   ```yaml
   - insert:
       - id: dsh-lawcite-adapter
         name: dsh-lawcite-adapter
   ```

   Todos los parámetros viven en el esquema Schemastery de `src/config.ts` y los valores por defecto sirven sin cambios; los umbrales de cada regla están en el paquete de reglas bajo `rules/`.

3. **Comprobar que se monta**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
   ```

   Después ejecuta el ejemplo incluido (alrededor de un minuto):

   ```sh
   node samples/quickstart/run.mjs --check
   ```

   La entrada del ejemplo está en `samples/quickstart/input/`, la salida esperada en `samples/quickstart/expected/result.json` y una ejecución capturada en `docs/assets/quickstart.png`.

**Desinstalar**: `dsh plugin --profile <name> remove dsh-lawcite-adapter` (o elimina la fila del patch del perfil).

<details>
<summary>Instalar desde el mercado de DSH Desktop</summary>

Todos los complementos de PerryLink están en el mercado integrado de DSH Desktop: **Mercado → Fuentes → Añadir fuente → pega** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ selecciona**. La instalación sigue pasando por la verificación de identidad npm del mercado y tu confirmación.

</details>

## Capacidades clave

El complemento registra la herramienta `lawcite_adapter`: lee un inventario de citas (cabecera del documento más una fila por cita), aplica un paquete de reglas versionado y devuelve un informe estructurado.

- **El paquete de reglas es dato, no código** — cada regla vive en `rules/lawcite-adapter.yaml`; cambiar el archivo cambia el conjunto de reglas sin tocar TypeScript, y el paquete se valida al cargar, no se da por bueno.
- **La gravedad sigue a la evidencia** — una regla que se apoya en la configuración de tu institución (`institutional-configuration`) queda como máximo en `info`; una que se apoya en un principio general (`derived-from-principle`) queda como máximo en `warn`; ninguna puede declararse `error` (hay un test que lo exige). Las ocho reglas actuales son `institutional-configuration` en `info`.
- **Una lista vacía nunca es «todo correcto»** — cada comprobación que no pudo ejecutarse se declara en `skipped` con su motivo, y una regla cuya lista requerida está sin configurar se declara en `skipped` en lugar de pasar en silencio (la lista `values` de `LC-004` viene vacía).
- **Sin juicio** — el informe enumera diferencias y nunca se pronuncia sobre cumplimiento, responsabilidad o corrección; un guardián de redacción obliga a que el informe lleve siempre el descargo de responsabilidad.
- **Fundamento tal como se obtuvo** — cada regla lleva documento, número, descripción de la cláusula, extracto y URL de lectura; el extracto debe ser una cita real de al menos ocho caracteres. Cuando el texto literal no se obtuvo, el extracto lo dice y la regla se marca como derivada de principio o configurada por la institución: nunca se presenta una paráfrasis como cita.

```text
inventario de citas (cabecera · una fila por cita) ──lawcite_adapter──▶ paquete LC-001…LC-008 ──▶ informe (findings + skipped)
        ▲                                                                                              │
        └────────────────────────────── el original nunca se modifica ────────────────────────────────┘
```

### Las reglas de un vistazo

| Regla | Comprueba | Gravedad | Tipo de fundamento |
|---|---|---|---|
| `LC-001` | se indican el nombre de la ley y el número de artículo | info | local |
| `LC-002` | el número de artículo sigue la forma china | info | local |
| `LC-003` | la cita literal está transcrita | info | local |
| `LC-004` | el estado de vigencia proviene de tu vocabulario (desactivada por defecto) | info | local |
| `LC-005` | la cita indica su ubicación y su finalidad argumental | info | local |
| `LC-006` | el documento declara su título y su tipo | info | local |
| `LC-007` | los números de cita son únicos | info | local |
| `LC-008` | la columna de cita literal no conserva marcadores sin sustituir | info | local |

`LC-004` viene con la lista de valores vacía, así que se declara en `skipped` hasta que la configures: nunca pasa en silencio.

### Ejemplos

Estos son los puntos de entrada reales del complemento; instálalo una vez y llama a uno.

**Salida detallada** — herramienta `lawcite_adapter`, entrada:

```json
{"documentTitle":"某某买卖合同纠纷起诉状","documentType":"民事起诉状","rows":[{"法律法规名称":"","条号":"","引用原文":"当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"}]}
```

Salida:

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

Es la **salida real** del complemento para su propio fixture `LC-001`, no una ilustración. El paquete de reglas nunca fabrica una cita, por lo que cada hallazgo indica tanto el fundamento del que se leyó como el hecho de que el texto de ese fundamento no se obtuvo en esta ronda.

### Qué responde

| Tú preguntas | Qué responde |
|---|---|
| Una fila trae número de artículo pero el nombre de la ley está vacío. ¿Se informa? | Sí. `LC-001` exige el nombre de la ley y el número de artículo (`lawName`, `articleNo`) en cada fila e informa de la fila que deja cualquiera de los dos vacío. Comprueba que estén escritos, no que la ley o el artículo existan: no contiene ninguna base de datos normativa ni la consulta. |
| El número de artículo se escribe con un espacio dentro, o con un número de párrafo añadido. ¿Pasará? | `LC-002` compara `articleNo` con el patrón anclado documentado en «Formato del material», así que tanto la forma con espacio como la forma mixta se informan. Solo comprueba la forma del número, nada sobre si el artículo existe; el párrafo o el inciso van en su propia columna, de modo que la columna del artículo conserva solo la parte del artículo. El `pattern` se ajusta a tu estilo interno. |
| La columna de cita literal de una fila está vacía y otra aún conserva un marcador de plantilla. ¿Se detectan ambas? | Sí, con dos reglas. `LC-003` exige que `quotedText` esté transcrito en cada fila; `LC-008` informa de la fila cuyo `quotedText` aún contiene un término de plantilla (la lista de fábrica cubre corchetes y llaves de plantilla, un marcador de equis y los avisos habituales de «rellenar»; la lista exacta está documentada en el paquete de reglas). Ninguna compara el texto con la ley: `LC-003` comprueba que la cita esté presente y `LC-008` solo que no sobreviva ningún marcador. El marcador de abreviación está deliberadamente ausente, así que un recorte normal de una cita larga pasa. |
| El informe muestra `LC-004` como `skipped` en lugar de aprobada. ¿Por qué? | Porque la lista `values` de `LC-004` viene vacía, es decir, el vocabulario del estado de vigencia no está configurado, así que la regla se declara en `skipped` en vez de pasar en silencio. Rellena `values` con tu propio vocabulario (por ejemplo los términos locales de vigente, modificada, derogada) y entonces `LC-004` comprobará que `effectiveStatus` esté en esa lista. Comprueba la pertenencia a tu lista, no si el estado registrado coincide con los hechos. |
| Las filas nombran la ley y la citan, pero no dicen dónde se usa la cita ni qué sostiene, y la cabecera no da el tipo de documento. ¿Se informa? | Sí. `LC-005` exige `usage` y `purpose` en cada fila de cita e informa de la fila que deja ambas en blanco; no juzga si la cita sostiene realmente ese argumento. `LC-006` exige que la cabecera declare `documentTitle` y `documentType`, y no juzga si el tipo se eligió bien. |
| El mismo artículo se cita en dos secciones y ambas filas llevan el número de cita 3. ¿Es un hallazgo? | Sí. `LC-007` informa del `citationNo` que se repite dentro del inventario, porque un número repetido impide que las notas al pie localicen cada cita. Citar la misma disposición en varias secciones es normal: da a cada cita su propio número. La regla no juzga si citar dos veces la misma disposición es adecuado. |

## Configuración

Todos los parámetros viven en el esquema Schemastery de `src/config.ts`, así que se cambian desde `cordis.yml` sin editar código; los umbrales de cada regla están en el paquete de reglas bajo `rules/`. Las cinco claves siguientes son la lista completa; después vienen los parámetros de regla.

| Clave | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de regla que se dejan de ejecutar; cada uno aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estos ids de regla; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

Parámetros de regla que conviene conocer:

- `LC-002` `pattern` — la forma del número de artículo: por defecto la marca de artículo con un numeral chino o árabe y un sufijo opcional de subartículo. Ajusta el patrón si tu estilo interno escribe los números de otro modo.
- `LC-004` `values` — tu vocabulario de estado de vigencia, p. ej. `[vigente, modificada, derogada, no vigente]`. Vacío significa que no se comprueba, y tampoco hay ningún estado normativo incorporado.
- `LC-008` `terms` — los marcadores que se buscan. El marcador de abreviación está deliberadamente ausente: acortar una cita larga con puntos suspensivos es una forma normal de abreviarla.

Ejemplo de sobrescritura en el patch de tu perfil:

```yaml
- insert:
    - id: dsh-lawcite-adapter
      name: dsh-lawcite-adapter
      config:
        onlyRules: [LC-001, LC-002, LC-008]
        skipNotes: manual interno de la institución, edición 2026
```

## FAQ

<details>
<summary>¿Se modifica o se sube a algún sitio mi material?</summary>

No. La herramienta solo lee el texto JSON/YAML que le entregas y **nunca modifica el original**; el complemento es ESM puro, sin código nativo, **sin red y sin llamadas a modelos** (ver Compatibilidad), así que el material no sale de tu máquina.

</details>

<details>
<summary>Sin vocabulario de estado de vigencia configurado, ¿algo pasa en silencio?</summary>

No. La lista `values` de `LC-004` viene vacía, y una regla cuya lista está sin configurar se declara en `skipped` con el motivo, así que una lista de diferencias vacía nunca se lee como «no falta nada». Una vez configurada, la regla solo comprueba que el valor registrado esté en tu lista, no que coincida con los hechos.

</details>

<details>
<summary>¿Puede verificar que una ley existe o está vigente?</summary>

No. El complemento no contiene ninguna base de datos normativa ni la consulta; comprueba si una cita dejó los elementos necesarios para verificarla: la ley, el artículo, la cita literal, el estado de vigencia y la finalidad. Confirmar que una ley o un artículo existe, está vigente o no ha sido modificado o derogado requiere la base nacional de leyes y reglamentos y los hechos del caso, que es trabajo de un profesional del Derecho. Ver «Normas que sigue».

</details>

<details>
<summary>El complemento se instala pero la herramienta nunca aparece. ¿Qué hago?</summary>

Comprueba que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` incorrecto hace que el cargador omita la entrada en silencio.

</details>

<details>
<summary>¿Puede con un documento largo o con un directorio entero en lote?</summary>

La herramienta funciona en modo `native` y `ptc`; para un lote sobre un directorio usa `ptc`, así el coste del esquema se paga una sola vez. Toda la aritmética es de reloj de pared sobre las cadenas de entrada, sin conversión de zona horaria.

</details>

## Normas que sigue

El paquete de reglas declara un fundamento para cada comprobación. La tabla recoge los documentos y números que las ocho reglas llevan actualmente; todos los fundamentos son configuración de la institución y todas las reglas están en `info`.

| Documento | Número | Reglas que lo citan |
|---|---|---|
| Criterio de revisión de documentos jurídicos de la institución (configuración propia) — antes atribuido a la Ley de Legislación de la RPC; se verificó que su artículo 65 es una cláusula de técnica legislativa | Sin norma uniforme (el fundamento es el criterio propio de gestión de citas de la institución) — se verificó el texto de la segunda modificación de 2023 de la Ley de Legislación y esta regla no la cita | LC-001 |
| Criterio de revisión de documentos jurídicos de la institución (configuración propia) — antes atribuido a GB/T 9704—2012, verificado como norma de maquetación | GB/T 9704—2012 (texto de la cláusula no obtenido en esta ronda) | LC-002, LC-003, LC-005, LC-006, LC-007, LC-008 |
| Medidas de revisión de documentos jurídicos de la institución (configuración propia) | Sin norma uniforme (el fundamento es el criterio propio de estado de vigencia de la institución) | LC-004 |

Títulos originales de los documentos citados:

```text
《中华人民共和国立法法》 2023 年第二次修正
《党政机关公文格式》 GB/T 9704—2012
本机构法律文书审查口径（本机构配置）
本机构法律文书审查办法（本机构配置）
```

**Límite:** este complemento comprueba un **inventario de citas** en cuanto a verificabilidad y elementos del documento: que cada cita nombre su ley y su artículo, que el número de artículo siga la forma china, que la cita literal esté transcrita, que el estado de vigencia provenga de tu vocabulario, que la cita indique dónde se usa y qué sostiene, que el documento declare su título y su tipo, que los números de cita sean únicos y que no sobreviva ningún marcador. **No** verifica que una ley exista, esté vigente, no haya sido modificada o derogada, ni que se aplique al caso.

> ### ⚠️ Este complemento no consulta una base de datos normativa, y ese es el punto
>
> **No puede encontrar el error más grave: la cita de una ley o un artículo que no existe o que ha sido derogado.** Confirmarlo exige la base nacional de leyes y reglamentos y los hechos del caso, que es trabajo de un profesional del Derecho. Lo que este complemento comprueba es si una cita dejó los elementos necesarios para verificarla: la ley, el artículo, el texto citado, el estado de vigencia y la finalidad.
>
> Ese límite está escrito en la cabecera del paquete, en las notas de `LC-001`, `LC-003` y `LC-004`, y en la sección de solución de problemas. Léelo antes de actuar sobre cualquier hallazgo: **un informe limpio de este complemento no afirma que las citas sean correctas.**
>
> `LC-002` comprueba la *forma* del número de artículo —la marca de artículo con un numeral chino o árabe y un sufijo opcional de subartículo— y nada sobre si el artículo existe. `LC-003` comprueba que una cita esté transcrita, no que la transcripción coincida con la ley. El vocabulario de estado de vigencia de `LC-004` viene **vacío** porque tampoco hay incorporado el estado actual de ninguna ley.
>
> **Cada `excerpt` del paquete de reglas dice, con todas las letras, que el texto de la cláusula no se obtuvo.** El régimen está en la Ley de Legislación de la RPC, en GB/T 9704—2012 y en las reglas de revisión de documentos jurídicos de cada institución. La pasada de verificación no pudo recuperar el texto literal, así que el paquete declara la laguna en el propio campo `excerpt` y mantiene cada regla en `warn` o `info`. **Cuando tengas los textos, sustituye cada `excerpt` por la cláusula real y eleva `kind` a `direct`.**
>
> ⚠️ **Un fundamento se corrigió en lugar de completarse.** Se verificó capítulo a capítulo que GB/T 9704—2012 es una norma de **maquetación**: papel, composición, encuadernación, colocación de los elementos del documento y formularios de muestra. **No contiene ninguna disposición sobre gestión de citas.** Seis reglas se habían colgado de ella de todos modos («toda cita debe nombrar el instrumento y el artículo», «la cita literal debe transcribirse», etc.). Esas seis declaran ahora como fundamento **la práctica de revisión de documentos jurídicos de la propia institución**, se califican **`institutional-configuration`** y por tanto quedan en **`info`** en lugar de `warn`. Dejarlas en `warn` mientras su propia nota dice «léase como práctica de la institución» habría sido contradictorio.
>
> **`LC-001` se corrigió después de la misma manera.** Citaba la Ley de Legislación. Esa ley se obtuvo completa y sí contiene una disposición de numeración: el artículo 65 organiza una ley en partes, capítulos, secciones, artículos, párrafos, incisos y apartados según su contenido, con reglas de numeración y una autorización al órgano de trabajo del Comité Permanente de la Asamblea Popular Nacional para redactar normas de técnica legislativa. Pero eso regula **cómo se redacta y numera una ley**; no dice nada sobre cómo un documento oficial cita una ley existente. Así que `LC-001` se une a las otras siete: **las ocho reglas de este paquete declaran ahora como fundamento la práctica de revisión de la propia institución y se califican `institutional-configuration` en `info`.** Ver `rules/evidence/clause-verification-basis-mismatch.md`.

## Formato del material

La herramienta acepta JSON o YAML:

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

Los nombres de columna se comparan sin distinguir mayúsculas y ignorando espacios, guiones bajos y guiones; se conservan los nombres propios del inventario, así que un hallazgo nombra la columna que leyó. Los números de artículo admiten cifras chinas o árabes; una forma árabe con espacios se informa para mantener coherente el estilo interno:

```text
Patrón de LC-002 (por defecto): ^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$

第577条          ✓ pasa LC-002
第12条之一        ✓ pasa LC-002
第 577 条        ✗ se informa: el número de artículo contiene un espacio
第12条第3款       ✗ se informa: pon 第12条 en la columna del artículo y el párrafo aparte
```

Los campos de cabecera (`documentTitle`, `documentType`, `author`, `draftedAt`, etc.) son opcionales en la capa de lectura y los valida el motor de comprobación, así que un material parcialmente exportado produce diferencias de «campo ausente» en lugar de bloquear la herramienta.

## Fuentes de las reglas

Los datos de las reglas están en `rules/lawcite-adapter.yaml`, separados del código. Cada regla lleva un documento, un número, una cláusula descrita en la numeración propia de la fuente, un extracto literal y la URL de la que se leyó. El cargador exige que un extracto sea una cita real de al menos ocho caracteres, y que una comprobación apoyada en un principio general (`derived-from-principle`, máximo `warn`) o en una política local (`institutional-configuration`, máximo `info`) **nunca** pueda declararse `error`. Un paquete que exagera su fundamento falla al cargar en lugar de producir un informe que parezca sólido.

⚠️ Todos los extractos de este paquete declaran que el texto de la cláusula no se obtuvo: la pasada de verificación no pudo recuperarlo, así que las ocho reglas se apoyan en el criterio de revisión de la propia institución, se califican `institutional-configuration` y quedan en `info`. **No es debilitar la exigencia: es negarse a anotar peso sobre un documento que no lo soporta.**

El informe completo de verificación de cláusulas —la enumeración capítulo a capítulo del alcance de GB/T 9704—2012, las fuentes comprobadas y descartadas, y la conclusión de que «el fundamento no coincide con el objeto»— está en `rules/evidence/clause-verification-basis-mismatch.md`.

## Compatibilidad

| Superficie | Estado |
|---|---|
| Harness | Rango de pares `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado que acepta tanto `0.2.0-rc.2` como `0.2.1-rc.2`. `engines.dsh` se declara como `>=0.2.1-0 <0.3.0` y lo aplica el anfitrión desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamadas a modelos) |
| Modo de herramienta | Funciona en `native` y `ptc`; para un lote sobre un directorio usa `ptc` |

## Solución de problemas

- **Aprobó una cita de una ley derogada.** Por diseño: comprueba si la cita es *verificable*, nunca si es *correcta*. Verificarlo exige la base nacional, que el complemento no consulta.
- **`LC-003` aprobó una cita que no coincide con la ley.** Comprueba que la cita esté *presente*. Compararla con la ley es el paso de verificación que omite deliberadamente.
- **`LC-002` salta con una forma que considero aceptable.** Ajusta `pattern` a tu estilo interno. Aquí los párrafos e incisos van en columnas propias, así que un valor mixto debe conservar solo la parte del artículo en su columna.
- **`LC-004` nunca se ejecuta.** Su vocabulario está vacío y no hay incorporado el estado de ninguna ley.
- **`LC-007` salta porque un artículo se cita dos veces.** Citar la misma disposición en varias secciones es normal: da a cada cita su número, o las notas al pie no podrán separarlas.
- **Una regla no se ejecutó.** Revisa el arreglo `skipped`: nombra el id de la regla y el motivo.
- **El lector rechaza el material.** No encontró ninguna de las columnas de cita conocidas (nombre de la ley, número de artículo, cita literal); rellénalas como describe «Formato del material» y vuelve a ejecutar.
- **El complemento se instala pero la herramienta nunca aparece.** Comprueba que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó; un `main` incorrecto hace que el cargador omita la entrada en silencio.
- **`dsh plugin add` rechaza el paquete por incompatibilidad.** El rango de pares cubre `0.1.x` y `0.2.x`; si tu entorno queda fuera, concede una exención explícita: `dsh plugin --profile <name> allow-version dsh-lawcite-adapter@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` informa `manifest-peers` como fallido.** El comprobador estático compara con un rango de pares fijo anterior a la línea 0.2. El entorno aplica la compatibilidad en la instalación, así que el rango declarado es el correcto; es un problema conocido de `dsh-plugin-dev`.
- **Los tiempos parecen desplazados.** Toda la aritmética es de reloj de pared sobre las cadenas de entrada, sin conversión de zona horaria.

## Ecosistema y calidad

- [Espejo en Gitee](https://gitee.com/perrylink/dsh-lawcite-adapter) (espejo sincronizado; GitHub es la referencia)
- [Página del complemento en dshfind](https://dshfind.com/plugins/PerryLink/dsh-lawcite-adapter) (instalaciones y clasificación)
- [Informe de OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-lawcite-adapter) (impulsado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (publicado)
- [Base de conocimiento del ecosistema: elegir un verificador por material](https://perrylink.github.io/zh/checkers/choose/) (índice completo de la familia: 62 verificadores y complementos generales)

## Desarrollo

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, fixtures emparejados por regla (tests/fixtures/<RULE>/)
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run check:readmes   # coherencia de los README en cinco idiomas
node ../scripts/sync-shared.mjs dsh-lawcite-adapter   # refresca src/shared desde ../_shared
```

El complemento es dirigido por datos: `src/model.ts` declara la forma de la tabla, el kit compartido aporta el lector y el motor de comprobación, y el paquete de reglas declara cada comprobación. El paquete de reglas es dato, no código: editar `rules/*.yaml` cambia el conjunto de reglas sin tocar TypeScript; el paquete se valida al cargar, no se da por bueno. Las imágenes del README se generan por programa con [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow): el hero es un conjunto de cuatro webp (zh/en × claro/oscuro) y el diagrama estructural es SVG escrito a mano (claro + oscuro, mapa de columnas campo × regla).

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `cordis`, `lawcite`

## Familia y agradecimientos

Este proyecto forma parte de la familia de complementos de DeepSeek Harness mantenida por [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Si este complemento te resulta útil, **una estrella** no desbloquea nada, pero ayuda a que la siguiente persona lo encuentre.

- [@PerryLink](https://github.com/PerryLink) — creador y mantenedor: la herramienta `lawcite_adapter`, el paquete de reglas con fundamento declarado para cada comprobación y su registro de verificación de cláusulas, y la documentación en cinco idiomas.

<details>
<summary>Expandir todos los complementos</summary>

| Complemento | Estado |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 RETIRADO (repo archivado) |
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
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 CONGELADO — ver el README del repo |
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
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 CONGELADO — ver el README del repo |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 RETIRADO (repo archivado) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 RETIRADO (repo archivado) |

</details>

## Licencia

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-lawcite-adapter contributors

<p align="center"><sub>Apache-2.0 · Complemento comunitario, sin relación con DeepSeek.</sub></p>
