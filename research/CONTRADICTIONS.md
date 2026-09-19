# Bot Lawyer: real contradictions and ambiguities between Discord's own sources

Research date: 2026-09-19. All quotes are verbatim from pages fetched on that date (raw copies in `raw/`). Zendesk article `updated_at` values come from the Help Center API; `edited_at` is the last content edit.

Big context you must know first: on **June 10, 2026** Discord replaced the "100 servers" privileged-intent threshold with a "10,000 users" threshold and decoupled App Verification from intent review (support-dev article 40281523410967, change log entry "June 10, 2026"). Roughly half of the contradictions below are fallout from that change landing in some pages and not others.

---

## C1. Privileged intent threshold: "100 servers" vs "10,000 users" (same docs site, live today)

**Developer question:** "My bot is in 120 servers. Do I need to apply for the Message Content / Guild Members / Presence intent?"

**Source A** - Application Resource, application flags table
URL: https://docs.discord.com/developers/resources/application#application-object-application-flags
> `1 << 12` | GATEWAY_PRESENCE | Intent required for bots in **100 or more servers** to receive `presence_update` events
> `1 << 13` | GATEWAY_PRESENCE_LIMITED | Intent required for bots in under 100 servers to receive `presence_update` events, found on the **Bot** page in your app's settings
> `1 << 14` | GATEWAY_GUILD_MEMBERS | Intent required for bots in **100 or more servers** to receive member-related events like `guild_member_add`.
> `1 << 18` | GATEWAY_MESSAGE_CONTENT | Intent required for bots in **100 or more servers** to receive message content
> `1 << 19` | GATEWAY_MESSAGE_CONTENT_LIMITED | Intent required for bots in under 100 servers to receive message content, found on the **Bot** page in your app's settings

**Source B** - Gateway, "Privileged Intent Access Review"
URL: https://docs.discord.com/developers/events/gateway#privileged-intents
> Apps with fewer than 10,000 users can access privileged intents by enabling them in the Developer Portal.
> When an app has more than 10,000 unique users who can see your app across all the servers it's in, it requires review for continued access to Privileged Intents.

**Source C** - "Changes to Privileged Intent Access for Discord Apps" (support-dev, created 2026-05-06, edited 2026-06-11)
URL: https://support-dev.discord.com/hc/en-us/articles/40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps
> Previously, apps in fewer than 100 servers could access Privileged Intents by toggling them on in the Developer Portal, and apps in 100+ servers needed to apply for access.
> Starting today, the threshold is based on the number of users your app can access across all the servers it belongs to.

**What differs:** the unit of the threshold (servers vs users) and the number (100 vs 10,000). The flags table is the machine-readable reference that libraries (discord.js, discord.py) mirror in their enum docs, and it still encodes the pre-June-2026 rule. Bonus: the "message content" link in the flags table points to article 4404772028055 ("Message Content Privileged Intent FAQ"), which now 301-redirects to "What are Privileged Intents?" (6207308062871), a page that says 10,000 users. So the link contradicts the row it sits in.

**Correct answer today:** server count is irrelevant; the trigger is 10,000 unique server-installed users, and Discord does not show you that number ("We don't display your app's user count in the Developer Portal", article 40281523410967).

---

## C2. Same page, two rules: does Message Content need "approval after verification" or just a toggle?

**Developer question:** "My bot is unverified, in 30 servers, 2,000 users. Do I need approval for the Message Content intent or can I just turn it on?"

**Source A** - Gateway, "Privileged Intent Access Review" (top of section)
URL: https://docs.discord.com/developers/events/gateway#privileged-intents
> Apps with fewer than 10,000 users can access privileged intents by enabling them in the Developer Portal.

**Source B** - Gateway, "Message Content Intent" info box (same page, ~25 lines lower)
URL: https://docs.discord.com/developers/events/gateway#message-content-intent
> Like other privileged intents, `MESSAGE_CONTENT` must be approved for your app. After your app is verified, you can apply for the intent from your app's settings within the Developer Portal. You can read more about the message content intent review policy in the Help Center.

and, same page, "Gateway Restrictions" / "HTTP Restrictions":
> If you pass a privileged intent in the `intents` parameter without configuring it in your app's settings, or being approved for it during verification, your Gateway connection will be closed with a (`4014` close code).
> ...your app must enable the `GUILD_MEMBERS` intent (and be approved for it if eligible for verification).

