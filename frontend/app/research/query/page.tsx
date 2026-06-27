'use client'

import { useState } from 'react'

export default function QueryPage() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!query.trim()) return
    setLoading(true)
    setResult(null)
    try {
      const res = await fetch('/api/research/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      const data = await res.json()
      setResult(data.result || data.detail || 'Query submitted successfully')
    } catch {
      setResult('Failed to submit query. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-800 p-4">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <a href="/research" className="text-gray-400 hover:text-white">← Back</a>
          <h1 className="text-2xl font-bold">Research Query</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto p-6">
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <label className="block text-sm font-medium text-gray-300 mb-2">Research Question</label>
          <textarea
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Describe what you want to research..."
            rows={4}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-green-500 resize-none"
          />
          <button
            onClick={handleSubmit}
            disabled={loading || !query.trim()}
            className="mt-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-medium transition-colors"
          >
            {loading ? 'Researching...' : 'Start Research'}
          </button>
        </div>
        {result && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-3">Result</h2>
            <p className="text-gray-300 whitespace-pre-wrap">{result}</p>
          </div>
        )}
      </main>
    </div>
  )
}
