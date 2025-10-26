import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'NASA EONET Dashboard | Natural Event Tracker',
  description: 'Real-time monitoring of global natural disasters including wildfires, storms, volcanoes, and more. Powered by NASA Earth Observatory Natural Event Tracker (EONET)',
  keywords: 'NASA, EONET, natural disasters, wildfires, climate, data visualization, earth observatory',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}