**Source C** - June 2026 announcement
URL: https://support-dev.discord.com/hc/en-us/articles/40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps
> 4. App Verification and Privileged Intent review are now separate. Previously, App Verification and Privileged Intent review were part of the same review process. With this change, we have separated App Verification and the Privileged Intent review process.

**What differs:** whether approval is tied to verification at all. Source B says "after your app is verified, you can apply"; Source C says verification and intent review are now unrelated; Source A says under 10k users no approval exists. The "review policy" link in Source B (article 5324827539479, "Message Content Intent Review Policy") now redirects to the generic "Getting Started with Privileged Intent Review" guide, so the specific policy it references no longer exists as a document.

**Correct answer today:** under 10,000 users, toggle it on, no approval, verification irrelevant. Over 10,000, apply within 90 days of the notification; verification still irrelevant.

---

## C3. What is the effective date of the intent change? "Today" with no date on the page

**Developer question:** "When exactly did the 10,000-user rule start? I need the date for my privacy policy / compliance log."

**Source A** - the announcement itself (support-dev)
URL: https://support-dev.discord.com/hc/en-us/articles/40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps
> **Today, we're announcing changes to how Discord Apps access Privileged Intents**
> Starting today, the threshold is based on the number of users your app can access...

The rendered page carries no date. The Zendesk API metadata reads `created_at: 2026-05-06T19:20:18Z`, `edited_at: 2026-06-11T00:17:07Z`, `updated_at: 2026-09-16T08:07:19Z`.

**Source B** - Developer docs guide
URL: https://docs.discord.com/developers/gateway/getting-started-with-privileged-intent-review#whats-changed
> As of June 10th, 2026, we've made some changes to the Privileged Intents review process.

**Source C** - Change log entry
URL: https://docs.discord.com/developers/change-log
> label="June 10, 2026" ... Today, we're announcing changes to how Discord Apps access Privileged Intent

**What differs:** the only page that says "starting today" has no date on it; its own metadata says it was created 2026-05-06 and edited 2026-06-11; the docs say June 10; the Zendesk "updated" timestamp is 2026-09-16 (Zendesk bumps `updated_at` on any metadata change, not content). Three candidate dates for one rule. For the agent, the defensible answer is June 10, 2026 (change log), with the caveat that the primary source is undated.

---

## C4. The 100-server cap, the "75 servers" error and whether verification still gates growth

**Developer question:** "My unverified bot is at 97 servers. Will it stop being able to join servers at 100? Do I need to verify?"

**Source A** - "How Do I Get My App Verified?" (support-dev, content last edited 2024-08-30, still live and listed as updated 2026-09-19)
URL: https://support-dev.discord.com/hc/en-us/articles/23926564536471-How-Do-I-Get-My-App-Verified
> Verification is required for your app to scale past 100 servers.

**Source B** - June 2026 announcement
URL: https://support-dev.discord.com/hc/en-us/articles/40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps
> Previously, when an app hit 100 servers and was required to apply for continued access to its Privileged Intents, it was blocked from joining new servers until the review was complete. That's no longer the case.
> Guild installs are also not blocked while you are in review.

**Source C** - Enabling Discovery (docs) gives verification a different purpose entirely
URL: https://docs.discord.com/developers/discovery/enabling-discovery
> To enable **Discovery** for your app, we require your team owner to complete identity and application verification. **App Verification** also allows you to add monetization features to your app

**Source D** - Developer Portal strings quoted in GitHub issue #7806 (2025-09-04, closed by Discord staff 2025-10-16)
URL: https://github.com/discord/discord-api-docs/issues/7806
> "This application is not currently in the minimum number of servers required for intent verification, please try again once in 75 servers."
> "You may continue to use Privileged Intents until your app joins 100 servers."
> "Your app is temporarily approved for Intents and has been limited to joining 100 servers."

Discord staff reply in the same issue:
> there's a discrepancy between the install count reported on the General Information page vs the install count used for privileged intents. The install count reported in General Information is the most expansive version of the metric... For privileged intents we care about the subset of guild installs that can actually use those privileged intents.

