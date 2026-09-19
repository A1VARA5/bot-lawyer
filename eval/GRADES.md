# Bot Lawyer eval grades

Run: `eval/results.json`, 28 items, graded 2026-09-19 against `expectedAnswer`, `expectedRules` and `note`, with claims spot-checked against `seed/seed.ndjson`. Strict marking: PASS needs the right ruling, at least one source URL, an effective date, and for traps no fall to the stale answer; unknowns pass only if the agent admits the gap and invents nothing.

## Summary

**23 PASS / 5 PARTIAL / 0 FAIL** (trap 5/3/0, standard 16/1/0, unknown 2/1/0). Average 13.4 s per answer (min 8.8 s, max 22.1 s). 28 of 28 answers cite at least one source URL and state an effective date. 12 of 28 surface a contradiction (7 name a `contradictionId`: C4, C5, C6, C8, C9, C10; 5 more show two sources disagreeing without the id). No trap item fell for the stale "100 servers" answer.

Style flags: 13 answers contain an em dash (q01, q03, q04, q05, q10, q11, q17, q18, q19, q20, q21, q22, u02), almost all in the "em dash then [Source](url)" attribution line. 4 answers contain an exclamation mark (q09, q10, q11 inside the quoted article title "My Bot is Being Rate Limited!", q15 inside the quoted example "Welcome to the server!"). No en dashes. None of the phrases "let me check", "I'll look up" or "both sources agree" appear; q23 comes close with "Two Discord sources agree on this".

## Table

