"use client";

import { useState, useEffect } from "react";

interface Campaign {
  campaign_id: string;
  name: string;
  campaign_type: string;
  objectives: Array<{ type: string; target: number; metric: string }>;
  timeline: Array<{ week: number; phase: string; focus: string }>;
  budget_allocation: Record<string, number>;
  kpis: Array<{ metric: string; target: number; current: number }>;
}

export default function CampaignPlanner() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const response = await fetch("/api/strategy/campaigns", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      });
      if (response.ok) {
        const data = await response.json();
        setCampaigns(data);
        if (data.length > 0) setSelectedCampaign(data[0]);
      }
    } catch (error) {
      console.error("Failed to load campaigns:", error);
    } finally {
      setLoading(false);
    }
  };

  const createCampaign = async (params: any) => {
    try {
      const response = await fetch("/api/strategy/campaigns", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(params)
      });

      if (response.ok) {
        const campaign = await response.json();
        setCampaigns(prev => [campaign, ...prev]);
        setSelectedCampaign(campaign);
        setShowCreateModal(false);
      }
    } catch (error) {
      console.error("Failed to create campaign:", error);
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
            <h1 className="text-3xl font-bold">Campaign Planner</h1>
            <p className="text-gray-400 mt-1">Plan and manage content campaigns</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition"
          >
            + Create Campaign
          </button>
        </div>

        <div className="grid grid-cols-12 gap-6">
          {/* Campaign List */}
          <div className="col-span-3 bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold mb-4">Campaigns</h2>
            <div className="space-y-2">
              {campaigns.map((campaign) => (
                <button
                  key={campaign.campaign_id}
                  onClick={() => setSelectedCampaign(campaign)}
                  className={`w-full text-left p-3 rounded-lg transition ${
                    selectedCampaign?.campaign_id === campaign.campaign_id
                      ? "bg-blue-600"
                      : "bg-gray-700 hover:bg-gray-600"
                  }`}
                >
                  <div className="font-medium text-sm">{campaign.name}</div>
                  <div className="text-xs text-gray-400 mt-1 capitalize">
                    {campaign.campaign_type.replace("_", " ")}
                  </div>
                </button>
              ))}
              {campaigns.length === 0 && (
                <p className="text-gray-500 text-sm">No campaigns yet</p>
              )}
            </div>
          </div>

          {/* Campaign Details */}
          <div className="col-span-9 space-y-6">
            {selectedCampaign ? (
              <>
                {/* Campaign Header */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-2xl font-bold">{selectedCampaign.name}</h2>
                      <p className="text-gray-400 mt-1 capitalize">
                        {selectedCampaign.campaign_type.replace("_", " ")} Campaign
                      </p>
                    </div>
                    <span className="px-3 py-1 bg-blue-600 rounded-full text-sm">
                      Active
                    </span>
                  </div>
                </div>

                {/* Objectives */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Objectives</h3>
                  <div className="grid grid-cols-3 gap-4">
                    {selectedCampaign.objectives.map((obj, idx) => (
                      <div key={idx} className="bg-gray-700 rounded-lg p-4">
                        <div className="text-gray-400 text-sm capitalize">{obj.type}</div>
                        <div className="text-2xl font-bold mt-1">
                          {obj.target.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-500">{obj.metric}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Timeline */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Timeline</h3>
                  <div className="space-y-3">
                    {selectedCampaign.timeline.map((phase, idx) => (
                      <div key={idx} className="flex items-center gap-4 bg-gray-700 rounded-lg p-4">
                        <div className="w-16 text-center">
                          <div className="text-sm text-gray-400">Week</div>
                          <div className="text-xl font-bold">{phase.week}</div>
                        </div>
                        <div className="flex-1">
                          <div className="font-medium">{phase.phase}</div>
                          <div className="text-sm text-gray-400">{phase.focus}</div>
                        </div>
                        <div className="w-32 bg-gray-600 rounded-full h-2">
                          <div
                            className="bg-blue-500 h-2 rounded-full"
                            style={{ width: `${((idx + 1) / selectedCampaign.timeline.length) * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Budget Allocation */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-4">Budget Allocation</h3>
                  <div className="grid grid-cols-4 gap-4">
                    {Object.entries(selectedCampaign.budget_allocation).map(([key, value]) => (
                      <div key={key} className="bg-gray-700 rounded-lg p-4">
                        <div className="text-gray-400 text-sm capitalize">
                          {key.replace("_", " ")}
                        </div>
                        <div className="text-xl font-bold mt-1">
                          {value}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-gray-800 rounded-lg p-12 text-center">
                <div className="text-gray-500 text-lg">No campaign selected</div>
                <p className="text-gray-600 mt-2">Create a new campaign to get started</p>
              </div>
            )}
          </div>
        </div>

        {/* Create Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
              <h2 className="text-xl font-bold mb-4">Create New Campaign</h2>
              <CreateCampaignForm
                onCreate={createCampaign}
                onCancel={() => setShowCreateModal(false)}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function CreateCampaignForm({
  onCreate,
  onCancel
}: {
  onCreate: (params: any) => void;
  onCancel: () => void;
}) {
  const [formData, setFormData] = useState({
    name: "",
    campaign_type: "product_launch",
    start_date: new Date().toISOString().split("T")[0],
    end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
    budget_usd: 5000,
    target_audiences: ["farmers", "agriculture_enthusiasts"],
    platforms: ["instagram", "tiktok"]
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate({
      ...formData,
      start_date: new Date(formData.start_date).toISOString(),
      end_date: new Date(formData.end_date).toISOString(),
      objectives: [
        { type: "awareness", target: 100000, metric: "impressions" },
        { type: "engagement", target: 5000, metric: "likes" }
      ]
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm text-gray-400 mb-1">Campaign Name</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full bg-gray-700 rounded-lg px-4 py-2"
          placeholder="e.g., Summer Harvest Campaign"
          required
        />
      </div>

      <div>
        <label className="block text-sm text-gray-400 mb-1">Campaign Type</label>
        <select
          value={formData.campaign_type}
          onChange={(e) => setFormData({ ...formData, campaign_type: e.target.value })}
          className="w-full bg-gray-700 rounded-lg px-4 py-2"
        >
          <option value="product_launch">Product Launch</option>
          <option value="seasonal">Seasonal</option>
          <option value="educational">Educational</option>
          <option value="brand_awareness">Brand Awareness</option>
          <option value="engagement">Engagement</option>
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
          className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
        >
          Create Campaign
        </button>
      </div>
    </form>
  );
}
