'use client'

// Renders the rule documents a groq_query actually returned, so the structure behind a ruling is visible:
// effective range, source authority, conflicts, superseded state. No model involved, this is the data.

type Rule = {
  _id?: string
  title?: string
  effectiveFrom?: string
  effectiveTo?: string | null
  confidence?: string
  contradictionId?: string | null
  conflicts?: {_id?: string; title?: string}[] | null
  conflictsWith?: unknown[] | null
  source?: {title?: string; kind?: string; url?: string; authority?: number} | null
  appliesWhen?: Record<string, unknown> | null
}

export function extractRules(output: unknown): Rule[] {
  try {
    let payload: unknown = output
    if (payload && typeof payload === 'object' && 'content' in payload) {
      const content = (payload as {content: {type: string; text?: string}[]}).content
      const text = content?.find((c) => c.type === 'text')?.text
      payload = text ? JSON.parse(text) : null
    } else if (typeof payload === 'string') {
      payload = JSON.parse(payload)
    }
    const result = (payload as {result?: unknown})?.result ?? payload
    if (!Array.isArray(result)) return []
    return result.filter((r) => r && typeof r === 'object' && ('title' in r || 'effectiveFrom' in r)) as Rule[]
  } catch {
    return []
  }
}

const KIND: Record<string, string> = {
  developerDocs: 'developer docs',
  developerPolicy: 'Developer Policy',
  developerTerms: 'Developer Terms',
  terms: 'Terms of Service',
  privacy: 'Privacy Policy',
  guidelines: 'Community Guidelines',
  monetizationTerms: 'Monetization Terms',
  developerSupport: 'developer support',
  userSupport: 'user support',
  changelog: 'change log',
  announcement: 'announcement',
  github: 'GitHub',
}

function applies(w: Record<string, unknown> | null | undefined) {
  if (!w) return []
  const out: string[] = []
  if (w.minUsers != null) out.push(`≥ ${Number(w.minUsers).toLocaleString()} users`)
  if (w.maxUsers != null) out.push(`≤ ${Number(w.maxUsers).toLocaleString()} users`)
  if (w.minServers != null) out.push(`≥ ${w.minServers} servers`)
  if (w.maxServers != null) out.push(`≤ ${w.maxServers} servers`)
  if (Array.isArray(w.intents) && w.intents.length) out.push((w.intents as string[]).join(', '))
  if (w.verificationState && w.verificationState !== 'any') out.push(String(w.verificationState))
  if (w.ownerAge && w.ownerAge !== 'any') out.push(String(w.ownerAge).replace('plus', '+'))
  if (w.region) out.push(String(w.region))
  return out
}