| id | kind | verdict | reason |
|---|---|---|---|
| q01 | trap | PARTIAL | Did not fall for the trap ("The old 100-server rule is superseded and explicitly marked stale") but ruled "Can't say yet" and asked for the user count. Expected a definite "no, toggle it on" at 4,000 users. Root cause: run_eval.py never sends the situation block, so the agent never saw the 4,000. Em dashes. |
| q02 | trap | PASS | "Discord does not show you a user count anywhere in the Developer Portal"; cites the support article and gateway page with dates, warns the portal server counts are "leftover metrics from the pre-June-2026 100-server regime". |
| q03 | trap | PARTIAL | Ruling right: "Prior approval carries over, but it is not permanent: you now have to reapply annually." Misses rule.intent-access-continues-during-review and ties the 90-day window only to the 10,000 crossing, not to the annual reapply notice as the dataset says. Em dash. |
| q04 | trap | PARTIAL | Definition correct: "you tried to use a privileged intent that your app has not enabled in the portal, or has not been approved for", never mentions verification or 100 servers, distinguishes 4013. But gives two conditional fixes and asks "Tell me your unique user count" instead of ruling at 3,000 users (situation not sent). Em dashes. |
| q05 | standard | PASS | "Yes, but only under specific conditions"; quotes both the June 2026 guide and the gateway page with dates, names C8, and applies the union resolution. Em dashes in attribution lines. |
| q06 | trap | PASS | "Depends, and honestly unresolved: no current Discord page confirms a hard 100-server cap for unverified apps anymore, but none explicitly retracts it either." Cites all three pages, names C4, recommends developer support. |
| q07 | standard | PASS | "Not on your own ID"; quotes both 2022-05-23 rules with URL, explains a 16+ team owner files it and must keep owning the team. Omits the "at 16 you can verify yourself" line, minor. |
| q08 | trap | PASS | "Yes, you can transfer a verified bot's team, but the transfer strips verification and the new owner must re-verify"; dual consent, 30 days, support ticket, and the Under 16 article shown as superseded with its effectiveTo. |
| q09 | trap | PASS | "Seconds. A retry_after of 2.5 means wait two and a half seconds, not 2.5 ms." Docs, v8 changelog and the wrong support article all quoted, C5 named with the authority reasoning. Exclamation mark is inside the quoted article title. |
| q10 | standard | PASS | "50 requests per second, and no, interaction (slash command) responses do not count against it, though a support article says otherwise and is wrong"; C6 named, per-route limits still apply. Leaves out the 10,000 invalid requests ban (expected but not asked). Em dash, exclamation in quoted title. |
| q11 | standard | PASS | "Sharding becomes mandatory once your bot is in 2,500 or more guilds"; 2,000 planning, 1 per 1,000, 150,000 large bot sharding, session limit formula, both sources cited. Em dashes, exclamation in quoted title. |
| q12 | standard | PARTIAL | Ruling right: "Yes, but only as much as you actually need for your bot's stated functionality"; covers purpose limit, deletion triggers, encryption, no fixed window, ML ban. Never mentions the privacy policy duty (rule.privacy-policy-required, Developer Terms 5a), a real condition on storing data. |
| q13 | standard | PASS | "Yes, even a bot in a single private server needs a privacy policy"; quotes Developer Terms with URL and 2024-07-08 date. |
| q14 | standard | PASS | "No, you may not use message content from your bot to fine-tune an LLM without Discord's express permission"; Policy rule 21 quoted verbatim, notes it did not exist in the October 1, 2022 version. |
| q15 | standard | PASS | "No, not by default"; quotes Policy rule 5 with date and explains "The server owner turning on a welcome DM feature does not count as the joining user's permission". Exclamation mark inside quoted example text. |
| q16 | standard | PASS | Asks for region but gives the full conditional ruling with the 2024-10-07 quote: "If your team is in the US, UK, or an EU member state, you are not free to sell only via Patreon... Outside those regions... Patreon-only is fine." Matches "Depends on region". |
| q17 | standard | PASS | "No. Premium Apps monetisation is not currently available for teams based in Canada, India, or Brazil"; docs and support locale list quoted with dates, "soon but gives no date". Em dashes in attribution. |
| q18 | standard | PASS | Full checklist quoted, surfaces C10 ("approval for Message Content only exists above 10,000 unique users... that is a real gap") and C9 net-of-fees. Omits max 50 SKUs; minor self-contradiction on whether verification is "part of the checklist". Em dashes. |
| q19 | trap | PASS | Does not stop at "$100 in sales": "treat the $100 as net of payment processing and transaction fees, not gross revenue"; 45 days, $25 minimum, C9 with both sources. Em dashes in attribution. |
| q20 | standard | PASS | "You need app verification first, then policy compliance and a complete Discovery profile"; 24-hour rule and the 13+ content rule quoted with URLs and dates. Em dashes. |
| q21 | standard | PASS | "Yes, they are the same thing"; VERIFIED_BOT 1 << 16, VERIFIED_DEVELOPER 1 << 17 legacy, Active Developer Badge decommissioned 2025-12-05 (matches dataset). Em dashes. |
| q22 | standard | PASS | "100 global slash (CHAT_INPUT) commands, 15 user-context and 15 message-context commands, plus 1 primary entry point... 200 creates per day per guild"; error codes 30032/30034 are real. Omits the applications.commands scope rule (not asked). Em dashes. |
| q23 | standard | PASS | "No. Automating your own user account, even privately, is banned outright"; Guidelines rule 14 (2025-09-29) and the support article quoted with URLs. Near-miss phrase "Two Discord sources agree on this". |
| q24 | standard | PASS | Quotes the baseline list with URL and 2024-05-31 date, flags "discriminators" as stale, maps the gaps to Message Content, Presence and Guild Members. Says "just not message content" without the documented exceptions, minor. |
| q25 | standard | PASS | "As of today, the July 8, 2024 Developer Policy is the one that governs your app"; 2022 and 2020 editions with dates and URLs. Skips the Developer Terms lineage, the 2017 version and the arbitration opt out, which the question did not ask about. First tool call was an empty `[0...0]` query. |
| u01 | unknown | PASS | Admits the gap: "no current Discord page confirms a 100-server cap for unverified apps, but no current page retracts it either"; cites both pages, C4, "file a ticket and get it in writing". Invents nothing. |
| u02 | unknown | PASS | "There is no page in the dataset or knowledge base titled Message Content Intent FAQ, so I cannot quote it"; falls back to the Developer Terms retention duty. The 2017 seven-day rule it mentions is in the dataset (rule.retention-2017-tos). Does not learn the article was deleted, since no source records that. Em dashes. |
| u03 | unknown | PARTIAL | Right date, "took effect on June 10, 2026", but delivered as a confident single answer and cites the undated announcement as evidence for it. Dataset has rule.intent-change-date-announcement-undated (C3) whose resolution says "flag that the primary source is undated"; the filtered GROQ query never retrieved it. |

