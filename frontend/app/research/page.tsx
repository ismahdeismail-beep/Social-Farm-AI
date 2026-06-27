'use client'

import { useState, useEffect } from 'react'

interface ResearchQuery {
  id: string
  query: string
  status: string
  created_at: string
}

export default function ResearchPage() {
  const [queries, setQueries] = useState<ResearchQuery[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/research/queries')
      .then(res => res.json())
      .then(data => setQueries(Array.isArray(data) ? data : []))
      .catch(() => setQueries([]))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-800 p-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold">Research Engine</h1>
          <p className="text-gray-400 text-sm">Deep research and trend intelligence</p>
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <a href="/research/query" className="bg-gray-800 rounded-lg p-6 hover:ring-1 hover:ring-green-500 transition-all">
            <h3 className="text-lg font-semibold mb-2">New Query</h3>
            <p className="text-gray-400 text-sm">Start a deep research query</p>
          </a>
          <a href="/research/collections" className="bg-gray-800 rounded-lg p-6 hover:ring-1 hover:ring-green-500 transition-all">
            <h3 className="text-lg font-semibold mb-2">Collections</h3>
            <p className="text-gray-400 text-sm">Browse research collections</p>
          </a>
          <a href="/research/explorer" className="bg-gray-800 rounded-lg p-6 hover:ring-1 hover:ring-green-500 transition-all">
            <h3 className="text-lg font-semibold mb-2">Explorer</h3>
            <p className="text-gray-400 text-sm">Explore research data</p>
          </a>
        </div>
        <h2 className="text-xl font-bold mb-4">Recent Queries</h2>
        {loading ? (
          <p className="text-gray-400">Loading...</p>
        ) : queries.length === 0 ? (
          <div className="bg-gray-800 rounded-lg p-8 text-center">
            <p className="text-gray-400">No research queries yet. Start your first query!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {queries.map(q => (
              <div key={q.id} className="bg-gray-800 rounded-lg p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium">{q.query}</p>
                  <p className="text-gray-400 text-sm">{q.created_at}</p>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${q.status === 'completed' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'}`}>
                  {q.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
