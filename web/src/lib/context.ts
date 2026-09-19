import {createMCPClient} from '@ai-sdk/mcp'

// Two Sanity Context endpoints, one per mode. A single endpoint cannot serve both:
// when an endpoint has a dataset source, its knowledge base sources are ignored.
//   rules  -> GROQ mode over the curated rules dataset (structured lookups)
//   kb     -> Knowledge Base mode over the snapshotted Discord pages (prose, quotes, context)
const ORG = process.env.SANITY_ORGANIZATION_ID
const TOKEN = process.env.SANITY_ORGANIZATION_TOKEN
const RULES_ENDPOINT = process.env.SANITY_CONTEXT_RULES_ENDPOINT ?? 'bot-lawyer-rules'
const KB_ENDPOINT = process.env.SANITY_CONTEXT_KB_ENDPOINT ?? 'bot-lawyer-kb'

function endpointUrl(name: string) {
  if (!ORG || !TOKEN) throw new Error('SANITY_ORGANIZATION_ID and SANITY_ORGANIZATION_TOKEN are required')
  return `https://api.sanity.io/v1/context/organizations/${ORG}/mcp/${name}`
}

const headers = () => ({Authorization: `Bearer ${TOKEN}`})

// The /initial-context payload rarely changes, so cache it per server instance.
const initialContextCache = new Map<string, {text: string; at: number}>()
const CACHE_MS = 10 * 60 * 1000

export async function fetchInitialContext(name: string): Promise<string> {
  const hit = initialContextCache.get(name)
  if (hit && Date.now() - hit.at < CACHE_MS) return hit.text
  const url = new URL(endpointUrl(name))
  url.pathname = `${url.pathname.replace(/\/$/, '')}/initial-context`
  const res = await fetch(url, {headers: headers()})
  if (!res.ok) throw new Error(`initial-context ${name}: ${res.status} ${await res.text()}`)
  const text = await res.text()
  initialContextCache.set(name, {text, at: Date.now()})
  return text
}

export async function connectContext() {
  const [rules, kb] = await Promise.all([
    createMCPClient({transport: {type: 'http', url: endpointUrl(RULES_ENDPOINT), headers: headers()}}),
    createMCPClient({transport: {type: 'http', url: endpointUrl(KB_ENDPOINT), headers: headers()}}),
  ])

  // Both endpoints expose initial_context. Drop both and inline the payloads into the system prompt instead.
  const {initial_context: _a, ...rulesTools} = await rules.tools()
  const {initial_context: _b, ...kbTools} = await kb.tools()

  // Re-describe the generic tools so the model routes by intent, not by tool name.
  const tools = {
    ...rulesTools,
    ...(rulesTools.groq_query && {
      groq_query: {
        ...rulesTools.groq_query,
        description:
          'Query the curated RULES dataset with GROQ. Use this first for anything that depends on numbers or state: ' +
          'server count, unique user count, intents in use, verification state, owner age, region, or a date. ' +
          'Documents: rule (title, plainAnswer, quote, appliesWhen{minUsers,maxUsers,minServers,maxServers,intents,verificationState,region,ownerAge}, ' +
          'effectiveFrom, effectiveTo, confidence, contradictionId, resolution, supersedes->, conflictsWith[]->, source->{title,kind,authority,url,publishedAt,lastEditedAt}, area->{title,slug}), ' +
          'source, policyArea. Filter rules by area with area._ref. The eleven area ids are exactly: area.intents, area.verification, area.dataRetention, area.rateLimits, area.monetisation, area.appDirectory, area.tokensAndSecurity, area.oauth, area.ownership, area.ageRequirements, area.formatting (markdown syntax, message and embed limits, channel names and counts, mention and timestamp formats; query it whenever the developer asks to write, format, fix or name something for Discord). ' +
          'Good first query: *[_type == "rule" && area._ref == "area.intents"]{_id, title, plainAnswer, quote, appliesWhen, effectiveFrom, effectiveTo, confidence, contradictionId, resolution, "conflicts": conflictsWith[]->{_id, title}, "source": source->{title, kind, url, authority}} | order(effectiveFrom desc). ' +
          'Narrow with title match or quote match (wildcards like *retry*), or by contradictionId. Always project source->url, effectiveFrom and confidence (say inferred when it is). Rules with effectiveTo set are superseded; include them only to explain what changed.',
      },
    }),
    ...kbTools,
    ...(kbTools.knowledge_base_read && {
      knowledge_base_read: {
        ...kbTools.knowledge_base_read,
        description:
          'SECOND step only, after groq_query has been called. Read entries from the KNOWLEDGE BASE built from Discord\'s own pages (developer docs, Developer Policy and Terms, ' +
          'legal terms, support articles, GitHub issues). Use it when the developer asks what a page actually says, needs the ' +
          'surrounding context of a rule, or when the rules dataset returns nothing. Pass entry paths from the outline verbatim; ' +
          'read several entries in one call.',
      },
    }),
  }

  const close = async () => {
    await Promise.all([rules.close(), kb.close()])
  }
  return {tools, close}
}

export const endpointNames = {rules: RULES_ENDPOINT, kb: KB_ENDPOINT}
