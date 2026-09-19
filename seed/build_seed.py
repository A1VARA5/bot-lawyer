# Builds seed/seed.ndjson for the Bot Lawyer Sanity dataset.
# Every quote is verbatim from research/raw (validate_seed.py checks this).
# Run: python seed/build_seed.py  (from bot-lawyer/)
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "seed.ndjson")
SNAPSHOT = "2026-09-19"

docs = []


def ref(_id):
    return {"_type": "reference", "_ref": _id}


def refs(ids):
    return [{"_type": "reference", "_ref": i, "_key": i.replace(".", "-")} for i in ids]


# ---------------------------------------------------------------- policy areas
AREAS = [
    ("area.intents", "Intents", "intents", 1,
     "Privileged gateway intents (Message Content, Guild Members, Presence): who must apply, at what user or server count, what happens during review, annual reapplication, close code 4014, what content you get without the intent."),
    ("area.verification", "Verification", "verification", 2,
     "App Verification: what it requires (team owner identity through Stripe), what it unlocks (Discovery, monetisation), how it used to gate intents and growth, the Verified Bot badge."),
    ("area.dataRetention", "Data handling and policy versions", "data-retention", 3,
     "How long you may keep API data, storing user IDs and message content, privacy policy duties, encryption, training AI on message content, unsolicited DMs, and which Developer Policy or Terms version applies on a given date."),
    ("area.rateLimits", "Rate limits and API limits", "rate-limits", 4,
     "Global 50 requests per second, invalid request bans, retry_after units, interaction endpoints, sharding thresholds, IDENTIFY limits, command registration quotas, upload size limits."),
    ("area.monetisation", "Monetisation (Premium Apps)", "monetisation", 5,
     "Premium Apps eligibility, supported regions, payout thresholds and timing, platform fee, SKU limits, and the October 7, 2024 price parity requirement."),
    ("area.appDirectory", "App Directory and Discovery", "app-directory", 6,
     "Getting into the App Directory: verification prerequisite, Discovery checklist, content requirements, time to appear."),
    ("area.tokensAndSecurity", "Tokens, security and account automation", "tokens-and-security", 7,
     "Bot token handling and reset, 2FA prompts, credential storage duties, self-bot and user-bot bans."),
    ("area.oauth", "OAuth2, scopes and permissions", "oauth", 8,
     "The bot and applications.commands scopes, 2FA enforcement for elevated permissions, what team applications can request."),
    ("area.ownership", "Ownership and teams", "ownership", 9,
     "Transferring apps and developer teams, dual consent windows, what happens to verification on transfer."),
    ("area.ageRequirements", "Age requirements", "age-requirements", 10,
     "13 to use Discord and the APIs, 16 to submit ID for verification, 18 to monetise, and the 2026 age assurance rollout."),
    ("area.formatting", "Formatting and limits", "formatting-and-limits", 11,
     "Discord markdown (headers, subtext, bold, italic, underline, strikethrough, spoilers, block quotes, lists, masked links, code blocks), mention, emoji and timestamp syntax, message length (2000, 4000 with Nitro), embed limits, channel name rules, channel and category counts, and the community emoji naming convention for channels."),
]
for _id, title, slug, order, desc in AREAS:
    docs.append({
        "_id": _id, "_type": "policyArea", "title": title,
        "slug": {"_type": "slug", "current": slug},
        "description": desc, "order": order,
    })

# ---------------------------------------------------------------- sources
KIND_AUTH = {
    "developerDocs": 80, "developerPolicy": 90, "developerTerms": 90, "terms": 100, "privacy": 100,
    "guidelines": 100, "monetizationTerms": 100, "developerSupport": 60, "userSupport": 40,
    "changelog": 50, "announcement": 70, "github": 30,
}


def source(_id, title, kind, url, snapshotFile, publishedAt=None, lastEditedAt=None, notes=None, authority=None):
    d = {"_id": _id, "_type": "source", "title": title, "kind": kind, "authority": authority if authority is not None else KIND_AUTH[kind],
         "url": url, "snapshotAt": SNAPSHOT, "snapshotFile": snapshotFile}
    if publishedAt:
        d["publishedAt"] = publishedAt
    if lastEditedAt:
        d["lastEditedAt"] = lastEditedAt
    if notes:
        d["notes"] = notes
    docs.append(d)


D = "https://docs.discord.com/developers/"
SD = "https://support-dev.discord.com/hc/en-us/articles/"
SU = "https://support.discord.com/hc/en-us/articles/"

# developer docs
source("source.gateway", "Gateway (developer docs)", "developerDocs", D + "events/gateway", "devdocs/events_gateway.md",
       notes="Updated for the 10,000 user rule in June 2026, but the Message Content info box still says you apply after verification, and the intents bullet still says verification is required for apps in 100+ guilds. The review policy link in the info box (article 5324827539479) redirects to the generic review guide.")
source("source.intent-review-guide", "Getting Started with Privileged Intent Review (developer docs)", "developerDocs",
       D + "gateway/getting-started-with-privileged-intent-review", "devdocs/gateway_getting-started-with-privileged-intent-review.md",
       publishedAt="2026-06-10", notes="Says 'As of June 10th, 2026'. The only developer docs page that dates the intent change.")
source("source.you-might-not-need", "You Might Not Need a Privileged Intent (developer docs)", "developerDocs",
       D + "gateway/you-might-not-need-a-privileged-intent", "devdocs/gateway_you-might-not-need-a-privileged-intent.md",
       publishedAt="2026-06-10", notes="New guide published with the June 2026 change. The only page that lists replies (with ping on reply) as a message content exception.")
source("source.rate-limits", "Rate Limits (developer docs)", "developerDocs", D + "topics/rate-limits", "devdocs/topics_rate-limits.md",
       notes="retry_after is a float in seconds. Interaction endpoints are exempt from the global limit only.")
source("source.application-resource", "Application resource (developer docs)", "developerDocs", D + "resources/application", "devdocs/resources_application.md",
       notes="The application flags table still says 'Intent required for bots in 100 or more servers' and links the message content rows to article 4404772028055, which now redirects to a page that says 10,000 users. Libraries mirror this table in their enums.")
source("source.user-resource", "User resource (developer docs)", "developerDocs", D + "resources/user", "devdocs/resources_user.md",
       notes="User flags table: 1 << 16 VERIFIED_BOT, 1 << 17 VERIFIED_DEVELOPER (Early Verified Bot Developer).")
source("source.opcodes", "Opcodes and Status Codes (developer docs)", "developerDocs", D + "topics/opcodes-and-status-codes", "devdocs/topics_opcodes-and-status-codes.md")
source("source.reference", "API Reference (developer docs)", "developerDocs", D + "reference", "devdocs/reference.md",
       notes="Uploading files section updated in September 2026 to say the default limit is 20 MiB for all users. Before that it said 10 MiB while a user support article said 20 MiB (GitHub issue 8572).")
source("source.enabling-monetization", "Enabling Monetization (developer docs)", "developerDocs", D + "monetization/enabling-monetization", "devdocs/monetization_enabling-monetization.md",
       notes="Eligibility checklist still says 'approved for the privileged Message Content intent'; that state only exists above 10,000 users since June 10, 2026. Payout sentence says $100 without the net of fees qualifier.")
source("source.managing-skus", "Managing SKUs (developer docs)", "developerDocs", D + "monetization/managing-skus", "devdocs/monetization_managing-skus.md")
source("source.enabling-discovery", "Enabling Discovery (developer docs)", "developerDocs", D + "discovery/enabling-discovery", "devdocs/discovery_enabling-discovery.md",
       notes="Describes App Verification purely as the prerequisite for Discovery and monetisation. Says nothing about server counts.")
source("source.application-commands", "Application Commands (developer docs)", "developerDocs", D + "interactions/application-commands", "devdocs/interactions_application-commands.md")
source("source.oauth2", "OAuth2 (developer docs)", "developerDocs", D + "topics/oauth2", "devdocs/topics_oauth2.md")
source("source.getting-started", "Getting Started quick start (developer docs)", "developerDocs", D + "quick-start/getting-started", "devdocs/quick-start_getting-started.md")
source("source.receiving-and-responding", "Receiving and Responding to Interactions (developer docs)", "developerDocs", D + "interactions/receiving-and-responding", "devdocs/interactions_receiving-and-responding.md")
source("source.change-log", "Change Log (developer docs)", "changelog", D + "change-log", "devdocs/change-log.md",
       lastEditedAt="2026-09-17", notes="Dated Update blocks from 2016 to September 17, 2026. The best effective date source on the site. Entries used here: September 24, 2020 (API v8, retry_after in seconds), October 27, 2020 (v6 intent restrictions), February 14, 2022 (API v10, Message Content announced for August 31, 2022), September 01, 2022 (Message Content privileged), December 16, 2024 (upload limit to 10 MiB on January 16, 2025), June 10, 2026 (intent threshold change), September 3, 2026 (upload limit to 20 MiB).")

# policy and legal
source("source.dev-policy-2024", "Discord Developer Policy (current, effective July 8, 2024)", "developerPolicy", SD + "8563934450327-Discord-Developer-Policy",
       "support-dev/Discord-Developer-Policy-8563934450327.md", publishedAt="2024-07-08", lastEditedAt="2024-08-02",
       notes="Printed: Effective date July 8, 2024, Last updated June 6, 2024. Zendesk created 2022-08-31, content edited 2024-08-02. 21 numbered rules. Rule 21 (no training ML or AI on message content) is new in this version. Monetization Requirements section carries the October 7, 2024 price parity rule. Links article 10575066024983 as 'Monetization Policy' with the slug Server-Monetization-Policy.")
source("source.dev-tos-2024", "Discord Developer Terms of Service (current, effective July 8, 2024)", "developerTerms", SD + "8562894815383-Discord-Developer-Terms-of-Service",
       "support-dev/Discord-Developer-Terms-of-Service-8562894815383.md", publishedAt="2024-07-08", lastEditedAt="2025-03-17",
       notes="Printed: Effective date July 8, 2024, Last updated June 6, 2024. Section 5 covers privacy, retention and security; Section 6 App Review; Section 11 EEA and UK transfers (SCCs); Section 12(e) arbitration opt out within 30 days of July 8, 2024 or first Application. No separate developer DPA exists; Section 11 is the equivalent.")
source("source.dev-policy-2022", "2022 Discord Developer Policy (effective October 1, 2022)", "developerPolicy", SD + "25280499088279-2022-Discord-Developer-Policy",
       "support-dev/2022-Discord-Developer-Policy-25280499088279.md", publishedAt="2022-10-01", lastEditedAt="2024-08-01",
       notes="Printed: Effective October 1, 2022, Last Updated September 1, 2022. Archived copy published to the help center on 2024-07-30. Bullet style rules; no rule about training AI models.")
source("source.dev-tos-2022", "2022 Discord Developer Terms of Service (effective October 1, 2022)", "developerTerms", SD + "25280523748759-2022-Discord-Developer-Terms-of-Service",
       "support-dev/2022-Discord-Developer-Terms-of-Service-25280523748759.md", publishedAt="2022-10-01", lastEditedAt="2024-08-01",
       notes="Archived copy published 2024-07-30. Section 5(b) retention wording is identical to the 2024 version.")
source("source.dev-policy-2020", "2020 Discord Developer Policy (last updated July 1, 2020)", "developerPolicy", SD + "25279999805975-2020-Discord-Developer-Policy",
       "support-dev/2020-Discord-Developer-Policy-25279999805975.md", publishedAt="2020-07-01", lastEditedAt="2024-07-30",
       notes="Printed: Last updated July 1, 2020. No effective date printed. Archived copy published 2024-07-30.")
source("source.dev-tos-2020", "2020 Discord Developer Terms of Service (effective August 18, 2020)", "developerTerms", SD + "25280483153687-2020-Discord-Developer-Terms-of-Service",
       "support-dev/2020-Discord-Developer-Terms-of-Service-25280483153687.md", publishedAt="2020-08-18", lastEditedAt="2024-08-01",
       notes="Archived copy published 2024-07-30.")
source("source.dev-tos-2017", "2017 Discord Developer Terms of Service (effective August 20, 2017)", "developerTerms", SD + "25280443568791-2017-Discord-Developer-Terms-of-Service",
       "support-dev/2017-Discord-Developer-Terms-of-Service-25280443568791.md", publishedAt="2017-08-20", lastEditedAt="2024-08-01",
       notes="Archived copy published 2024-07-30. The only version with a numeric deletion deadline (seven days after account termination).")
source("source.discord-terms", "Discord Terms of Service", "terms", "https://discord.com/terms", "legal/discord-terms.md",
       publishedAt="2025-09-29", lastEditedAt="2025-08-29",
       notes="Printed: Effective September 29, 2025, Last Updated August 29, 2025. 'Third-party services' clause says apps must follow the Developer Terms and Developer Policy. Scraped with nav chrome; content starts at 'Effective:'.")
source("source.discord-privacy", "Discord Privacy Policy", "privacy", "https://discord.com/privacy", "legal/discord-privacy.md",
       publishedAt="2025-09-29", lastEditedAt="2025-08-29",
       notes="Printed: Effective September 29, 2025, Last Updated August 29, 2025. Section 'Services offered by third parties' names the Developer Terms and Policy and says certain popular apps must apply for access to certain data.")
source("source.discord-guidelines", "Discord Community Guidelines", "guidelines", "https://discord.com/guidelines", "legal/discord-guidelines.md",
       publishedAt="2025-09-29", lastEditedAt="2025-08-29",
       notes="Printed: Effective September 29, 2025, Last Updated August 29, 2025. Rule 13 bans spam tools, rule 14 bans self-bots and user-bots.")
source("source.monetization-terms", "Monetization Terms", "monetizationTerms", SU + "5330075836311-Monetization-Terms", "support/Monetization-Terms-5330075836311.md",
       publishedAt="2024-06-06", lastEditedAt="2024-06-06",
       notes="Printed: Effective Date June 6, 2024, Last Updated June 6, 2024. Requires the accepting party to be at least 18.")

# developer support (support-dev.discord.com)
source("source.intent-changes-2026", "Changes to Privileged Intent Access for Discord Apps (developer support)", "developerSupport",
       SD + "40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps", "support-dev/Changes-to-Privileged-Intent-Access-for-Discord-Apps-40281523410967.md",
       publishedAt="2026-05-06", lastEditedAt="2026-06-11",
       notes="The primary announcement of the 10,000 user threshold. Says 'Today' and 'Starting today' but prints no date. Zendesk metadata: created 2026-05-06, content edited 2026-06-11, updated 2026-09-16. The change log dates the change June 10, 2026.")
source("source.what-are-privileged-intents", "What are Privileged Intents? (developer support)", "developerSupport", SD + "6207308062871-What-are-Privileged-Intents",
       "support-dev/What-are-Privileged-Intents-6207308062871.md", publishedAt="2022-05-20", lastEditedAt="2026-06-10",
       notes="The deleted 2022 Message Content Privileged Intent FAQ (4404772028055) now 301 redirects here. Updated for the 10,000 user rule.")
source("source.how-to-get-privileged-intents", "How do I get Privileged Intents for my bot? (developer support)", "developerSupport", SD + "6205754771351-How-do-I-get-Privileged-Intents-for-my-bot",
       "support-dev/How-do-I-get-Privileged-Intents-for-my-bot-6205754771351.md", publishedAt="2022-05-19", lastEditedAt="2026-06-11",
       notes="Updated for the 10,000 user rule. Says apps under 10,000 users use privileged intents without applying.")
source("source.how-to-get-verified", "How Do I Get My App Verified? (developer support)", "developerSupport", SD + "23926564536471-How-Do-I-Get-My-App-Verified",
       "support-dev/How-Do-I-Get-My-App-Verified-23926564536471.md", publishedAt="2024-06-03", lastEditedAt="2024-08-30",
       notes="Content last edited 2024-08-30, before the June 2026 change. Still says 'Verification is required for your app to scale past 100 servers.' Zendesk updated_at is 2026-09-19 but that reflects metadata, not content.")
source("source.under-16", "An Update on Verifications for Users Under 16 (developer support)", "developerSupport", SD + "6276106082583-An-Update-on-Verifications-for-Users-Under-16",
       "support-dev/An-Update-on-Verifications-for-Users-Under-16-6276106082583.md", publishedAt="2022-05-23", lastEditedAt="2024-06-13",
       notes="Says team ownership cannot be transferred after verification. Not updated when the September 2025 transfer process was published.")
