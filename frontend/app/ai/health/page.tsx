"use client";

import { useState, useEffect } from "react";

interface HealthStatus {
  status: string;
  components: { [key: string]: string };
  timestamp: string;
}

interface Metrics {
  total_executions: number;
  success_rate: number;
  total_cost_usd: number;
  average_execution_time_ms: number;
}

export default function HealthPage() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [healthRes, metricsRes] = await Promise.all([
        fetch("/api/ai/health"),
        fetch("/api/ai/metrics"),
      ]);
      const healthData = await healthRes.json();
      const metricsData = await metricsRes.json();
      setHealth(healthData);
      setMetrics(metricsData);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "text-green-400 bg-green-400/10";
      case "degraded":
        return "text-yellow-400 bg-yellow-400/10";
      case "unhealthy":
        return "text-red-400 bg-red-400/10";
      default:
        return "text-gray-400 bg-gray-400/10";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "healthy":
        return "✓";
      case "degraded":
        return "⚠";
      case "unhealthy":
        return "✕";
      default:
        return "?";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">System Health</h1>
          <p className="text-gray-400 mt-2">
            Real-time monitoring of AI system components
          </p>
        </div>

        {/* Overall Status */}
        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">Overall System Status</h2>
              <p className="text-gray-400 text-sm mt-1">
                Last updated:{" "}
                {health?.timestamp
                  ? new Date(health.timestamp).toLocaleString()
                  : "Never"}
              </p>
            </div>
            <div
              className={`px-4 py-2 rounded-lg font-semibold ${getStatusColor(health?.status || "unknown")}`}
            >
              {getStatusIcon(health?.status || "unknown")}{" "}
              {health?.status?.toUpperCase() || "UNKNOWN"}
            </div>
          </div>
        </div>

        {/* Components Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {health?.components &&
            Object.entries(health.components).map(([name, status]) => (
              <div
                key={name}
                className="bg-gray-800 rounded-lg p-4 flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-10 h-10 rounded-lg flex items-center justify-center ${getStatusColor(status)}`}
                  >
                    {getStatusIcon(status)}
                  </div>
                  <div>
                    <h3 className="font-medium capitalize">{name}</h3>
                    <p className="text-sm text-gray-400">{status}</p>
                  </div>
                </div>
              </div>
            ))}
        </div>

        {/* Metrics */}
        {metrics && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">System Metrics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <MetricCard
                label="Total Executions"
                value={metrics.total_executions.toString()}
                icon="🔄"
              />
              <MetricCard
                label="Success Rate"
                value={`${(metrics.success_rate * 100).toFixed(1)}%`}
                icon="✅"
              />
              <MetricCard
                label="Total Cost"
                value={`$${metrics.total_cost_usd.toFixed(4)}`}
                icon="💰"
              />
              <MetricCard
                label="Avg Execution Time"
                value={`${metrics.average_execution_time_ms.toFixed(0)}ms`}
                icon="⚡"
              />
            </div>
          </div>
        )}

        {/* Refresh Button */}
        <div className="mt-6 text-center">
          <button
            onClick={fetchData}
            className="bg-gray-800 hover:bg-gray-700 px-6 py-3 rounded-lg transition-colors"
          >
            Refresh Status
          </button>
        </div>
      </div>
    </div>
  );
}

function MetricCard({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon: string;
}) {
  return (
    <div className="text-center">
      <div className="text-3xl mb-2">{icon}</div>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-sm text-gray-400">{label}</div>
    </div>
  );
}
