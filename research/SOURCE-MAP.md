# Bot Lawyer: source map

Research date: 2026-09-19. Raw copies live in `raw/` (see "Raw files" at the bottom). robots.txt copies: `raw/robots-*.txt`.

## Hosts

| Host | What it is | robots.txt (fetched 2026-09-19) | Practical crawlability | Size |
|---|---|---|---|---|
| `docs.discord.com/developers/...` | Canonical developer docs (Mintlify). `discord.com/developers/docs/*` 301-redirects here. | `User-agent: *`, `Content-Signal: ai-train=yes, search=yes, ai-input=yes`, only `/cdn-cgi/` and `/_next/` disallowed. Sitemap: `https://docs.discord.com/sitemap.xml` | Excellent. Every page serves clean markdown at `<url>.md`. Index at `https://docs.discord.com/llms.txt` (180 entries, 169 unique URLs). Plain `curl` works. | 169 pages. Change log alone is 301 KB. |
| `support-dev.discord.com/hc/en-us` | Developer Help Center (Zendesk). Hosts the Developer Policy, Developer ToS, intents FAQs, verification, monetization, App Directory articles. | Zendesk default: `/hc/*/articles` allowed; `/hc/*/search`, `/hc/requests` etc. disallowed. Sitemap `/hc/sitemap.xml`. | HTML is behind Cloudflare JS challenge (curl and `scrapling extract get` return 403). Two working routes: (a) Zendesk JSON API, no auth: `https://support-dev.discord.com/api/v2/help_center/en-us/articles.json?per_page=100` and `/articles/{id}.json` (body is HTML, convert with markdownify); (b) `scrapling extract fetch` (headless browser) follows redirects fine. | 53 articles total, ~35 relevant to bots. |
| `support.discord.com/hc/en-us` | User Help Center (Zendesk). Legal add-ons (Monetization Terms, Monetization Policy, DPA, Data Security Terms), "Visibility of Bot Data Access", self-bot rules. | Same as above. | Same as above (API works). | 512 articles, ~20 relevant. |
| `discord.com/terms`, `/privacy`, `/guidelines` | Terms of Service, Privacy Policy, Community Guidelines (Webflow). | `Allow: /terms`, `Allow: /privacy` explicitly; `/developers` not disallowed. | `scrapling extract get` works (200). Pages include nav chrome; strip everything before "Effective:". | 3 pages, 25-73 KB each. All three: "Effective: September 29, 2025 / Last Updated: August 29, 2025". |
| `github.com/discord/discord-api-docs` | Source of the docs (MDX under `developers/`), change log MDX, issue tracker. | For `ClaudeBot`/`anthropic-ai`: `Crawl-delay: 1`, `Disallow: /*/tree/`, `/*/raw/`, `/*/blame/`, `/*/*/issues/search`. Issues pages are crawlable; use the REST API instead. | REST API unauthenticated works (60 req/h). `raw.githubusercontent.com` works. | 673 files. 300 open issues. Last push 2026-09-18T22:52Z. Policy MDX files are 126-146 byte stubs that redirect to support-dev. |
| `discord.com/blog` | Company blog. Developer announcements from 2022 were here; slug `message-content-privileged-intent-for-verified-bots` now returns the generic blog index (200), so the 2022 post is gone. | RSS at `https://discord.com/blog/rss.xml`. | Low value for this project. | RSS 78 KB, no intent-related posts in current feed. |
| `gist.github.com/msciotti/223272a6f976ce4fda22d271c23d72d9` | 2020 "Gateway Intents and Presence Data" announcement by Discord PM Mason Sciotti (the origin of the 100-guild rule). | n/a | `raw` URL works with curl. | 1 page. |
| `web.archive.org` | Needed for the deleted 2022 Message Content FAQ (4404772028055) and Review Policy (5324827539479). | n/a | Rate-limited (429) from this machine; WebFetch blocked. Not obtained. | - |

## Page-level map: developer docs (docs.discord.com)

