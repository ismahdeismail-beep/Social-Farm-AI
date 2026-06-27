'use client'

import { useState } from 'react'

export default function ExplorerPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!searchTerm.trim()) return
    setLoading(true)
    try {
      const res = await fetch(`/api/research/search?q=${encodeURIComponent(searchTerm)}`)
      const data = await res.json()
      setResults(Array.isArray(data) ? data : [])
    } catch {
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-800 p-4">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <a href="/research" className="text-gray-400 hover:text-white">← Back</a>
          <h1 className="text-2xl font-bold">Research Explorer</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-6">
        <div className="flex gap-3 mb-8">
          <input
            type="text"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            placeholder="Search research data..."
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
          />
          <button
            onClick={handleSearch}
            className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Search
          </button>
        </div>
        {loading ? (
          <p className="text-gray-400">Searching...</p>
        ) : results.length > 0 ? (
          <div className="space-y-3">
            {results.map((r, i) => (
              <div key={i} className="bg-gray-800 rounded-lg p-4">
                <p className="font-medium">{r.title || r.query || 'Result'}</p>
                <p className="text-gray-400 text-sm mt-1">{r.description || r.summary || ''}</p>
              </div>
            ))}
          </div>
        ) : searchTerm ? (
          <div className="bg-gray-800 rounded-lg p-8 text-center">
            <p className="text-gray-400">No results found.</p>
          </div>
        ) : (
          <div className="bg-gray-800 rounded-lg p-8 text-center">
            <p className="text-gray-400">Enter a search term to explore research data.</p>
          </div>
        )}
      </main>
    </div>
  )
}
