import {convertToModelMessages, streamText, type UIMessage} from 'ai'
import {connectContext, endpointNames, fetchInitialContext} from '@/lib/context'
import {buildSystemPrompt} from '@/lib/prompt'
import {checkRateLimit} from '@/lib/ratelimit'
import {insightsFor} from '@/lib/insights'
import {overDailyBudget, recordUsage} from '@/lib/metering'
import {isBillingOrLimitError, markPrimaryDead, pickModel} from '@/lib/model'

export const maxDuration = 60

// Spend guard: the demo runs on a small test key. Sonnet by default because Haiku ignored the tool order.
const MAX_STEPS = 8
const MAX_OUTPUT_TOKENS = 3000
const MAX_MESSAGES = 12

const isoDate = (s: unknown) => (typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s) ? s : null)

export async function POST(req: Request) {
  const limited = checkRateLimit(req)
  if (limited) return limited
  if (overDailyBudget()) {
    return new Response(JSON.stringify({error: 'Counsel has hit the daily retainer cap. Back tomorrow.'}), {
      status: 503,
      headers: {'Content-Type': 'application/json'},
    })
  }

  const body = (await req.json()) as {messages: UIMessage[]; asOf?: string; threadId?: string; brief?: boolean}
  const messages = body.messages
  if (!Array.isArray(messages) || messages.length === 0) {
    return new Response('messages required', {status: 400})
  }
  const trimmed = messages.slice(-MAX_MESSAGES)

  // "Rule as of" lets the developer ask what applied on a past date. Rules carry effectiveFrom and effectiveTo,
  // so the same question can get a different ruling on a different date. That is the structure doing the work.
  const today = new Date().toISOString().slice(0, 10)
  const asOf = isoDate(body.asOf) ?? today

  const [rulesContext, kbContext] = await Promise.all([
    fetchInitialContext(endpointNames.rules),
    fetchInitialContext(endpointNames.kb),
  ])
  const {tools, close} = await connectContext()
  const {model, provider} = pickModel()

  const result = streamText({
    model,
    // The system prompt (two initial contexts plus instructions) is identical on every call, so cache it.
    // Cached reads are about a tenth of the price. This is what drained the first test key.
    system: {
      role: 'system',
      content: buildSystemPrompt(rulesContext, kbContext, asOf, today, body.brief === true),
      providerOptions: {anthropic: {cacheControl: {type: 'ephemeral', ttl: '1h'}}},
    },
    messages: await convertToModelMessages(trimmed),
    tools,
    stopWhen: ({steps}) => steps.length >= MAX_STEPS,
    maxOutputTokens: MAX_OUTPUT_TOKENS,
    experimental_telemetry: insightsFor(body.threadId),
    onFinish: ({totalUsage}) => {
      recordUsage(totalUsage, `chat/${provider}`)
      return close()
    },
    onError: ({error}) => {
      if (provider === 'anthropic' && isBillingOrLimitError(error)) markPrimaryDead()
      return close()
    },
  })

  return result.toUIMessageStreamResponse({
    onError: (err) => {
      const msg = err instanceof Error ? err.message : String(err)
      if (/credit|billing|quota|insufficient/i.test(msg)) return 'Counsel is out of retainer (the model provider says the credit balance is too low). The Sanity side is fine, the lawyer just needs paying.'
      if (/rate limit|429|overloaded/i.test(msg)) return 'The model provider is rate limiting us. Try again in a minute.'
      return 'Counsel hit an error talking to the model provider. Try again in a minute.'
    },
  })
}