source("source.transfer-ownership", "How to Transfer Ownership of a Developer Team (developer support)", "developerSupport", SD + "34905402845591-How-to-Transfer-Ownership-of-a-Developer-Team",
       "support-dev/How-to-Transfer-Ownership-of-a-Developer-Team-34905402845591.md", publishedAt="2025-09-12", lastEditedAt="2026-07-27",
       notes="Documents a support ticket process with dual consent within 30 days and removal of verification. Contradicts the older Under 16 article.")
source("source.rate-limited", "My Bot is Being Rate Limited! (developer support)", "developerSupport", SD + "6223003921559-My-Bot-is-Being-Rate-Limited",
       "support-dev/My-Bot-is-Being-Rate-Limited-6223003921559.md", publishedAt="2022-05-20", lastEditedAt="2025-07-14",
       notes="Says retry_after is milliseconds (pre API v8 wording, wrong since September 24, 2020) and that ephemeral responses do not count towards the rate limits (the docs say all interaction endpoints are exempt from the global limit only).")
source("source.token-copy", "Why can't I copy my bot's token? (developer support)", "developerSupport", SD + "6470840524311-Why-can-t-I-copy-my-bot-s-token",
       "support-dev/Why-can-t-I-copy-my-bot-s-token-6470840524311.md", publishedAt="2022-06-01", lastEditedAt="2025-05-27")
source("source.app-directory-inclusion", "App Directory Inclusion Guidelines (developer support)", "developerSupport", SD + "8852009977879-App-Directory-Inclusion-Guidelines",
       "support-dev/App-Directory-Inclusion-Guidelines-8852009977879.md", publishedAt="2022-09-13", lastEditedAt="2025-10-09")
source("source.what-are-premium-apps", "What Are Premium Apps? (developer support)", "developerSupport", SD + "17709085688727-What-Are-Premium-Apps",
       "support-dev/What-Are-Premium-Apps-17709085688727.md", publishedAt="2023-09-21", lastEditedAt="2024-12-12")
source("source.how-to-monetize", "How Do I Monetize My App? (developer support)", "developerSupport", SD + "17297949965079-How-Do-I-Monetize-My-App",
       "support-dev/How-Do-I-Monetize-My-App-17297949965079.md", publishedAt="2023-09-05", lastEditedAt="2024-12-12",
       notes="Supported Locales section lists the United States, United Kingdom and all 27 EU member states.")
source("source.premium-onboarding", "Premium Apps Onboarding (developer support)", "developerSupport", SD + "17708927296663-Premium-Apps-Onboarding",
       "support-dev/Premium-Apps-Onboarding-17708927296663.md", publishedAt="2023-09-21", lastEditedAt="2024-12-12")
source("source.premium-payout", "Premium Apps Payout (developer support)", "developerSupport", SD + "17299902720919-Premium-Apps-Payout",
       "support-dev/Premium-Apps-Payout-17299902720919.md", publishedAt="2023-09-05", lastEditedAt="2025-09-19",
       notes="More specific than the docs: $100 net of processing and transaction fees, then $25 minimum per cycle, paid within 45 days after month end.")
source("source.active-developer-badge", "Active Developer Badge (developer support)", "developerSupport", SD + "10113997751447-Active-Developer-Badge",
       "support-dev/Active-Developer-Badge-10113997751447.md", publishedAt="2022-11-09", lastEditedAt="2025-12-05", notes="Badge decommissioned.")
source("source.age-assurance-2026", "Upcoming Discord Age Assurance Changes: What You Need To Know (developer support)", "developerSupport",
       SD + "38338398970263-Upcoming-Discord-Age-Assurance-Changes-What-You-Need-To-Know", "support-dev/Upcoming-Discord-Age-Assurance-Changes-What-You-Need-To-Know-38338398970263.md",
       publishedAt="2026-02-11", lastEditedAt="2026-02-24")

# user support (support.discord.com)
source("source.visibility-bot-data", "Visibility of Bot Data Access (user support)", "userSupport", SU + "7933951485975-Visibility-of-Bot-Data-Access",
       "support/Visibility-of-Bot-Data-Access-7933951485975.md", publishedAt="2022-08-04", lastEditedAt="2024-05-31",
       notes="Written for users. Still lists discriminators in the baseline data, which were removed in 2023. Per Discord staff, support articles reflect functionality for users, not bots.")
source("source.self-bots", "Automated User Accounts (Self-Bots) (user support)", "userSupport", SU + "115002192352-Automated-User-Accounts-Self-Bots",
       "support/Automated-User-Accounts-Self-Bots-115002192352.md", publishedAt="2017-10-17", lastEditedAt="2024-04-05")

# github
source("source.gh-7806", "GitHub issue 7806: Inconsistent Server Count Behavior When Requesting Privileged Intents Approval", "github",
       "https://github.com/discord/discord-api-docs/issues/7806", "github/issue-7806.md", publishedAt="2025-09-04", lastEditedAt="2025-10-16",
       notes="Developer Portal strings quoted: 'try again once in 75 servers', 'until your app joins 100 servers'. Closed by Discord staff (HamzaAtDiscord) admitting two different install count metrics. All pre June 2026.")
source("source.gh-8572", "GitHub issue 8572: API rejects file uploads over 10 MiB despite support article stating a 20 MiB limit", "github",
       "https://github.com/discord/discord-api-docs/issues/8572", "github/issue-8572.md", publishedAt="2026-09-01", lastEditedAt="2026-09-05",
       notes="Staff statement (advaith1, 2026-09-01): 'Support articles reflect functionality for users, not bots.' Docs, user support and the API disagreed on the upload limit for four days. The change log entry raising the default to 20 MiB is labelled September 3, 2026; the issue was last updated 2026-09-05.")

# announcement
source("source.gist-2020", "Gateway Intents and Presence Data (2020 announcement gist by Mason Sciotti, Discord PM)", "announcement",
       "https://gist.github.com/msciotti/223272a6f976ce4fda22d271c23d72d9", "blog/2020-gist-msciotti-privileged-intents.md",
       notes="Origin of the 100 guild rule, originally for Presence Update events. The gist body is undated (placeholders like announcement_date); the change log entry of October 27, 2020 records the v6 intent restrictions taking effect.")

# ---------------------------------------------------------------- rules
INTENTS3 = ["MESSAGE_CONTENT", "GUILD_MEMBERS", "GUILD_PRESENCES"]


def rule(_id, title, area, plain, quote, src, anchor, frm, to=None, applies=None, conf="confirmed",
         supersedes=None, conflicts=None, resolution=None, cid=None):
    d = {"_id": _id, "_type": "rule", "title": title, "area": ref(area), "plainAnswer": plain, "quote": quote,
         "effectiveFrom": frm, "source": ref(src), "confidence": conf}
    if anchor:
        d["sourceAnchor"] = anchor
    if to:
        d["effectiveTo"] = to
    if applies:
        # arrays of primitive strings (intents) carry no _key in Sanity; only object items do
        d["appliesWhen"] = dict(applies)
    if supersedes:
        d["supersedes"] = ref(supersedes)
    if conflicts:
        d["conflictsWith"] = refs(conflicts)
    if resolution:
        d["resolution"] = resolution
    if cid:
        d["contradictionId"] = cid
    docs.append(d)


RES_C1 = ("The gateway page and the June 10, 2026 change log carry the current rule: 10,000 unique users. The application flags "
          "table on the same docs site still encodes the pre June 2026 100 server rule and was not updated. The change log is newer "
          "and explicit, so 10,000 users wins and server count is irrelevant.")
RES_C2 = ("Two paragraphs on the same gateway page disagree. The 'fewer than 10,000 users can access privileged intents by enabling "
          "them' paragraph matches the June 10, 2026 change log and the announcement that separated App Verification from intent "
          "review, so it wins. The info box and bullet that say 'after your app is verified, you can apply' are pre June 2026 text. "
          "Under 10,000 users: toggle it on, no approval, verification irrelevant. Over 10,000: apply within 90 days, verification still irrelevant.")
RES_C3 = ("We rule June 10, 2026. The change log entry is dated June 10, 2026 and the review guide says 'As of June 10th, 2026'. "
          "The announcement page says 'today' but prints no date; its Zendesk metadata says created May 6, 2026, edited June 11, 2026, "
          "updated September 16, 2026. Cite the change log and flag that the primary source is undated.")
RES_C4 = ("Unresolved. The June 10, 2026 announcement says growth is no longer blocked during intent review and that verification is a "
          "separate process, and the Discovery docs describe verification only as the prerequisite for Discovery and monetisation. But no "
          "current page retracts the 100 server cap for unverified apps either; the only page that states it was last edited "
          "2024-08-30. Our ruling: cite both, say no current source states a cap, and recommend asking developer support.")
RES_C5 = ("Seconds. The developer docs (authority 80) and the September 24, 2020 API v8 change log entry both say seconds, and the "
          "docs example pairs Retry-After: 65 with retry_after: 64.57. The support article (authority 60, edited 2025-07-14) kept the "
          "pre v8 milliseconds wording. Sleeping for milliseconds re-hits the limit and counts toward the 10,000 invalid requests per 10 minutes ban.")
RES_C6 = ("The developer docs win (authority 80 over 60) and are precise: all interaction endpoints, ephemeral or not, are exempt from "
          "the global 50 per second limit only; per route and shared limits still apply. The support article's 'ephemeral messages do "
          "not count towards the rate limits' is narrower (ephemeral only) and broader (all limits) at the same time, and wrong on both counts.")
RES_C7 = ("The transfer article (created September 12, 2025, edited July 27, 2026) documents a support ticket process: dual consent "
          "within 30 days, verification removed, identity data deleted, new owner re-verifies. It is newer and more specific, so it "
          "wins. The Under 16 article (content from 2024) was never updated and its 'can't be transferred' is obsolete.")
RES_C8 = ("Three official lists differ. We give the union: messages the app sends, DMs with the app, messages that mention the app, "
          "replies to a regular bot message when the user has ping on reply enabled (not replies to slash command responses), and the "
          "target message of a message context menu command. The reply exception appears only in the June 2026 guide and the context "
          "menu exception only on the gateway page; each page is incomplete rather than wrong.")
RES_C9 = ("The support article is more specific: the $100 is net of payment processing and transaction fees, then $25 minimum per "
          "cycle, paid within 45 days after month end. The docs sentence is a simplification of the same rule, not a different rule. "
          "Answer with the net figure and cite both.")
RES_C10 = ("Ambiguous, not a hard contradiction. The checklist's 'approved for' Message Content is a state that since June 10, 2026 "
           "exists only for apps above 10,000 users. A sub 10,000 user prefix command bot has the intent but was never approved, so the "
           "checklist text does not cover it. Use slash commands to be safe, or ask developer support before enabling Premium Apps.")

# ---- intents
rule("rule.intent-threshold-10k-users", "Privileged intents need review at 10,000 users, not at 100 servers", "area.intents",
     "The trigger is 10,000 unique users who can see your app across all its servers. Server count no longer matters: under 10,000 users you toggle the intents on, at 10,000 you must apply for continued access.",
     "When an app has more than 10,000 unique users who can see your app across all the servers it's in, it requires review for continued access to Privileged Intents. Once you hit this threshold, the app or team owner will receive a system DM and/or an email.",
     "source.gateway", "#privileged-intents (Privileged Intent Access Review)", "2026-06-10",
     applies={"minUsers": 10000, "intents": INTENTS3}, supersedes="rule.intent-threshold-100-servers",
     conflicts=["rule.flags-table-100-servers"], resolution=RES_C1, cid="C1")

rule("rule.flags-table-100-servers", "Application flags table still says intents are required at 100 or more servers", "area.intents",
     "The flags table is stale. It describes the rule that applied before June 10, 2026 and must not be used to decide whether you need to apply.",
     "GATEWAY_MESSAGE_CONTENT | Intent required for bots in **100 or more servers** to receive message content",
     "source.application-resource", "#application-object-application-flags", "2022-09-01", to="2026-06-09",
     applies={"minServers": 100, "intents": INTENTS3}, conf="inferred",
     conflicts=["rule.intent-threshold-10k-users", "rule.intent-threshold-announcement-2026"], resolution=RES_C1, cid="C1")

rule("rule.intent-threshold-announcement-2026", "Discord's announcement: the threshold is now user count, not server count", "area.intents",
     "Since the announcement, apps under 10,000 users toggle intents on in the Developer Portal and apps at 10,000 users must apply for access.",
     "Starting today, the threshold is based on the number of users your app can access across all the servers it belongs to. If your app has fewer than 10,000 users, you can continue accessing Privileged Intents by toggling them on in the Developer Portal. Once your app reaches 10,000 users, you'll need to apply for Privileged Intent access.",
     "source.intent-changes-2026", "What's Changing, item 1", "2026-06-10",
     applies={"intents": INTENTS3}, conflicts=["rule.flags-table-100-servers"], resolution=RES_C1, cid="C1")

rule("rule.intent-threshold-100-servers", "Before June 10, 2026: intents were self-serve under 100 servers and needed an application at 100+", "area.intents",
     "Until June 9, 2026 an app in fewer than 100 servers could toggle privileged intents on, and an app in 100 or more servers had to apply, a process tied to verification.",
     "Previously, apps in fewer than 100 servers could access Privileged Intents by toggling them on in the Developer Portal, and apps in 100+ servers needed to apply for access.",
     "source.intent-changes-2026", "What's Changing, item 1", "2020-10-27", to="2026-06-09",
     applies={"minServers": 100, "intents": INTENTS3}, conf="inferred")

rule("rule.presence-100-guilds-2020", "2020: presence data was unrestricted until 100 guilds, then required an application", "area.intents",
     "The original 100 guild threshold came from the 2020 Gateway Intents announcement for Presence Update events. It stopped applying on June 10, 2026.",
     "You may operate unrestricted on Discord until you join 100 guilds",
     "source.gist-2020", "Privacy", "2020-10-27", to="2026-06-09",
     applies={"minServers": 100, "intents": ["GUILD_PRESENCES"]}, conf="inferred")

rule("rule.intent-under-10k-toggle", "Under 10,000 users: just toggle the intent on, no approval and no verification", "area.intents",
     "If fewer than 10,000 unique users can see your app, enable the intent on the Bot page in the Developer Portal. There is nothing to apply for and verification is irrelevant.",
     "Apps with fewer than 10,000 users can access privileged intents by enabling them in the Developer Portal.",
     "source.gateway", "#privileged-intents (Privileged Intent Access Review)", "2026-06-10",
     applies={"maxUsers": 9999, "intents": INTENTS3},
     conflicts=["rule.message-content-needs-verification-approval", "rule.gateway-stale-100-guilds-bullet"], resolution=RES_C2, cid="C2")

rule("rule.message-content-needs-verification-approval", "Gateway info box still says Message Content is approved after verification", "area.intents",
     "This text predates June 10, 2026. Verification and intent review are now separate, and under 10,000 users there is no approval step at all.",
     "Like other privileged intents, `MESSAGE_CONTENT` must be approved for your app. After your app is verified, you can apply for the intent from your app's settings within the Developer Portal.",
     "source.gateway", "#message-content-intent (info box)", "2022-09-01", to="2026-06-09",
     applies={"intents": ["MESSAGE_CONTENT"]}, conf="inferred",
     conflicts=["rule.intent-under-10k-toggle", "rule.verification-intent-review-separate"], resolution=RES_C2, cid="C2")

rule("rule.gateway-stale-100-guilds-bullet", "Gateway intents bullet still says verification is required for apps in 100+ guilds", "area.intents",
     "Stale line from before June 10, 2026. Verification is no longer tied to intents or to guild count.",
     "For verified apps (required for apps in 100+ guilds), the intent must also be approved after the verification process to use the intent.",
     "source.gateway", "#gateway-intents (Privileged intents bullet)", "2022-09-01", to="2026-06-09",
     applies={"minServers": 100, "intents": INTENTS3}, conf="inferred",
     conflicts=["rule.intent-under-10k-toggle", "rule.verification-intent-review-separate"], resolution=RES_C2, cid="C2")

