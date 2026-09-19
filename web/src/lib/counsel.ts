import {generateText, stepCountIs} from 'ai'
import {connectContext, endpointNames, fetchInitialContext} from '@/lib/context'
import {buildSystemPrompt} from '@/lib/prompt'
import {insightsFor} from '@/lib/insights'
import {overDailyBudget, recordUsage} from '@/lib/metering'
import {isBillingOrLimitError, markPrimaryDead, pickModel} from '@/lib/model'

// One shot, non streaming version of the agent for surfaces that cannot stream (the Discord slash command).
// Same endpoints, same prompt, same spend guards as the chat route.

export async function runCounsel(question: string, opts: {asOf?: string; threadId?: string} = {}) {
  if (overDailyBudget()) throw new Error('daily budget reached')
  const today = new Date().toISOString().slice(0, 10)
  const asOf = opts.asOf && /^\d{4}-\d{2}-\d{2}$/.test(opts.asOf) ? opts.asOf : today
  const [rulesContext, kbContext] = await Promise.all([
    fetchInitialContext(endpointNames.rules),
    fetchInitialContext(endpointNames.kb),
  ])
  const {tools, close} = await connectContext()
  try {
    const run = (model: ReturnType<typeof pickModel>['model']) => generateText({
      model,
      system: {
        role: 'system',
        content: buildSystemPrompt(rulesContext, kbContext, asOf, today),
        providerOptions: {anthropic: {cacheControl: {type: 'ephemeral', ttl: '1h'}}},
      },
      prompt: question,
      tools,
      stopWhen: stepCountIs(8),
      maxOutputTokens: 3000,
      experimental_telemetry: insightsFor(opts.threadId),
    })
    let picked = pickModel()
    let out
    try {
      out = await run(picked.model)
    } catch (err) {
      if (picked.provider === 'anthropic' && isBillingOrLimitError(err)) {
        markPrimaryDead()
        picked = pickModel()
        if (picked.provider === 'gateway') out = await run(picked.model)
        else throw err
      } else throw err
    }
    const {text, steps, totalUsage} = out
    recordUsage(totalUsage, `discord/${picked.provider}`)
    const toolCalls = steps.flatMap((s) => s.toolCalls.map((c) => c.toolName))
    return {text, toolCalls, asOf}
  } finally {
    await close()
  }
}
