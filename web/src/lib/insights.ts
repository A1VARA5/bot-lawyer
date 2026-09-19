import {createClient} from '@sanity/client'
import {sanityInsightsIntegration} from '@sanity/context/ai-sdk'

// Every conversation is saved to Sanity Context Insights (org level), so the Context dashboard can score it,
// tag sentiment and surface content gaps. Best effort: if the token lacks the grant, the chat still works.
const ORG = process.env.SANITY_ORGANIZATION_ID
const TOKEN = process.env.SANITY_INSIGHTS_TOKEN ?? process.env.SANITY_ORGANIZATION_TOKEN

const client =
  ORG && TOKEN
    ? createClient({
        apiVersion: 'v2025-11-27',
        token: TOKEN,
        context: {organizationId: ORG},
        useCdn: false,
        useProjectHostname: false,
      })
    : null

export function insightsFor(threadId?: string) {
  if (!client || process.env.BOT_LAWYER_INSIGHTS === 'off') return undefined
  const id = threadId && /^[a-zA-Z0-9_-]{8,64}$/.test(threadId) ? threadId : `anon-${Date.now()}`
  return {
    isEnabled: true,
    integrations: [
      sanityInsightsIntegration({
        client,
        threadId: id,
        metadata: {mcpEndpoints: 'bot-lawyer-rules,bot-lawyer-kb', app: 'bot-lawyer'},
      }),
    ],
  }
}
