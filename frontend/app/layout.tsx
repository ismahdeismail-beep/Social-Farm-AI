import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Social Farm AI OS',
  description:
    'AI-powered social media content creation, research, trend intelligence, planning, publishing, analytics, and multi-agent orchestration platform.',
  keywords: [
    'ai',
    'social-media',
    'content-creation',
    'fastapi',
    'nextjs',
    'automation',
    'analytics',
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-900 text-white antialiased">
        {children}
      </body>
    </html>
  )
}
