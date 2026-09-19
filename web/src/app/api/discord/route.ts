import nacl from 'tweetnacl'
import {after} from 'next/server'
import {runCounsel} from '@/lib/counsel'
import {fixDraftLength} from '@/lib/draft'

// Bot Lawyer as an actual Discord app, via the HTTP interactions endpoint. No gateway, no intents, no message
// content, so it complies with its own rulings. Discord POSTs here; we must answer within 3 seconds, so we
// acknowledge with a deferred response and PATCH the real answer in afterwards.
export const maxDuration = 60

const PUBLIC_KEY = process.env.DISCORD_PUBLIC_KEY ?? ''
const APP_ID = process.env.DISCORD_APPLICATION_ID ?? ''

const hex = (s: string) => Uint8Array.from(Buffer.from(s, 'hex'))

function verify(req: Request, body: string) {
  const sig = req.headers.get('x-signature-ed25519')
  const ts = req.headers.get('x-signature-timestamp')
  if (!sig || !ts || !PUBLIC_KEY) return false
  try {
    return nacl.sign.detached.verify(Buffer.from(ts + body), hex(sig), hex(PUBLIC_KEY))
  } catch {
    return false
  }
}

const tidy = (s: string) => fixDraftLength(s).replace(/\s*—\s*/g, ', ').replace(/\s*–\s*/g, ', ')

function verdictColor(text: string) {
  const head = (text.match(/\*\*Ruling:\*\*\s*([^.\n]*)/i)?.[1] ?? '').toLowerCase()
  if (/^(yes|seconds|fixable|allowed|you can)/.test(head)) return 0x57f287
  if (/^(no|not |never|banned)/.test(head)) return 0xed4245
  if (/^(depends|unclear|unresolved|it depends|partly|officially)/.test(head)) return 0xfee75c
  return 0x5865f2
}

async function patchOriginal(token: string, payload: unknown) {
  const res = await fetch(`https://discord.com/api/v10/webhooks/${APP_ID}/${token}/messages/@original`, {
    method: 'PATCH',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  })
  if (!res.ok) console.error('discord patch failed', res.status, await res.text())
}

export async function POST(req: Request) {
  const body = await req.text()
  if (!verify(req, body)) return new Response('bad signature', {status: 401})

  const interaction = JSON.parse(body) as {
    type: number
    token: string
    data?: {name: string; options?: {name: string; value: string}[]}
    member?: {user?: {id: string}}
    user?: {id: string}
  }

  // Discord's liveness check when you save the endpoint URL
  if (interaction.type === 1) return Response.json({type: 1})

  if (interaction.type === 2 && interaction.data?.name === 'ask') {
    const question = interaction.data.options?.find((o) => o.name === 'question')?.value?.trim() ?? ''
    const asOf = interaction.data.options?.find((o) => o.name === 'as_of')?.value?.trim()
    const token = interaction.token
    const userId = interaction.member?.user?.id ?? interaction.user?.id ?? 'unknown'

    if (!question) return Response.json({type: 4, data: {content: 'Counsel needs a question.', flags: 64}})

    after(async () => {
      try {
        const {text, toolCalls, asOf: used} = await runCounsel(question, {asOf, threadId: `discord-${userId}-${Date.now().toString(36)}`})
        const clean = tidy(text)
        const isDraft = /```/.test(clean) && !/\*\*Ruling:\*\*/i.test(clean)
        if (isDraft) {
          // A draft is for copying: post it as a normal message so Discord shows the copy button on the code block.
          const content = `> ${question.slice(0, 150)}
${clean}`.slice(0, 1990)
          await patchOriginal(token, {content, allowed_mentions: {parse: []}})
          return
        }
        const description = clean.slice(0, 4000)
        await patchOriginal(token, {
          content: `> ${question.slice(0, 200)}`,
          embeds: [
            {
              title: 'Memorandum from counsel',
              description,
              color: verdictColor(text),
              footer: {
                text: `Bot Lawyer · rule as of ${used} · ${toolCalls.length} lookup${toolCalls.length === 1 ? '' : 's'} in Sanity Context · counsel does not read replies (no Message Content intent, as advised), use /ask again`,
              },
            },
          ],
        })
      } catch (err) {
        console.error('counsel failed', err)
        const msg = err instanceof Error ? err.message : ''
        const content = /budget/.test(msg)
          ? 'Counsel has hit today’s retainer cap. Back tomorrow.'
          : /credit|billing/i.test(msg)
            ? 'Counsel is out of retainer (the model provider says the credit balance is too low). The Sanity side is fine.'
            : 'Counsel is unavailable. Something broke on our side, not Discord’s. Try again in a minute.'
        await patchOriginal(token, {content})
      }
    })

    // type 5 = deferred channel message, shows "Bot Lawyer is thinking..." until we PATCH
    return Response.json({type: 5})
  }

  return Response.json({type: 4, data: {content: 'Counsel does not recognise that command.', flags: 64}})
}
