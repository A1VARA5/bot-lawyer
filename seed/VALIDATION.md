# Seed validation: seed/seed.ndjson

Generated 2026-09-19 by `seed/build_seed.py`, checked by `seed/validate_seed.py`, imported with `npx sanity dataset import ../seed/seed.ndjson production --replace` from `studio/`.

## Counts

| Type | Count |
|---|---|
| policyArea | 10 |
| source | 47 |
| rule | 100 |
| question | 28 (17 standard, 8 trap, 3 unknown) |
| total documents | 185 |

Rules by area: intents 24, dataRetention 21, rateLimits 18, monetisation 9, verification 7, ageRequirements 7, tokensAndSecurity 5, ownership 4, appDirectory 3, oauth 2.

Rules with `effectiveTo` (superseded or obsolete): 16. Rules with `supersedes`: 11. Rules with `conflictsWith`: 26. Confidence: 55 confirmed, 45 inferred.

Sources by kind: developerDocs 15, developerSupport 15, developerTerms 4, developerPolicy 3, userSupport 2, github 2, changelog 1, terms 1, privacy 1, guidelines 1, monetizationTerms 1, announcement 1. Authority per kind: legal 100, developer policy and terms 90, developer docs 80, announcement 70, developer support 60, change log 50, user support 40, github 30.

Three sources are cited in CONTRADICTIONS.md but not quoted by any rule (kept for the agent to cite as redirect targets and checklist mirrors): `source.what-are-privileged-intents`, `source.what-are-premium-apps`, `source.premium-onboarding`.

## Contradiction coverage (both sides as separate rules, conflictsWith in both directions)

| ID | Rules |
|---|---|
| C1 | rule.intent-threshold-10k-users, rule.intent-threshold-announcement-2026 vs rule.flags-table-100-servers |
| C2 | rule.intent-under-10k-toggle, rule.verification-intent-review-separate vs rule.message-content-needs-verification-approval, rule.gateway-stale-100-guilds-bullet |
| C3 | rule.intent-change-date-changelog, rule.intent-change-date-guide vs rule.intent-change-date-announcement-undated |
| C4 | rule.verification-required-past-100-servers vs rule.growth-not-blocked-during-review, rule.verification-unlocks-discovery-monetisation |
| C5 | rule.retry-after-seconds vs rule.retry-after-milliseconds-support (plus rule.retry-after-v8-changelog as evidence) |
| C6 | rule.interaction-endpoints-exempt-global vs rule.ephemeral-not-counted-support |
| C7 | rule.ownership-transfer-process vs rule.ownership-cannot-transfer-after-verification |
| C8 | rule.message-content-exceptions-gateway, rule.message-content-exceptions-guide, rule.message-content-exceptions-changelog-2022 (all three pairwise) |
| C9 | rule.payout-threshold-100-docs vs rule.payout-threshold-100-net-support |
| C10 | rule.monetisation-requires-slash-or-approved-mc vs rule.intents-under-10k-no-approval-support |

Supersedes chain examples: rule.intent-threshold-10k-users supersedes rule.intent-threshold-100-servers (2020-10-27 to 2026-06-09); rule.message-content-privileged-2022 supersedes rule.message-content-announced-feb-2022; retention 2024 > 2022 > 2020 policy > 2017 terms; Developer Terms versions 2024 > 2022 > 2020 > 2017; rule.upload-limit-20mib supersedes rule.upload-limit-10mib-2025; rule.ownership-transfer-process supersedes rule.ownership-cannot-transfer-after-verification.

## Structural checks (validate_seed.py)

- Duplicate `_id`: none.
- Dangling `_ref`: none (area, source, supersedes, conflictsWith, expectedRules all resolve inside the file). Confirmed after import with GROQ: `count(*[_type=="rule" && !defined(source->_id)])` = 0.
- `_key` on every object array item (references): yes, unique per array. Arrays of plain strings (`appliesWhen.intents`, `situation.intents`) carry no `_key`, which is correct for Sanity primitive arrays.
- List values match the schema: source.kind, rule.confidence, appliesWhen.intents, verificationState, ownerAge, question.kind.
- All dates are `YYYY-MM-DD`; no `effectiveTo` earlier than `effectiveFrom`.
- Every rule with a `contradictionId` has both `conflictsWith` and `resolution`; every conflict is symmetric.
- No em dash or en dash in title, plainAnswer, resolution, notes, description, text, expectedAnswer, note.

## Quote verification

All 100 rule quotes were searched in the `snapshotFile` of their source under `research/raw`:

- 82 found byte for byte.
- 18 found after markdown normalisation only (raw has `\_` escapes in tables, `[text](url)` links, `<url>` angle brackets, or table padding whitespace; the quote carries the rendered text). These are: flags-table-100-servers, intent-change-date-changelog, message-content-exceptions-gateway, intent-4014-disallowed, verification-intent-review-separate, verification-unlocks-discovery-monetisation, verified-bot-flag, third-party-services-must-follow-dev-terms, interaction-endpoints-exempt-global, retry-after-seconds, upload-limit-20mib, support-articles-users-not-bots, monetisation-eligibility-checklist, payout-threshold-100-docs, age-min-operate-bot, token-reset-2fa, applications-commands-scope, 2fa-elevated-permissions.
- 0 missing. No rule was dropped for lack of a verbatim quote.

### grep spot check (15 quotes, `grep -c -F` against the raw file, first line of multi line quotes)