| Topic | Canonical URL | Notes / last-updated evidence |
|---|---|---|
| Gateway (intents, privileged intents, sharding) | https://docs.discord.com/developers/events/gateway | 53 KB. Updated for 10,000-user rule (June 2026) but info box still says "After your app is verified, you can apply for the intent". |
| Gateway events | https://docs.discord.com/developers/events/gateway-events | 137 KB |
| Privileged intent review guide | https://docs.discord.com/developers/gateway/getting-started-with-privileged-intent-review | "As of June 10th, 2026" |
| You Might Not Need a Privileged Intent | https://docs.discord.com/developers/gateway/you-might-not-need-a-privileged-intent | New June 2026 |
| Rate limits | https://docs.discord.com/developers/topics/rate-limits | 50 req/s global; 10,000 invalid/10 min; `retry_after` seconds |
| OAuth2 | https://docs.discord.com/developers/topics/oauth2 | 42 KB |
| Permissions | https://docs.discord.com/developers/topics/permissions | 2FA-required permissions footnote |
| Application resource (flags table) | https://docs.discord.com/developers/resources/application | Flags table still says "100 or more servers" |
| User resource (VERIFIED_BOT flag) | https://docs.discord.com/developers/resources/user | `1 << 16 VERIFIED_BOT`, `1 << 17 VERIFIED_DEVELOPER "Early Verified Bot Developer"` |
| Message resource | https://docs.discord.com/developers/resources/message | 25 MiB request cap |
| Webhook resource / Webhooks platform page / Webhook events | https://docs.discord.com/developers/resources/webhook , /platform/webhooks , /events/webhook-events | |
| Interactions overview / receiving & responding / application commands | https://docs.discord.com/developers/interactions/overview , /interactions/receiving-and-responding , /interactions/application-commands | |
| Reference (API versions, uploading files, snowflakes) | https://docs.discord.com/developers/reference | Upload limit changed to 20 MiB on 2026-09-05 |
| Opcodes and status codes | https://docs.discord.com/developers/topics/opcodes-and-status-codes | 4014 Disallowed intents |
| Change log | https://docs.discord.com/developers/change-log | Dated `<Update label="...">` blocks, 2016 to June 10, 2026. Best "effective date" source on the site. |
| Discovery / App Directory | https://docs.discord.com/developers/discovery/overview , /discovery/enabling-discovery , /discovery/best-practices , /platform/discovery | Verification required for Discovery |
| Monetization / Premium Apps | https://docs.discord.com/developers/monetization/overview , /enabling-monetization , /managing-skus , /implementing-app-subscriptions , /implementing-one-time-purchases , /platform/app-monetization | Eligibility checklist, US/UK/EU only |
| Developer Policy (docs slot) | https://docs.discord.com/developers/policies/developer-policy | 307 -> support-dev 8563934450327 |
| Developer ToS (docs slot) | https://docs.discord.com/developers/policies/developer-terms-of-service | 307 -> support-dev 8562894815383 |
| Bots overview / intro / getting started | https://docs.discord.com/developers/bots/overview , /intro , /quick-start/getting-started | |

## Page-level map: legal and policy

| Document | Canonical URL | Effective / last updated | Notes |
|---|---|---|---|
| Discord Developer Policy (current) | https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy | Effective July 8, 2024; Last updated June 6, 2024 | 21 numbered rules; Oct 7, 2024 price-parity rule; rule 21 bans training ML on message content |
| Discord Developer Terms of Service (current) | https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service | Effective July 8, 2024; Last updated June 6, 2024 | Section 5 (privacy, retention, security), Section 6 (App Review), Section 11 (EEA/UK SCCs) |
| 2022 Developer Policy | https://support-dev.discord.com/hc/en-us/articles/25280499088279-2022-Discord-Developer-Policy | Effective Oct 1, 2022; Last updated Sept 1, 2022 | |
| 2022 Developer ToS | https://support-dev.discord.com/hc/en-us/articles/25280523748759-2022-Discord-Developer-Terms-of-Service | Effective Oct 1, 2022 | |
| 2020 Developer Policy | https://support-dev.discord.com/hc/en-us/articles/25279999805975-2020-Discord-Developer-Policy | Last updated July 1, 2020 | bullet-style rules ("retain data any longer than necessary") |
| 2020 Developer ToS | https://support-dev.discord.com/hc/en-us/articles/25280483153687-2020-Discord-Developer-Terms-of-Service | | |
| 2017 Developer ToS | https://support-dev.discord.com/hc/en-us/articles/25280443568791-2017-Discord-Developer-Terms-of-Service | | |
| Discord Terms of Service | https://discord.com/terms | Effective Sept 29, 2025; Last updated Aug 29, 2025 | "Third-party services" clause |
| Privacy Policy | https://discord.com/privacy | Effective Sept 29, 2025; Last updated Aug 29, 2025 | "Services offered by third parties" section names Developer ToS/Policy; "We also require that certain popular apps apply for access to certain data" |
| Community Guidelines | https://discord.com/guidelines | Effective Sept 29, 2025; Last updated Aug 29, 2025 | Rule 13 spam tools, Rule 14 self-bots |
| Monetization Terms | https://support.discord.com/hc/en-us/articles/5330075836311-Monetization-Terms | Effective June 6, 2024 | |
| Monetization Policy | https://support.discord.com/hc/en-us/articles/10575066024983-Monetization-Policy | | linked as "Server Monetization Policy" from Dev Policy |
| Data Processing Agreement (Discord as Processor) | https://support.discord.com/hc/en-us/articles/37891902561687-Data-Processing-Agreement-Discord-as-a-Processor | Effective Jan 22, 2026 | For advertising partners, NOT for bot developers. Developer-side DPA equivalent is Section 11 of the Developer ToS (SCCs). No public bot-developer DPA exists. |
| Data Security Terms | https://support.discord.com/hc/en-us/articles/37894290456087-Data-Security-Terms | | advertising partners |
| Additional Terms and Policies (index) | https://support.discord.com/hc/en-us/articles/4420312247575-Additional-Terms-and-Policies | | |
| Discord Social SDK Terms | https://support-dev.discord.com/hc/en-us/articles/30225844245271-Discord-Social-SDK-Terms | | |
| Events API Terms | https://support.discord.com/hc/en-us/articles/41618861207959-Events-API-Terms | | |

