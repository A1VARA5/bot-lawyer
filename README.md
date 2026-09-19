# Bot Lawyer

Bot Lawyer tells Discord bot developers which rule applies to them, quotes the page with a date, and shows both sides when two of Discord's own pages disagree. It reads a Sanity dataset of 136 rules and a Sanity Context knowledge base of 90 Discord pages through two MCP endpoints.

## Try it

Web: https://bot-lawyer.vercel.app. Ask "My bot is in 90 servers with about 4,000 users, do I need Message Content approved?" Then set "Rule as of" to 2026-05-01 and ask again.

Discord: the app BOT LAWYER answers `/ask question:<your situation> as_of:<YYYY-MM-DD>` over the HTTP interactions endpoint. No gateway, no intents, so it follows its own advice.

Ledger: https://bot-lawyer.vercel.app/contradictions, all 11 contradictions, both sides, dates, resolution.

Studio: https://bot-lawyer.sanity.studio (project `v6745vem`, dataset `production`).

Install the Discord app in your own server (Send Messages only): https://discord.com/oauth2/authorize?client_id=1550945390789140661&scope=bot%20applications.commands&permissions=2048

## How it works

Two Sanity Context endpoints, because an endpoint with a dataset source ignores its knowledge base sources.

`bot-lawyer-rules`: GROQ mode over the dataset, filtered to `_type in ["rule","source","policyArea"]` so the agent cannot see the eval questions. Tools: `initial_context` (schema summary), `schema_explorer`, `groq_query`, `array_field_reader`.

`bot-lawyer-kb`: knowledge base mode over the page snapshots. Tools: `initial_context` (the outline), `knowledge_base_read` (up to 20 entries per call).

The app merges both clients into one Vercel AI SDK tool set and inlines both initial contexts into the cached system prompt. Every ruling runs `groq_query` over the whole policy area, fetches conflicting rules when a result carries a `contradictionId`, then reads the matching knowledge base entry.

The rule document, shortened:

```
rule
  quote                 verbatim, the only text allowed in a blockquote
  appliesWhen           minUsers, maxUsers, minServers, maxServers, intents[],
                        verificationState, region, ownerAge
  effectiveFrom, effectiveTo
  source -> source      title, kind, url, authority, publishedAt, lastEditedAt
  confidence            confirmed | inferred
  supersedes -> rule
  conflictsWith[] -> rule
  resolution, contradictionId
```

Time travel: "Rule as of" is a date, and the prompt rules only with rules in force on it. The same 120 servers question gets "Yes, 120 servers clears the threshold" as of 2026-05-01 (rule in force 2020-10-27 to 2026-06-09) and "No, 4,000 users is under 10,000, server count is irrelevant" today.

Rules on file: the documents each `groq_query` returned, rendered under the answer with effective range, thresholds, authority bar, conflict badge and superseded strikethrough. Parsed from the tool output, no model involved. Also a short answers toggle and a drafting mode for welcome messages and channel lists.

## The content

136 rules, 58 sources, 11 policy areas, 40 eval questions, 11 contradictions (C1 to C11). Sources: docs.discord.com, both help centers through their JSON API (which gives edit dates), legal pages, GitHub issues. All 136 quotes were checked against the raw snapshots; 55 of the first 100 rules are confirmed, 45 inferred.

On June 10, 2026 Discord replaced the 100 servers privileged intent threshold with 10,000 unique users, split verification from intent review and added annual reapplication. About half of its pages were updated. In the 2026-09-19 snapshot the application flags table still says 100 servers, and the gateway page says 10,000 users at the top of a section and "after your app is verified, you can apply" 25 lines lower.

The ledger is generated from every rule with a `contradictionId`.

## Eval

| kind | PASS | PARTIAL | FAIL | items |
|---|---|---|---|---|
| trap | 7 | 1 | 0 | 8 |
| standard | 22 | 6 | 1 | 29 |
| unknown | 2 | 1 | 0 | 3 |
| all | 31 | 8 | 1 | 40 |

Ruling right on 39 of 40, 0 of 8 traps fooled, 22 of 40 read the knowledge base, 12 surfaced a contradiction, 20.6 s average. The one FAIL put a knowledge base summary sentence in a blockquote as if it were page wording. Fixed after the eval with a provenance rule, not measured again.

Honest limit: I wrote the 40 questions with the same agents that built the dataset, a separate model agent graded them, and the grades were spot checked by hand. So this measures whether the agent reads the structure correctly, not whether the structure is complete. Not a benchmark.

## Run it yourself

```
npx sanity@latest login
cd studio                                  # point sanity.config.ts at your project
npx sanity schema deploy
npx sanity deploy                          # GROQ mode needs a deployed Studio
npx sanity dataset import ../seed/seed.ndjson production --replace
npx sanity dataset import ../seed/seed-formatting.ndjson production
npx sanity dataset import ../seed/seed-kb-questions.ndjson production

npx sanity context create --organization <org-id> --title "Discord bot rules"
npx sanity context imports create <kb-id> --file ./corpus.zip   # snapshots not in repo
npx sanity context build <kb-id> --watch
# Dashboard: bot-lawyer-rules (GROQ mode, filter above), bot-lawyer-kb (Knowledge Base mode)

cd web
cp .env.example .env.local
npm install
npm run dev
node --env-file=.env.local scripts/register-commands.mjs   # /ask in your guild
```

## What broke

- Studio deploy failed twice: `studioHost` missing, then `@sanity/icons` v5 has no named exports from the index.
- First knowledge base build refused at 303 of 150 indexed documents on this plan. Dropped the 177 page crawl for an 80 file snapshot.
- Build 1 died at "thin_leaves (1 remaining)". Build 2 resumed and passed.
- Haiku skipped `groq_query` and said "both sources agree" on a documented contradiction. Sonnet now.
- My GROQ hint used the wrong slug format twice.
- The case file UI never rendered: MCP tools arrive as `dynamic-tool` parts, not `tool-<name>`.
- First design: black text on black.
- The $7 model key ran out mid eval and took the demo down. Now cached, metered, capped at $3 a day, with a Vercel AI Gateway fallback.
- Anonymous reads on the public dataset return empty on this Growth trial project. Server side read token as a workaround.
- One Context issue (App Directory support server vs Monetization SKUs) is two processes, not a conflict, and resolution is binary. Left pending on purpose.
- The bot had all three privileged intent toggles on until the test pass caught it.

## What is not done

- The post eval prompt fixes are deployed but not measured again.
- `/ask` is registered in my test guild only.
- 21 rules from undated docs pages carry the snapshot date as `effectiveFrom`, so time travel before 2026 is thin there.
- The knowledge base read runs on every ruling and doubled answer time.

## Credits

Built with Claude Code. I direct, the tools build: four research agents, a seeding agent, a formatting agent, two graders, a test pass agent. Two endpoints, merged tools and inlined initial context follow the Sanity Labs agent workshop. The content is Discord's own docs, support articles, policies, change log and GitHub issues.

## License

MIT.
