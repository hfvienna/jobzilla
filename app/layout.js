// app/layout.js

import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Jobzilla',
  description: 'Jobzilla stomps onto the job search scene, ferociously sniffing out opportunities like a wild beast on the hunt, aggressively tracking down opportunities and crushing its competition with its monstrous AI might.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" data-theme="light">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