rule("rule.intent-change-date-changelog", "The intent change is dated June 10, 2026 in the change log", "area.intents",
     "Use June 10, 2026 as the effective date of the 10,000 user rule. It is the only dated official record of the change.",
     "Today, we're announcing changes to how Discord Apps access Privileged Intent with a new user-based threshold for when access requires review and an annual process to reapply for continued access.",
     "source.change-log", 'Update label="June 10, 2026"', "2026-06-10",
     conflicts=["rule.intent-change-date-announcement-undated"], resolution=RES_C3, cid="C3")

rule("rule.intent-change-date-guide", "The review guide says the changes took effect as of June 10th, 2026", "area.intents",
     "The developer guide dates the change June 10, 2026, matching the change log.",
     "As of June 10th, 2026, we've made some changes to the Privileged Intents review process.",
     "source.intent-review-guide", "#whats-changed", "2026-06-10",
     conflicts=["rule.intent-change-date-announcement-undated"], resolution=RES_C3, cid="C3")

rule("rule.intent-change-date-announcement-undated", "The announcement says 'today' but carries no date", "area.intents",
     "The page that introduced the rule is undated. Its metadata says it was created May 6, 2026 and last edited June 11, 2026, so do not cite it alone for the effective date.",
     "Today, we're announcing changes to how Discord Apps access Privileged Intents (Guild Members, Presence, and Message Content): a new user-based threshold for when access requires review, and an annual process to reapply for continued access.",
     "source.intent-changes-2026", "A Note to App Developers", "2026-06-10", conf="inferred",
     conflicts=["rule.intent-change-date-changelog", "rule.intent-change-date-guide"], resolution=RES_C3, cid="C3")

rule("rule.intent-90-day-window", "At 10,000 users you get 90 days from the notification to apply", "area.intents",
     "When you cross 10,000 users Discord notifies you by email, system DM and a Developer Portal alert. You have 90 days to submit; miss it and the intents are removed, though you can apply again at any time.",
     "You will have **90 days** from the date of the notification to submit your application. If you do not apply within this window, your app's access to Privileged Intents will be removed. You can still apply at any time to request access again.",
     "source.intent-changes-2026", "How we count users for your app", "2026-06-10",
     applies={"minUsers": 10000, "intents": INTENTS3})

rule("rule.intent-access-continues-during-review", "Your intents keep working while your application is under review", "area.intents",
     "Submitting inside the 90 day window keeps your current intent access live during the review.",
     "If you submit your request during the 90-day window, your app will retain its current intent access while your submission is under review.",
     "source.intent-changes-2026", "What's Changing, item 2", "2026-06-10",
     applies={"minUsers": 10000, "intents": INTENTS3})

rule("rule.intent-annual-reapply", "Access granted through a past review must be renewed every year", "area.intents",
     "If your intents were approved in a prior review (for example in 2023), you must reapply annually. Discord notifies you first, then you have 90 days; do not reapply before the notice arrives.",
     "If your app already has Privileged Intent access granted from a prior review, you're good for now, but you will need to reapply annually.",
     "source.intent-review-guide", "Step 1: Access already granted", "2026-06-10",
     applies={"intents": INTENTS3})

rule("rule.intent-user-count-not-shown", "Discord does not show your app's user count", "area.intents",
     "There is no user count in the Developer Portal. Discord counts unique users across all servers the app is installed in, and tells you when you cross 10,000 with a portal alert plus email or system DM. The server install count shown under Privileged Gateway Intents is a different metric.",
     "We don’t display your app’s user count in the Developer Portal. When your app grows beyond the 10,000-user threshold and triggers Privileged Intents access review, you’ll see an alert in the Developer Portal and receive a notification via email and/or system DM.",
     "source.intent-changes-2026", "Common Questions", "2026-06-10")

rule("rule.staff-two-install-metrics", "Discord staff: the portal's install count and the intents install count are different numbers", "area.intents",
     "The General Information install count is the broadest metric. The number Discord used for intents was the smaller server bot install count under Privileged Gateway Intents. Since June 2026 the real trigger is users, which is not shown at all.",
     "there's a discrepancy between the install count reported on the General Information page vs the install count used for privileged intents. The install count reported in General Information is the most expansive version of the metric, and is meant to give developers a rough idea of their total reach.",
     "source.gh-7806", "Comment by HamzaAtDiscord, 2025-10-16", "2025-10-16")

rule("rule.portal-75-servers-error", "Before June 2026 the portal opened intent applications at 75 servers and required them at 100", "area.intents",
     "The old portal strings used two numbers: 75 servers to be allowed to apply, 100 servers where approval became mandatory. Both are obsolete since June 10, 2026.",
     "This application is not currently in the minimum number of servers required for intent verification, please try again once in 75 servers.",
     "source.gh-7806", "Issue body (Developer Portal string)", "2025-09-04", to="2026-06-09",
     applies={"minServers": 75, "intents": INTENTS3}, conf="inferred")

rule("rule.message-content-privileged-2022", "Message Content became a privileged intent on September 1, 2022", "area.intents",
     "From September 1, 2022 message content fields are empty unless the intent is enabled, and verified or verification eligible apps had to be approved for it.",
     "As of today, message content is a privileged intent for all verified apps and apps eligible for verification.",
     "source.change-log", 'Update label="September 01, 2022"', "2022-09-01",
     applies={"intents": ["MESSAGE_CONTENT"]}, supersedes="rule.message-content-announced-feb-2022")

rule("rule.message-content-announced-feb-2022", "February 2022 notice: Message Content to become privileged for verified bots in 75+ servers on August 31, 2022", "area.intents",
     "The announced date was August 31, 2022 and the threshold wording was 75+ servers. The change log then recorded it as in effect on September 1, 2022.",
     "`MESSAGE_CONTENT` is becoming a privileged intent for verified bots in 75+ servers **on August 31, 2022**.",
     "source.change-log", 'Update label="February 14, 2022"', "2022-02-14", to="2022-08-31",
     applies={"minServers": 75, "intents": ["MESSAGE_CONTENT"], "verificationState": "verified"})

rule("rule.message-content-exceptions-gateway", "Without the intent you still get content for: your own messages, DMs, mentions, and context menu targets", "area.intents",
     "The gateway page lists four exceptions. It does not mention replies.",
     "Apps **without** the intent will receive empty values in fields that contain user-inputted content with a few exceptions:\n\n* Content in messages that an app sends\n* Content in DMs with the app\n* Content in which the app is mentioned\n* Content of the message a message context menu command is used on",
     "source.gateway", "#message-content-intent", "2022-09-01",
     applies={"intents": ["MESSAGE_CONTENT"]},
     conflicts=["rule.message-content-exceptions-guide", "rule.message-content-exceptions-changelog-2022"], resolution=RES_C8, cid="C8")

rule("rule.message-content-exceptions-guide", "The June 2026 guide adds replies (with ping on reply) as a content exception and omits context menu targets", "area.intents",
     "The guide lists own messages, DMs, mentions, and replies to a regular bot message when the user has ping on reply enabled. Replies to slash command responses are not covered.",
     "The Message Content intent is **not** needed for your app to access message content in these situations:\n\n* **Messages your app sends**\n* **Direct Messages sent to your app**\n* **Messages that @mention your app**\n* **Replies to your app's messages.** Note: this applies to replies sent using Discord's reply feature to a regular bot message (not an interaction response) and the user has \"ping on reply\" enabled. It does not apply to replies to slash command responses.",
     "source.you-might-not-need", "#exceptions-when-you-get-message-content-without-the-privileged-intent", "2026-06-10",
     applies={"intents": ["MESSAGE_CONTENT"]},
     conflicts=["rule.message-content-exceptions-gateway", "rule.message-content-exceptions-changelog-2022"], resolution=RES_C8, cid="C8")

rule("rule.message-content-exceptions-changelog-2022", "The 2022 change log lists only three exceptions: own messages, DMs, mentions", "area.intents",
     "The original 2022 entry names three exceptions. Later pages added replies and context menu targets.",
     "These restrictions do not apply for messages that a bot or app sends, in DMs that it receives, or in messages in which it is mentioned.",
     "source.change-log", 'Update label="September 01, 2022"', "2022-09-01",
     applies={"intents": ["MESSAGE_CONTENT"]},
     conflicts=["rule.message-content-exceptions-gateway", "rule.message-content-exceptions-guide"], resolution=RES_C8, cid="C8")

rule("rule.intent-4014-disallowed", "Close code 4014 means you passed an intent that is not enabled or not approved", "area.intents",
     "4014 is Disallowed intent(s): the toggle is off in the portal, or over 10,000 users you have not been granted it. Fix the toggle or apply. 4013 is a different error for an invalid bitfield.",
     "You sent a disallowed intent for a Gateway Intent. You may have tried to specify an intent that you have not enabled or are not approved for.",
     "source.opcodes", "#gateway-gateway-close-event-codes", "2020-10-27",
     applies={"intents": INTENTS3}, conf="inferred")

rule("rule.intents-under-10k-no-approval-support", "Support: under 10,000 users you use privileged intents without applying, so there is no 'approved' state", "area.intents",
     "Below 10,000 users there is no application and no approval; you turn the intents on from the Bot page.",
     "Note that apps with fewer than 10,000 users can use Privileged Intents without needing to apply; just turn them on from the bot’s page on the Developer Portal.",
     "source.how-to-get-privileged-intents", "Details", "2026-06-10",
     applies={"maxUsers": 9999, "intents": INTENTS3}, conf="inferred",
     conflicts=["rule.monetisation-requires-slash-or-approved-mc"], resolution=RES_C10, cid="C10")

# ---- verification
rule("rule.verification-intent-review-separate", "App Verification and Privileged Intent review are separate processes", "area.verification",
     "Since June 10, 2026, being verified neither grants nor is required for privileged intents. They are two different reviews.",
     "Previously, App Verification and Privileged Intent review were part of the same review process. With this change, we have separated App Verification and the Privileged Intent review process.",
     "source.intent-changes-2026", "What's Changing, item 4", "2026-06-10",
     conflicts=["rule.message-content-needs-verification-approval", "rule.gateway-stale-100-guilds-bullet"], resolution=RES_C2, cid="C2")

rule("rule.verification-required-past-100-servers", "Support article still says verification is required to scale past 100 servers", "area.verification",
     "This sentence was written in 2024, before the June 2026 change. No current page confirms a 100 server cap for unverified apps, so treat it as unresolved and ask Discord support.",
     "Verification is required for your app to scale past 100 servers.",
     "source.how-to-get-verified", "Getting Your App Verified", "2024-08-30",
     applies={"minServers": 100, "verificationState": "unverified"}, conf="inferred",
     conflicts=["rule.growth-not-blocked-during-review", "rule.verification-unlocks-discovery-monetisation"], resolution=RES_C4, cid="C4")

rule("rule.growth-not-blocked-during-review", "Hitting the threshold no longer blocks your app from joining new servers", "area.verification",
     "Since June 10, 2026 an app under intent review keeps joining servers and reaching new users. The old block at 100 servers is gone.",
     "Previously, when an app hit 100 servers and was required to apply for continued access to its Privileged Intents, it was blocked from joining new servers until the review was complete.\n\nThat's no longer the case. Under the new user-based threshold, apps can continue joining servers and reaching new users while their submission is under review.",
     "source.intent-changes-2026", "What's Changing, item 3", "2026-06-10",
     conflicts=["rule.verification-required-past-100-servers"], resolution=RES_C4, cid="C4")

rule("rule.verification-unlocks-discovery-monetisation", "What verification unlocks: Discovery (App Directory) and monetisation", "area.verification",
     "Verification is the prerequisite for enabling Discovery and for Premium Apps. It is not a prerequisite for privileged intents or for growing past any server count.",
     "**App Verification** also allows you to add monetization features to your app, such as in-app purchases and subscriptions.",
     "source.enabling-discovery", "App Verification", "2026-06-10", conf="inferred",
     conflicts=["rule.verification-required-past-100-servers"], resolution=RES_C4, cid="C4")

rule("rule.verification-owner-stripe-id", "To verify, the team owner must verify their identity through Stripe", "area.verification",
     "The owner of the team that owns the app submits a qualifying ID to Stripe, then completes the App Verification checklist in the Developer Portal.",
     "The most noteworthy requirement is that the owner of the development team which owns the app will need to verify their identity through Stripe, our identity verification provider.",
     "source.how-to-get-verified", "Getting Your App Verified", "2024-06-03", conf="inferred")

rule("rule.verified-bot-flag", "'Verified Bot' badge and 'verified app' are the same thing; the API flag is VERIFIED_BOT (1 << 16)", "area.verification",
     "The user flag VERIFIED_BOT is the badge a verified app's bot user shows. VERIFIED_DEVELOPER (1 << 17) is the legacy Early Verified Bot Developer badge. The Active Developer Badge is unrelated and decommissioned.",
     "`1 << 16` | VERIFIED_BOT | Verified Bot",
     "source.user-resource", "#user-object-user-flags", SNAPSHOT, conf="inferred")

rule("rule.active-developer-badge-decommissioned", "The Active Developer Badge no longer exists", "area.verification",
     "The Active Developer Badge was decommissioned and removed from profiles. It was never related to App Verification.",
     "The Active Developer Badge has been decommissioned and is no longer available to earn. Any Active Developer Badges that were previously displayed on user profiles have been removed.",
     "source.active-developer-badge", "Active Developer Badge - No Longer Available", "2025-12-05", conf="inferred")

# ---- data handling and policy versions
rule("rule.retention-no-longer-necessary-2024", "How long can I keep API data? Only as long as necessary for your stated functionality; no fixed number", "area.dataRetention",
     "There is no numeric retention window in any Discord document. You must delete API data promptly once it is no longer necessary for your app's stated (and, if reviewed, approved) functionality, when you shut down, when Discord asks, or when the user asks.",
     "you will (1) promptly update the API Data upon request from us or the applicable user, and (2) promptly delete the API Data when: (a) retaining it is no longer necessary for your Application’s stated (and approved through App Review, as applicable) functionality that is permitted under the Terms; (b) you stop operating your Application (whether on your own, due to an enforcement action by us, or otherwise); (c) we request you delete it; (d) the applicable user requests you delete it; or (e) required by applicable laws or regulations.",
     "source.dev-tos-2024", "Section 5(b): API Data Sharing & Retention", "2024-07-08", supersedes="rule.retention-no-longer-necessary-2022")

rule("rule.retention-no-longer-necessary-2022", "2022 Developer Terms: delete API data when no longer necessary (same wording as 2024)", "area.dataRetention",
     "Between October 1, 2022 and July 7, 2024 the retention duty was worded exactly as it is today: delete promptly when no longer necessary for stated functionality.",
     "you will (1) promptly update the API Data upon request from us or the applicable user, and (2) promptly delete the API Data when: (a) retaining it is no longer necessary for your Application’s stated (and approved through App Review, as applicable) functionality that is permitted under the Terms;",
     "source.dev-tos-2022", "Section 5(b)", "2022-10-01", to="2024-07-07", supersedes="rule.retention-2020-policy")

rule("rule.retention-2020-policy", "2020 Developer Policy: do not retain data longer than necessary for the operation of your application", "area.dataRetention",
     "From July 1, 2020 to September 30, 2022 the rule was a single bullet: no retention beyond what the operation of your application needs.",
     "retain data any longer than necessary for the operation of your application;",
     "source.dev-policy-2020", "Handle data with care", "2020-07-01", to="2022-09-30", supersedes="rule.retention-2017-tos")

rule("rule.retention-2017-tos", "2017 Developer Terms: delete End User Data within seven days of account termination; keep chat logs only as needed", "area.dataRetention",
     "The 2017 terms are the only version with a number: seven days after the user terminates their account. Chat logs could be kept only as necessary for the operation of your application.",
     "You shall delete all End User Data upon Discord’s or the End User’s request and within seven (7) days following the End User’s termination of the End User’s account. You may only retain chat logs as necessary for the operation of your Applications.",
     "source.dev-tos-2017", "2.4 End User Data", "2017-08-20", to="2020-08-17")

