"use client";

import { useState, useEffect } from "react";

interface Agent {
  id: string;
  name: string;
  display_name: string;
  agent_type: string;
  status: string;
  health_status: string;
  active_executions: number;
  success_rate: number;
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch("/api/ai/agents");
      const data = await response.json();
      setAgents(data);
    } catch (error) {
      console.error("Failed to fetch agents:", error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "bg-green-500";
      case "degraded":
        return "bg-yellow-500";
      case "unhealthy":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  const getAgentIcon = (type: string) => {
    switch (type) {
      case "trend":
        return "📈";
      case "research":
        return "🔍";
      case "script":
        return "📝";
      case "media":
        return "🎨";
      case "publishing":
        return "📤";
      case "analytics":
        return "📊";
      case "quality":
        return "✅";
      case "orchestrator":
        return "🧠";
      default:
        return "🤖";
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
          <h1 className="text-3xl font-bold">AI Agents</h1>
          <p className="text-gray-400 mt-2">
            Monitor and manage all registered AI agents
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{getAgentIcon(agent.agent_type)}</span>
                  <div>
                    <h3 className="font-semibold text-lg">{agent.display_name}</h3>
                    <p className="text-sm text-gray-400">{agent.agent_type}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div
                    className={`w-3 h-3 rounded-full ${getHealthColor(agent.health_status)}`}
                  ></div>
                  <span className="text-sm capitalize">{agent.health_status}</span>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Status</span>
                  <span
                    className={
                      agent.status === "active" ? "text-green-400" : "text-gray-500"
                    }
                  >
                    {agent.status}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Active Executions</span>
                  <span>{agent.active_executions}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Success Rate</span>
                  <span>{(agent.success_rate * 100).toFixed(1)}%</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-700">
                <button className="w-full bg-gray-700 hover:bg-gray-600 py-2 rounded-lg text-sm transition-colors">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
