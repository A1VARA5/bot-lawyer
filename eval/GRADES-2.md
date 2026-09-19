# Bot Lawyer eval grades, run 2

Run: `eval/results.json` (run 1 preserved as `eval/results-run1.json`), 36 questions fetched via the Sanity CLI, `run_eval.py` now appends the situation block to each question. Graded 2026-09-19 (evening) against `expectedAnswer`, `expectedRules` and `note`. Same strict marking as GRADES.md: PASS needs the right ruling, at least one source URL, an effective date, and for traps no fall to the stale answer. Drafting questions q26 to q33 would PASS only as a single ```md code block followed by exactly one Length line.

## Summary

**15 PASS / 3 PARTIAL / 0 FAIL out of 18 answered; 18 of 36 NOT RUN.** (trap 7/1/0, standard 8/2/0, unknown 0/0/0 answered.) The run died at q19: the Anthropic key behind both localhost and production returned "Your credit balance is too low to access the Anthropic API" (confirmed with a direct call to api.anthropic.com from web/.env.local). The AI SDK stream masks this as "An error occurred." in 1 to 1.5 s, and because errors return instantly the runner then hit the app's own 6 per minute rate limit, so q22 to u03 are HTTP 429 without ever reaching the model. All eight drafting questions (q26 to q33) and all three unknowns are therefore ungraded. Average 14.7 s per answered item (min 10.4 s, max 32.4 s). 17 of 18 answers cite a URL and an effective date (q16 cites nothing, it only asks for the region). 5 of 18 name a contradictionId (C1, C2, C4, C5, C6, C9, C10); q05 and q08 show two sources disagreeing without the id. No trap item fell for a stale answer.

Style flags: 1 answer contains an em dash (q01, inside the quoted flags table title "Intent required for bots in 100 or more servers", not in the attribution line). 3 answers contain an exclamation mark (q09, q10, q11), all inside the quoted article title "My Bot is Being Rate Limited!". No en dashes. "let me check" and "sources agree" do not appear. New leak: q13 and q14 open with a narration line before the Ruling ("Found the direct rule. No conflicts flagged on it." / "Found the rule directly on point, in force today, no conflicts flagged."), which the prompt forbids in spirit ("never narrate"). Format drift: q03 puts `effective from 2026-06-10` inside the blockquote instead of before it; q11 prints the source as "Gateway (developer docs) (developerDocs)"; q05, q12, q13, q14, q15 print the raw enum kind ("developerDocs", "developerPolicy", "developerTerms") where other answers print "developer docs".

## Table

| id | kind | verdict | reason |
|---|---|---|---|
| q01 | trap | PASS | "No. Your server count does not matter anymore... 4,000 is well under the threshold, so you just toggle Message Content on"; Gateway quotes with 2026-06-10, names C1 (stale flags table) and C2 (verification separate), 90 day window. Situation delivered this time, so it rules instead of asking. Em dash inside the quoted table title. |
| q02 | trap | PASS | "Discord does not show you a user count anywhere in the Developer Portal"; support article and Gateway quoted with 2026-06-10, both portal counts explained as different metrics, GitHub staff comment quoted. |
| q03 | trap | PARTIAL | Ruling right ("that approval is no longer permanent. You now have to reapply annually") and "Do not preemptively reapply before that notice arrives". Still ties the 90 day window to crossing 10,000 users, says "before access is pulled" instead of "access continues during review", so rule.intent-access-continues-during-review is missing again. Effective date printed inside the blockquote. Same defect as run 1. |
| q04 | trap | PASS | "Your problem is not verification or server count, it is that GUILD_MEMBERS is not toggled on... at 3,000 users you don't need approval"; 4014 quote from Opcodes page dated 2020-10-27, Gateway 2026-06-10, fix given. Does not mention 4013. Used knowledge_base_read as a second step. |
| q05 | standard | PASS | Replies exception with the ping on reply and not slash command caveats, both the June 2026 guide (2026-06-10) and Gateway (2022-09-01) quoted, "each page is incomplete rather than wrong" resolution applied. Does not name C8 by id. Used a `title match "*content*"` filter despite the prompt. Raw kind label "developerDocs". |
| q06 | trap | PASS | "Depends... no current page states a hard 100-server cap"; C4 named, the 2024-08-30 support article and the 2026-06-10 announcement both quoted, "The dataset's own resolution note: unresolved". Does not tell the developer to ask developer support (expected). Calls the support article an "undated retraction", which it is not. |
| q07 | standard | PASS | "No, not directly. At 15 you cannot submit the ID"; both 2022-05-23 quotes with URL, sponsor via team owner explained. Omits "at 16 you can verify yourself". |
| q08 | trap | PASS | "Yes... the transfer strips its verification and the new owner has to re-verify"; 2025-09-12 rules quoted, dual consent, 30 days, the 2022-05-23 to 2025-09-11 superseded article named with its range. |
| q09 | trap | PASS | "Seconds. retry_after: 2.5 means wait two and a half seconds"; docs and v8 change log (2020-09-24), the wrong support article (2025-07-14), C5, authority 80 over 60 and the 65 / 64.57 example. Exclamation mark inside quoted title. |
| q10 | standard | PASS | "50 requests per second per bot, and no, slash command (interaction) responses do not count"; C6 named, ephemeral claim corrected, per route limits still apply, "page undated, confidence inferred, snapshot date used". Omits the 10,000 invalid requests ban (not asked). Exclamation in quoted title. |
| q11 | standard | PASS | "at 2,500 servers sharding is mandatory"; Gateway and support article quoted, 2,000 planning, 1 per 1,000, 150,000 large bot sharding. Omits the IDENTIFY 1,000 per 24 h limit (rule.identify-limit-1000, run 1 had it). Double kind label. Used a title match filter. Exclamation in quoted title. |
| q12 | standard | PASS | Now covers all five expected rules: stated functionality, privacy policy duty, encryption at rest, delete when no longer necessary, ML training ban, "no fixed retention window in days or months". Fixed from run 1. Raw kind labels. |
| q13 | standard | PASS | "Yes, you need a privacy policy even for a bot in one private server"; Developer Terms quote, 2024-07-08, "no threshold in appliesWhen". Opens with a narration line before the Ruling. Second groq_query on area.appDirectory was unnecessary. |
| q14 | standard | PASS | "No, not without Discord's express permission"; Policy rule 21 verbatim, 2024-07-08, notes the 2022 edition had no such rule. Narration line before the Ruling. |
| q15 | standard | PASS | "No, not by default... unless that user has personally opted in"; Policy rule 5 quoted, server owner toggle is not user permission. Does not cite rule 6 (no marketing). 32.4 s and three tool calls because it queried area.intents first; no area id in the tool description covers conduct rules, so the model guessed. |
| q16 | standard | PARTIAL | Only asks "is your team based in the US, UK, or an EU member state, or somewhere else?" and stops. No ruling, no quote, no URL, no date. Run 1 gave the full conditional ruling and passed. The prompt's "ask in one short line and stop" now overrides the two branch answer the dataset expects. |
| q17 | standard | PASS | "No, not yet. Premium Apps is limited to teams based in the United States, United Kingdom or European Union"; docs (undated, snapshot) and support (2024-12-12) quoted, "soon but gives no date". |
| q18 | standard | PARTIAL | Checklist quoted but the blockquote stops at "App has a link to your Terms of Service", and the ruling omits payouts set up, no harmful language, agreeing to the Monetization Terms and the 50 SKU cap (rule.max-50-skus expected). C10 and C9 both surfaced correctly. For a question that asks for "the exact eligibility requirements" this is incomplete. |
| q19 | trap | NOT RUN | "An error occurred." in 1.4 s (Anthropic credit balance). |
| q20 | standard | NOT RUN | "An error occurred." in 0.7 s. |
| q21 | standard | NOT RUN | "An error occurred." in 0.7 s. |
| q22 to q25 | standard | NOT RUN | HTTP 429 from the app's own limiter (runner has no back off). |
| q26 to q33 | standard (drafting) | NOT RUN | HTTP 429. The drafting format rule (single ```md block plus one Length line) is untested in this run. |
| u01 to u03 | unknown | NOT RUN | HTTP 429. |

