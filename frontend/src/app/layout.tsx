import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Auditor Job Posting Agent',
  description: 'AI-powered job posting analysis and outreach system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-white shadow-sm border-b">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-8">
                <h1 className="text-xl font-bold text-gray-900">
                  Auditor Job Agent
                </h1>
                <div className="hidden md:flex space-x-6">
                  <Link 
                    href="/" 
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    Dashboard
                  </Link>
                  <Link 
                    href="/jobs" 
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    Jobs
                  </Link>
                  <Link 
                    href="/matches" 
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    Matches
                  </Link>
                  <Link 
                    href="/outreach" 
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    Outreach
                  </Link>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">System Online</span>
              </div>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  )
}