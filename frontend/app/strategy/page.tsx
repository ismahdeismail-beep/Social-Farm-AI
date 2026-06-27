"use client";

import { useState, useEffect } from "react";

interface Strategy {
  strategy_id: string;
  name: string;
  vision: string;
  goals: Array<{ name: string; metric: string; target_value: number }>;
  kpis: Array<{ metric: string; target: number; unit: string }>;
  content_pillars: Array<{ name: string; description: string }>;
  confidence_score: number;
  status: string;
  created_at: string;
}

export default function StrategyDashboard() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [selectedStrategy, setSelectedStrategy] = useState<Strategy | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [showGenerateModal, setShowGenerateModal] = useState(false);

  useEffect(() => {
    loadStrategies();
  }, []);

  const loadStrategies = async () => {
    try {
      const response = await fetch("/api/strategy/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      });
      if (response.ok) {
        const data = await response.json();
        setStrategies(data);
        if (data.length > 0) setSelectedStrategy(data[0]);
      }
    } catch (error) {
      console.error("Failed to load strategies:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateStrategy = async (params: any) => {
    setGenerating(true);
    try {
      const response = await fetch("/api/strategy/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(params)
      });

      if (response.ok) {
        const strategy = await response.json();
        setStrategies(prev => [strategy, ...prev]);
        setSelectedStrategy(strategy);
        setShowGenerateModal(false);
      }
    } catch (error) {
      console.error("Failed to generate strategy:", error);
    } finally {
      setGenerating(false);
    }
  };

  const approveStrategy = async (strategyId: string) => {
    try {
      const response = await fetch(`/api/strategy/approve?strategy_id=${strategyId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify({ approved: true })
      });

      if (response.ok) {
        loadStrategies();
      }
    } catch (error) {
      console.error("Failed to approve strategy:", error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">Content Strategy</h1>
            <p className="text-gray-400 mt-1">Autonomous CMO - Strategic Planning</p>
          </div>
          <button
            onClick={() => setShowGenerateModal(true)}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition"
          >
            + Generate Strategy
          </button>
        </div>

        <div className="grid grid-cols-12 gap-6">
          {/* Strategy List */}
          <div className="col-span-3 bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-4">Strategies</h2>
            <div className="space-y-2">
              {strategies.map((strategy) => (
                <button
                  key={strategy.strategy_id}
                  onClick={() => setSelectedStrategy(strategy)}
                  className={`w-full text-left p-3 rounded-lg transition ${
                    selectedStrategy?.strategy_id === strategy.strategy_id
                      ? "bg-blue-600"
                      : "bg-gray-700 hover:bg-gray-600"
                  }`}
                >
                  <div className="font-medium text-sm">{strategy.name}</div>
                  <div className="text-xs text-gray-400 mt-1">
                    Confidence: {(strategy.confidence_score * 100).toFixed(0)}%
                  </div>
                </button>
              ))}
              {strategies.length === 0 && (
                <p className="text-gray-500 text-sm">No strategies yet</p>
              )}
            </div>
          </div>

          {/* Strategy Details */}
          <div className="col-span-9 space-y-6">
            {selectedStrategy ? (
              <>
                {/* Vision & Mission */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-2xl font-bold">{selectedStrategy.name}</h2>
                      <p className="text-gray-400 mt-2">{selectedStrategy.vision}</p>
                    </div>
                    <div className="flex gap-2">
                      <span className="px-3 py-1 bg-green-600 rounded-full text-sm">
                        {(selectedStrategy.confidence_score * 100).toFixed(0)}% Confidence
                      </span>
                      <button
                        onClick={() => approveStrategy(selectedStrategy.strategy_id)}
                        className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-sm transition"
                      >
                        Approve
                      </button>
                    </div>
                  </div>
                </div>

                {/* KPIs */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Key Performance Indicators</h3>
                  <div className="grid grid-cols-4 gap-4">
                    {selectedStrategy.kpis.map((kpi, idx) => (
                      <div key={idx} className="bg-gray-700 rounded-lg p-4">
                        <div className="text-gray-400 text-sm">{kpi.metric}</div>
                        <div className="text-2xl font-bold mt-1">
                          {kpi.target.toLocaleString()} {kpi.unit}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Content Pillars */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Content Pillars</h3>
                  <div className="grid grid-cols-3 gap-4">
                    {selectedStrategy.content_pillars.map((pillar, idx) => (
                      <div key={idx} className="bg-gray-700 rounded-lg p-4">
                        <div className="font-medium">{pillar.name}</div>
                        <div className="text-sm text-gray-400 mt-1">{pillar.description}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Goals */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Strategic Goals</h3>
                  <div className="space-y-3">
                    {selectedStrategy.goals.map((goal, idx) => (
                      <div key={idx} className="flex items-center justify-between bg-gray-700 rounded-lg p-4">
                        <div>
                          <div className="font-medium">{goal.name}</div>
                          <div className="text-sm text-gray-400">{goal.metric}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-bold text-blue-400">
                            {goal.target_value.toLocaleString()}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-gray-800 rounded-lg p-12 text-center">
                <div className="text-gray-500 text-lg">No strategy selected</div>
                <p className="text-gray-600 mt-2">Generate a new strategy to get started</p>
              </div>
            )}
          </div>
        </div>

        {/* Generate Modal */}
        {showGenerateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
              <h2 className="text-xl font-bold mb-4">Generate New Strategy</h2>
              <GenerateStrategyForm
                onGenerate={generateStrategy}
                onCancel={() => setShowGenerateModal(false)}
                loading={generating}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function GenerateStrategyForm({
  onGenerate,
  onCancel,
  loading
}: {
  onGenerate: (params: any) => void;
  onCancel: () => void;
  loading: boolean;
}) {
  const [formData, setFormData] = useState({
    brand_id: "default",
    strategy_type: "quarterly",
    start_date: new Date().toISOString().split("T")[0],
    end_date: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
    goals: ["Increase brand awareness", "Drive engagement"],
    budget_usd: 10000,
    target_platforms: ["instagram", "tiktok"],
    industry: "agriculture"
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate({
      ...formData,
      start_date: new Date(formData.start_date).toISOString(),
      end_date: new Date(formData.end_date).toISOString()
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm text-gray-400 mb-1">Strategy Type</label>
        <select
          value={formData.strategy_type}
          onChange={(e) => setFormData({ ...formData, strategy_type: e.target.value })}
          className="w-full bg-gray-700 rounded-lg px-4 py-2"
        >
          <option value="quarterly">Quarterly</option>
          <option value="monthly">Monthly</option>
          <option value="campaign">Campaign</option>
          <option value="always_on">Always-On</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Start Date</label>
          <input
            type="date"
            value={formData.start_date}
            onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
            className="w-full bg-gray-700 rounded-lg px-4 py-2"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">End Date</label>
          <input
            type="date"
            value={formData.end_date}
            onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
            className="w-full bg-gray-700 rounded-lg px-4 py-2"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm text-gray-400 mb-1">Budget (USD)</label>
        <input
          type="number"
          value={formData.budget_usd}
          onChange={(e) => setFormData({ ...formData, budget_usd: Number(e.target.value) })}
          className="w-full bg-gray-700 rounded-lg px-4 py-2"
        />
      </div>

      <div>
        <label className="block text-sm text-gray-400 mb-1">Target Platforms</label>
        <div className="flex gap-2">
          {["instagram", "tiktok", "youtube", "linkedin", "facebook"].map((platform) => (
            <button
              key={platform}
              type="button"
              onClick={() => {
                const platforms = formData.target_platforms.includes(platform)
                  ? formData.target_platforms.filter((p) => p !== platform)
                  : [...formData.target_platforms, platform];
                setFormData({ ...formData, target_platforms: platforms });
              }}
              className={`px-3 py-1 rounded-full text-sm transition ${
                formData.target_platforms.includes(platform)
                  ? "bg-blue-600"
                  : "bg-gray-700 hover:bg-gray-600"
              }`}
            >
              {platform}
            </button>
          ))}
        </div>
      </div>

      <div className="flex gap-4 mt-6">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition disabled:opacity-50"
        >
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>
    </form>
  );
}
