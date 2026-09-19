import type {LanguageModelUsage} from 'ai'

// Spend metering. Per serverless instance (Vercel), so it is a floor on protection, not a guarantee,
// but it makes cost visible in the logs and stops a runaway before it drains a key.
// Prices are per million tokens; override with env if the model changes.
const PRICE_IN = Number(process.env.BOT_LAWYER_PRICE_IN ?? 3)
const PRICE_OUT = Number(process.env.BOT_LAWYER_PRICE_OUT ?? 15)
const PRICE_CACHE_READ = Number(process.env.BOT_LAWYER_PRICE_CACHE_READ ?? 0.3)
const DAILY_USD = Number(process.env.BOT_LAWYER_DAILY_USD ?? 3)

let day = ''
let spentUsd = 0
let calls = 0

function rollover() {
  const today = new Date().toISOString().slice(0, 10)
  if (today !== day) {
    day = today
    spentUsd = 0
    calls = 0
  }
}

export function estimateUsd(u: LanguageModelUsage) {
  const cached = u.cachedInputTokens ?? 0
  const fresh = Math.max(0, (u.inputTokens ?? 0) - cached)
  return (fresh * PRICE_IN + cached * PRICE_CACHE_READ + (u.outputTokens ?? 0) * PRICE_OUT) / 1_000_000
}

export function recordUsage(u: LanguageModelUsage, where: string) {
  rollover()
  const usd = estimateUsd(u)
  spentUsd += usd
  calls += 1
  console.log(
    `[bot-lawyer usage] ${where} in=${u.inputTokens ?? 0} cached=${u.cachedInputTokens ?? 0} out=${u.outputTokens ?? 0} ` +
      `est=$${usd.toFixed(4)} today=$${spentUsd.toFixed(3)} calls=${calls}`,
  )
  return usd
}

export function overDailyBudget() {
  rollover()
  return spentUsd >= DAILY_USD
}

export function budgetSummary() {
  rollover()
  return {day, spentUsd: Number(spentUsd.toFixed(3)), calls, capUsd: DAILY_USD}
}
