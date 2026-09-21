'use client'

import {useChat} from '@ai-sdk/react'
import {DefaultChatTransport} from 'ai'
import {useEffect, useRef, useState} from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {PagesRead, RulesOnFile, extractPages, extractRules} from './rules-on-file'
import {fixDraftLength} from '@/lib/draft'

// Belt and braces: the prompt forbids dashes and asks for a blank line before Source; the model sometimes forgets.
const tidy = (s: string) =>
  fixDraftLength(s)
    .replace(/\s*—\s*/g, ', ')
    .replace(/\s*–\s*/g, ', ')
    .replace(/([^\n])[ \t]*\n?[ \t]*(Source:\s*\[)/g, '$1\n\n$2')

const EXAMPLES = [
  'My bot is in 90 servers with about 4,000 unique users and reads message content. Do I need the Message Content intent approved?',
  'Is retry_after in seconds or milliseconds? I keep getting 429s.',
  'Does an unverified bot still stop at 100 servers?',
  'Can I transfer my verified app to my cofounder?',
  'What does the Developer Policy actually say about how long we can keep message content, and how did the 2020 version word it?',
  'Walk me through the payout timing on the Premium Apps page: when it runs, the minimum, the dispute window.',
  'We are a team in Germany, unverified, 800 users. Can we sell a premium subscription in our bot?',
  'Write a welcome message for my gaming server with a big header, three rules as a list, and a spoiler at the end',
]

type Part = {type: string; text?: string; state?: string; input?: unknown; output?: unknown; toolName?: string}
const isTool = (p: Part) => p.type === 'dynamic-tool' || p.type.startsWith('tool-')
const toolName = (p: Part) => p.toolName ?? p.type.replace(/^tool-/, '')

// Embed colour from the first line of the ruling, the way a verdict would be colour coded in a real bot.
function verdictColor(text: string) {
  const m = text.match(/\*\*Ruling:\*\*\s*([^.\n]*)/i)
  const head = (m?.[1] ?? '').toLowerCase()
  if (/^(yes|seconds|fixable|allowed|you can)/.test(head)) return 'var(--dc-green)'
  if (/^(no|not |never|banned|milliseconds is wrong)/.test(head)) return 'var(--dc-red)'
  if (/^(depends|unclear|unresolved|it depends|partly|officially)/.test(head)) return 'var(--dc-yellow)'
  return 'var(--dc-blurple)'
}

function timeNow() {
  return new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
}

function Avatar({kind}: {kind: 'bot' | 'user'}) {
  return kind === 'bot' ? (
    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blurple text-sm font-black text-white">
      BL
    </div>
  ) : (
    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-fuchsia text-sm font-black text-white">
      you
    </div>
  )
}

function CaseFile({part}: {part: Part}) {
  const name = toolName(part)
  const input = part.input as Record<string, unknown> | undefined
  const done = part.state === 'output-available'
  const label =
    name === 'groq_query'
      ? '/lookup rules dataset'
      : name === 'knowledge_base_read'
        ? '/read source pages'
        : name === 'schema_explorer'
          ? '/inspect schema'
          : `/${name}`
  const detail =
    name === 'groq_query' && input?.query
      ? String(input.query)
      : name === 'knowledge_base_read' && Array.isArray(input?.paths)
        ? (input!.paths as string[]).join('\n')
        : JSON.stringify(input ?? {}, null, 1)
  return (
    <details className="group my-1 max-w-2xl rounded border border-line bg-rail/60 text-xs">
      <summary className="flex cursor-pointer items-center gap-2 px-3 py-1.5 text-muted">
        <span className={`inline-block h-2 w-2 rounded-full ${done ? 'bg-green' : 'bg-yellow'}`} />
        <span className="font-mono text-text-2">{label}</span>
        <span className="italic">Only you can see this</span>
        <span className="ml-auto group-open:hidden">show</span>
      </summary>
      <pre className="whitespace-pre-wrap break-all border-t border-line px-3 py-2 font-mono text-[11px] leading-relaxed text-text-2">
        {detail}
      </pre>
    </details>
  )
}

export default function Home() {
  const [input, setInput] = useState('')
  const today = new Date().toISOString().slice(0, 10)
  const [asOf, setAsOf] = useState(today)
  const [brief, setBrief] = useState(false)
  // one thread per page load, so Insights groups the whole conversation
  const [threadId] = useState(() => 'bl-' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36))
  const endRef = useRef<HTMLDivElement>(null)
  const {messages, sendMessage, status, error} = useChat({
    transport: new DefaultChatTransport({api: '/api/lawyer'}),
  })
  const busy = status === 'submitted' || status === 'streaming'

  useEffect(() => {
    endRef.current?.scrollIntoView({behavior: 'smooth', block: 'end'})
  }, [messages, status])

  const ask = (text: string) => {
    if (!text.trim() || busy) return
    sendMessage({text}, {body: {asOf, threadId, brief}})
    setInput('')
  }

  return (
    <div className="flex h-screen w-full">
      {/* server rail */}
      <aside className="hidden w-[72px] shrink-0 flex-col items-center gap-2 bg-rail py-3 sm:flex">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blurple text-base font-black text-white">BL</div>
        <div className="my-1 h-[2px] w-8 rounded bg-line" />
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-sidebar text-lg" title="Sanity">
          🟥
        </div>
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-sidebar text-lg" title="Discord">
          🟦
        </div>
      </aside>

      {/* sidebar */}
      <aside className="hidden w-60 shrink-0 flex-col bg-sidebar md:flex">
        <div className="border-b border-rail px-4 py-3 text-[15px] font-semibold text-white shadow-sm">Bot Lawyer</div>
        <div className="px-2 pt-4 text-[11px] font-bold uppercase tracking-wide text-muted">Text channels</div>
        <div className="mx-2 mt-1 rounded bg-hover px-2 py-1.5 text-[15px] text-white">
          <span className="mr-1 text-muted">#</span>ask-counsel
        </div>
        <a href="/contradictions" className="mx-2 mt-0.5 block rounded px-2 py-1.5 text-[15px] text-muted hover:bg-hover hover:text-text">
          <span className="mr-1">#</span>contradictions
        </a>
        <div className="mx-2 mt-0.5 rounded px-2 py-1.5 text-[15px] text-muted">
          <span className="mr-1">#</span>billing-never
        </div>
        <div className="mt-auto space-y-1 border-t border-rail p-3 text-[11px] leading-relaxed text-muted">
          <p>Rules and sources: Sanity project <span className="font-mono text-text-2">v6745vem</span></p>
          <p>Served via two Sanity Context MCP endpoints (GROQ mode and Knowledge Base mode)</p>
          <p>Sources snapshotted 2026-09-19</p>
        </div>
      </aside>

      {/* chat */}
      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center gap-2 border-b border-rail px-4 py-3 shadow-sm">
          <span className="text-xl text-muted">#</span>
          <span className="font-semibold text-white">ask-counsel</span>
          <span className="mx-2 hidden h-5 w-px bg-line sm:block" />
          <span className="hidden truncate text-sm text-muted sm:block">
            Not a lawyer. A GROQ query with anxiety. Every ruling quotes the rule, links the page, states the date.
          </span>
          <button
            type="button"
            onClick={() => setBrief((b) => !b)}
            className={`ml-auto shrink-0 rounded px-2 py-1 text-xs ${brief ? 'bg-green/20 text-green' : 'bg-input text-text-2'}`}
            title="Short answers: ruling, one quote, one source"
          >
            {brief ? 'short answers on' : 'short answers'}
          </button>
          <label className="flex shrink-0 items-center gap-2 rounded bg-input px-2 py-1 text-xs text-text-2" title="Rules carry effective dates. Ask what applied on any day.">
            <span className="hidden sm:inline">Rule as of</span>
            <input
              type="date"
              value={asOf}
              max={today}
              min="2017-08-20"
              onChange={(e) => setAsOf(e.target.value || today)}
              className="bg-transparent font-mono text-xs text-text focus:outline-none"
            />
            {asOf !== today && (
              <button type="button" onClick={() => setAsOf(today)} className="rounded bg-yellow/20 px-1.5 text-yellow">
                time travel on · reset
              </button>
            )}
          </label>
        </header>

        <section className="flex-1 overflow-y-auto px-4 pb-4">
          {/* channel intro */}
          <div className="mt-6 mb-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blurple text-2xl font-black text-white">BL</div>
            <h1 className="mt-3 text-3xl font-bold text-white">
              Bot Lawyer <span className="ml-1 rounded bg-blurple px-1.5 py-0.5 align-middle text-[10px] font-bold uppercase text-white">app</span>
            </h1>
            <p className="mt-1 max-w-2xl text-[15px] text-text-2">
              This is the beginning of your direct message history with <b className="text-white">Bot Lawyer</b>. Counsel for
              Discord app developers. When Discord&apos;s own pages disagree, you get both sides and which one wins. If no page
              answers, counsel says so instead of guessing.
            </p>
          </div>

          {messages.length === 0 && (
            <div className="mb-6 flex max-w-2xl flex-wrap gap-2">
              {EXAMPLES.map((q) => (
                <button
                  key={q}
                  onClick={() => ask(q)}
                  className="rounded border border-line bg-sidebar px-3 py-1.5 text-left text-[13px] text-text hover:bg-hover"
                >
                  {q}
                </button>
              ))}
            </div>
          )}

          <div className="space-y-1">
            {messages.map((m) => {
              const isBot = m.role !== 'user'
              const textParts = (m.parts as Part[]).filter((p) => p.type === 'text')
              const toolParts = (m.parts as Part[]).filter(isTool)
              const full = textParts.map((p) => p.text ?? '').join('')
              return (
                <div key={m.id} className="msg -mx-4 flex gap-4 px-4 py-2">
                  <Avatar kind={isBot ? 'bot' : 'user'} />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-baseline gap-2">
                      <span className={`text-[15px] font-medium ${isBot ? 'text-white' : 'text-fuchsia'}`}>
                        {isBot ? 'Bot Lawyer' : 'you'}
                      </span>
                      {isBot && (
                        <span className="rounded bg-blurple px-1 py-px text-[10px] font-bold uppercase text-white">app</span>
                      )}
                      <span className="text-xs text-muted">Today at {timeNow()}</span>
                    </div>
                    {!isBot && <p className="text-[15px] text-text">{full}</p>}
                    {isBot && toolParts.map((p, i) => <CaseFile key={i} part={p} />)}
                    {isBot && full && (
                      <div
                        className="mt-1 max-w-2xl rounded bg-embed px-4 py-3"
                        style={{borderLeft: `4px solid ${verdictColor(full)}`}}
                      >
                        <div className="mb-1 text-xs font-semibold text-muted">Memorandum from counsel</div>
                        <div className="embed-md">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>{tidy(full)}</ReactMarkdown>
                        </div>
                        <div className="mt-2 text-[11px] text-muted">Bot Lawyer · sources snapshotted 2026-09-19 · content in Sanity, served by Sanity Context</div>
                      </div>
                    )}
                    {isBot && full && (
                      <PagesRead
                        pages={toolParts.filter((p) => toolName(p) === 'knowledge_base_read').flatMap((p) => extractPages(p.input, p.output))}
                      />
                    )}
                    {isBot && full && (
                      <RulesOnFile
                        rules={toolParts.filter((p) => toolName(p) === 'groq_query').flatMap((p) => extractRules(p.output))}
                        asOf={asOf}
                      />
                    )}
                  </div>
                </div>
              )
            })}
          </div>

          {busy && messages[messages.length - 1]?.role === 'user' && (
            <div className="mt-2 flex items-center gap-2 text-sm text-text-2">
              <span className="typing">
                <span /><span /><span />
              </span>
              <b className="text-white">Bot Lawyer</b> is typing...
            </div>
          )}
          {error && <p className="mt-2 rounded bg-red/20 px-3 py-2 text-sm text-red">Something broke on our side: {error.message}</p>}
          <div ref={endRef} />
        </section>

        <form
          className="px-4 pb-5"
          onSubmit={(e) => {
            e.preventDefault()
            ask(input)
          }}
        >
          <div className="flex items-center gap-2 rounded-lg bg-input px-4">
            <span className="text-xl text-muted">+</span>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message #ask-counsel (say how many users, which intents, verified or not)"
              className="flex-1 bg-transparent py-3 text-[15px] text-text placeholder:text-muted focus:outline-none"
            />
            <button disabled={busy || !input.trim()} className="text-sm font-semibold text-blurple disabled:opacity-40">
              Send
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}
