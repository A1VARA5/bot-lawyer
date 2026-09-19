// Small in-memory limiter so a public demo on a test key cannot be drained by one visitor.
// Per serverless instance, so it is a speed bump, not a wall. Good enough for a hackathon demo.
const WINDOW_MS = 60_000
const MAX_PER_WINDOW = 6
const buckets = new Map<string, number[]>()

export function checkRateLimit(req: Request): Response | null {
  const ip =
    req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ||
    req.headers.get('x-real-ip') ||
    'local'
  const now = Date.now()
  const hits = (buckets.get(ip) ?? []).filter((t) => now - t < WINDOW_MS)
  if (hits.length >= MAX_PER_WINDOW) {
    return new Response(
      JSON.stringify({error: 'Counsel is with another client. Six questions a minute, please.'}),
      {status: 429, headers: {'Content-Type': 'application/json', 'Retry-After': '60'}},
    )
  }
  hits.push(now)
  buckets.set(ip, hits)
  if (buckets.size > 5000) buckets.clear()
  return null
}
