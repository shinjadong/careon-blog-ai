import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CareOn Blog Automation - Admin Dashboard',
  description: 'Production-grade mobile blog automation system',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className="antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  )
}
