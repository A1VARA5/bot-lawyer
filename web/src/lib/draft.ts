// Drafts end with a "Length: N characters" line the model tends to miscount. Recompute it from the code block.
export function fixDraftLength(text: string) {
  const m = text.match(/```(?:md|markdown)?\r?\n([\s\S]*?)```/)
  if (!m) return text
  const n = m[1].replace(/\r?\n$/, '').length
  if (/Length:\s*\d+/i.test(text)) return text.replace(/Length:\s*\d+\s*characters?/i, `Length: ${n} characters`)
  return `${text.trimEnd()}\n\nLength: ${n} characters`
}