## Patterns

1. **The demo has a single point of failure and it failed.** One Anthropic test key serves localhost and production. When its credit ran out, every question on https://bot-lawyer.vercel.app started returning "Something broke on our side: An error occurred." within 1.5 s. Nothing in the app distinguishes "out of credit" from any other error, and nothing logs it where a visitor or the operator can see it without the Vercel console.
2. **The runner makes a bad minute worse.** `run_eval.py` fires the next question immediately after an error, so three instant errors were followed by fifteen 429s from the app's own limiter. It needs a sleep on error and a retry after `Retry-After`.
3. **Situation delivery fixed the two hedges from run 1 (q01, q04) but the "ask and stop" rule now over fires (q16).** When the missing fact has two branches (in region or not), the dataset expects both branches, not a question.
4. **Whole area queries fixed q12 but not q03.** The model still reads the 90 day window as tied to crossing 10,000 users and drops the access continues rule. The rule text itself may need a clearer plainAnswer.
5. **New style leaks replace old ones.** Em dashes are down from 13 to 1 (and that one is quoted text). But two answers narrate before the ruling, one puts the date inside the blockquote, and the source kind label is inconsistent (raw enum versus humanised) across answers.
6. **The model still filters by title match in 3 of 18 queries (q05, q11, q15)** despite the prompt saying whole area, no text filter. It got away with it this time.
7. **Answers are long.** Median answer is around 350 words for a format that promises a one sentence ruling. Judges skimming on a phone will read the Ruling and stop, which is fine only if the Ruling line is right, and it was in 17 of 18.

