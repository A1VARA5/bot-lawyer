import {createClient} from '@sanity/client'
import Link from 'next/link'

// A public ledger of every place Discord's own pages disagree, straight from the structured rules dataset.
// No model involved. This is what the agent reasons over.
export const revalidate = 300

// The dataset is public, but anonymous reads came back empty on this Growth trial project (see BUILD-LOG),
// so the server reads with a viewer token. Never shipped to the browser: this is a server component.
const client = createClient({
  projectId: 'v6745vem',
  dataset: 'production',
  apiVersion: '2025-08-15',
  useCdn: false,
  token: process.env.SANITY_READ_TOKEN,
})

type Rule = {
  _id: string
  title: string
  plainAnswer: string
  quote: string
  effectiveFrom: string
  effectiveTo?: string
  confidence: string
  contradictionId: string
  resolution?: string
  area?: {title: string}
  source?: {title: string; kind: string; url: string; authority: number; lastEditedAt?: string; publishedAt?: string}
}

const QUERY = `*[_type == "rule" && defined(contradictionId)] | order(contradictionId asc, effectiveFrom desc) {
  _id, title, plainAnswer, quote, effectiveFrom, effectiveTo, confidence, contradictionId, resolution,
  "area": area->{title},
  "source": source->{title, kind, url, authority, lastEditedAt, publishedAt}
}`

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

const HEADLINE: Record<string, string> = {
  C1: 'Is the privileged intent threshold 100 servers or 10,000 users?',
  C2: 'Does Message Content need approval after verification, or just a toggle under 10,000 users?',
  C3: 'When exactly did the June 2026 change take effect?',
  C4: 'Do unverified apps still stop at 100 servers?',
  C5: 'Is retry_after in seconds or milliseconds?',
  C6: 'Do interaction responses count against the global rate limit?',
  C7: 'Can a verified app change owners?',
  C8: 'Which messages does a bot see without the Message Content intent?',
  C9: 'Is the $100 payout threshold gross or net of fees?',
  C10: 'Can you monetise if your app never needed Message Content approval?',
}

export default async function Contradictions() {
  const rules = await client.fetch<Rule[]>(QUERY)
  const groups = new Map<string, Rule[]>()
  for (const r of rules) groups.set(r.contradictionId, [...(groups.get(r.contradictionId) ?? []), r])
  const ids = [...groups.keys()].sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)))

  return (
    <div className="h-screen overflow-y-auto">
      <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6">
        <div className="mb-6 flex items-center gap-3">
          <Link href="/" className="rounded bg-sidebar px-2 py-1 text-xs text-text-2 hover:bg-hover">
            ← back to #ask-counsel
          </Link>
        </div>
        <h1 className="text-3xl font-bold text-white">The contradiction ledger</h1>
        <p className="mt-2 max-w-2xl text-[15px] text-text-2">
          Every place Discord&apos;s own pages disagree with each other, as of the 2026-09-19 snapshot. Each side is a rule
          document in Sanity with its verbatim quote, source, authority score and effective dates. The resolution is ours, and
          it is what the agent applies. Most of these exist because Discord changed the privileged intent rules on
          2026-06-10 and updated about half of its pages.
        </p>
        <p className="mt-2 text-xs text-muted">
          {ids.length} contradictions · {rules.length} rules · project v6745vem · dataset production
        </p>

        <div className="mt-8 space-y-8">
          {ids.map((id) => {
            const group = groups.get(id)!
            const resolution = group.find((r) => r.resolution)?.resolution
            return (
              <section key={id} id={id} className="rounded-lg border border-line bg-sidebar p-5">
                <div className="flex flex-wrap items-baseline gap-2">
                  <span className="rounded bg-yellow/20 px-2 py-0.5 font-mono text-xs text-yellow">{id}</span>
                  <h2 className="text-lg font-semibold text-white">{HEADLINE[id] ?? group[0].area?.title}</h2>
                </div>
                <div className="mt-4 grid gap-3 md:grid-cols-2">
                  {group.map((r) => {
                    const superseded = !!r.effectiveTo
                    return (
                      <div key={r._id} className={`rounded border p-3 ${superseded ? 'border-line/60 bg-rail/40' : 'border-line bg-rail/70'}`}>
                        <div className={`text-[14px] ${superseded ? 'text-muted line-through' : 'text-text'}`}>{r.title}</div>
                        <blockquote className="mt-2 border-l-4 border-line pl-3 text-[13px] italic text-text-2">{r.quote}</blockquote>
                        <div className="mt-2 flex flex-wrap items-center gap-2 text-[11px] text-muted">
                          <span className="font-mono">
                            {r.effectiveFrom} → {r.effectiveTo ?? 'now'}
                          </span>
                          {superseded && <span className="rounded bg-red/20 px-1 text-red">superseded</span>}
                          {r.confidence === 'inferred' && <span className="rounded bg-line px-1">inferred</span>}
                          {r.source && (
                            <>
                              <span>{KIND[r.source.kind] ?? r.source.kind}</span>
                              <span className="flex items-center gap-1" title="source authority">
                                <span className="h-1 w-12 overflow-hidden rounded bg-line">
                                  <span className="block h-full bg-blurple" style={{width: `${r.source.authority}%`}} />
                                </span>
                                <span className="font-mono">{r.source.authority}</span>
                              </span>
                              <a href={r.source.url} target="_blank" rel="noreferrer" className="ml-auto text-link hover:underline">
                                {r.source.title}
                              </a>
                            </>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
                {resolution && (
                  <div className="mt-3 rounded border-l-4 border-green bg-rail/60 px-3 py-2 text-[13px] text-text">
                    <span className="mr-2 font-semibold text-green">Resolution</span>
                    {resolution}
                  </div>
                )}
              </section>
            )
          })}
        </div>

        <p className="mt-10 text-xs text-muted">
          Source of truth: the <code className="font-mono">rule</code> documents with a <code className="font-mono">contradictionId</code> in
          Sanity project v6745vem. The same documents are served to the agent through a Sanity Context MCP endpoint in GROQ mode,
          alongside a Knowledge Base built from the snapshotted pages.
        </p>
      </div>
    </div>
  )
}