rule("rule.api-data-stated-functionality", "Can I store user IDs and message content? Yes, if it is necessary for your stated functionality", "area.dataRetention",
     "Storing user IDs or content is allowed only as needed for your app's stated (and, if reviewed, approved) functionality. No Discord policy forbids storing user IDs; the purpose limit is what matters, and improvement use needs aggregated or de-identified data.",
     "You may not request, access, or use API Data for any purpose other than as necessary to provide your Application’s stated (and approved through App Review, as applicable) functionality; provided that you may also use API Data for the purpose of improving your Application only if it has been aggregated or de-identified such that it cannot be associated with, or used to identify, any individual.",
     "source.dev-policy-2024", "Handle Data with Care, rule 15", "2024-07-08")

rule("rule.privacy-policy-required", "Every app needs a privacy policy, even a bot in one private server", "area.dataRetention",
     "The Developer Terms apply to every Application. You must provide and follow a privacy policy that describes what you collect, how you use and share it, and how users can request deletion, and keep a public link to it in the Developer Portal.",
     "You will provide and adhere to a privacy policy for your Application that is compliant with applicable privacy laws and clearly, accurately, and fully describes to users of your Application what data you collect, how you use and share such data with us and third parties, and how users can request deletion of such data.",
     "source.dev-tos-2024", "Section 5(a): Implement Good Privacy Practices", "2024-07-08")

rule("rule.encrypt-at-rest", "API data must be encrypted at rest", "area.dataRetention",
     "Whatever you store from the API must be encrypted at rest and protected by administrative, physical and technical safeguards.",
     "These efforts will include: (i) encryption of the data at rest and (ii) maintaining administrative, physical, and technical safeguards that are designed to prevent unauthorized access and use and comply with applicable laws and regulations (including relating to data security and privacy).",
     "source.dev-tos-2024", "Section 5(c): Implement Good Security", "2024-07-08")

rule("rule.ml-training-ban", "You may not train ML or AI models on message content without Discord's express permission", "area.dataRetention",
     "Fine tuning an LLM on message content your bot collected is banned unless Discord grants express permission. The rule was added in the July 8, 2024 policy; the October 1, 2022 version had no such rule.",
     "**21. Do not use message content obtained through the APIs to train machine learning or AI models (including large language models) unless express permission is granted by Discord.**",
     "source.dev-policy-2024", "Handle Data with Care, rule 21", "2024-07-08",
     applies={"intents": ["MESSAGE_CONTENT"]})

rule("rule.no-unsolicited-dms", "Do not DM users without their explicit permission", "area.dataRetention",
     "A welcome DM on join is unsolicited unless the user themselves opted in. A server owner enabling a feature is not the user's permission; keep DMs tied to functionality the user triggered.",
     "**5. Do not contact users on Discord without their explicit permission.** This includes frequently sending unsolicited direct messages and/or sending direct messages not directly related to maintaining or improving an Application's functionality.",
     "source.dev-policy-2024", "Protect Discord Users, rule 5", "2024-07-08")

rule("rule.no-marketing", "Do not target users with advertisements or marketing", "area.dataRetention",
     "Messages from your app must be relevant to its function. Promotional content unrelated to the app is banned.",
     "**6. Do not target users with advertisements or marketing.** Messaging to Discord users from any Application or developer team should be relevant to the function of the Application and may not contain material unrelated to an Application’s function or information.",
     "source.dev-policy-2024", "Protect Discord Users, rule 6", "2024-07-08")

rule("rule.retention-explain-in-review", "In intent review you must explain why you store data and describe your retention policy", "area.dataRetention",
     "If you store data from privileged intents, the review form expects the reason, the retention policy and the security measures. Processing in memory and discarding is an acceptable answer.",
     "If you're storing the data, explain why it's necessary and describe your retention policy and security measures. If you're processing it in memory and discarding it, say so.",
     "source.intent-review-guide", "Step 3, Path B", "2026-06-10",
     applies={"minUsers": 10000, "intents": INTENTS3})

rule("rule.baseline-data-without-intents", "What a bot sees with zero privileged intents: profiles, roles, message metadata, voice state, reactions, locale", "area.dataRetention",
     "Every bot gets a baseline: usernames, avatars, banners, nicknames, roles, message metadata such as time sent, voice channel joins and voice state, reactions, and members' language setting. The article still lists discriminators, which were removed in 2023. Content fields need Message Content; join and leave events need Guild Members; status needs Presence.",
     "* Basic user profile information of server members (e.g., usernames, avatars, banners, discriminators, and nicknames);\n* Roles that members have in the server;\n* Metadata about messages (e.g., day and time sent);\n* The voice channel members join, as well as metadata about voice channels (e.g., muted, deafened, streaming, or have video on);\n* Message reactions by members; and\n* Language information selected by members in their User Settings.",
     "source.visibility-bot-data", "Baseline data list", "2024-05-31", conf="inferred")

rule("rule.privacy-popular-apps-apply", "Discord's Privacy Policy tells users that popular apps must apply for access to certain data", "area.dataRetention",
     "The user facing Privacy Policy states the intent review system exists and that developers must have a privacy policy. It gives no threshold; the developer docs supply the 10,000 user number.",
     "We also require that certain popular apps apply for access to certain data.",
     "source.discord-privacy", "Services offered by third parties", "2025-09-29")

rule("rule.dev-policy-version-2024", "Current Developer Policy: effective July 8, 2024, last updated June 6, 2024", "area.dataRetention",
     "The Developer Policy in force today took effect on July 8, 2024. It replaced the October 1, 2022 version.",
     "Effective date: July 8, 2024\n\nLast updated: June 6, 2024",
     "source.dev-policy-2024", "Header", "2024-07-08", supersedes="rule.dev-policy-version-2022")

rule("rule.dev-policy-version-2022", "2022 Developer Policy: effective October 1, 2022, last updated September 1, 2022", "area.dataRetention",
     "From October 1, 2022 to July 7, 2024 the 2022 Developer Policy applied. It has no rule about training AI models.",
     "*Effective: October 1, 2022*\n\n*Last Updated: September 1, 2022*",
     "source.dev-policy-2022", "Header", "2022-10-01", to="2024-07-07")

rule("rule.dev-tos-version-2024", "Current Developer Terms of Service: effective July 8, 2024, last updated June 6, 2024", "area.dataRetention",
     "The Developer Terms in force today took effect on July 8, 2024, the same day as the current Developer Policy.",
     "*Effective date: July 8, 2024*\n\n*Last updated: June 6, 2024*",
     "source.dev-tos-2024", "Header", "2024-07-08", supersedes="rule.dev-tos-version-2022")

rule("rule.dev-tos-version-2022", "2022 Developer Terms of Service: effective October 1, 2022", "area.dataRetention",
     "From October 1, 2022 to July 7, 2024 the 2022 Developer Terms applied.",
     "*Effective date: October 1, 2022*",
     "source.dev-tos-2022", "Header", "2022-10-01", to="2024-07-07", supersedes="rule.dev-tos-version-2020")

rule("rule.dev-tos-version-2020", "2020 Developer Terms of Service: effective August 18, 2020", "area.dataRetention",
     "From August 18, 2020 to September 30, 2022 the 2020 Developer Terms applied.",
     "**Effective date: August 18, 2020**",
     "source.dev-tos-2020", "Header", "2020-08-18", to="2022-09-30", supersedes="rule.dev-tos-version-2017")

rule("rule.dev-tos-version-2017", "2017 Developer Terms of Service: effective August 20, 2017", "area.dataRetention",
     "Before August 18, 2020 the 2017 Developer Terms applied.",
     "**Effective Date: August 20, 2017**",
     "source.dev-tos-2017", "Header", "2017-08-20", to="2020-08-17")

rule("rule.arbitration-opt-out", "Arbitration opt out: within 30 days of July 8, 2024 or of creating your first Application", "area.dataRetention",
     "US based developers can opt out of arbitration by email within 30 days of July 8, 2024 or of first creating an Application, whichever is later.",
     "the date for emailing an opt-out notice is within 30 days of July 8, 2024 or when you first create an Application, whichever is later.",
     "source.dev-tos-2024", "Section 12(e): Choice of Law; Dispute Resolution", "2024-07-08")

rule("rule.third-party-services-must-follow-dev-terms", "Discord's Terms of Service bind apps to the Developer Terms and Developer Policy", "area.dataRetention",
     "The user facing Terms (effective September 29, 2025) state that third party apps must follow the Developer Terms of Service and Developer Policy, and that Discord is not responsible for them.",
     "While these third parties do need to follow all policies that apply to them (which may include these Terms, our Community Guidelines, Developer Terms of Service, and Developer Policy), Discord is not responsible for any third-party services.",
     "source.discord-terms", "Third-party services", "2025-09-29")

# ---- rate limits and API limits
rule("rule.global-rate-limit-50", "Global rate limit: 50 requests per second per bot", "area.rateLimits",
     "Your bot can make 50 requests per second across the API, independent of per route limits. Without an authorization header the limit applies per IP.",
     "All bots can make up to 50 requests per second to our API. If no authorization header is provided, then the limit is applied to the IP address. This is independent of any individual rate limit on a route.",
     "source.rate-limits", "#global-rate-limit", SNAPSHOT, conf="inferred")

rule("rule.interaction-endpoints-exempt-global", "Interaction endpoints are exempt from the global rate limit, ephemeral or not", "area.rateLimits",
     "Responding to, following up on and editing interaction responses does not count against the 50 per second global limit. Per route and shared limits still apply, and ephemerality changes nothing.",
     "Interaction endpoints are not bound to the bot's Global Rate Limit.",
     "source.rate-limits", "#global-rate-limit", SNAPSHOT, conf="inferred",
     conflicts=["rule.ephemeral-not-counted-support"], resolution=RES_C6, cid="C6")

rule("rule.ephemeral-not-counted-support", "Support article says ephemeral interaction responses do not count towards the rate limits", "area.rateLimits",
     "Wrong on scope. The docs exempt all interaction endpoints from the global limit only; ephemerality is irrelevant and per route limits still apply.",
     "Bonus tip: Make Interaction Responses and follow-up messages ephemeral since they do not count towards the rate limits.",
     "source.rate-limited", "Consider Using Interactions Where Possible", "2025-07-14", conf="inferred",
     conflicts=["rule.interaction-endpoints-exempt-global"], resolution=RES_C6, cid="C6")

rule("rule.invalid-request-limit-10k", "10,000 invalid requests in 10 minutes gets your IP temporarily banned by Cloudflare", "area.rateLimits",
     "401, 403 and 429 responses count as invalid (except 429s with X-RateLimit-Scope: shared). Over 10,000 in 10 minutes and the IP is temporarily blocked.",
     "IP addresses that make too many invalid HTTP requests are automatically and temporarily restricted from accessing the Discord API. Currently, this limit is **10,000 per 10 minutes**. An invalid request is one that results in **401**, **403**, or **429** statuses.",
     "source.rate-limits", "#invalid-request-limit-aka-cloudflare-bans", SNAPSHOT, conf="inferred")

rule("rule.retry-after-seconds", "retry_after is seconds (float) on API v8 and later; the Retry-After header is integer seconds", "area.rateLimits",
     "Sleep for retry_after seconds. A value of 2.5 means two and a half seconds, not milliseconds. This has been true since API v8 on September 24, 2020 and applies to v8, v9 and v10.",
     "retry_after | float | The number of seconds to wait before submitting another request.",
     "source.rate-limits", "#exceeding-a-rate-limit (Rate Limit Response Structure)", "2020-09-24",
     conflicts=["rule.retry-after-milliseconds-support"], resolution=RES_C5, cid="C5")

rule("rule.retry-after-milliseconds-support", "Support article says retry_after is milliseconds", "area.rateLimits",
     "Wrong for every supported API version. This is the pre v8 unit that the support article never updated.",
     "`retry_after`: Milliseconds to wait before making another request",
     "source.rate-limited", "How to Identify Your Rate Limit Issue", "2025-07-14", conf="inferred",
     conflicts=["rule.retry-after-seconds"], resolution=RES_C5, cid="C5")

rule("rule.retry-after-v8-changelog", "API v8 (September 24, 2020) switched retry_after from milliseconds to seconds", "area.rateLimits",
     "The change log records the unit change: since v8, Retry-After and retry_after are in seconds.",
     "The `Retry-After` header value and `retry_after` body value is now based in seconds instead of milliseconds (e.g. `123` means 123 seconds)",
     "source.change-log", 'Update label="September 24, 2020"', "2020-09-24")

rule("rule.sharding-2500", "Sharding is mandatory at 2,500 guilds", "area.rateLimits",
     "Each shard can serve at most 2,500 guilds, so at 2,500 or more guilds you must shard. Get Gateway Bot returns a recommended shard count.",
     "Each shard can only support a maximum of 2500 guilds, and apps that are in 2500+ guilds *must* enable sharding.",
     "source.gateway", "#sharding", SNAPSHOT, applies={"minServers": 2500}, conf="inferred")

rule("rule.sharding-2500-support", "Support: plan sharding at 2,000 guilds, mandatory at 2,500, about 1 shard per 1,000 guilds", "area.rateLimits",
     "Consistent with the docs: sharding must be on at 2,500 guilds; the recommended ratio is roughly one shard per 1,000 guilds.",
     "It's recommended to start planning for sharding implementation when approaching 2,000 guilds, as sharding **must** be enabled at 2,500+ guilds. For optimal performance, follow the best practice of maintaining approximately 1 shard per 1,000 guilds.",
     "source.rate-limited", "Gateway Considerations and Sharding", "2025-07-14", applies={"minServers": 2000}, conf="inferred")

rule("rule.large-bot-sharding-150k", "Over 150,000 guilds Discord moves you to large bot sharding", "area.rateLimits",
     "Near 150,000 guilds Discord migrates the bot to large bot sharding, assigns a shard number that your shard count must be a multiple of, and raises the session start limit to max(2000, guild_count / 1000 * 5) per day.",
     "If your bot is in more than 150,000 guilds, there are some additional considerations you must take around sharding. Discord will migrate your bot to large bot sharding when it starts to get near the large bot sharding threshold.",
     "source.gateway", "#sharding-for-large-bots", SNAPSHOT, applies={"minServers": 150000}, conf="inferred")

rule("rule.identify-limit-1000", "1,000 IDENTIFY calls per 24 hours across all shards; exceeding it resets your token", "area.rateLimits",
     "The IDENTIFY limit is 1,000 per day globally across shards (RESUME does not count). Hitting it terminates all sessions, resets the bot token and emails the owner.",
     "Clients are limited to 1000 `IDENTIFY` calls to the websocket in a 24-hour period. This limit is global and across all shards, but does not include `RESUME` calls. Upon hitting this limit, all active sessions for the app will be terminated, the bot token will be reset, and the owner will receive an email notification.",
     "source.gateway", "#identifying (Identify rate limit)", SNAPSHOT, conf="inferred")

rule("rule.command-limits", "Command quotas: 100 global chat input, 15 user, 15 message, 1 entry point; same per guild", "area.rateLimits",
     "An app can register 100 global CHAT_INPUT commands, 15 global USER commands, 15 global MESSAGE commands and 1 PRIMARY_ENTRY_POINT command, and the same counts per guild for guild commands.",
     "* 100 global `CHAT_INPUT` commands\n* 15 global `USER` commands\n* 15 global `MESSAGE` commands\n* 1 global `PRIMARY_ENTRY_POINT` command",
     "source.application-commands", "#registering-a-command", SNAPSHOT, conf="inferred")

rule("rule.command-create-200-per-day", "200 command creates per day per guild", "area.rateLimits",
     "Creating commands is rate limited to 200 per day per guild. Register once at startup, not on every reconnect.",
     "There is a global rate limit of 200 application command creates per day, per guild",
     "source.application-commands", "#registering-a-command", SNAPSHOT, conf="inferred")

rule("rule.interaction-respond-3-seconds", "Respond to an interaction within 3 seconds; the token lives 15 minutes", "area.rateLimits",
     "You must send an initial response within 3 seconds or the interaction token is invalidated. After that you have 15 minutes for follow ups.",
     "Interaction `tokens` are valid for **15 minutes** and can be used to send followup messages but you **must send an initial response within 3 seconds of receiving the event**. If the 3 second deadline is exceeded, the token will be invalidated.",
     "source.receiving-and-responding", "#responding-to-an-interaction", SNAPSHOT, conf="inferred")