## Patterns

Recurring reasons behind the 5 PARTIALs:

1. **Hedging because the situation was never delivered (q01, q04).** `run_eval.py` line 19 builds the request from `item["text"]` only. The dataset's expected answers assume the agent knows the user count, so both trap items ended in "tell me your user count". The trap itself was not taken either time.
2. **Filtered GROQ queries drop the caveat rules (u03, q03, q12).** The agent narrows by `title match` / `quote match` and then rules on what came back. u03 missed C3 because the undated-announcement rule contains neither "10,000" nor "threshold". q03 retrieved the reapply rule but dropped its plainAnswer's "then you have 90 days" and the access-continues rule. q12 pulled the whole dataRetention area but still left the privacy policy duty out of a five-condition answer.
3. **Style leaks.** The attribution line "em dash, then [Source](url)" puts an em dash in 13 of 28 answers. Exclamation marks only appear inside quoted Discord text, but they still show up in a scan.
4. **Data quirk, not a verdict issue.** Seven answers print `effective from 2026-09-19` for docs-derived rules (q10, q11, q17, q18, q20, q21, q22). That is the crawl date, and to a reader it says the rule started today.

Three fixes, ranked by how many items they touch:

1. **Citation format rule in the system prompt (13 answers).** Require `Source: [Title](url), effective from YYYY-MM-DD` on its own line and forbid em and en dashes anywhere in the answer. This clears every dash flag in one line of prompt; also tell the agent to quote titles without trailing punctuation if the title ends in "!".
2. **Unfiltered area query plus a contradiction sweep (3 PARTIALs: u03, q03, q12).** Replace the `title match` / `quote match` filters with "fetch every rule in the area, then every rule with a `contradictionId` shared by any retrieved rule", and add to the prompt: "Before ruling, list each retrieved rule you are not using and say why." u03 would then see C3 and its resolution; q03 would carry the 90-day window and access-continues rules; q12 would keep the privacy policy duty.
3. **Send the situation block (2 PARTIALs: q01, q04).** In `run_eval.py` append `situation` to the user text (e.g. "Context: servers 150, users 4000, verified false, as of 2026-09-19") and in the prompt say "If the user has given the numbers the rule depends on, rule; do not ask for them again." Both hedges become definite rulings.

Also worth doing (data): set `effectiveFrom` on docs-derived rules to the docs page's real date or the change-log date rather than the crawl date, so answers stop saying a rule took effect on the day of the query.

## Three to screenshot

- **q09** (retry_after seconds vs ms): the cleanest trap. Docs, v8 changelog and the wrong support article are all quoted, C5 is named, the authority reasoning (80 vs 60, plus the 65 / 64.57 example) is shown, and the counsel line is a real consequence. No dashes.
- **q08** (transferring a verified team): shows the effectiveTo mechanic working, the superseded Under 16 article is named with its date range, and the answer has the whole process (ticket, dual consent, 30 days, re-verify). No dashes, no exclamation marks.
- **u01** (unverified bot at 100 servers): the honesty shot. It says "genuinely unresolved", quotes both sides, names C4, applies the dataset's resolution instead of picking a winner, and tells the developer to get it in writing. No dashes.