**Source E** - Change log, February 14, 2022 vs September 1, 2022
URL: https://docs.discord.com/developers/change-log
> `MESSAGE_CONTENT` is becoming a privileged intent for verified bots in 75+ servers **on August 31, 2022**.
> (Sept 1, 2022 entry) As of today, message content is a privileged intent for all verified apps *and* apps eligible for verification.

**What differs:** (1) whether a hard 100-server cap for unverified bots still exists: Source A says yes, Source B says growth is no longer blocked, Source C describes verification purely as a Discovery/monetization prerequisite. No live page states a current unverified-bot server cap. (2) 75 vs 100: 75 was the point at which verification/intent application *opened* (portal error, Feb 2022 changelog), 100 was where it became *required*; developers routinely conflate the two and Discord's own pages use both numbers without ever defining the pair. (3) two different "server count" metrics were used by the same portal (staff admission).

**Correct answer today:** verification is required for Discovery (App Directory) and Premium Apps; it is no longer coupled to intents or growth. Whether an unverified app is still capped at 100 servers is not stated anywhere current; the only page that says so was written in 2024. Treat as "unresolved, ask Discord support".

---

## C5. `retry_after`: seconds or milliseconds?

**Developer question:** "I got a 429 with `retry_after: 64.57`. How long do I sleep?"

**Source A** - Rate Limits (developer docs), rate limit response structure
URL: https://docs.discord.com/developers/topics/rate-limits#exceeding-a-rate-limit
> | retry_after | float | The number of seconds to wait before submitting another request. |
> ...
> < Retry-After: 65
> ...
> "retry_after": 64.57,

**Source B** - "My Bot is Being Rate Limited!" (support-dev, edited 2025-07-14)
URL: https://support-dev.discord.com/hc/en-us/articles/6223003921559-My-Bot-is-Being-Rate-Limited
> `retry_after`: Milliseconds to wait before making another request

**What differs:** unit, by a factor of 1000. A developer following the support article sleeps 64 ms and immediately re-hits the limit, which counts toward the 10,000-invalid-requests-per-10-minutes Cloudflare ban (documented on both pages). Historical cause: before API v8 the field was in milliseconds; v8+ (2020) switched to seconds. The support article kept the old unit.

**Correct answer today:** seconds (float) for API v8, v9, v10. The `Retry-After` header is integer seconds.

---

## C6. Do interaction responses count against rate limits? "Ephemeral doesn't count" vs "interaction endpoints are exempt from the global limit"

**Developer question:** "If I answer slash commands with ephemeral messages, does that save me rate limit budget?"

**Source A** - support-dev rate limit article
URL: https://support-dev.discord.com/hc/en-us/articles/6223003921559-My-Bot-is-Being-Rate-Limited
> Bonus tip: Make Interaction Responses and follow-up messages ephemeral since they do not count towards the rate limits.

**Source B** - developer docs
URL: https://docs.discord.com/developers/topics/rate-limits#global-rate-limit
> All bots can make up to 50 requests per second to our API.
> Interaction endpoints are not bound to the bot's Global Rate Limit.

**What differs:** scope and condition. Docs: *all* interaction endpoints (ephemeral or not) are exempt from the *global* limit only; per-route and shared limits still apply. Support: only *ephemeral* responses, and "the rate limits" (unqualified). Following the support article leads to wrong architecture decisions (making everything ephemeral to "save" budget, or assuming non-ephemeral interaction replies are globally limited).

---

## C7. Can a verified app's team ownership be transferred?

**Developer question:** "My parent verified my bot as team owner when I was 15. I'm 18 now. Can I take ownership?"

**Source A** - "An Update on Verifications for Users Under 16" (support-dev, live, updated 2026-09-11)
URL: https://support-dev.discord.com/hc/en-us/articles/6276106082583-An-Update-on-Verifications-for-Users-Under-16
> That person will need to be the owner of the team, and ownership can't be transferred after verification is complete.
> When your bot is verified, your parent's account will need to stay on the team going forward, and they'll need to retain ownership of the team and bot.

