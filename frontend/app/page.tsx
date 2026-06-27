'use client'

import { useState, useEffect } from 'react'

interface HealthStatus {
  status: string
  components?: Record<string, string>
}

export default function HomePage() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/ai/health')
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch(() => setHealth({ status: 'unavailable' }))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Social Farm AI OS</h1>
            <p className="text-gray-400 text-sm">
              Intelligent Content Operations Platform
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span
              className={`inline-block w-2 h-2 rounded-full ${
                health?.status === 'healthy'
                  ? 'bg-green-500'
                  : health?.status === 'degraded'
                    ? 'bg-yellow-500'
                    : loading
                      ? 'bg-gray-500'
                      : 'bg-red-500'
              }`}
            />
            <span className="text-sm text-gray-400">
              {loading ? 'Connecting...' : `API: ${health?.status || 'unknown'}`}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6">
        {/* Welcome */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Welcome to Social Farm AI</h2>
          <p className="text-gray-400 text-lg">
            Your AI-powered content operations command center
          </p>
        </div>

        {/* Navigation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* AI Command Center */}
          <a
            href="/ai"
            className="block bg-gray-800 rounded-lg p-6 hover:bg-gray-750 hover:ring-1 hover:ring-blue-500 transition-all group"
          >
            <div className="text-3xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold mb-2 group-hover:text-blue-400 transition-colors">
              AI Command Center
            </h3>
            <p className="text-gray-400 text-sm">
              Orchestrate AI agents, manage models, and monitor system health
            </p>
            <div className="mt-4 flex gap-2">
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Agents
              </span>
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Chat
              </span>
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Models
              </span>
            </div>
          </a>

          {/* Research Engine */}
          <a
            href="/research"
            className="block bg-gray-800 rounded-lg p-6 hover:bg-gray-750 hover:ring-1 hover:ring-green-500 transition-all group"
          >
            <div className="text-3xl mb-4">🔬</div>
            <h3 className="text-xl font-semibold mb-2 group-hover:text-green-400 transition-colors">
              Research Engine
            </h3>
            <p className="text-gray-400 text-sm">
              Deep research, trend analysis, and knowledge management
            </p>
            <div className="mt-4 flex gap-2">
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Queries
              </span>
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Collections
              </span>
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Explorer
              </span>
            </div>
          </a>

          {/* Content Strategy */}
          <a
            href="/strategy"
            className="block bg-gray-800 rounded-lg p-6 hover:bg-gray-750 hover:ring-1 hover:ring-purple-500 transition-all group"
          >
            <div className="text-3xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2 group-hover:text-purple-400 transition-colors">
              Content Strategy
            </h3>
            <p className="text-gray-400 text-sm">
              Plan campaigns, manage calendars, and discover opportunities
            </p>
            <div className="mt-4 flex gap-2">
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Calendar
              </span>
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Campaigns
              </span>
              <span className="text-xs bg-gray-700 rounded-full px-2 py-1 text-gray-300">
                Opportunities
              </span>
            </div>
          </a>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">System Status</div>
            <div className="text-lg font-semibold mt-1">
              {loading ? '...' : health?.status || 'Offline'}
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">AI Agents</div>
            <div className="text-lg font-semibold mt-1">Active</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Version</div>
            <div className="text-lg font-semibold mt-1">0.3.0</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Documentation</div>
            <div className="text-lg font-semibold mt-1">
              <a
                href="/docs"
                className="text-blue-400 hover:text-blue-300 transition-colors"
              >
                View Docs
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
