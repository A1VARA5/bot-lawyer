# Bot Lawyer: 25 realistic developer questions with structured answers

Style of the questions: what actually gets asked in the Discord Developers server `#api-help`, Stack Overflow `[discord.js]`/`[discord.py]`, and discord-api-docs issues. Every answer has the branching variable(s), the answer per branch, the source URL, and the effective date where one exists. "As of" = 2026-09-19.

Legend for the branching variables: **users** = unique server-installed users (Discord's June 2026 metric); **servers** = guild count; **verified** = App Verification (Stripe ID + checklist); **region** = team owner's country.

---

### 1. "My bot is in 150 servers. Do I need to apply for the Message Content intent?"
Depends on: users (not servers), date.
- Before June 10, 2026: yes, 100+ servers required application (and verification).
- On or after June 10, 2026: server count is irrelevant. Under 10,000 users: toggle it on in Developer Portal > Bot > Privileged Gateway Intents. At or above 10,000 users: you get a portal alert + email/DM, and have 90 days to apply; access continues meanwhile.
Source: https://support-dev.discord.com/hc/en-us/articles/40281523410967 ; https://docs.discord.com/developers/events/gateway#privileged-intents (change log entry June 10, 2026).
Trap: https://docs.discord.com/developers/resources/application flags table still says "100 or more servers" (see CONTRADICTIONS C1).

### 2. "How do I see how many users my app has, so I know if I'm near 10,000?"
Depends on: nothing, it's just not shown.
- Discord: "We don't display your app's user count in the Developer Portal." You get notified when you cross it. The portal shows a *server bot install count* under Privileged Gateway Intents (added late 2025), which is a different metric.
Source: https://support-dev.discord.com/hc/en-us/articles/40281523410967 (Common Questions) ; https://github.com/discord/discord-api-docs/issues/7806 (staff comment 2025-10-16).

### 3. "I already got Message Content approved in 2023. Do I need to do anything?"
Depends on: whether access came from a prior review.
- Yes: annual reapplication. You get a notification, then 90 days to reapply; access stays during review. Don't reapply before the notice ("please wait until you receive the notice").
Source: https://docs.discord.com/developers/gateway/getting-started-with-privileged-intent-review ("Access already granted").

### 4. "I got close code 4014 when connecting. What's wrong?"
Depends on: portal toggle state and user count.
- 4014 = "Disallowed intent(s)": the intent in your IDENTIFY bitfield is not enabled in the portal (or, over 10k users, not granted). Fix the toggle, or apply. 4013 is a different error (invalid bitfield).
Source: https://docs.discord.com/developers/topics/opcodes-and-status-codes#gateway-gateway-close-event-codes ; https://docs.discord.com/developers/events/gateway#gateway-restrictions.

### 5. "Can my bot read message content without the intent if the user replies to it?"
Depends on: which page you read (CONTRADICTIONS C8).
- Always exempt (all sources): messages the app sends, DMs to the app, messages that @mention the app.
- Also exempt per the "You Might Not Need" guide: replies to a regular bot message when the user has "ping on reply" enabled; not replies to slash-command responses.
- Also exempt per the gateway page: the target message of a message context-menu command.
Source: https://docs.discord.com/developers/gateway/you-might-not-need-a-privileged-intent ; https://docs.discord.com/developers/events/gateway#message-content-intent.

### 6. "Do I need to be verified to go past 100 servers?"
Depends on: date and what you want.
- Verification is required for: Discovery/App Directory, Premium Apps monetization. Since June 10, 2026 it is not coupled to intents, and "apps can continue joining servers" during intent review.
- The support article "How Do I Get My App Verified?" (content from 2024) still says "Verification is required for your app to scale past 100 servers." No current page confirms or retracts a hard cap for unverified apps.
Answer to give: "Officially undetermined; the only page claiming a 100-server cap predates the June 2026 change. Ask Discord dev support and cite both." (CONTRADICTIONS C4)
Sources: https://support-dev.discord.com/hc/en-us/articles/23926564536471 ; https://support-dev.discord.com/hc/en-us/articles/40281523410967 ; https://docs.discord.com/developers/discovery/enabling-discovery.

### 7. "I'm 15. Can I verify my bot?"
Depends on: age of the team owner who submits ID.
- Under 16: not on your own ID. A 16+ team owner (parent, guardian, co-dev) with a Stripe-qualifying ID verifies; they must own the team; you stay a member. Minimum age to *operate* a bot is Discord's minimum age for your country (13 in most places).
- 16+: verify yourself via Stripe Identity.
Source: https://support-dev.discord.com/hc/en-us/articles/6276106082583 ; https://support-dev.discord.com/hc/en-us/articles/6275923204375.

### 8. "Can I transfer my verified bot's team to someone else?"
Depends on: verified or not.
- Unverified app, individual to team: self-serve "Transfer App to Team" in General Information.
- Verified app or team owning verified apps: support ticket, dual consent within 30 days, verification is removed and identity data deleted, new owner re-verifies.
- Note the older Under-16 article says "ownership can't be transferred after verification is complete" (CONTRADICTIONS C7); the 2025 process supersedes it.
Source: https://support-dev.discord.com/hc/en-us/articles/34905402845591.

### 9. "I got a 429 with retry_after 2.5. Is that seconds or ms?"
Depends on: API version.
- v8+ (all supported versions, v10 current): seconds, float. `Retry-After` header is integer seconds. The support article's "Milliseconds" is wrong (CONTRADICTIONS C5).
Source: https://docs.discord.com/developers/topics/rate-limits#exceeding-a-rate-limit.

### 10. "What's the global rate limit and do slash command responses count?"
- 50 requests/second per bot (per IP if unauthenticated). Interaction endpoints (respond, followup, edit original) are exempt from the global limit, ephemeral or not; per-route and shared limits still apply. Invalid requests (401/403/429 except shared-scope 429) over 10,000 per 10 minutes = temporary Cloudflare ban.
Source: https://docs.discord.com/developers/topics/rate-limits#global-rate-limit ; #invalid-request-limit-aka-cloudflare-bans.

### 11. "When must I shard?"
- Each shard supports max 2,500 guilds; at 2,500+ guilds sharding is mandatory. Recommended ~1 shard per 1,000 guilds. Over 150,000 guilds Discord migrates you to large bot sharding (session start limit becomes max(2000, guild_count/1000*5)/day). IDENTIFY limit: 1,000 per 24h across all shards.
Source: https://docs.discord.com/developers/events/gateway#sharding ; #sharding-for-large-bots ; https://support-dev.discord.com/hc/en-us/articles/6223003921559.

### 12. "Can I store user IDs and message content in my database?"
Depends on: purpose, and whether your app went through App Review.
- Allowed only "as necessary to provide your Application's stated (and approved through App Review, as applicable) functionality" (Developer Policy 15). Must be described in your privacy policy (Dev ToS 5a), encrypted at rest (5c), deleted promptly when no longer necessary / on user request / when you shut down (5b). No fixed retention window exists in any Discord document. Message content may not be used to train ML/AI models without Discord's express permission (Policy 21).
Source: https://support-dev.discord.com/hc/en-us/articles/8563934450327 (effective July 8, 2024) ; https://support-dev.discord.com/hc/en-us/articles/8562894815383 (effective July 8, 2024).

### 13. "Do I need a privacy policy for a bot in one private server?"
- The Developer ToS applies to every Application with an Application ID, regardless of size: "You will provide and adhere to a privacy policy for your Application ... You will maintain publicly available, up-to-date links to your privacy policy in the Developer Portal". Enforcement risk scales with reach, but the obligation does not.
Source: https://support-dev.discord.com/hc/en-us/articles/8562894815383 Section 5(a).

### 14. "Can I use message content from my bot to fine-tune an LLM?"
- No, unless Discord grants express permission. Policy 21 (added in the July 8, 2024 version; absent from the Oct 1, 2022 version).
Source: https://support-dev.discord.com/hc/en-us/articles/8563934450327 vs https://support-dev.discord.com/hc/en-us/articles/25280499088279.

### 15. "Can I DM users a welcome message when they join?"
- Only with explicit permission: Policy 5 "Do not contact users on Discord without their explicit permission", and Policy 6 bans marketing. A server owner enabling a welcome-DM feature is not the user's permission; keep DMs tied to app functionality the user triggered.
Source: https://support-dev.discord.com/hc/en-us/articles/8563934450327.

### 16. "My bot sells premium via Patreon. Am I forced to use Discord's Premium Apps?"
Depends on: region and date.
- Since October 7, 2024, in regions where Premium Apps exists (US, UK, EU), any paid feature must also be purchasable through Premium Apps, at a price no higher than elsewhere. Outside those regions the rule does not bite yet.
Source: https://support-dev.discord.com/hc/en-us/articles/8563934450327 ("Monetization Requirements") ; https://support-dev.discord.com/hc/en-us/articles/17709085688727.

### 17. "I'm in Canada / India / Brazil. Can I enable Premium Apps?"
- No. Supported: United States, United Kingdom, all 27 EU member states. "Premium Apps is not currently available outside of these regions."
Source: https://docs.discord.com/developers/monetization/enabling-monetization ; https://support-dev.discord.com/hc/en-us/articles/17297949965079 (Supported Locales).

### 18. "What are the exact eligibility requirements for monetization?"
- Verified app; owned by a team; team owner 18+; team emails verified + 2FA; app uses slash commands or "has been approved for" Message Content (ambiguous under 10k users, CONTRADICTIONS C10); ToS link; privacy policy link; no harmful language in name/description/commands; payouts set up; agree to Monetization Terms (effective June 6, 2024) and Developer Policy. Max 50 SKUs per app.
Source: https://docs.discord.com/developers/monetization/enabling-monetization ; https://support-dev.discord.com/hc/en-us/articles/17708927296663.

### 19. "When do I get paid?"
- Eligible after the first $100 earned net of processing/transaction fees; then cycles of $25+; paid within 45 days after month end; balance under $25 rolls over. (Docs say "$100" without the net qualifier, CONTRADICTIONS C9.)
Source: https://support-dev.discord.com/hc/en-us/articles/17299902720919.

### 20. "How do I get into the App Directory?"
- Verify app (Stripe ID by team owner + checklist) > Developer Portal > Discovery > Discovery Status checklist > Discovery Settings metadata > enable; up to 24h to appear. Must be appropriate for 13+, no graphic/sexual content, obey Dev Policy/ToS, IP-clean.
Source: https://docs.discord.com/developers/discovery/enabling-discovery ; https://support-dev.discord.com/hc/en-us/articles/8852009977879.

### 21. "Is the 'Verified Bot' badge the same as 'verified app'?"
- Same thing under two names. API: user flag `1 << 16 VERIFIED_BOT` ("Verified Bot"), `1 << 17 VERIFIED_DEVELOPER` ("Early Verified Bot Developer", a legacy badge). Help center and docs now say "App Verification". The Active Developer Badge is a third, unrelated thing and has been decommissioned.
Source: https://docs.discord.com/developers/resources/user#user-object-user-flags ; https://support-dev.discord.com/hc/en-us/articles/10113997751447.

### 22. "How many slash commands can I register, and how fast?"
- 100 global CHAT_INPUT commands, 15 global USER commands, 15 global MESSAGE commands, 1 PRIMARY_ENTRY_POINT; the same counts per guild for guild commands; 200 command creates per day per guild; 8,000 chars combined per command. Global commands need `applications.commands` scope (included in `bot` scope).
Source: https://docs.discord.com/developers/interactions/application-commands#registering-a-command ; https://docs.discord.com/developers/topics/oauth2#shared-resources-oauth2-scopes.

### 23. "Can I run a 'self-bot' or automate my user account for a private tool?"
- No. Community Guidelines rule 14 "Do not use self-bots or user-bots" (effective Sept 29, 2025); support article "Automated User Accounts (Self-Bots)". Only bot accounts (Application with a bot user) may automate.
Source: https://discord.com/guidelines ; https://support.discord.com/hc/en-us/articles/115002192352.

### 24. "What data does my bot get from a server with zero privileged intents?"
- Baseline: usernames/avatars/banners/nicknames (the article also lists "discriminators", which no longer exist), member roles, message metadata (time sent), voice channel joins and voice state metadata, reactions, members' locale. Content fields are empty without Message Content (exceptions in Q5). Member join/leave events need GUILD_MEMBERS; presence needs GUILD_PRESENCES.
Source: https://support.discord.com/hc/en-us/articles/7933951485975 ; https://docs.discord.com/developers/events/gateway#list-of-intents.

### 25. "Which version of the Developer Policy applies to me and when did it change?"
Depends on: date.
- Current: Developer Policy and Developer ToS, effective July 8, 2024 (last updated June 6, 2024). Arbitration opt-out: within 30 days of July 8, 2024 or of creating your first Application.
- Oct 1, 2022 to July 7, 2024: 2022 versions (effective Oct 1, 2022).
- July 1, 2020 to Sept 30, 2022: 2020 versions.
- Before: 2017 Developer ToS.
- Discord ToS/Privacy/Guidelines: effective Sept 29, 2025.
Source: https://support-dev.discord.com/hc/en-us/articles/8563934450327 ; .../8562894815383 ; .../25280499088279 ; .../25280523748759 ; .../25279999805975 ; .../25280483153687 ; .../25280443568791 ; https://discord.com/terms.

---

### Extra questions with no determinable answer (good "the agent should say it doesn't know" tests)
- "Does an unverified bot still stop at 100 servers?" (Q6: no current source.)
- "What exactly was in the Message Content Intent FAQ about storing content?" (article 4404772028055 deleted, Wayback not reachable from this environment.)
- "What is the exact date the 10,000-user rule started?" (announcement page is undated; change log says June 10, 2026; article metadata says created May 6, 2026.)
