'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { href: '/research', label: 'Dashboard' },
  { href: '/research/query', label: 'New Query' },
  { href: '/research/collections', label: 'Collections' },
  { href: '/research/explorer', label: 'Explorer' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-gray-800 border-r border-gray-700 min-h-screen p-4">
      <div className="mb-8">
        <h2 className="text-lg font-bold text-green-400">Research Engine</h2>
        <p className="text-xs text-gray-500 mt-1">Social Farm AI</p>
      </div>
      <nav className="space-y-1">
        {navItems.map(item => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block px-3 py-2 rounded-lg text-sm transition-colors ${
                isActive
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-750'
              }`}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-8 pt-4 border-t border-gray-700">
        <Link href="/" className="block px-3 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-gray-750 transition-colors">
          ← Back to Home
        </Link>
      </div>
    </aside>
  )
}