## Ranked fixes

1. **Put credit on the key or switch to a funded key, and add a plain error message for the billing case** (blocks everything else; 15 minutes). Check the Vercel env var as well as .env.local, they are the same key.
2. **Back off in run_eval.py**: on `error` or HTTP 429 sleep 61 s and retry once, then continue (10 minutes). Then rerun q19 to u03 and grade them; this file has 18 blanks.
3. **Prompt, three lines** (15 minutes): "Never write anything before **Ruling:**"; "The effective date goes in the sentence before the blockquote, never inside it"; "Print the source kind as words: developer docs, developer support, Developer Policy, Developer Terms, change log, GitHub". Removes the q13, q14, q03 and q05/q11/q12 cosmetic defects.
4. **Prompt, one line for two branch facts** (5 minutes): "If the missing fact has only two or three possible values (a region list, verified or not), give the ruling for each branch instead of asking." Fixes q16 and the first example question on the home page, which today ends with "Roughly how many unique users does your app reach?" instead of a ruling.
5. **Data: reword rule.intent-90-day-window and rule.intent-access-continues-during-review plainAnswers** so the 90 days is explicitly attached to the annual reapply notice as well as the first crossing (10 minutes). q03 has been PARTIAL twice for the same reason.
6. **q18: tell the model to quote the whole checklist** when the question asks for exact requirements ("do not truncate a list you are quoting") (5 minutes).

## Comparison with GRADES.md (run 1)

| | Run 1 | Run 2 |
|---|---|---|
| Items | 28 | 36 (18 answered, 18 not run) |
| PASS / PARTIAL / FAIL | 23 / 5 / 0 | 15 / 3 / 0 of 18 |
| Same 18 items (q01 to q18) | 15 PASS / 3 PARTIAL (q01, q03, q04, q12 were PARTIAL; q16, q18 PASS) | 15 PASS / 3 PARTIAL (q03, q16, q18) |
| Fixed since run 1 | | q01, q04 (situation now sent, both rule definitively), q12 (privacy policy duty now included) |
| Regressed since run 1 | | q16 (asks for region instead of the two branch ruling), q18 (checklist truncated, more items missing) |
| Unchanged defect | | q03 (90 day window misattributed, access continues rule missing) |
| Em dash answers | 13 of 28 | 1 of 18 (inside quoted text) |
| Exclamation answers | 4 of 28 (all quoted text) | 3 of 18 (all quoted text) |
| Narration before Ruling | 0 | 2 (q13, q14) |
| Average seconds | 13.4 | 14.7 |
| Contradiction ids named | 7 of 28 | 5 of 18 |
| KB reads | not counted | 2 of 18 (q04, q15) |
| Errors | 0 | 18 (3 upstream credit, 15 self inflicted 429) |

Net: the run 1 fixes worked on the items they targeted (q01, q04, q12) and the dash problem is gone from the model output. The cost was one new hedge (q16) and one unchanged (q03). The bigger finding is operational: the key ran dry mid run and production went down with it, which no amount of prompt work covers.
