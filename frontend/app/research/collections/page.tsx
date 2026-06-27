'use client'

import { useState, useEffect } from 'react'

interface Collection {
  id: string
  name: string
  description: string
  query_count: number
}

export default function CollectionsPage() {
  const [collections, setCollections] = useState<Collection[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/research/collections')
      .then(res => res.json())
      .then(data => setCollections(Array.isArray(data) ? data : []))
      .catch(() => setCollections([]))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-800 p-4">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <a href="/research" className="text-gray-400 hover:text-white">← Back</a>
          <h1 className="text-2xl font-bold">Research Collections</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-6">
        {loading ? (
          <p className="text-gray-400">Loading collections...</p>
        ) : collections.length === 0 ? (
          <div className="bg-gray-800 rounded-lg p-8 text-center">
            <p className="text-gray-400">No collections yet. Start a research query to create one.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {collections.map(c => (
              <div key={c.id} className="bg-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-2">{c.name}</h3>
                <p className="text-gray-400 text-sm mb-4">{c.description}</p>
                <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                  {c.query_count} queries
                </span>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
