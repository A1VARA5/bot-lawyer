# VERDICT: does Discord bot compliance carry a "the answer depends on your situation and the date" agent?

Research date: 2026-09-19. Evidence: `CONTRADICTIONS.md` (10 items), `SOURCE-MAP.md`, `questions.md`, raw pages in `raw/`.

## Short answer

**Yes, and it is better than expected, for one specific reason: Discord changed the single most important rule (privileged intent threshold) on June 10, 2026 and only half of its own pages were updated.** That gives you, today, live and verbatim:

- a reference table on docs.discord.com that says "100 or more servers" (C1),
- a paragraph 25 lines below the new rule on the same gateway page that still says "after your app is verified, you can apply for the intent" (C2),
- an announcement that says "starting today" with no date on it, while the change log says June 10 and the article metadata says May 6 (C3),
- a 2024 support article still telling developers "Verification is required for your app to scale past 100 servers" next to a 2026 announcement saying growth is no longer blocked (C4),
- and two independent, non-intent contradictions that are pure numbers: `retry_after` seconds vs milliseconds (C5) and interaction endpoints vs ephemeral messages (C6).

Plus C7 (ownership transfer "can't" vs documented process), C8 (three different exception lists for message content), C9 ($100 gross vs net), C10 ("approved" state that no longer exists under 10k users).

Five of these (C1, C2, C4, C5, C7) are hard contradictions where two live official pages give incompatible instructions. The others are ambiguities or scope mismatches. All quotes are verbatim and re-fetchable.

## Why this domain works for the demo

1. **Structure is real, not invented.** The answer to "do I need to apply for Message Content?" genuinely branches on: date (before/after June 10, 2026), user count (10,000), whether access came from a prior review (annual reapply), and for monetization on region (US/UK/EU) and age (16 to verify, 18 to monetize). That is exactly the "depends on your situation" shape.
2. **Effective dates exist and are clean.** Developer Policy/ToS: July 8, 2024 (prior: Oct 1, 2022; July 1, 2020; 2017). Discord ToS/Privacy/Guidelines: Sept 29, 2025. Monetization Terms: June 6, 2024. Price-parity rule: Oct 7, 2024. Intent change: June 10, 2026. Message content intent: Sept 1, 2022 (announced Feb 14, 2022 as "Aug 31"). Presence/members intents: Oct 2020 (gist). The agent can show a timeline per rule.
3. **Sources are crawlable with zero drama.** docs.discord.com serves `.md` for every page and publishes `llms.txt` with `Content-Signal: ai-train=yes`. Both Zendesk help centers expose an unauthenticated JSON API with `created_at`/`updated_at`/`edited_at` per article, which is a gift: the agent can say "this page's content was last edited 2024-08-30, before the June 2026 change" as evidence for why it distrusts it. Legal pages on discord.com are explicitly allowed in robots.txt.
4. **The audience asks these exact questions.** The GitHub issues (#7806, #2134, #6191, #7483, #8572) and the 2022 discussion thread are developers being confused by precisely these thresholds, in public, with Discord staff replying. Real user stories for the pitch.
5. **There is a "Discord's own staff admits it" moment.** Issue #7806: "there's a discrepancy between the install count reported on the General Information page vs the install count used for privileged intents." And #8572: "Support articles reflect functionality for users, not bots."

## Weak spots to be honest about

- **The contradictions cluster around one event.** C1 to C4 and C10 are all fallout from June 10, 2026. If Discord fixes the flags table and the gateway info box (both are one-line PRs to discord-api-docs), the demo's strongest live examples vanish. Mitigation: snapshot everything now (done, in `raw/`), and pin the agent's corpus to dated snapshots so the demo doesn't depend on Discord staying sloppy. The pitch line becomes "this is what the docs said on 2026-09-19; here is the diff since."
- **No numeric retention rule.** Developers often ask "how long can I keep messages?"; the honest answer is "no number anywhere, only 'no longer than necessary'". That is a fine answer for a lawyer-agent, but it is not a contradiction.
- **The best historical artefact is gone.** The 2022 "Message Content Privileged Intent FAQ" (with the 75-server wording) was deleted and now redirects; Wayback was rate-limited from this machine. Worth one manual retry from a browser to capture it for the timeline.
- **Legal-doc contradictions are thin.** Developer Policy vs Developer ToS vs Privacy Policy are consistent with each other (they cross-reference). The real inconsistencies are docs vs help center vs portal strings, not policy vs policy. Frame the agent as "Discord's docs, help center and policies disagree", not "Discord's policies contradict each other".
- **Verification still gating growth is unknowable.** C4 ends in "ask support". Good for a demo of epistemic honesty, bad if a judge wants a crisp answer.

## Recommendation

Go with Discord. Build the corpus from the three crawlable sources (docs `.md`, Zendesk API for both help centers, discord.com legal pages) with per-page `fetched_at` and `edited_at`, and make the agent cite `edited_at` when two pages disagree. Lead the demo with C1 + C5 (numbers, unambiguous, verbatim, both live today), use C3/C4 to show the "depends on the date" behaviour, and C7/C8 as the "here is the union of what Discord says" behaviour.

## If you need the fallback anyway

Streaming platform music/monetisation rules (Kick, Twitch, YouTube, Suno) would also carry the agent, but with a different risk profile:

- Twitch: Music Guidelines, Community Guidelines, Affiliate/Partner agreements, Soundtrack deprecation (2023), DJ Program (2024, revenue-share on music). Dated, versioned, contradictions between "Music Guidelines" and the "DJ Program" FAQ about which music is allowed are real and well known.
- YouTube: Content ID vs Partner Program vs "Licensed music" rules; contradictions are mostly between YouTube's Help Center and the Audio Library terms. Crawlable but Google Help Center is JS-heavy.
- Kick: Terms, Community Guidelines, Creator Program; the docs are thin and change often; fewer sources to contradict each other.
- Suno: Terms of Service (commercial use depends on Pro/Premier tier and on the date you generated), plus the 2024/2025 label lawsuits and settlements changed the terms. Strong "depends on the date and your plan" shape.

That domain has more legal exposure (copyright) and less clean structure (four companies, four crawling regimes, no `llms.txt`). It is broader but shallower; Discord is narrower and deeper, and has one authoritative change log with dated entries which the streaming platforms lack. Only switch if the hackathon brief rewards breadth of platforms over depth of citation.