rule("rule.upload-limit-20mib", "Default file upload limit is 20 MiB per file (since September 2026)", "area.rateLimits",
     "Bots, webhooks and interaction responses can upload 20 MiB per file by default, more when the user's Nitro or the server's boost tier allows. Between January 16, 2025 and early September 2026 the default was 10 MiB.",
     "The file upload size limit applies to each file in a request. The default limit is `20 MiB` for all users, but may be higher for users depending on their Nitro status or by the server's Boost Tier.",
     "source.reference", "#uploading-files", "2026-09-03", supersedes="rule.upload-limit-10mib-2025")

rule("rule.upload-limit-changelog-2026", "Change log: default upload limit raised from 10 MiB to 20 MiB for users, bots, webhooks and interactions", "area.rateLimits",
     "The change log entry labelled September 3, 2026 records the increase. GitHub issue 8572 shows the API and docs caught up with the user support article by September 5, 2026.",
     "The default file upload limit has been increased from 10 MiB to 20 MiB for users, bots, webhooks, and interaction responses!",
     "source.change-log", 'Update label="September 3, 2026"', "2026-09-03")

rule("rule.upload-limit-10mib-2025", "January 16, 2025: default upload limit dropped from 25 MiB to 10 MiB", "area.rateLimits",
     "From January 16, 2025 until the September 2026 increase, the default per file limit was 10 MiB.",
     "On January 16, 2025, the default file upload limit will change from 25 MiB to 10 MiB.",
     "source.change-log", 'Update label="December 16, 2024"', "2025-01-16", to="2026-09-02")

rule("rule.support-articles-users-not-bots", "Discord staff: support articles describe user functionality, not bot functionality", "area.rateLimits",
     "When a support.discord.com article and the developer docs disagree about what bots can do, the developer docs describe what bots get. Discord staff said this in the September 2026 upload limit issue.",
     "The API docs still list the 10 mb limit. Once bots get the 20 mb limit the docs will be updated. Support articles reflect functionality for users, not bots.",
     "source.gh-8572", "Comment by advaith1, 2026-09-01", "2026-09-01")

# ---- monetisation
rule("rule.monetisation-eligibility-checklist", "Premium Apps eligibility: verified app, owned by a team, owner 18+, emails verified and 2FA, slash commands or approved Message Content, ToS and privacy links", "area.monetisation",
     "To enable monetisation the app must be verified and owned by a team whose owner is at least 18 with verified emails and 2FA on; the app must use slash commands or have approved Message Content, link a Terms of Service and a Privacy Policy, have clean naming, payouts set up, and accept the Monetization Terms and Developer Policy.",
     "* App must be verified\n* App belongs to a developer team\n* Team owner must be at least 18 years old\n* Team must have verified emails and 2FA set up\n* App uses slash commands, or has been approved for the privileged `Message Content` intent\n* App has a link to your Terms of Service",
     "source.enabling-monetization", "#step-2-complete-the-eligibility-checklist", SNAPSHOT,
     applies={"verificationState": "verified", "ownerAge": "18plus"}, conf="inferred")

rule("rule.monetisation-requires-slash-or-approved-mc", "Monetisation checklist: app must use slash commands or be approved for Message Content", "area.monetisation",
     "The checklist accepts slash commands, or an approved Message Content intent. Since June 10, 2026 approval only exists above 10,000 users, so a prefix command bot under 10,000 users is not clearly covered.",
     "App uses slash commands, or has been approved for the privileged `Message Content` intent",
     "source.enabling-monetization", "#step-2-complete-the-eligibility-checklist", SNAPSHOT, conf="inferred",
     applies={"verificationState": "verified", "intents": ["MESSAGE_CONTENT"]},
     conflicts=["rule.intents-under-10k-no-approval-support"], resolution=RES_C10, cid="C10")

rule("rule.monetisation-regions-docs", "Premium Apps is only available to teams based in the US, UK or EU", "area.monetisation",
     "If your team owner is outside the United States, the United Kingdom or the European Union you cannot enable Premium Apps yet.",
     "Premium Apps is not currently available outside of these regions. These features will be made available to more regions soon.",
     "source.enabling-monetization", "#step-3-set-up-team-payouts (If You are Based Outside of the United States, European Union, or United Kingdom)", SNAPSHOT,
     applies={"region": "Outside US, UK, EU"}, conf="inferred")

rule("rule.monetisation-regions-support", "Supported locales for Premium Apps: United States, United Kingdom, European Union (all 27 member states)", "area.monetisation",
     "The support article lists the US, the UK and every EU member state. Canada, India, Brazil and other countries are not supported.",
     "* United States\n* United Kingdom\n* European Union",
     "source.how-to-monetize", "Supported Locales", "2024-12-12", applies={"region": "US, UK, EU"}, conf="inferred")

rule("rule.payout-threshold-100-docs", "Docs: you become eligible for payout after your first $100", "area.monetisation",
     "The developer docs state the threshold as $100 made, without saying whether fees are deducted first.",
     "Once your app has made its first $100 it will become eligible for payout.",
     "source.enabling-monetization", "#step-3-set-up-team-payouts", SNAPSHOT, conf="inferred",
     conflicts=["rule.payout-threshold-100-net-support"], resolution=RES_C9, cid="C9")

rule("rule.payout-threshold-100-net-support", "Support: payout eligibility starts at $100 earned net of processing and transaction fees", "area.monetisation",
     "The $100 threshold is counted after payment processing and transaction fees. $100 of gross sales may not be enough.",
     "your team will become eligible for payout review after the first 100 dollars is earned [less applicable payment processing fees and transaction fees].",
     "source.premium-payout", "Introduction", "2025-09-19", conf="inferred",
     conflicts=["rule.payout-threshold-100-docs"], resolution=RES_C9, cid="C9")

rule("rule.payout-45-days-25-min", "Payouts arrive within 45 days after month end; $25 minimum per cycle, smaller balances roll over", "area.monetisation",
     "After the first $100 net, each later cycle pays out only amounts above $25, within 45 days after the end of the calendar month. Under $25 rolls over to the next cycle.",
     "Eligible payouts will be provided within 45 days after the end of each calendar month. For example, for offerings purchased in January, you will receive payouts within 45 days after January 31st. An eligible payout can be defined as the first $100 earned [less applicable payment processing fees and transaction fees] and for the following billing cycles, in amounts greater than $25.",
     "source.premium-payout", "Payout", "2025-09-19", conf="inferred")

rule("rule.price-parity-2024", "Since October 7, 2024 paid features must also be sold through Premium Apps at no higher price (US, UK, EU)", "area.monetisation",
     "If you sell premium features anywhere (Patreon, your website) and your team is in a Premium Apps region, you must also offer them through Premium Apps at a price no higher than elsewhere. Outside the supported regions the rule does not bite yet.",
     "Beginning on October 7, 2024, in regions where Discord supports monetization through its Premium Apps products, all developers who offer paid features or capabilities for their Application will be required to:\n\n* (i) support purchase of such features or capabilities through Discord’s Premium Apps products; and,\n* (ii) offer such features or capabilities at prices on Discord that are no higher than the prices at which they are offered through other payment options.",
     "source.dev-policy-2024", "Monetization Requirements", "2024-10-07", applies={"region": "US, UK, EU"})

rule("rule.max-50-skus", "Up to 50 SKUs per app", "area.monetisation",
     "An app can have at most 50 SKUs in total across subscriptions and one time purchases.",
     "* You can create up to 50 total SKUs per app.",
     "source.managing-skus", "#creating-a-sku", SNAPSHOT, conf="inferred")

# ---- app directory
rule("rule.discovery-requires-verification", "Discovery (App Directory) requires the team owner to complete identity and app verification", "area.appDirectory",
     "You cannot enable Discovery until the team owner has verified their identity through Stripe and the app has passed App Verification. Then complete the Discovery Status checklist and metadata in the Developer Portal.",
     "To enable **Discovery** for your app, we require your team owner to complete identity and application verification.",
     "source.enabling-discovery", "App Verification", SNAPSHOT, applies={"verificationState": "verified"}, conf="inferred")

rule("rule.discovery-24-hours", "After enabling Discovery it can take up to 24 hours to appear", "area.appDirectory",
     "Once enabled, allow up to 24 hours for the app to show in the App Directory and App Launcher.",
     "Once you enable **Discovery**, it may take up to 24 hours for your app to appear in the App Directory and App Launcher.",
     "source.enabling-discovery", "Enabling Discovery", SNAPSHOT, conf="inferred")

rule("rule.app-directory-13-plus", "App Directory content must be appropriate for ages 13+", "area.appDirectory",
     "No graphic violence, sexual content or other age restricted topics in a discoverable app; it must suit all ages 13 and up.",
     "**3. Do not host graphic or sexual content.** Graphic violence, sexual content, or other age-restricted topics are not allowed in public spaces. Apps opting into discoverability should be appropriate for audiences of all ages 13+.",
     "source.app-directory-inclusion", "Rule 3", "2025-10-09", conf="inferred")

# ---- tokens and security
rule("rule.token-viewable-once", "A bot token is shown once; if you lose it you must reset it", "area.tokensAndSecurity",
     "The Developer Portal shows the token only once. After leaving the page the copy button is gone and the only way back is Reset Token, which invalidates the old token.",
     "You won't be able to view your token again unless you regenerate it, so make sure to keep it somewhere safe (like in a password manager).",
     "source.getting-started", "Fetching your credentials", SNAPSHOT, conf="inferred")

rule("rule.token-reset-2fa", "Reset Token lives on the Bot page and may ask for your 2FA code", "area.tokensAndSecurity",
     "Bot page, Reset Token under Build-a-Bot, confirm, enter your two factor code if prompted, then copy the new token straight into your config. The old token stops working.",
     "Press the **Reset Token** button located under the **Build-a-Bot** section.\n4. A pop-up window will show up asking you to confirm.\n5. Enter your Two-Factor Authentication code, if requested.",
     "source.token-copy", "How to Regenerate the Bot's Token", "2025-05-27", conf="inferred")

rule("rule.credentials-not-in-open-source", "Tokens must be kept encrypted and never embedded in open source projects", "area.tokensAndSecurity",
     "Keep API keys and tokens encrypted in any file third parties can reach, and never commit developer credentials to an open source repository.",
     "you will keep API keys and tokens encrypted in any files or other materials accessible by third parties (other than your Service Providers, subject to Section 12(a)). For the avoidance of doubt, developer credentials may not be embedded in open source projects.",
     "source.dev-tos-2024", "Section 2: Use of the APIs", "2024-07-08")

rule("rule.self-bots-banned-guidelines", "Self-bots and user-bots are banned by the Community Guidelines (rule 14)", "area.tokensAndSecurity",
     "Automating a user account, even for a private tool, violates Community Guidelines rule 14. Only bot accounts (an Application with a bot user) may automate.",
     "**14. Do not use self-bots or user-bots.** Each account must be associated with a human, not a bot.",
     "source.discord-guidelines", "Rule 14", "2025-09-29")

rule("rule.self-bots-banned-support", "Support: automating a normal user account outside the OAuth2 and bot API can get the account terminated", "area.tokensAndSecurity",
     "Discord's stance since 2017: self-bots are forbidden and can result in account termination.",
     "Automating normal user accounts (generally called \"self-bots\") outside of the OAuth2/bot API is forbidden, and can result in an account termination if found.",
     "source.self-bots", "Body", "2024-04-05", conf="inferred")

# ---- oauth
rule("rule.applications-commands-scope", "Global slash commands need the applications.commands scope, which the bot scope includes", "area.oauth",
     "Add applications.commands to your install link, or just use the bot scope, which includes it by default.",
     "applications.commands | allows your app to add commands to a guild - included by default with the `bot` scope",
     "source.oauth2", "#shared-resources-oauth2-scopes", SNAPSHOT, conf="inferred")

rule("rule.2fa-elevated-permissions", "Bots with elevated permissions need 2FA on the owner's account in servers with server-wide 2FA", "area.oauth",
     "If your bot requests a permission marked with an asterisk (for example Ban Members, Manage Guild) and the server has server-wide 2FA on, the bot owner's account must have two factor authentication enabled.",
     "For bots with elevated permissions (permissions with a `*` next to them), we enforce two-factor authentication on the owner's account when added to guilds that have server-wide 2FA enabled.",
     "source.oauth2", "#two-factor-authentication-requirement", SNAPSHOT, conf="inferred")

# ---- ownership
rule("rule.ownership-cannot-transfer-after-verification", "Under 16 article: team ownership cannot be transferred after verification", "area.ownership",
     "Obsolete. This 2024 text says a verified team's ownership is frozen; the September 2025 transfer article documents a support ticket process that removes verification and lets the new owner re-verify.",
     "That person will need to be the owner of the team, and ownership can't be transferred after verification is complete.",
     "source.under-16", "I haven't verified my bot yet, and I'm under 16", "2022-05-23", to="2025-09-11",
     applies={"verificationState": "verified"}, conf="inferred",
     conflicts=["rule.ownership-transfer-process"], resolution=RES_C7, cid="C7")

rule("rule.ownership-transfer-process", "A verified app's team can be transferred, but verification is removed and the new owner re-verifies", "area.ownership",
     "Yes, via a Developer Support ticket: the current owner requests, the recipient consents within 30 days, verification is stripped and identity data deleted, then the new owner (16+ with a Stripe qualifying ID) re-verifies.",
     "If your developer team owns verified applications, transferring ownership will require **removing verification** from those applications. The new owner will need to reapply for verification after the transfer is complete.",
     "source.transfer-ownership", "Before You Start", "2025-09-12",
     applies={"verificationState": "verified"}, supersedes="rule.ownership-cannot-transfer-after-verification",
     conflicts=["rule.ownership-cannot-transfer-after-verification"], resolution=RES_C7, cid="C7")

rule("rule.ownership-transfer-30-days", "Ownership transfer needs dual consent; both parties have 30 days to respond", "area.ownership",
     "Only the current owner can request a transfer. Discord then asks the recipient to consent; if either side declines or does not respond within 30 days the request is denied. Typical total time is 30 to 60 days.",
     "After the **current owner** requests a transfer, Discord requires **consent from the recipient** before any ownership transfer. Both parties have **30 days to respond** to our requests.",
     "source.transfer-ownership", "Step 1: Dual-Party Consent Required", "2025-09-12")

rule("rule.ownership-individual-to-team-self-serve", "Unverified apps move from an individual to a team with the self-serve 'Transfer App to Team' option", "area.ownership",
     "For an unverified app you do not need a ticket: General Information, Transfer App to Team, pick the team, confirm. Verified apps need Developer Support.",
     "If you currently own unverified applications individually and want to transfer them to your team:\n\n1. Ensure your team has completed identity verification\n2. Navigate to your application settings\n3. Go to the \"General Information\" section\n4. Look for the \"Transfer App to Team\" option below",
     "source.transfer-ownership", "Individual to Team Transfer", "2025-09-12", applies={"verificationState": "unverified"})

# ---- age requirements
rule("rule.age-13-platform", "You must be at least 13 (or your country's minimum) to use Discord at all", "area.ageRequirements",
     "The platform minimum is 13, or higher where local law requires it. Discord's Terms, Privacy Policy and Community Guidelines all took effect on September 29, 2025.",
     "By accessing our services, you confirm that you’re at least 13 years old and meet the minimum age required by the laws in your country. Our services are not designed for nor directed towards users under the age of 13.",
     "source.discord-terms", "Who can use Discord", "2025-09-29")

rule("rule.age-13-dev-tos", "You must be at least 13 to accept the Developer Terms; under the age of consent a parent must agree for you", "area.ageRequirements",
     "Creating an Application means accepting the Developer Terms, which requires being 13 and meeting your country's minimum. If you are too young to consent, your parent or guardian agrees on your behalf and is responsible.",
     "You also confirm and agree that (i) you are at least 13 years of age and meet the minimum age required by the laws in your country, and (ii) if you are not old enough to have authority to consent to the Terms in your country, that your parent or legal guardian must agree to the Terms on your behalf.",
     "source.dev-tos-2024", "Section 1(a): Accepting the Terms", "2024-07-08")

rule("rule.age-16-verify", "The person who submits ID for verification must be 16 or over", "area.ageRequirements",
     "Under 16 you cannot verify on your own ID. A team owner who is 16 or over (parent, guardian, friend or co-developer) with a Stripe qualifying ID verifies on the app's behalf and must keep owning the team; you stay a member.",
     "However, the individual who applies to verify your bot will need to be 16 or over.",
     "source.under-16", "I haven't verified my bot yet, and I'm under 16", "2022-05-23", applies={"ownerAge": "16plus"})

