// Registers the /ask slash command globally (any server that installs the app; can take up to an hour to appear)
// and in Aivaras's guild (instant).
// Usage: node --env-file=.env.local scripts/register-commands.mjs
const appId = process.env.DISCORD_APPLICATION_ID
const token = process.env.DISCORD_BOT_TOKEN
const guild = process.env.DISCORD_GUILD_ID
if (!appId || !token || !guild) throw new Error('DISCORD_APPLICATION_ID, DISCORD_BOT_TOKEN and DISCORD_GUILD_ID are required')

const commands = [
  {
    name: 'ask',
    description: 'Ask Bot Lawyer. Say how many users, which intents, verified or not.',
    options: [
      {type: 3, name: 'question', description: 'Your question, with your situation', required: true, max_length: 500},
      {type: 3, name: 'as_of', description: 'Rule as of a date (YYYY-MM-DD). Time travel.', required: false, max_length: 10},
    ],
  },
]

for (const url of [
  `https://discord.com/api/v10/applications/${appId}/commands`,
  `https://discord.com/api/v10/applications/${appId}/guilds/${guild}/commands`,
]) {
  const res = await fetch(url, {
    method: 'PUT',
    headers: {Authorization: `Bot ${token}`, 'Content-Type': 'application/json'},
    body: JSON.stringify(commands),
  })
  const body = await res.json()
  console.log(res.status, url.includes('/guilds/') ? 'guild' : 'global', Array.isArray(body) ? body.map((c) => c.name) : body)
}
