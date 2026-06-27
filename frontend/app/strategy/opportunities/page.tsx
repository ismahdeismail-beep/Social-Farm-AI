"use client";

import { useState, useEffect } from "react";

interface Opportunity {
  id: string;
  title: string;
  description: string;
  opportunity_type: string;
  priority_score: number;
  suggested_formats: string[];
  suggested_platforms: string[];
  status: "new" | "reviewing" | "approved" | "rejected";
}

export default function OpportunityBoard() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");
  const [selectedOpportunity, setSelectedOpportunity] = useState<Opportunity | null>(null);

  useEffect(() => {
    loadOpportunities();
  }, []);

  const loadOpportunities = async () => {
    try {
      const response = await fetch(
        "/api/strategy/opportunities?brand_id=default&industry=agriculture",
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
        }
      );
      if (response.ok) {
        const data = await response.json();
        setOpportunities(data.map((o: any) => ({ ...o, status: "new" })));
      }
    } catch (error) {
      console.error("Failed to load opportunities:", error);
    } finally {
      setLoading(false);
    }
  };

  const updateOpportunityStatus = (id: string, status: string) => {
    setOpportunities((prev) =>
      prev.map((o) => (o.id === id ? { ...o, status: status as any } : o))
    );
  };

  const getPriorityColor = (score: number) => {
    if (score >= 0.8) return "text-green-400 bg-green-900";
    if (score >= 0.6) return "text-yellow-400 bg-yellow-900";
    if (score >= 0.4) return "text-orange-400 bg-orange-900";
    return "text-red-400 bg-red-900";
  };

  const getTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      trend: "📈",
      seasonal: "🗓️",
      competitor_gap: "🎯",
      audience_insight: "👥",
      content_gap: "📝",
      viral_potential: "🚀",
      partnership: "🤝",
      event: "📅"
    };
    return icons[type] || "💡";
  };

  const filteredOpportunities = opportunities.filter(
    (o) => filter === "all" || o.status === filter
  );

  const statusCounts = {
    all: opportunities.length,
    new: opportunities.filter((o) => o.status === "new").length,
    reviewing: opportunities.filter((o) => o.status === "reviewing").length,
    approved: opportunities.filter((o) => o.status === "approved").length,
    rejected: opportunities.filter((o) => o.status === "rejected").length
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
            <h1 className="text-3xl font-bold">Opportunity Board</h1>
            <p className="text-gray-400 mt-1">Discover content opportunities</p>
          </div>
          <button
            onClick={loadOpportunities}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
          >
            Refresh
          </button>
        </div>

        {/* Status Filter Tabs */}
        <div className="flex gap-2 mb-6">
          {(["all", "new", "reviewing", "approved", "rejected"] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-4 py-2 rounded-lg transition ${
                filter === status ? "bg-blue-600" : "bg-gray-800 hover:bg-gray-700"
              }`}
            >
              <span className="capitalize">{status}</span>
              <span className="ml-2 text-sm text-gray-400">
                ({statusCounts[status as keyof typeof statusCounts]})
              </span>
            </button>
          ))}
        </div>

        {/* Opportunities Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredOpportunities.map((opportunity) => (
            <div
              key={opportunity.id}
              onClick={() => setSelectedOpportunity(opportunity)}
              className="bg-gray-800 rounded-lg p-4 cursor-pointer hover:bg-gray-750 transition border border-gray-700 hover:border-gray-600"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{getTypeIcon(opportunity.opportunity_type)}</span>
                  <span className="text-xs text-gray-400 capitalize">
                    {opportunity.opportunity_type.replace("_", " ")}
                  </span>
                </div>
                <span
                  className={`px-2 py-1 rounded text-xs ${getPriorityColor(
                    opportunity.priority_score
                  )}`}
                >
                  {(opportunity.priority_score * 100).toFixed(0)}%
                </span>
              </div>

              {/* Title & Description */}
              <h3 className="font-semibold mb-2">{opportunity.title}</h3>
              <p className="text-sm text-gray-400 line-clamp-2 mb-3">
                {opportunity.description}
              </p>

              {/* Platforms */}
              <div className="flex gap-2 mb-3">
                {opportunity.suggested_platforms.map((platform) => (
                  <span
                    key={platform}
                    className="px-2 py-1 bg-gray-700 rounded text-xs capitalize"
                  >
                    {platform}
                  </span>
                ))}
              </div>

              {/* Formats */}
              <div className="flex gap-2 mb-4">
                {opportunity.suggested_formats.slice(0, 3).map((format) => (
                  <span
                    key={format}
                    className="px-2 py-1 bg-gray-700 rounded text-xs"
                  >
                    {format}
                  </span>
                ))}
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    updateOpportunityStatus(opportunity.id, "approved");
                  }}
                  className="flex-1 px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm transition"
                >
                  Approve
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    updateOpportunityStatus(opportunity.id, "reviewing");
                  }}
                  className="flex-1 px-3 py-1 bg-yellow-600 hover:bg-yellow-700 rounded text-sm transition"
                >
                  Review
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    updateOpportunityStatus(opportunity.id, "rejected");
                  }}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredOpportunities.length === 0 && (
          <div className="bg-gray-800 rounded-lg p-12 text-center">
            <div className="text-gray-500 text-lg">No opportunities found</div>
            <p className="text-gray-600 mt-2">Try adjusting your filters</p>
          </div>
        )}

        {/* Detail Modal */}
        {selectedOpportunity && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-gray-800 rounded-lg p-6 w-full max-w-lg">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">
                    {getTypeIcon(selectedOpportunity.opportunity_type)}
                  </span>
                  <div>
                    <h2 className="text-xl font-bold">{selectedOpportunity.title}</h2>
                    <span className="text-sm text-gray-400 capitalize">
                      {selectedOpportunity.opportunity_type.replace("_", " ")}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedOpportunity(null)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>

              <p className="text-gray-300 mb-4">{selectedOpportunity.description}</p>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-sm text-gray-400">Priority Score</div>
                  <div className="text-2xl font-bold">
                    {(selectedOpportunity.priority_score * 100).toFixed(0)}%
                  </div>
                </div>
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-sm text-gray-400">Status</div>
                  <div className="text-2xl font-bold capitalize">
                    {selectedOpportunity.status}
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <div className="text-sm text-gray-400 mb-2">Suggested Platforms</div>
                <div className="flex gap-2">
                  {selectedOpportunity.suggested_platforms.map((platform) => (
                    <span
                      key={platform}
                      className="px-3 py-1 bg-blue-600 rounded-full text-sm capitalize"
                    >
                      {platform}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <div className="text-sm text-gray-400 mb-2">Suggested Formats</div>
                <div className="flex gap-2">
                  {selectedOpportunity.suggested_formats.map((format) => (
                    <span
                      key={format}
                      className="px-3 py-1 bg-purple-600 rounded-full text-sm"
                    >
                      {format}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => {
                    updateOpportunityStatus(selectedOpportunity.id, "approved");
                    setSelectedOpportunity(null);
                  }}
                  className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition"
                >
                  Approve & Create Content
                </button>
                <button
                  onClick={() => {
                    updateOpportunityStatus(selectedOpportunity.id, "reviewing");
                    setSelectedOpportunity(null);
                  }}
                  className="flex-1 px-4 py-2 bg-yellow-600 hover:bg-yellow-700 rounded-lg transition"
                >
                  Mark for Review
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Stats Summary */}
        <div className="grid grid-cols-4 gap-4 mt-6">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">High Priority</div>
            <div className="text-2xl font-bold text-green-400">
              {opportunities.filter((o) => o.priority_score >= 0.8).length}
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Medium Priority</div>
            <div className="text-2xl font-bold text-yellow-400">
              {opportunities.filter(
                (o) => o.priority_score >= 0.5 && o.priority_score < 0.8
              ).length}
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Approved</div>
            <div className="text-2xl font-bold text-blue-400">
              {opportunities.filter((o) => o.status === "approved").length}
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Total</div>
            <div className="text-2xl font-bold">{opportunities.length}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