rule("rule.age-min-operate-bot", "The minimum age to operate a verified bot is Discord's minimum age for your country", "area.ageRequirements",
     "You can run a verified bot at 13 (or your country's minimum); only the ID submitted for verification must belong to someone 16 or over.",
     "As before, the minimum age for operating a verified bot on Discord is the same as the minimum age for using Discord in your country.",
     "source.under-16", "I haven't verified my bot yet, and I'm under 16", "2022-05-23")

rule("rule.age-18-monetise", "The team owner must be at least 18 to enable monetisation", "area.ageRequirements",
     "Premium Apps requires the team owner to be 18 or older. Verification at 16 is not enough to monetise.",
     "* Team owner must be at least 18 years old",
     "source.enabling-monetization", "#step-2-complete-the-eligibility-checklist", SNAPSHOT, applies={"ownerAge": "18plus"}, conf="inferred")

rule("rule.monetisation-terms-age-18", "Accepting the Monetization Terms requires being at least 18", "area.ageRequirements",
     "The Monetization Terms (effective June 6, 2024) can only be accepted by someone who is at least 18 and meets the age of digital consent in their country.",
     "By accepting these Monetization Terms, you agree to comply with the Terms and that the Terms control your relationship with us. You also confirm and agree that you are at least 18 years of age and meet the minimum age of digital consent in your country.",
     "source.monetization-terms", "Acceptance", "2024-06-06", applies={"ownerAge": "18plus"})

rule("rule.age-assurance-no-dev-action", "2026 age assurance rollout: no action expected from developers", "area.ageRequirements",
     "Discord's teen by default and age assurance changes roll out in the second half of 2026. Discord does not expect developers to change integrations; you keep managing age requirements for your own app.",
     "**TLDR: We do not expect any action to be required from developers.**",
     "source.age-assurance-2026", "TLDR", "2026-02-11")

# ---------------------------------------------------------------- questions
def question(_id, text, situation, expected, rules, kind="standard", note=None):
    d = {"_id": _id, "_type": "question", "text": text, "expectedAnswer": expected, "kind": kind,
         "expectedRules": refs(rules)}
    if situation:
        d["situation"] = situation
    if note:
        d["note"] = note
    docs.append(d)


ASOF = SNAPSHOT
question("question.q01", "My bot is in 150 servers. Do I need to apply for the Message Content intent?",
         {"servers": 150, "users": 4000, "intents": ["MESSAGE_CONTENT"], "verified": False, "asOf": ASOF},
         "Server count is irrelevant since June 10, 2026. With about 4,000 users you are under the 10,000 user threshold: toggle Message Content on in Developer Portal > Bot > Privileged Gateway Intents, no application, no verification. At 10,000 users you get a notification and 90 days to apply. Before June 10, 2026 the answer was yes (100+ servers required application and verification). The application flags table that still says 100 or more servers is stale.",
         ["rule.intent-threshold-10k-users", "rule.intent-under-10k-toggle", "rule.intent-threshold-100-servers", "rule.flags-table-100-servers", "rule.intent-90-day-window"],
         kind="trap", note="Stale answer: 'yes, you are over 100 servers so you must apply and verify'. That was true until June 9, 2026 and the flags table still says it.")

question("question.q02", "How do I see how many users my app has, so I know if I'm near 10,000?",
         {"asOf": ASOF},
         "You cannot. Discord does not display the user count in the Developer Portal; it counts unique users across all servers the app is installed in and notifies you (portal alert, email or system DM) when you cross 10,000. The server bot install count under Privileged Gateway Intents is a different metric, as Discord staff admitted in GitHub issue 7806.",
         ["rule.intent-user-count-not-shown", "rule.staff-two-install-metrics"],
         kind="trap", note="Stale answer: 'check the server count on General Information, you need approval at 100'. Server counts are the wrong metric.")

question("question.q03", "I already got Message Content approved in 2023. Do I need to do anything?",
         {"intents": ["MESSAGE_CONTENT"], "verified": True, "asOf": ASOF},
         "Yes. Access granted through a prior review must be reapplied for annually. You will receive a notification, then have 90 days to reapply; access continues during review. Do not reapply before the notice arrives.",
         ["rule.intent-annual-reapply", "rule.intent-90-day-window", "rule.intent-access-continues-during-review"],
         kind="trap", note="Stale answer: 'no, approval is permanent'. Annual reapplication started June 10, 2026.")

question("question.q04", "I got close code 4014 when connecting. What's wrong?",
         {"servers": 120, "users": 3000, "intents": ["GUILD_MEMBERS"], "verified": False, "asOf": ASOF},
         "4014 is Disallowed intent(s): an intent in your IDENTIFY bitfield is not enabled in the Developer Portal (or, above 10,000 users, not granted). With 3,000 users you are under the threshold, so turn the toggle on under Bot > Privileged Gateway Intents and reconnect. Being in 120 servers is irrelevant. 4013 is a different error for an invalid bitfield.",
         ["rule.intent-4014-disallowed", "rule.intent-under-10k-toggle", "rule.intent-threshold-10k-users"],
         kind="trap", note="Stale answer: 'you are over 100 servers so you need to get verified and approved first'.")

question("question.q05", "Can my bot read message content without the intent if the user replies to it?",
         {"intents": [], "asOf": ASOF},
         "Sometimes. All sources agree on three exceptions: messages the app sends, DMs with the app, messages that mention the app. The June 2026 guide adds replies to a regular bot message when the user has ping on reply enabled (not replies to slash command responses). The gateway page adds the target message of a message context menu command and omits replies. Give the union and cite both pages.",
         ["rule.message-content-exceptions-gateway", "rule.message-content-exceptions-guide", "rule.message-content-exceptions-changelog-2022"])

question("question.q06", "Do I need to be verified to go past 100 servers?",
         {"servers": 97, "verified": False, "asOf": ASOF},
         "Officially undetermined. Verification is required for Discovery (App Directory) and Premium Apps, and since June 10, 2026 it is separate from intents and growth is not blocked during review. The only page saying 'Verification is required for your app to scale past 100 servers' was last edited 2024-08-30 and no current page confirms or retracts a cap. Cite both and ask Discord developer support.",
         ["rule.verification-required-past-100-servers", "rule.growth-not-blocked-during-review", "rule.verification-unlocks-discovery-monetisation", "rule.verification-intent-review-separate"],
         kind="trap", note="Stale answer: 'yes, unverified bots stop at 100 servers'. The honest answer is that no current source states a cap.")

question("question.q07", "I'm 15. Can I verify my bot?",
         {"verified": False, "asOf": ASOF},
         "Not on your own ID. Since 2022 the person submitting ID to Stripe must be 16 or over. A 16+ team owner (parent, guardian, friend or co-developer) verifies on the app's behalf and must own the team; you stay a member. Operating a bot only needs Discord's minimum age for your country (13 in most places). At 16 you can verify yourself.",
         ["rule.age-16-verify", "rule.age-min-operate-bot", "rule.verification-owner-stripe-id"])

question("question.q08", "Can I transfer my verified bot's team to someone else?",
         {"verified": True, "asOf": ASOF},
         "Yes, through a Developer Support ticket: the current owner requests, the recipient consents, both have 30 days, verification is removed and identity data deleted, and the new owner re-verifies. Unverified apps move to a team self-serve via Transfer App to Team. The older Under 16 article's 'ownership can't be transferred after verification' is superseded by the September 2025 process.",
         ["rule.ownership-transfer-process", "rule.ownership-transfer-30-days", "rule.ownership-cannot-transfer-after-verification", "rule.ownership-individual-to-team-self-serve"],
         kind="trap", note="Stale answer: 'no, ownership can't be transferred after verification'. That article was never updated.")

question("question.q09", "I got a 429 with retry_after 2.5. Is that seconds or ms?",
         {"asOf": ASOF},
         "Seconds. On API v8 and later (v10 is current) retry_after is a float in seconds and the Retry-After header is integer seconds; v8 changed this on September 24, 2020. The support article that says milliseconds is wrong. Sleep 2.5 seconds.",
         ["rule.retry-after-seconds", "rule.retry-after-milliseconds-support", "rule.retry-after-v8-changelog"],
         kind="trap", note="Stale answer: 'milliseconds', which the support article still says.")

question("question.q10", "What's the global rate limit and do slash command responses count?",
         {"asOf": ASOF},
         "50 requests per second per bot (per IP if unauthenticated). Interaction endpoints (respond, follow up, edit original) are exempt from the global limit whether or not the response is ephemeral; per route and shared limits still apply. Invalid requests (401, 403, 429 except shared scope 429) above 10,000 per 10 minutes trigger a temporary Cloudflare ban.",
         ["rule.global-rate-limit-50", "rule.interaction-endpoints-exempt-global", "rule.ephemeral-not-counted-support", "rule.invalid-request-limit-10k"])

question("question.q11", "When must I shard?",
         {"servers": 2500, "asOf": ASOF},
         "At 2,500 guilds sharding is mandatory; each shard supports at most 2,500 guilds and about one shard per 1,000 guilds is recommended. Above 150,000 guilds Discord migrates you to large bot sharding. IDENTIFY is limited to 1,000 calls per 24 hours across all shards.",
         ["rule.sharding-2500", "rule.sharding-2500-support", "rule.large-bot-sharding-150k", "rule.identify-limit-1000"])

question("question.q12", "Can I store user IDs and message content in my database?",
         {"intents": ["MESSAGE_CONTENT"], "asOf": ASOF},
         "Yes, only as necessary for your app's stated (and, if reviewed, approved) functionality (Developer Policy 15). It must be described in your privacy policy (Developer Terms 5a), encrypted at rest (5c) and deleted promptly when no longer necessary, on user request, or when you shut down (5b). No fixed retention window exists in any Discord document. Message content may not be used to train ML or AI models without Discord's express permission (Policy 21).",
         ["rule.api-data-stated-functionality", "rule.privacy-policy-required", "rule.encrypt-at-rest", "rule.retention-no-longer-necessary-2024", "rule.ml-training-ban"])

question("question.q13", "Do I need a privacy policy for a bot in one private server?",
         {"servers": 1, "asOf": ASOF},
         "Yes. The Developer Terms apply to every Application regardless of size: you must provide and adhere to a privacy policy and keep a public link to it in the Developer Portal. Enforcement risk scales with reach, the obligation does not.",
         ["rule.privacy-policy-required", "rule.age-13-dev-tos"])

question("question.q14", "Can I use message content from my bot to fine-tune an LLM?",
         {"intents": ["MESSAGE_CONTENT"], "asOf": ASOF},
         "No, unless Discord grants express permission. Developer Policy rule 21, in force since July 8, 2024. The October 1, 2022 policy had no such rule.",
         ["rule.ml-training-ban", "rule.dev-policy-version-2024", "rule.dev-policy-version-2022"])

question("question.q15", "Can I DM users a welcome message when they join?",
         {"asOf": ASOF},
         "Only with the user's explicit permission. Developer Policy 5 bans contacting users without explicit permission and 6 bans marketing. A server owner enabling a welcome DM feature is not the user's permission; keep DMs tied to functionality the user triggered.",
         ["rule.no-unsolicited-dms", "rule.no-marketing"])

question("question.q16", "My bot sells premium via Patreon. Am I forced to use Discord's Premium Apps?",
         {"asOf": ASOF},
         "Depends on region. Since October 7, 2024, in regions where Premium Apps exists (US, UK, EU), any paid feature must also be purchasable through Premium Apps at a price no higher than elsewhere. You can keep Patreon alongside. Outside those regions the rule does not apply yet.",
         ["rule.price-parity-2024", "rule.monetisation-regions-docs"])

question("question.q17", "I'm in Canada / India / Brazil. Can I enable Premium Apps?",
         {"asOf": ASOF},
         "No. Premium Apps is available only to teams based in the United States, the United Kingdom and the 27 EU member states. Discord says more regions will follow but gives no date.",
         ["rule.monetisation-regions-docs", "rule.monetisation-regions-support"])

question("question.q18", "What are the exact eligibility requirements for monetization?",
         {"verified": True, "asOf": ASOF},
         "Verified app owned by a team; team owner 18+; team emails verified and 2FA on; app uses slash commands or has been approved for Message Content (ambiguous under 10,000 users where no approval exists); links to a Terms of Service and a Privacy Policy; no harmful language in name, description, commands or metadata; payouts set up; agree to the Monetization Terms (effective June 6, 2024) and the Developer Policy. Max 50 SKUs per app.",
         ["rule.monetisation-eligibility-checklist", "rule.monetisation-requires-slash-or-approved-mc", "rule.intents-under-10k-no-approval-support", "rule.max-50-skus", "rule.monetisation-terms-age-18"])

question("question.q19", "When do I get paid?",
         {"asOf": ASOF},
         "After the first $100 earned net of payment processing and transaction fees; later cycles pay out amounts above $25, within 45 days after the end of the calendar month; balances under $25 roll over. The developer docs say '$100' without the net qualifier; the support article is the more specific one.",
         ["rule.payout-threshold-100-net-support", "rule.payout-45-days-25-min", "rule.payout-threshold-100-docs"],
         kind="trap", note="Obvious answer: '$100 in sales'. The threshold is net of fees.")

question("question.q20", "How do I get into the App Directory?",
         {"verified": False, "asOf": ASOF},
         "Get verified first (team owner Stripe ID plus the App Verification checklist), then Developer Portal > Discovery > Discovery Status checklist, fill Discovery Settings, enable, and allow up to 24 hours. Content must suit ages 13+, no graphic or sexual content, and respect the Developer Policy and IP rights.",
         ["rule.discovery-requires-verification", "rule.discovery-24-hours", "rule.app-directory-13-plus", "rule.verification-owner-stripe-id"])

question("question.q21", "Is the 'Verified Bot' badge the same as 'verified app'?",
         {"asOf": ASOF},
         "Yes, same thing under two names. The API user flag is 1 << 16 VERIFIED_BOT ('Verified Bot'); 1 << 17 VERIFIED_DEVELOPER is the legacy Early Verified Bot Developer badge. The Active Developer Badge is unrelated and has been decommissioned.",
         ["rule.verified-bot-flag", "rule.active-developer-badge-decommissioned"])

question("question.q22", "How many slash commands can I register, and how fast?",
         {"asOf": ASOF},
         "100 global CHAT_INPUT, 15 global USER, 15 global MESSAGE and 1 PRIMARY_ENTRY_POINT command, with the same counts per guild for guild commands; 200 command creates per day per guild. Global commands need the applications.commands scope, which the bot scope includes.",
         ["rule.command-limits", "rule.command-create-200-per-day", "rule.applications-commands-scope"])

question("question.q23", "Can I run a 'self-bot' or automate my user account for a private tool?",
         {"asOf": ASOF},
         "No. Community Guidelines rule 14 (effective September 29, 2025) bans self-bots and user-bots, and the support article says automating a user account outside the OAuth2 and bot API can get the account terminated. Use a bot account.",
         ["rule.self-bots-banned-guidelines", "rule.self-bots-banned-support"])

question("question.q24", "What data does my bot get from a server with zero privileged intents?",
         {"intents": [], "asOf": ASOF},
         "Baseline: usernames, avatars, banners, nicknames (the article also lists discriminators, which no longer exist), roles, message metadata such as time sent, voice channel joins and voice state, reactions, and members' language. Content fields are empty without Message Content except for the documented exceptions; join and leave events need Guild Members; status needs Presence.",
         ["rule.baseline-data-without-intents", "rule.message-content-exceptions-gateway"])

question("question.q25", "Which version of the Developer Policy applies to me and when did it change?",
         {"asOf": ASOF},
         "Today: Developer Policy and Developer Terms effective July 8, 2024 (last updated June 6, 2024), arbitration opt out within 30 days of that date or of your first Application. October 1, 2022 to July 7, 2024: the 2022 versions. August 18, 2020 (Terms) and July 1, 2020 (Policy) to September 30, 2022: the 2020 versions. Before that the 2017 Developer Terms (effective August 20, 2017). Discord's Terms, Privacy Policy and Guidelines: effective September 29, 2025.",
         ["rule.dev-policy-version-2024", "rule.dev-policy-version-2022", "rule.dev-tos-version-2024", "rule.dev-tos-version-2022", "rule.dev-tos-version-2020", "rule.dev-tos-version-2017", "rule.arbitration-opt-out", "rule.age-13-platform"])