**Source B** - "How to Transfer Ownership of a Developer Team" (support-dev, created 2025-09-12, edited 2026-07-27)
URL: https://support-dev.discord.com/hc/en-us/articles/34905402845591-How-to-Transfer-Ownership-of-a-Developer-Team
> If your developer team owns verified applications, transferring ownership will require **removing verification** from those applications. The new owner will need to reapply for verification after the transfer is complete.
> Both parties have **30 days to respond** to our requests.

**What differs:** "can't be transferred" (absolute) vs a documented process with a 30-day dual-consent window and verification reset. Source A was never updated when Source B was published a year later.

**Correct answer today:** yes, via support ticket, dual consent within 30 days, verification is stripped and the new owner (16+ with Stripe-qualifying ID) must re-verify.

---

## C8. Which messages does an app see without the Message Content intent? Three official lists, three different sets

**Developer question:** "Without the intent, can my bot read replies to its own messages? What about message context-menu commands?"

**Source A** - Gateway page
URL: https://docs.discord.com/developers/events/gateway#message-content-intent
> Apps **without** the intent will receive empty values in fields that contain user-inputted content with a few exceptions:
> * Content in messages that an app sends
> * Content in DMs with the app
> * Content in which the app is mentioned
> * Content of the message a message context menu command is used on

**Source B** - "You Might Not Need a Privileged Intent" guide
URL: https://docs.discord.com/developers/gateway/you-might-not-need-a-privileged-intent
> The Message Content intent is **not** needed for your app to access message content in these situations:
> * **Messages your app sends**
> * **Direct Messages sent to your app**
> * **Messages that @mention your app**
> * **Replies to your app's messages.** Note: this applies to replies sent using Discord's reply feature to a regular bot message (not an interaction response) and the user has "ping on reply" enabled. It does not apply to replies to slash command responses.

**Source C** - Change log, September 1, 2022
URL: https://docs.discord.com/developers/change-log
> These restrictions do not apply for messages that a bot or app sends, in DMs that it receives, or in messages in which it is mentioned.

**What differs:** Source A includes context-menu targets and omits replies; Source B includes replies (with a ping-on-reply condition) and omits context-menu targets; Source C has only three. The union is probably the truth (a reply with ping-on-reply is technically a mention), but no single page gives it and the ping-on-reply condition appears in exactly one place.

---

## C9. Monetization payout threshold: gross or net of fees?

**Developer question:** "I've sold $100 of subscriptions. Am I eligible for payout?"

**Source A** - Enabling Monetization (docs)
URL: https://docs.discord.com/developers/monetization/enabling-monetization#step-3-set-up-team-payouts
> Once your app has made its first $100 it will become eligible for payout.

**Source B** - Premium Apps Payout (support-dev, updated 2026-06-11)
URL: https://support-dev.discord.com/hc/en-us/articles/17299902720919-Premium-Apps-Payout
> your team will become eligible for payout review after the first 100 dollars is earned [less applicable payment processing fees and transaction fees].
> An eligible payout can be defined as the first $100 earned [less applicable payment processing fees and transaction fees] and for the following billing cycles, in amounts greater than $25.

**What differs:** docs say $100 made; support says $100 net of processing and transaction fees, then a $25 minimum per cycle and a 45-day payout window that the docs never mention. Minor in money, but exactly the kind of "depends which page you read" that the agent should surface.

---

## C10. Monetization eligibility still says "approved for the Message Content intent"

**Developer question:** "My bot uses prefix commands with Message Content toggled on (under 10k users, so never 'approved'). Can I enable Premium Apps?"

**Source A** - Enabling Monetization checklist (docs) and Premium Apps Onboarding (support-dev)
URL: https://docs.discord.com/developers/monetization/enabling-monetization#step-2-complete-the-eligibility-checklist
> App uses slash commands, or has been approved for the privileged `Message Content` intent

**Source B** - "How do I get Privileged Intents for my bot?" (support-dev)
URL: https://support-dev.discord.com/hc/en-us/articles/6205754771351-How-do-I-get-Privileged-Intents-for-my-bot
> Note that apps with fewer than 10,000 users can use Privileged Intents without needing to apply; just turn them on from the bot's page on the Developer Portal.

**What differs:** "approved" is a state that, after June 10, 2026, only exists for apps over 10,000 users. A sub-10k prefix-command bot has the intent but has never been "approved", so its monetization eligibility is undefined by the text. Ambiguity, not a hard contradiction.

---

