import type {Metadata} from 'next'
import {Inter, JetBrains_Mono} from 'next/font/google'
import './globals.css'

const body = Inter({variable: '--font-body', subsets: ['latin']})
const code = JetBrains_Mono({variable: '--font-code', subsets: ['latin']})

export const metadata: Metadata = {
  title: 'Bot Lawyer',
  description:
    'Counsel for Discord bot developers. Rulings with the exact quote, the page it came from and the date it took effect, served from Sanity Context.',
}

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en" className={`${body.variable} ${code.variable} h-full`}>
      <body className="h-full overflow-hidden">{children}</body>
    </html>
  )
}