question("question.u01", "Does an unverified bot still stop at 100 servers?",
         {"servers": 99, "verified": False, "asOf": ASOF},
         "Unknown. No current source states a server cap for unverified apps. The one page that says verification is required to scale past 100 servers was last edited in August 2024, before the June 2026 change that decoupled verification from intents and unblocked growth during review. The agent should say it cannot determine this and recommend asking Discord developer support, citing both pages.",
         ["rule.verification-required-past-100-servers", "rule.growth-not-blocked-during-review"],
         kind="unknown", note="The correct behaviour is to admit the gap, not to pick a side.")

question("question.u02", "What exactly did the Message Content Intent FAQ say about storing message content?",
         {"intents": ["MESSAGE_CONTENT"], "asOf": ASOF},
         "Unknown. Article 4404772028055 (Message Content Privileged Intent FAQ) was deleted and now redirects to 'What are Privileged Intents?', which says nothing about storage. The Wayback copy was not captured. The agent should say the source no longer exists and fall back to the Developer Terms retention duty (delete when no longer necessary).",
         ["rule.retention-no-longer-necessary-2024"],
         kind="unknown", note="The agent must not invent FAQ wording.")

question("question.u03", "What is the exact date the 10,000-user rule started?",
         {"asOf": ASOF},
         "Best answer: June 10, 2026, from the change log and the review guide. But the announcement page itself is undated (it says 'today'), its metadata says created May 6, 2026 and edited June 11, 2026. The agent should give June 10, 2026 with the caveat that the primary source carries no date.",
         ["rule.intent-change-date-changelog", "rule.intent-change-date-guide", "rule.intent-change-date-announcement-undated"],
         kind="unknown", note="Partial knowledge: a defensible date with an explicit caveat, not a confident single answer.")


# ---------------------------------------------------------------- formatting and limits (added 2026-09-19)
# FORMATTING_START marks the new docs so the script can also write seed-formatting.ndjson
# (only the new documents, for a non replacing import on top of the 185 already in production).
FORMATTING_START = len(docs)
F = "formatting/"

# sources: user support
source("source.markdown-101", "Markdown Text 101 (Chat Formatting: Bold, Italic, Underline) (user support)", "userSupport",
       SU + "210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline", F + "Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-210298617.md",
       publishedAt="2015-09-17", lastEditedAt="2025-04-23",
       notes="The only Discord page that documents headers, subtext, masked links, lists, block quotes and code blocks. Prints no date; Zendesk created 2015-09-17, content edited 2025-04-23. Written for users; says nothing about which formatting bots or embeds render.")
source("source.spoiler-tags", "Spoiler Tags! (user support)", "userSupport", SU + "360022320632-Spoiler-Tags", F + "Spoiler-Tags-360022320632.md",
       publishedAt="2019-01-27", lastEditedAt="2022-01-30",
       notes="Spoiler syntax ||text||, /spoiler, and the code block exception. Content edited 2022-01-30.")
source("source.sending-messages", "Sending Messages (user support)", "userSupport", SU + "360034632292-Sending-Messages", F + "Sending-Messages-360034632292.md",
       publishedAt="2019-10-09", lastEditedAt="2024-04-08",
       notes="Character Limit section: 2000 per message, 4000 with Nitro, longer pastes become a text file. Written for users; the bot API limit stays 2000 regardless of Nitro.")
source("source.nitro-perks", "What are Nitro & Nitro Basic? (user support)", "userSupport", SU + "115000435108-What-are-Nitro-Nitro-Basic", F + "What-are-Nitro-Nitro-Basic-115000435108.md",
       publishedAt="2016-12-22", lastEditedAt="2026-07-01",
       notes="Perk table lists Longer Messages (4000 characters) as a Nitro perk; Nitro Basic does not get it. Content edited 2026-07-01.")
source("source.server-caps", "Discord Account Caps, Server Caps, and More (user support)", "userSupport", SU + "33694251638295-Discord-Account-Caps-Server-Caps-and-More", F + "Discord-Account-Caps-Server-Caps-and-More-33694251638295.md",
       publishedAt="2025-07-24", lastEditedAt="2026-03-02",
       notes="Tables of account and server caps: message length 2000 (4000 Nitro), 500 channels including categories, 50 channels per category, 50 categories per server, 250 roles, 100 character role names. Content edited 2026-03-02. The docs error code 30030 says 5 categories, which disagrees (C11).")

# sources: developer docs
source("source.message-resource", "Message resource (developer docs)", "developerDocs", D + "resources/message", F + "devdocs_resources_message.md",
       notes="Create Message params: content up to 2000 characters, up to 10 rich embeds, 6000 characters across embeds. Embed Limits table. Page prints no date; snapshot copy with header under research/raw/formatting, identical bytes to devdocs/resources_message.md.")
source("source.channel-resource", "Channels resource (developer docs)", "developerDocs", D + "resources/channel", F + "devdocs_resources_channel.md",
       notes="Channel object: name 1-100 characters, topic 0-1024 (0-4096 for forum and media), each parent category can contain up to 50 channels. Says nothing about lowercase or spaces in text channel names. Page prints no date.")
source("source.guild-resource", "Guild resource (developer docs)", "developerDocs", D + "resources/guild", F + "devdocs_resources_guild.md",
       notes="Create Guild Channel params: channel name 1-100 characters. Does not state the 500 channel or 50 category limits; those live in the opcodes error table and the user support caps article. Page prints no date.")

# sources: community convention (not Discord)
source("source.emojidb-channel-symbols", "Community convention: channel name symbols (emojidb)", "github", "https://emojidb.org/discord-channel-name-symbols-emojis",
       F + "emojidb-discord-channel-name-symbols.md", authority=20,
       notes="Community copy and paste catalogue of separators and decorations used in Discord channel names (┃ ・ │ ┆ ︱ ⋆ ✦ and so on). Not a Discord page and not a Discord rule: a convention catalogue only. Page prints no author or date; fetched 2026-09-19.")
source("source.emojidb-channel-emojis", "Community convention: channel emojis (emojidb)", "github", "https://emojidb.org/discord-channel-emojis",
       F + "emojidb-discord-channel-emojis.md", authority=20,
       notes="Community copy and paste catalogue of emoji commonly put in front of Discord channel names (💬 📢 📜 🔊 👋 and so on) with examples like 👋 | WELCOME and ✅┃Verification. Not a Discord page and not a Discord rule. Page prints no author or date; fetched 2026-09-19.")
source("source.gh-1646", "GitHub issue 1646: Allow capital letters and spaces in text channel names", "github",
       "https://github.com/discord/discord-api-docs/issues/1646", F + "issue-1646.md", publishedAt="2020-05-18", lastEditedAt="2020-05-18",
       notes="Community feature request, closed the same day by Discord PM Mason Sciotti as a product request, not a docs issue. The only written record we hold that text channel names reject capital letters and spaces while allowing most of Unicode. No Discord page states this rule.")

RES_C11 = ("Support says a server can have 50 categories and 500 channels including categories (caps article, edited 2026-03-02). The docs "
           "error table says code 30030 is 'Maximum number of server categories has been reached (5)'. The docs line is a bare error string "
           "with no context and the 5 most likely refers to something other than channel categories, but Discord does not say so. Our ruling: "
           "plan for 50 channel categories and 500 channels in total, cite both, and treat 30030 as the error to expect if a category create fails.")

# ---- markdown syntax (support article, content edited 2025-04-23)
MD = "source.markdown-101"
MD_FROM = "2025-04-23"
rule("rule.md-header-space", "Headers need a space after #, ## or ### at the start of the line", "area.formatting",
     "A header only renders when the line starts with #, ## or ### followed by a space. '##Rules' stays literal; '## Rules' becomes a header. One # is the biggest, ### the smallest.",
     "**Note:** Don’t forget to add a space between the leading heading character (`#`, `##`, `###`) and your text!\n\nTo create a header you just need to include a specific number of the hash/pound sign character (`#`). Use (`#`) for a big header, (`##`) for a smaller header, or (`###`) for an even smaller header as the first character(s) in a new line to make a header.",
     MD, "Organizational Text Formatting > Headers", MD_FROM, conf="inferred")

rule("rule.md-subtext", "Subtext is -# at the very start of the line, followed by a space", "area.formatting",
     "Put -# then a space at the very beginning of a line to render it as small grey subtext. It fails if anything precedes the -# on that line or if the space is missing.",
     "Like **Headers**, you can add subtext to any chat message. To do so, add a (`-#` ) before the text you want to appear in the subtext. Don’t forget the space after # before your message.",
     MD, "Organizational Text Formatting > Subtext", MD_FROM, conf="inferred")

rule("rule.md-inline-styles", "Bold, italic, underline, strikethrough and their combinations", "area.formatting",
     "*italics* or _italics_, **bold**, ***bold italics***, __underline__, ~~strikethrough~~. Underline combines with the others by wrapping the whole thing in double underscores, for example __**underline bold**__.",
     "| *Italics* | \\*italics\\* **or** \\_italics\\_ | *Underline italics* | \\_\\_\\*underline italics\\*\\_\\_ |\n| **Bold** | \\*\\*bold\\*\\* | **Underline bold** | \\_\\_\\*\\*underline bold\\*\\*\\_\\_ |\n| ***Bold Italics*** | \\*\\*\\*bold italics\\*\\*\\* | ***underline bold italics*** | \\_\\_\\*\\*\\*underline bold italics\\*\\*\\*\\_\\_ |\n| Underline | \\_\\_underline\\_\\_ | ~~Strikethrough~~ | ~~Strikethrough~~ |",
     MD, "Text Formatting table", MD_FROM, conf="inferred")

rule("rule.md-spoiler", "Spoilers are ||text||, and a code block cancels them", "area.formatting",
     "Wrap text in two vertical bars on each side, ||like this||, to hide it until clicked. Spoiler markup inside a code block is shown as plain text, not hidden.",
     "**Note:** Spoilers is another type of formatting too! Using the syntax || around your text will mark it as a spoiler. Please note, this is negated by a code block.",
     MD, "closing note", MD_FROM, conf="inferred")

rule("rule.spoiler-code-block", "Spoiler tags article: ||text|| or /spoiler; not hidden inside code blocks", "area.formatting",
     "Manual syntax is ||Insert spoilers here|| or the /spoiler command before the message. Text marked as a spoiler inside a code block stays visible, and server invite embeds cannot be hidden by spoiler tags.",
     "You can also manually tag spoilers by using the Markdown syntax ||Insert spoilers here|| or typing /spoiler before your message.",
     "source.spoiler-tags", "How does it work?", "2022-01-30", conf="inferred")

rule("rule.md-block-quote", "Block quote: > plus a space at the start of the line", "area.formatting",
     "Start a line with > and a space to quote that one line. Without the space it stays a literal greater-than sign.",
     "**Note:** Don’t forget to add a space between the leading > and your text!\n\nAnother option is using block quotes. To use a block quote, you just need to put (`>`) at the beginning of a line of text to create a single block quote.",
     MD, "Block Quotes", MD_FROM, conf="inferred")

rule("rule.md-block-quote-multiline", "Multi line block quote: >>> before the first line quotes everything after it", "area.formatting",
     ">>> at the start of a line turns that line and every following line of the message into one block quote. Nothing after it can leave the quote, so put >>> last if you also need normal text.",
     "If you want to add multiple lines to a single block quote, just add (`>>>`) before the first line.",
     MD, "Block Quotes", MD_FROM, conf="inferred")

rule("rule.md-lists", "Bulleted lists: - or * at the start of each line, then a space", "area.formatting",
     "Start each item with - or * and a space. Numbered items use 1. and a space. Without the space the dash is literal text.",
     "**Note:** Don’t forget to add a space between the list bullet (`-`, `*`, `1.`, etc) and your text!\n\nYou can create a bulleted list using either (`-`) or (`*)` in the beginning of each line.",
     MD, "Organizational Text Formatting > Lists", MD_FROM, conf="inferred")

rule("rule.md-list-nesting", "Nest a list item by indenting it with 2 spaces", "area.formatting",
     "Indent a bullet with two spaces before the - or * to make it a sub item. Discord's page shows one level of indentation.",
     "You can also indent your list by adding 2 spaces before (`-`) or (`*`) at the beginning of each line.",
     MD, "Organizational Text Formatting > Lists", MD_FROM, conf="inferred")

rule("rule.md-masked-links", "Masked links: [display text](https://url)", "area.formatting",
     "Write the visible text in square brackets followed by the URL in parentheses. The support article presents this as ordinary chat formatting for everyone; no current Discord page restricts masked links to bots, webhooks or embeds, so do not promise a developer that users cannot send them.",
     "You can use masked links to make text a clickable or pressable hyperlink. To do so, you need to include the text you want displayed in brackets and then the URL in parentheses.",
     MD, "Organizational Text Formatting > Masked links", MD_FROM, conf="inferred")

rule("rule.md-code-blocks", "Inline code uses single backticks, multi line code blocks use triple backticks", "area.formatting",
     "Wrap inline code in one backtick on each side and multi line blocks in three backticks on their own lines. A language name right after the opening fence (for example ```js) gives syntax highlighting in the client, but no Discord page we hold documents that, so treat it as client behaviour, not a rule.",
     "You can make your own code blocks by wrapping your text in backticks (`` ` ``).",
     MD, "Code Blocks", MD_FROM, conf="inferred")

# ---- message length
rule("rule.message-2000-chars", "Users: 2000 characters per message, longer text becomes a file", "area.formatting",
     "A message is capped at 2000 characters. If a user pastes more, the client turns it into a text file attachment instead of a message.",
     "The character cap per message is **2000**. Messages with more than **2000** characters will be converted into a text file.",
     "source.sending-messages", "Character Limit", "2024-04-08", conf="inferred")

rule("rule.message-4000-nitro", "Nitro raises the user message cap to 4000 characters", "area.formatting",
     "A Nitro subscriber (not Nitro Basic) can send up to 4000 characters. This is a user perk: it does not change the 2000 character limit on the bot API's content field.",
     "You can raise the character cap limit to **4000** when you subscribe to Discord Nitro.",
     "source.sending-messages", "Character Limit", "2024-04-08", conf="inferred")

rule("rule.caps-message-length", "Caps table: message length 2000 on Base and Basic, 4000 on Nitro", "area.formatting",
     "Discord's caps table gives 2000 characters for free accounts and Nitro Basic, 4000 for Nitro. When drafting for a bot, count against 2000.",
     "| Message length | 2000 character | Same | 4000 character |",
     "source.server-caps", "Account Caps", "2026-03-02", conf="inferred")

# ---- bot API message and embed limits (undated docs pages: snapshot date, inferred)
MSG = "source.message-resource"
rule("rule.api-content-2000", "Bot API: message content is up to 2000 characters", "area.formatting",
     "The content field on Create Message and Edit Message accepts at most 2000 characters. Nitro does not apply to bots. Split longer text across messages, an embed description (4096) or a file.",
     "Message contents (up to 2000 characters)",
     MSG, "#create-message-jsonform-params", SNAPSHOT, conf="inferred")

rule("rule.api-10-embeds-6000", "Bot API: up to 10 rich embeds per message, 6000 characters across them", "area.formatting",
     "A message can carry at most 10 rich embeds and the text across all of them may not exceed 6000 characters.",
     "Up to 10 `rich` embeds (up to 6000 characters)",
     MSG, "#create-message-jsonform-params", SNAPSHOT, conf="inferred")

rule("rule.embed-field-limits", "Embed limits: title 256, description 4096, 25 fields, field name 256, field value 1024, footer 2048, author 256", "area.formatting",
     "Each embed: title 256 characters, description 4096, up to 25 fields, field name 256, field value 1024, footer text 2048, author name 256. Limits are inclusive and leading or trailing whitespace is trimmed before counting.",
     "| title | 256 characters |\n| description | 4096 characters |\n| fields | Up to 25 field objects |\n| field.name | 256 characters |\n| field.value | 1024 characters |\n| footer.text | 2048 characters |\n| author.name | 256 characters |",
     MSG, "#embed-object-embed-limits", SNAPSHOT, conf="inferred")