## Page-level map: help center articles about bots (support-dev unless noted)

| Article | URL | updated_at (API) | content edited_at |
|---|---|---|---|
| Changes to Privileged Intent Access for Discord Apps | https://support-dev.discord.com/hc/en-us/articles/40281523410967 | 2026-09-16 | 2026-06-11 (created 2026-05-06) |
| What are Privileged Intents? | https://support-dev.discord.com/hc/en-us/articles/6207308062871 | 2026-09-07 | 2026-06-10 |
| How do I get Privileged Intents for my bot? | https://support-dev.discord.com/hc/en-us/articles/6205754771351 | 2026-09-19 | |
| How Do I Get My App Verified? | https://support-dev.discord.com/hc/en-us/articles/23926564536471 | 2026-09-19 | 2024-08-30 (still says "scale past 100 servers") |
| An Update on Verifications for Users Under 16 | https://support-dev.discord.com/hc/en-us/articles/6276106082583 | 2026-09-11 | |
| Bot Verification FAQ for Parents, Legal Guardians, and Other Sponsors | https://support-dev.discord.com/hc/en-us/articles/6275923204375 | 2026-09-18 | |
| Stripe Identity Verification FAQ | https://support-dev.discord.com/hc/en-us/articles/6226051178775 | 2026-09-17 | |
| How to Transfer Ownership of a Developer Team | https://support-dev.discord.com/hc/en-us/articles/34905402845591 | 2026-09-16 | 2026-07-27 |
| Creating and Managing a Developer Team | https://support-dev.discord.com/hc/en-us/articles/34905563063703 | 2026-09-12 | |
| My Bot is Being Rate Limited! | https://support-dev.discord.com/hc/en-us/articles/6223003921559 | 2026-09-17 | 2025-07-14 |
| Why can't I copy my bot's token? | https://support-dev.discord.com/hc/en-us/articles/6470840524311 | 2026-09-15 | |
| How Do I Change My Bot's Name? | https://support-dev.discord.com/hc/en-us/articles/6129090215959 | 2026-09-15 | |
| Where can I find my Application/Team/Server ID? | https://support-dev.discord.com/hc/en-us/articles/360028717192 | 2026-09-19 | |
| App Directory Intro | https://support-dev.discord.com/hc/en-us/articles/9506257727255 | 2026-06-17 | |
| App Directory Inclusion Guidelines | https://support-dev.discord.com/hc/en-us/articles/8852009977879 | 2026-09-05 | |
| App Directory: App profile pages | https://support-dev.discord.com/hc/en-us/articles/6378525413143 | 2026-09-16 | |
| App Discovery: Content Requirements Policy | https://support-dev.discord.com/hc/en-us/articles/9489299950487 | 2026-09-09 | |
| What Are Premium Apps? | https://support-dev.discord.com/hc/en-us/articles/17709085688727 | 2026-08-11 | |
| How Do I Monetize My App? | https://support-dev.discord.com/hc/en-us/articles/17297949965079 | 2026-09-17 | |
| Premium Apps Onboarding | https://support-dev.discord.com/hc/en-us/articles/17708927296663 | 2026-07-11 | 2024-12-12 |
| Premium Apps Payout | https://support-dev.discord.com/hc/en-us/articles/17299902720919 | 2026-06-11 | |
| Premium Apps SKU and Store Setup | https://support-dev.discord.com/hc/en-us/articles/17298449675927 | 2026-03-06 | |
| Premium Apps' Required Support for Monetizing Apps | https://support-dev.discord.com/hc/en-us/articles/23810643331735 | 2026-08-29 | |
| Active Developer Badge (decommissioned) | https://support-dev.discord.com/hc/en-us/articles/10113997751447 | 2026-09-19 | |
| Updating Apps to Support Unique Usernames | https://support-dev.discord.com/hc/en-us/articles/13667755828631 | 2026-09-13 | |
| Upcoming Discord Age Assurance Changes | https://support-dev.discord.com/hc/en-us/articles/38338398970263 | 2026-09-16 | |
| Visibility of Bot Data Access (support.discord.com) | https://support.discord.com/hc/en-us/articles/7933951485975 | 2026-09-18 | 2024-05-31 |
| Automated User Accounts (Self-Bots) (support.discord.com) | https://support.discord.com/hc/en-us/articles/115002192352 | 2026-09-19 | |
| Scam/Phishing Bots (support.discord.com) | https://support.discord.com/hc/en-us/articles/360037660611 | 2026-09-19 | |
| About Discord Link Previews and the Discordbot (support.discord.com) | https://support.discord.com/hc/en-us/articles/42500550752919 | 2026-09-19 | |