## C11. Category limit: "50" (support caps table) vs "5" (docs error code 30030)

Added 2026-09-19 with the formatting and limits area.

**Developer question:** "How many categories can my bot create in a server before it errors?"

**Source A** - Discord Account Caps, Server Caps, and More (support.discord.com, created 2025-07-24, edited 2026-03-02)
URL: https://support.discord.com/hc/en-us/articles/33694251638295-Discord-Account-Caps-Server-Caps-and-More
> | Server categories | 50 | Same | Same | Same |
> | Channels (includes voice/text/categories) | 500 | Same | Same | Same |
> | Max number of channels in one category | 50 | Same | Same | Same |

**Source B** - Opcodes and Status Codes, JSON error codes (docs)
URL: https://docs.discord.com/developers/topics/opcodes-and-status-codes#json-json-error-codes
> | 30013 | Maximum number of guild channels reached (500) |
> | 30030 | Maximum number of server categories has been reached (5) |

**What differs:** the category maximum, 50 against 5. The docs line is a bare error string with no context; the 5 most likely refers to something other than channel categories, but Discord does not say so anywhere. The 500 channel total and the 50 channels per category agree across the docs (channel object: "each parent category can contain up to 50 channels") and the caps table.

**Correct answer today:** plan for 50 channel categories and 500 channels in total, cite both, and expect 30030 as the error if a category create is refused. Rules: rule.caps-categories-50 vs rule.error-30030-categories-5.

---

## Suspected contradictions that turned out consistent (or resolved)

- **File upload limit 10 MiB vs 20 MiB** (GitHub issue #8572, 2026-09-01): docs said 10 MiB, support article said 20 MiB, API enforced 10 MiB. Resolved on 2026-09-05; docs now read "The default limit is `20 MiB` for all users". Good example of 4-day drift, not a live contradiction. Staff comment worth keeping: "Support articles reflect functionality for users, not bots."
- **Message content retention period**: no source gives a number. Developer ToS 5(b) (effective July 8, 2024): "promptly delete the API Data when: (a) retaining it is no longer necessary for your Application's stated (and approved through App Review, as applicable) functionality". 2020 Developer Policy: "retain data any longer than necessary for the operation of your application". Intent review guide: "If you're storing the data, explain why it's necessary and describe your retention policy". Consistent: storage allowed if justified, no fixed window. The old Message Content FAQ (4404772028055) that may have had specific retention wording is gone (redirected).
- **Storing user IDs**: allowed under Developer Policy 15 ("necessary to provide your Application's stated functionality"); Developer ToS 5(a) requires a privacy policy describing it; no page forbids it. Consistent.
- **Sharding threshold**: docs "apps that are in 2500+ guilds *must* enable sharding" and support "sharding **must** be enabled at 2,500+ guilds". Consistent.
- **Invalid request limit**: 10,000 per 10 minutes on both docs and support. Consistent.
- **Premium Apps regions**: US, UK, EU on docs, "What Are Premium Apps" and "How Do I Monetize My App" (which lists all 27 EU states). Consistent.
- **October 7, 2024 price-parity rule**: Developer Policy and "What Are Premium Apps" agree.
- **Token reset / 2FA**: support article says 2FA code "if requested"; docs say token viewable once. Consistent.
- **Verification age**: ID holder must be 16+ (Under-16 article), monetization team owner must be 18+, platform minimum 13. Different thresholds for different features, consistent.
- **"Monetization Policy" vs "Server Monetization Policy"**: Developer Policy links article 10575066024983 as "Monetization Policy" with slug `Server-Monetization-Policy`; the article title is "Monetization Policy". Naming only.
- **Policy version dates**: Developer Policy and Developer ToS both "Effective date: July 8, 2024, Last updated: June 6, 2024"; 2022 versions "Effective: October 1, 2022"; 2020 Policy "Last updated: July 1, 2020"; 2017 ToS archived. Consistent, and a clean date-versioned chain the agent can use.
- **Stale but not contradictory**: "Visibility of Bot Data Access" (support.discord.com, edited 2024-05-31) still lists "discriminators" as baseline data bots receive; discriminators were removed in 2023 (article 13667755828631). "Bot Verification FAQ for Parents" still says invite "by typing the relevant username and four-digit discriminator".