rule("rule.embed-total-6000", "Embed limits: 6000 characters combined across all embeds, or 400 Bad Request", "area.formatting",
     "Add up title, description, field names, field values, footer text and author name across every embed on the message; the sum must stay at or under 6000 characters or the request fails with Bad Request.",
     "Additionally, the combined sum of characters in all `title`, `description`, `field.name`, `field.value`, `footer.text`, and `author.name` fields across all embeds attached to a message must not exceed 6000 characters. Violating any of these constraints will result in a `Bad Request` response.",
     MSG, "#embed-object-embed-limits", SNAPSHOT, conf="inferred")

rule("rule.content-strip-chars", "Discord may strip characters that break formatting; sanitise user strings and set allowed_mentions", "area.formatting",
     "If you put user supplied text into content, Discord may remove invalid unicode or characters that cause unexpected formatting. Sanitise it and use allowed_mentions so a pasted @everyone does not ping.",
     "Discord may strip certain characters from message content, like invalid unicode characters or characters which cause unexpected message formatting. If you are passing user-generated strings into message content, consider sanitizing the data to prevent unexpected behavior and using `allowed_mentions` to prevent unexpected mentions.",
     MSG, "#create-message (warning box)", SNAPSHOT, conf="inferred")

# ---- mention, emoji and timestamp syntax (API reference, existing source)
REF = "source.reference"
rule("rule.fmt-mentions", "Mention syntax: <@USER_ID>, <#CHANNEL_ID>, <@&ROLE_ID>", "area.formatting",
     "Users are <@id>, channels <#id>, roles <@&id>. The <@!id> form is deprecated and treated like a plain user mention.",
     "| User                                | `<@USER_ID>`                             | `<@80351110224678912>`                |\n| User \\*                             | `<@!USER_ID>`                            | `<@!80351110224678912>`               |\n| Channel                             | `<#CHANNEL_ID>`                          | `<#103735883630395392>`               |\n| Role                                | `<@&ROLE_ID>`                            | `<@&165511591545143296>`              |",
     REF, "#message-formatting", SNAPSHOT, conf="inferred")

rule("rule.fmt-allowed-mentions", "Mentions notify according to the sender's permissions and allowed_mentions", "area.formatting",
     "Writing a user or role mention pings the target only if the sender may ping them and allowed_mentions permits it. Bots should set allowed_mentions explicitly when echoing user text.",
     "Using the markdown for users or roles will mention the target(s), and notify them depending on the sender's permissions as well as the value of the `allowed_mentions` field when creating a message.",
     REF, "#message-formatting", SNAPSHOT, conf="inferred")

rule("rule.fmt-custom-emoji", "Custom emoji: <:name:id>, animated: <a:name:id>, standard emoji are plain Unicode", "area.formatting",
     "Static custom emoji are written <:name:id>, animated ones <a:name:id>; standard emoji are the Unicode character itself. Bots need the numeric id, the name alone is not enough.",
     "| Custom emoji                        | `<:NAME:ID>`                             | `<:mmLol:216154654256398347>`         |\n| Animated custom emoji               | `<a:NAME:ID>`                            | `<a:b1nzy:392938283556143104>`        |",
     REF, "#message-formatting", SNAPSHOT, conf="inferred")

rule("rule.fmt-timestamps", "Timestamps: <t:UNIX> or <t:UNIX:STYLE>, in seconds, shown in each viewer's timezone", "area.formatting",
     "Write <t:1618953630> or <t:1618953630:R>. The number is Unix seconds, not milliseconds, and every reader sees it in their own timezone and locale.",
     "Timestamps are expressed in **seconds** and display the given timestamp in the user's timezone and locale.",
     REF, "#message-formatting", SNAPSHOT, conf="inferred")

rule("rule.fmt-timestamp-styles", "Timestamp styles: t, T, d, D, f (default), F, s, S, R (relative)", "area.formatting",
     "Styles: t short time, T medium time, d short date, D long date, f long date with short time (the default), F full date, s short date and time, S short date and medium time, R relative like '4 years ago'.",
     "| t     | 16:20                            | Short Time              |\n| T     | 16:20:30                         | Medium Time             |\n| d     | 20/04/2021                       | Short Date              |\n| D     | April 20, 2021                   | Long Date               |\n| f \\*  | April 20, 2021 at 16:20          | Long Date, Short Time   |\n| F     | Tuesday, April 20, 2021 at 16:20 | Full Date, Short Time   |\n| s     | 20/04/2021, 16:20                | Short Date, Short Time  |\n| S     | 20/04/2021, 16:20:30             | Short Date, Medium Time |\n| R     | 4 years ago                      | Relative Time           |",
     REF, "#message-formatting-timestamp-styles", SNAPSHOT, conf="inferred")

rule("rule.fmt-slash-command-mention", "Slash command mentions: </name:command_id>, clickable since August 22, 2022", "area.formatting",
     "Write </name:COMMAND_ID> (or </name subcommand:ID>) to render a clickable command mention. Plain /name is just text. The change log dates the rollout to the week of August 22, 2022.",
     "| Slash command                       | `</NAME:COMMAND_ID>`                     | `</airhorn:816437322781949972>`       |",
     REF, "#message-formatting", "2022-08-22", conf="inferred")

# ---- channel names and counts
CH = "source.channel-resource"
rule("rule.channel-name-1-100", "Channel names are 1 to 100 characters", "area.formatting",
     "A channel name must be between 1 and 100 characters. Emoji, symbols and other Unicode count toward the 100. The docs give no other constraint on the name.",
     "the name of the channel (1-100 characters)",
     CH, "#channel-object-channel-structure", SNAPSHOT, conf="inferred")

rule("rule.channel-topic-limits", "Channel topic: 0 to 1024 characters, 0 to 4096 for forum and media channels", "area.formatting",
     "Topics are capped at 1024 characters on normal channels and 4096 on GUILD_FORUM and GUILD_MEDIA channels.",
     "the channel topic (0-4096 characters for `GUILD_FORUM` and `GUILD_MEDIA` channels, 0-1024 characters for all others)",
     CH, "#channel-object-channel-structure", SNAPSHOT, conf="inferred")

rule("rule.category-50-channels-docs", "A category holds at most 50 channels", "area.formatting",
     "Each parent category can contain up to 50 channels. Past that, create another category.",
     "an organizational category that contains up to 50 channels",
     CH, "#channel-object-channel-types (GUILD_CATEGORY)", SNAPSHOT, conf="inferred")

rule("rule.create-channel-name-1-100", "Create Guild Channel: name is the only required field, 1 to 100 characters", "area.formatting",
     "POST /guilds/{id}/channels needs MANAGE_CHANNELS and a name of 1 to 100 characters; every other parameter is optional.",
     "channel name (1-100 characters)",
     "source.guild-resource", "#create-guild-channel-json-params", SNAPSHOT, conf="inferred")

rule("rule.max-500-channels-docs", "Error 30013: a server can have at most 500 channels", "area.formatting",
     "Creating a channel past 500 fails with JSON error code 30013. The 500 counts every channel type, and categories count too according to the support caps table.",
     "Maximum number of guild channels reached (500)",
     "source.opcodes", "#json-error-codes", SNAPSHOT, conf="inferred")

rule("rule.caps-categories-50", "Caps table: 50 categories per server, 500 channels including categories, 50 channels per category", "area.formatting",
     "The support caps table says a server can have 50 categories, 500 channels in total (voice, text and categories all count) and at most 50 channels in one category.",
     "| Server categories | 50 | Same | Same | Same |",
     "source.server-caps", "Server Caps", "2026-03-02", conf="inferred",
     conflicts=["rule.error-30030-categories-5"], resolution=RES_C11, cid="C11")

rule("rule.error-30030-categories-5", "Error 30030 says the category maximum is 5, which contradicts the support caps table", "area.formatting",
     "The docs error table gives 5 as the category maximum for code 30030 with no explanation. The support caps table says 50. Treat 50 as the working number and expect 30030 as the error when a category create is refused.",
     "Maximum number of server categories has been reached (5)",
     "source.opcodes", "#json-error-codes", SNAPSHOT, conf="inferred",
     conflicts=["rule.caps-categories-50"], resolution=RES_C11, cid="C11")

rule("rule.text-channel-lowercase-no-spaces", "Text channel names: no capital letters or spaces, most Unicode allowed (undocumented, GitHub record only)", "area.formatting",
     "No Discord page states it, but text channel names cannot contain capital letters or spaces (the client and API turn them into lowercase and hyphens), while most Unicode symbols and emoji are accepted. The only written record we hold is a 2020 GitHub feature request that Discord closed as a product matter. Voice channel and category names are not lowercased.",
     "Discord has already permitted most of Unicode to be used in text channel names, so it seems quite arbitrary that capital letters and spaces are still banned.",
     "source.gh-1646", "issue body", "2020-05-18", conf="inferred")

# ---- community naming convention (not a Discord rule)
rule("rule.convention-emoji-separator-name", "Community convention: emoji + separator + lowercase name, for example 👋┆welcome", "area.formatting",
     "Community convention, not a Discord rule: put an emoji first, then a separator, then the lowercase hyphenated name. Examples: 👋┆welcome, 🔴・live-now. The only Discord rules underneath are 1 to 100 characters and, for text channels, no capitals or spaces.",
     "📜 • rules",
     "source.emojidb-channel-symbols", "symbol list", SNAPSHOT, conf="inferred")

rule("rule.convention-separators", "Community convention: common separators are ┆ ・ │ ︱ ⋆ ✦ (also ┃ and 〢)", "area.formatting",
     "Community convention, not a Discord rule: the usual separators between emoji and name are ┆ ・ │ ︱ ⋆ ✦, with ┃ and 〢 also common. They are ordinary Unicode characters, so Discord accepts them and each counts as one of the 100 characters. Pick one and use it for every channel.",
     "┃\n・\n│\nㆍ",
     "source.emojidb-channel-symbols", "symbol list (first entries)", SNAPSHOT, conf="inferred")

rule("rule.convention-channel-emojis", "Community convention: common channel emoji are 💬 📢 📜 🔊 👋 📸 🚨 🎮 📝 🤖", "area.formatting",
     "Community convention, not a Discord rule: 💬 chat, 📢 announcements, 📜 rules, 🔊 voice, 👋 welcome, 📸 media, 🚨 alerts, 🎮 gaming, 📝 notes, 🤖 bots, ✅ verification. Examples on the page: 👋 | WELCOME and ✅┃Verification; remember a text channel will lowercase those.",
     "┃\n・\n💬\n📢\n│",
     "source.emojidb-channel-emojis", "emoji list (first entries)", SNAPSHOT, conf="inferred")

# ---- questions
question("question.q26", "My ## header shows as literal text in the message. Why?",
         {"asOf": ASOF},
         "Because there is no space after the hashes. Discord only renders a header when the line starts with #, ## or ### followed by a space ('## Rules', not '##Rules'), and the hashes must be the first characters on the line. Same rule for -# subtext, > block quotes and - list bullets. Source: Markdown Text 101 (user support, edited 2025-04-23).",
         ["rule.md-header-space", "rule.md-subtext"],
         note="Formatting area. The answer is one missing space.")

question("question.q27", "What is the maximum number of characters in an embed description, and in the whole embed?",
         {"asOf": ASOF},
         "Description: 4096 characters. Per embed: title 256, up to 25 fields with name 256 and value 1024, footer 2048, author name 256. Across all embeds on one message the sum of those text fields must not exceed 6000 characters, and a message carries at most 10 embeds; break either and the API returns 400 Bad Request. Limits are inclusive and whitespace is trimmed first. Source: Message resource, Embed Limits (developer docs, undated, snapshot 2026-09-19).",
         ["rule.embed-field-limits", "rule.embed-total-6000", "rule.api-10-embeds-6000"])

question("question.q28", "Can a text channel name have spaces or capital letters?",
         {"asOf": ASOF},
         "No. The documented rule is only 1 to 100 characters (Channels resource), but text channel names are lowercased and spaces become hyphens; no Discord page states that, the only written record is GitHub issue 1646 (2020), so say 'inferred'. Emoji and Unicode symbols are accepted and count toward the 100. Voice channels and categories keep capitals and spaces.",
         ["rule.channel-name-1-100", "rule.text-channel-lowercase-no-spaces"],
         note="The agent must flag that the lowercase rule is undocumented.")

question("question.q29", "How many channels and categories can my server have?",
         {"asOf": ASOF},
         "500 channels in total, counting text, voice and categories (error 30013 and the support caps table); at most 50 channels inside one category (Channels resource); 50 categories per server per the caps table, although the docs error code 30030 says 5 with no explanation (contradiction C11). Plan for 50 categories and cite both.",
         ["rule.max-500-channels-docs", "rule.category-50-channels-docs", "rule.caps-categories-50", "rule.error-30030-categories-5"],
         note="Contradiction C11 must be surfaced.")

question("question.q30", "My bot sends a 3000 character message and gets a 400. A user says Nitro allows 4000, so why not for my bot?",
         {"asOf": ASOF},
         "The bot API caps content at 2000 characters (Create Message params). The 4000 limit is a Nitro user perk in the client and does not apply to apps. Split the text, put up to 4096 characters in an embed description, or attach a file.",
         ["rule.api-content-2000", "rule.message-4000-nitro", "rule.embed-field-limits"],
         note="Nitro is a user perk, not an API change.")

question("question.q31", "How do I show a time that renders in each reader's own timezone, like 'in 2 hours'?",
         {"asOf": ASOF},
         "Use <t:UNIX_SECONDS:R> for relative ('in 2 hours'), or another style letter: t, T, d, D, f (default), F, s, S. The number must be Unix seconds, not milliseconds. Source: API Reference, Message Formatting (developer docs, undated, snapshot 2026-09-19).",
         ["rule.fmt-timestamps", "rule.fmt-timestamp-styles"])

question("question.q32", "Write a welcome message for my server with a header, a rules list and a spoiler.",
         {"asOf": ASOF},
         "A message in a ```md code block such as:\n# Welcome to the server\n-# Read this once, it takes a minute.\n\n**Rules**\n- Be kind, no harassment.\n- No spam or self promotion.\n- Keep NSFW out of every channel.\n\n> Questions go to <#CHANNEL_ID>.\n\n||The mods are watching, but they are friendly.||\n\nfollowed by one line per rule applied with its source link (header needs a space, -# subtext, - list bullets, > block quote, ||spoiler||) and a character count against the 2000 limit (4000 only for Nitro users, never for bots).",
         ["rule.md-header-space", "rule.md-subtext", "rule.md-lists", "rule.md-block-quote", "rule.md-spoiler", "rule.api-content-2000"],
         note="Draft request. Graded on correct syntax in a copyable code block, rule citations and a character count.")

question("question.q33", "Give me channel names for a crypto community server: welcome, rules, announcements, live streams, general chat, trading, memes",
         {"asOf": ASOF},
         "A channel list in a ```md code block using the community convention emoji + separator + lowercase name, for example 👋┆welcome, 📜┆rules, 📢┆announcements, 🔴┆live-streams, 💬┆general-chat, 📈┆trading, 😂┆memes, under category headers in caps (INFO, COMMUNITY). It must state the Discord constraints it respected: 1 to 100 characters (Channels resource), text channel names lowercase with hyphens and no spaces (undocumented, GitHub 1646, inferred), 50 channels per category and 500 per server, and mark the emoji and separator choice as community convention, not a Discord rule.",
         ["rule.channel-name-1-100", "rule.text-channel-lowercase-no-spaces", "rule.convention-emoji-separator-name", "rule.convention-separators", "rule.convention-channel-emojis", "rule.category-50-channels-docs"],
         note="Draft request. The answer must separate Discord rules from taste.")

FORMATTING_DOCS = [d for d in docs if d["_id"] == "area.formatting"] + docs[FORMATTING_START:]


# ---------------------------------------------------------------- write
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for d in docs:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

OUT_FMT = os.path.join(HERE, "seed-formatting.ndjson")
with open(OUT_FMT, "w", encoding="utf-8", newline="\n") as f:
    for d in FORMATTING_DOCS:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")

from collections import Counter
print("wrote", OUT)
print(Counter(d["_type"] for d in docs))
print("wrote", OUT_FMT, "(formatting area only)")
print(Counter(d["_type"] for d in FORMATTING_DOCS))