| Rule | Raw file | Matches |
|---|---|---|
| rule.intent-threshold-10k-users | devdocs/events_gateway.md | 1 |
| rule.intent-under-10k-toggle | devdocs/events_gateway.md | 1 |
| rule.message-content-needs-verification-approval | devdocs/events_gateway.md | 1 |
| rule.intent-threshold-announcement-2026 | support-dev/Changes-to-Privileged-Intent-Access-for-Discord-Apps-40281523410967.md | 1 |
| rule.verification-required-past-100-servers | support-dev/How-Do-I-Get-My-App-Verified-23926564536471.md | 1 |
| rule.retry-after-milliseconds-support | support-dev/My-Bot-is-Being-Rate-Limited-6223003921559.md | 1 |
| rule.ephemeral-not-counted-support | support-dev/My-Bot-is-Being-Rate-Limited-6223003921559.md | 1 |
| rule.ownership-cannot-transfer-after-verification | support-dev/An-Update-on-Verifications-for-Users-Under-16-6276106082583.md | 1 |
| rule.ownership-transfer-process | support-dev/How-to-Transfer-Ownership-of-a-Developer-Team-34905402845591.md | 1 |
| rule.payout-threshold-100-net-support | support-dev/Premium-Apps-Payout-17299902720919.md | 1 |
| rule.ml-training-ban | support-dev/Discord-Developer-Policy-8563934450327.md | 1 |
| rule.self-bots-banned-guidelines | legal/discord-guidelines.md | 1 |
| rule.retention-2020-policy | support-dev/2020-Discord-Developer-Policy-25279999805975.md | 1 |
| rule.message-content-privileged-2022 | devdocs/change-log.md | 1 |
| rule.upload-limit-changelog-2026 | devdocs/change-log.md | 1 |

15 of 15 matched.

## Dating decisions worth knowing

- June 10, 2026 (change log label) is used as `effectiveFrom` for every rule that came with the intent change, including quotes taken from the undated support-dev announcement (created 2026-05-06, edited 2026-06-11).
- The pre June 2026 100 server rules are dated `effectiveFrom` 2020-10-27 (change log "Gateway v6 Intent Restrictions") and `effectiveTo` 2026-06-09, confidence inferred.
- Stale text still live on pages (flags table, gateway info box, gateway bullet, "scale past 100 servers", "ownership can't be transferred") is dated from the change it describes and given an `effectiveTo` of the day before the change that made it obsolete, with confidence inferred, so the agent can say "this page is out of date" rather than "this rule applies".
- Upload limit: the change log labels the 20 MiB increase September 3, 2026, while GitHub issue 8572 (which the brief dates 2026-09-05) was last updated 2026-09-05. Rules use 2026-09-03 and the source note records both dates.
- 21 rules quote developer docs pages that print no date and have no edit metadata in the research (rate limits, sharding, command quotas, monetisation checklist, discovery, scopes, token handling). These carry `effectiveFrom` = 2026-09-19 (the snapshot date) with confidence inferred. If the agent filters rules by an earlier "as of" date these will not match; to fix, backdate them from the discord-api-docs git history.
- Support article rules use the Zendesk `edited_at` date as `effectiveFrom` with confidence inferred, as instructed.

## Import result

```
✔ [100%] Reading/validating data file (29ms)
✔ [100%] Importing documents (939ms)
✔ [100%] Strengthening references (558ms)
Done! Imported 185 documents to dataset "production"
```

Post import GROQ: rules 100, sources 47, questions 28, areas 10, rules with contradictionId C1: 3, rules with a dangling source reference: 0.

## Update 2026-09-19: formatting and limits area

Added by `seed/build_seed.py` (same script, new section) and validated by `seed/validate_seed.py`: 1 policyArea (`area.formatting`, order 11), 11 sources, 36 rules, 8 questions (all standard, two of them draft requests: q32 welcome message, q33 channel names). Totals now 11 policyArea, 58 source, 136 rule, 36 question = 241 documents. The 185 existing documents are byte identical to the previous build (checked by diffing ids and lines).

The script also writes `seed/seed-formatting.ndjson` with only the 56 new documents, imported with `npx sanity dataset import ../seed/seed-formatting.ndjson production` (no `--replace`) so nothing already in production is touched.

Quotes: 36 of 36 found in `research/raw` (28 byte for byte, 8 after markdown normalisation: spoiler-code-block, message-2000-chars, message-4000-nitro, embed-field-limits, category-50-channels-docs, caps-categories-50 carry stripped link targets or collapsed table padding). Six rules quote `devdocs/reference.md` through the existing `source.reference` (mentions, allowed_mentions, custom emoji, timestamps, timestamp styles, slash command mentions) and two quote `source.opcodes` (error 30013 and 30030); the other 28 quote the new snapshots under `research/raw/formatting/`.

Dating: support articles print no date, so their rules use the Zendesk `edited_at` date with confidence inferred (Markdown 101: 2025-04-23; Spoiler Tags: 2022-01-30; Sending Messages: 2024-04-08; caps table: 2026-03-02). Developer docs pages are undated, so those rules carry the snapshot date 2026-09-19, inferred, like the 21 earlier docs rules. Slash command mentions are dated 2022-08-22 from the change log entry of that week. The lowercase and no spaces rule for text channel names is stated by no Discord page; it quotes GitHub issue 1646 (2020-05-18) and is marked inferred so the agent says so. The three community convention rules quote two emojidb.org catalogue pages modelled as kind `github` with authority 20 (lowest in the dataset) and say "community convention, not a Discord rule" in their titles and answers.

New contradiction C11 (category limit 50 on the support caps table against 5 in docs error code 30030) recorded in `research/CONTRADICTIONS.md` with both sides as rules, symmetric conflictsWith and a resolution.
