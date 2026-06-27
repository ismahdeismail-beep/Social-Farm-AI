"use client";

import { useState, useEffect } from "react";

interface Model {
  provider: string;
  model_id: string;
  display_name: string;
  cost_per_1k_tokens: number;
  average_latency_ms: number;
  quality_score: number;
  capabilities: string[];
}

export default function ModelsPage() {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedProvider, setSelectedProvider] = useState<string>("all");

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await fetch("/api/ai/models");
      const data = await response.json();
      setModels(data);
    } catch (error) {
      console.error("Failed to fetch models:", error);
    } finally {
      setLoading(false);
    }
  };

  const providers = ["all", ...new Set(models.map((m) => m.provider))];
  const filteredModels =
    selectedProvider === "all"
      ? models
      : models.filter((m) => m.provider === selectedProvider);

  const getProviderColor = (provider: string) => {
    switch (provider) {
      case "openai":
        return "bg-green-600";
      case "anthropic":
        return "bg-orange-600";
      case "google":
        return "bg-blue-600";
      default:
        return "bg-gray-600";
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
          <h1 className="text-3xl font-bold">AI Models</h1>
          <p className="text-gray-400 mt-2">
            Available models across all providers
          </p>
        </div>

        {/* Provider Filter */}
        <div className="mb-6 flex gap-2">
          {providers.map((provider) => (
            <button
              key={provider}
              onClick={() => setSelectedProvider(provider)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedProvider === provider
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-400 hover:bg-gray-700"
              }`}
            >
              {provider === "all" ? "All Providers" : provider}
            </button>
          ))}
        </div>

        {/* Models Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredModels.map((model) => (
            <div
              key={`${model.provider}:${model.model_id}`}
              className="bg-gray-800 rounded-lg p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-semibold text-lg">{model.display_name}</h3>
                  <p className="text-sm text-gray-400 font-mono">
                    {model.model_id}
                  </p>
                </div>
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${getProviderColor(model.provider)}`}
                >
                  {model.provider}
                </span>
              </div>

              <div className="space-y-3 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Cost (per 1K tokens)</span>
                  <span className="font-mono">
                    ${model.cost_per_1k_tokens.toFixed(4)}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Avg Latency</span>
                  <span>{model.average_latency_ms}ms</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Quality Score</span>
                  <span>{(model.quality_score * 100).toFixed(0)}%</span>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-400 mb-2">Capabilities</p>
                <div className="flex flex-wrap gap-2">
                  {model.capabilities.map((cap) => (
                    <span
                      key={cap}
                      className="px-2 py-1 bg-gray-700 rounded text-xs"
                    >
                      {cap}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
