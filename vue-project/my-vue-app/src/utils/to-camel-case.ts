/**
 * キャメルケースに変換するための型定義
 * @template T オブジェクトの型
 * @typedef {object} CamelCase
 * - もしTがオブジェクト（Record<string, unknown>）ならば、その全てのキーをキャメルケースに変換する
 * - もしTが配列ならば、その要素を再帰的にキャメルケースに変換する
 * - それ以外の場合、Tをそのまま返す
 */
type CamelCase<T> = T extends Record<string, unknown>
  ? { [K in keyof T]: CamelCase<T[K]> }
  : T extends (infer U)[]
  ? U extends Record<string, unknown>
    ? CamelCase<U>[]
    : T
  : T

/**
 * スネークケースやケバブケースの文字列をキャメルケースに変換する関数
 * @function toCamelCase
 * @template T オブジェクトの型
 * @param {T} obj スネークケースやケバブケースのキーを持つオブジェクト
 * @returns {CamelCase<T>} キャメルケースのキーを持つオブジェクト
 * @description
 * - もし入力が配列ならば、その要素を再帰的にキャメルケースに変換する
 * - もし入力がオブジェクトならば、そのキーをキャメルケースに変換する
 * - それ以外の場合、入力をそのまま返す
 */
const toCamelCase = <T extends Record<string, unknown>>(
  obj: T
): CamelCase<T> => {
  if (Array.isArray(obj)) {
    return obj.map(toCamelCase) as unknown as CamelCase<T>
  }
  if (obj !== null && typeof obj === 'object') {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [
        key.replace(/([-_][a-z])/g, (group) =>
          group.toUpperCase().replace('-', '').replace('_', '')
        ),
        toCamelCase(value as Record<string, unknown>)
      ])
    ) as unknown as CamelCase<T>
  }
  return obj as CamelCase<T>
}

export default toCamelCase
