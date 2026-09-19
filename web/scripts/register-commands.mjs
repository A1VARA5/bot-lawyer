// Registers the /ask slash command. Guild scoped so it appears instantly in Aivaras's server.
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

const res = await fetch(`https://discord.com/api/v10/applications/${appId}/guilds/${guild}/commands`, {
  method: 'PUT',
  headers: {Authorization: `Bot ${token}`, 'Content-Type': 'application/json'},
  body: JSON.stringify(commands),
})
console.log(res.status, (await res.json()).map?.((c) => c.name) ?? (await res.text()))