export function RulesOnFile({rules, asOf}: {rules: Rule[]; asOf: string}) {
  if (rules.length === 0) return null
  const shown = rules.slice(0, 8)
  return (
    <div className="mt-2 max-w-2xl">
      <div className="mb-1 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wide text-muted">
        Rules on file <span className="rounded bg-rail px-1.5 py-px font-mono text-[10px] normal-case">{rules.length} returned</span>
        <span className="font-normal normal-case">from the Sanity rules dataset, as of {asOf}</span>
      </div>
      <div className="grid gap-1.5 sm:grid-cols-2">
        {shown.map((r, i) => {
          const superseded = !!r.effectiveTo && r.effectiveTo < asOf
          const notYet = !!r.effectiveFrom && r.effectiveFrom > asOf
          const conflicts = (r.conflicts?.length ?? 0) > 0 || (r.conflictsWith?.length ?? 0) > 0 || !!r.contradictionId
          const auth = r.source?.authority ?? null
          const cond = applies(r.appliesWhen)
          return (
            <div
              key={r._id ?? i}
              className={`rounded border px-3 py-2 text-xs ${superseded || notYet ? 'border-line/60 bg-rail/40 text-muted' : 'border-line bg-rail/70 text-text-2'}`}
            >
              <div className={`text-[13px] leading-snug ${superseded ? 'line-through' : 'text-text'}`}>{r.title ?? r._id}</div>
              <div className="mt-1 flex flex-wrap items-center gap-1.5">
                <span className="font-mono">
                  {r.effectiveFrom ?? '?'} → {r.effectiveTo ?? 'now'}
                </span>
                {superseded && <span className="rounded bg-red/20 px-1 text-red">superseded</span>}
                {notYet && <span className="rounded bg-yellow/20 px-1 text-yellow">not yet in force</span>}
                {conflicts && (
                  <span className="rounded bg-yellow/20 px-1 text-yellow">conflict{r.contradictionId ? ` ${r.contradictionId}` : ''}</span>
                )}
                {r.confidence === 'inferred' && <span className="rounded bg-line px-1">inferred</span>}
              </div>
              {cond.length > 0 && <div className="mt-1 text-[11px]">applies when: {cond.join(' · ')}</div>}
              {r.source && (
                <div className="mt-1 flex items-center gap-2 text-[11px]">
                  <span className="truncate">{KIND[r.source.kind ?? ''] ?? r.source.kind}</span>
                  {auth != null && (
                    <span className="flex items-center gap-1" title={`source authority ${auth}/100`}>
                      <span className="h-1 w-14 overflow-hidden rounded bg-line">
                        <span className="block h-full bg-blurple" style={{width: `${auth}%`}} />
                      </span>
                      <span className="font-mono">{auth}</span>
                    </span>
                  )}
                  {r.source.url && (
                    <a href={r.source.url} target="_blank" rel="noreferrer" className="ml-auto text-link hover:underline">
                      source
                    </a>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
      {rules.length > shown.length && <div className="mt-1 text-[11px] text-muted">and {rules.length - shown.length} more</div>}
    </div>
  )
}


// The knowledge base entries the agent read for this answer, with the source pages the entry cites.
// Parsed from the knowledge_base_read tool input (paths) and output (entry markdown). No model involved.
export function extractPages(input: unknown, output: unknown): {path: string; sources: string[]}[] {
  const paths: string[] = Array.isArray((input as {paths?: string[]})?.paths) ? (input as {paths: string[]}).paths : []
  let text = ''
  try {
    if (output && typeof output === 'object' && 'content' in output) {
      const c = (output as {content: {type: string; text?: string}[]}).content
      text = c?.filter((x) => x.type === 'text').map((x) => x.text ?? '').join(' ') ?? ''
    } else if (typeof output === 'string') text = output
  } catch {}
  const urls = Array.from(new Set((text.match(/https?:\/\/[^\s)\]>"']+/g) ?? []).map((u) => u.replace(/[.,;:]+$/, ''))))
  return paths.map((path) => ({path, sources: urls}))
}

export function PagesRead({pages}: {pages: {path: string; sources: string[]}[]}) {
  if (pages.length === 0) return null
  const allSources = Array.from(new Set(pages.flatMap((p) => p.sources))).slice(0, 8)
  return (
    <div className="mt-2 max-w-2xl">
      <div className="mb-1 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wide text-muted">
        Pages read <span className="rounded bg-rail px-1.5 py-px font-mono text-[10px] normal-case">{pages.length} knowledge base entr{pages.length === 1 ? 'y' : 'ies'}</span>
        <span className="font-normal normal-case">from the Sanity Context knowledge base</span>
      </div>
      <div className="rounded border border-line bg-rail/70 px-3 py-2 text-xs text-text-2">
        <div className="flex flex-wrap gap-1.5">
          {pages.map((p) => (
            <span key={p.path} className="rounded bg-line px-1.5 py-px font-mono text-[11px] text-text">
              {p.path}
            </span>
          ))}
        </div>
        {allSources.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-[11px]">
            {allSources.map((u) => (
              <a key={u} href={u} target="_blank" rel="noreferrer" className="text-link hover:underline">
                {u.replace(/^https?:\/\//, '').replace(/\/hc\/en-us\/articles\/\d+-?/, '/').slice(0, 60)}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
