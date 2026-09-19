import {anthropic} from '@ai-sdk/anthropic'
import {gateway} from 'ai'

// Model selection with a fallback. Primary is the Anthropic key. If it fails on billing or rate limits,
// the next request goes through Vercel AI Gateway (its own credits, OIDC on Vercel, or AI_GATEWAY_API_KEY),
// so a drained key cannot take the public demo down again. Recovers to primary every 15 minutes.
const PRIMARY_MODEL = process.env.BOT_LAWYER_MODEL ?? 'claude-sonnet-5'
const GATEWAY_MODEL = process.env.BOT_LAWYER_GATEWAY_MODEL ?? 'anthropic/claude-sonnet-4.5'
const GATEWAY_ENABLED = process.env.BOT_LAWYER_GATEWAY !== 'off'

let primaryDeadUntil = 0

export function isBillingOrLimitError(err: unknown) {
  const msg = err instanceof Error ? err.message : String(err)
  return /credit|billing|quota|insufficient|rate limit|429|overloaded|529/i.test(msg)
}

export function markPrimaryDead() {
  primaryDeadUntil = Date.now() + 15 * 60 * 1000
}

export function pickModel(): {model: ReturnType<typeof anthropic>; provider: 'anthropic' | 'gateway'} {
  const usePrimary = Date.now() > primaryDeadUntil || !GATEWAY_ENABLED
  if (usePrimary) return {model: anthropic(PRIMARY_MODEL), provider: 'anthropic'}
  return {model: gateway(GATEWAY_MODEL) as unknown as ReturnType<typeof anthropic>, provider: 'gateway'}
}