Deleted / redirected articles that are still linked from live docs:
- 4404772028055 "Message Content Privileged Intent FAQ" -> 301 to 6207308062871 (linked from application flags table and the 2022 change log).
- 5324827539479 "Message Content Intent Review Policy" -> redirects to the intent review guide (linked from the gateway page info box).
- 8561391080471 (2022 grace-period article) -> gone (linked from the Sept 1, 2022 change log entry).

## GitHub issues worth indexing (discord/discord-api-docs)

| # | Title | State | Why it matters |
|---|---|---|---|
| 7806 | Inconsistent Server Count Behavior When Requesting Privileged Intents Approval | closed 2025-10-16 | Portal strings "75 servers" / "100 servers"; staff admits two different install-count metrics |
| 8572 | API rejects file uploads >10 MiB despite support article stating a 20 MiB limit | closed 2026-09-05 | Docs/support/API disagreed for 4 days; "Support articles reflect functionality for users, not bots" |
| 7680 | Inconsistent ratelimit implementation between routes | open | |
| 8082 | Thread endpoints behaviour goes against documented ratelimit behaviour | closed | |
| 8570 | GET /gateway/bot returns HTTP 429 with ~23h Retry-After | closed | |
| 7483 | What does unique requirements mean in the Message Privileged Intents? | closed | intent form wording |
| 6191 | Unverified bots are able to apply for privileged intents | closed | pre-2026 behaviour |
| 2134 | Can't enable Privileged Intents on private bots with fewer than 100 guilds | closed | 2021, 20 comments |
| Discussion 5412 | Message Content is Now a Privileged Intent (shaydewael, 2022-09-01) | | the 2022 announcement text |

## Raw files

- `raw/devdocs/*.md` - 39 developer-doc pages (markdown straight from Mintlify).
- `raw/support-dev/*.md` - all 53 developer help center articles (via Zendesk API, header block with created/updated/edited timestamps).
- `raw/support/*.md` - 14 user help center articles.
- `raw/legal/discord-{terms,privacy,guidelines}.md` - scraped with scrapling.
- `raw/github/*.mdx`, `raw/github/issue-*.md`, `raw/github/issues-*.json` - repo sources, issues with comments, search results.
- `raw/blog/2020-gist-msciotti-privileged-intents.md` - 2020 announcement.
- `raw/docs-discord-llms.txt`, `raw/docs-discord-all-urls.txt`, `raw/support-dev-articles.tsv`, `raw/support-articles.tsv` - indexes.
- `raw/zd.py` - the Zendesk fetch helper (`python zd.py list <host> out.tsv`, `python zd.py fetch <host> <outdir> <id...>`).
