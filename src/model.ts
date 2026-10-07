/**
 * dsh-lawcite-adapter — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'lawcite_adapter'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  citationNo: ['序号', '引用编号', '编号', 'citationNo'],
  lawName: ['法律法规名称', '法律名称', '文件名称', 'lawName'],
  articleNo: ['条号', '条款号', '第几条', 'articleNo'],
  paragraphNo: ['款号', '款项', '第几款', 'paragraphNo'],
  itemNo: ['项号', '第几项', '项', 'itemNo'],
  quotedText: ['引用原文', '引文', '法条原文', 'quotedText'],
  usage: ['引用位置', '所在章节', '用途', 'usage'],
  purpose: ['论证作用', '引用目的', '说明', 'purpose'],
  effectiveStatus: ['效力状态', '是否现行', '效力', 'effectiveStatus'],
  versionNote: ['版本说明', '修订情况', '版本', 'versionNote'],
  citationStyle: ['引用格式', '著录格式', '格式', 'citationStyle'],
  note: ['备注', '说明', 'note', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'citations', '引用'],
  columns: COLUMNS,
  header: {
  documentTitle: ['documentTitle', '文书标题', '文稿名称'],
  documentType: ['documentType', '文书类型', '文种'],
  author: ['author', '撰写人', '作者'],
  draftedAt: ['draftedAt', '成文日期', '撰写日期'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '法律法规名称',
  'lawName',
  '条号',
  'articleNo',
  '引用原文',
  'quotedText',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
