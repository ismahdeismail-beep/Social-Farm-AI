"use client";

import { useState, useEffect } from "react";

interface CalendarEntry {
  id: string;
  date: string;
  platform: string;
  content_type: string;
  topic: string;
  pillar: string;
  status: "draft" | "scheduled" | "published";
  hook?: string;
}

export default function ContentCalendar() {
  const [entries, setEntries] = useState<CalendarEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<"month" | "week" | "list">("month");
  const [filterPlatform, setFilterPlatform] = useState<string>("all");

  useEffect(() => {
    loadCalendar();
  }, []);

  const loadCalendar = async () => {
    try {
      const response = await fetch("/api/strategy/calendar", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      });
      if (response.ok) {
        const data = await response.json();
        setEntries(data.entries || []);
      }
    } catch (error) {
      console.error("Failed to load calendar:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateSampleCalendar = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/strategy/calendar?strategy_id=default", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
      });
      if (response.ok) {
        const data = await response.json();
        setEntries(data.entries || []);
      }
    } catch (error) {
      console.error("Failed to generate calendar:", error);
    } finally {
      setLoading(false);
    }
  };

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay();

    const days: Array<{ date: Date; isCurrentMonth: boolean }> = [];

    // Previous month days
    for (let i = startingDay - 1; i >= 0; i--) {
      const d = new Date(year, month, -i);
      days.push({ date: d, isCurrentMonth: false });
    }

    // Current month days
    for (let i = 1; i <= daysInMonth; i++) {
      days.push({ date: new Date(year, month, i), isCurrentMonth: true });
    }

    // Next month days
    const remaining = 42 - days.length;
    for (let i = 1; i <= remaining; i++) {
      days.push({ date: new Date(year, month + 1, i), isCurrentMonth: false });
    }

    return days;
  };

  const getEntriesForDate = (date: Date) => {
    const dateStr = date.toISOString().split("T")[0];
    return entries.filter((entry) => {
      const entryDate = entry.date.split("T")[0];
      const platformMatch = filterPlatform === "all" || entry.platform === filterPlatform;
      return entryDate === dateStr && platformMatch;
    });
  };

  const getPlatformColor = (platform: string) => {
    const colors: Record<string, string> = {
      instagram: "bg-pink-600",
      tiktok: "bg-black",
      youtube: "bg-red-600",
      linkedin: "bg-blue-700",
      facebook: "bg-blue-600",
      twitter: "bg-sky-500"
    };
    return colors[platform] || "bg-gray-600";
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: "bg-gray-600",
      scheduled: "bg-yellow-600",
      published: "bg-green-600"
    };
    return colors[status] || "bg-gray-600";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const today = new Date();
  const [currentMonth, setCurrentMonth] = useState(today);
  const days = getDaysInMonth(currentMonth);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">Content Calendar</h1>
            <p className="text-gray-400 mt-1">Plan and schedule your content</p>
          </div>
          <div className="flex gap-4">
            <button
              onClick={generateSampleCalendar}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition"
            >
              Generate Calendar
            </button>
            <select
              value={filterPlatform}
              onChange={(e) => setFilterPlatform(e.target.value)}
              className="bg-gray-800 rounded-lg px-4 py-2"
            >
              <option value="all">All Platforms</option>
              <option value="instagram">Instagram</option>
              <option value="tiktok">TikTok</option>
              <option value="youtube">YouTube</option>
              <option value="linkedin">LinkedIn</option>
            </select>
            <div className="flex bg-gray-800 rounded-lg">
              {(["month", "week", "list"] as const).map((mode) => (
                <button
                  key={mode}
                  onClick={() => setViewMode(mode)}
                  className={`px-4 py-2 capitalize transition ${
                    viewMode === mode ? "bg-blue-600" : "hover:bg-gray-700"
                  }`}
                >
                  {mode}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Month Navigation */}
        <div className="flex justify-between items-center mb-6">
          <button
            onClick={() => {
              const newMonth = new Date(currentMonth);
              newMonth.setMonth(newMonth.getMonth() - 1);
              setCurrentMonth(newMonth);
            }}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition"
          >
            Previous
          </button>
          <h2 className="text-xl font-semibold">
            {currentMonth.toLocaleString("default", { month: "long", year: "numeric" })}
          </h2>
          <button
            onClick={() => {
              const newMonth = new Date(currentMonth);
              newMonth.setMonth(newMonth.getMonth() + 1);
              setCurrentMonth(newMonth);
            }}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition"
          >
            Next
          </button>
        </div>

        {/* Calendar Grid */}
        {viewMode === "month" && (
          <div className="bg-gray-800 rounded-lg p-4">
            {/* Day Headers */}
            <div className="grid grid-cols-7 gap-2 mb-2">
              {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
                <div key={day} className="text-center text-gray-400 text-sm py-2">
                  {day}
                </div>
              ))}
            </div>

            {/* Calendar Days */}
            <div className="grid grid-cols-7 gap-2">
              {days.map((day, idx) => {
                const dayEntries = getEntriesForDate(day.date);
                const isToday =
                  day.date.toISOString().split("T")[0] === today.toISOString().split("T")[0];

                return (
                  <div
                    key={idx}
                    onClick={() => setSelectedDate(day.date.toISOString().split("T")[0])}
                    className={`min-h-[100px] p-2 rounded-lg cursor-pointer transition ${
                      day.isCurrentMonth ? "bg-gray-700" : "bg-gray-800"
                    } ${isToday ? "ring-2 ring-blue-500" : ""} ${
                      selectedDate === day.date.toISOString().split("T")[0]
                        ? "ring-2 ring-blue-400"
                        : ""
                    }`}
                  >
                    <div
                      className={`text-sm mb-1 ${
                        isToday ? "text-blue-400 font-bold" : "text-gray-400"
                      }`}
                    >
                      {day.date.getDate()}
                    </div>
                    <div className="space-y-1">
                      {dayEntries.slice(0, 3).map((entry) => (
                        <div
                          key={entry.id}
                          className={`text-xs p-1 rounded ${getPlatformColor(entry.platform)}`}
                        >
                          <div className="truncate">{entry.topic}</div>
                        </div>
                      ))}
                      {dayEntries.length > 3 && (
                        <div className="text-xs text-gray-400">
                          +{dayEntries.length - 3} more
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* List View */}
        {viewMode === "list" && (
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="space-y-2">
              {entries
                .filter(
                  (e) => filterPlatform === "all" || e.platform === filterPlatform
                )
                .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
                .map((entry) => (
                  <div
                    key={entry.id}
                    className="flex items-center gap-4 bg-gray-700 rounded-lg p-4"
                  >
                    <div className="w-20 text-center">
                      <div className="text-sm text-gray-400">
                        {new Date(entry.date).toLocaleDateString("default", { weekday: "short" })}
                      </div>
                      <div className="text-lg font-bold">
                        {new Date(entry.date).getDate()}
                      </div>
                    </div>
                    <div
                      className={`px-3 py-1 rounded-full text-xs ${getPlatformColor(
                        entry.platform
                      )}`}
                    >
                      {entry.platform}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium">{entry.topic}</div>
                      <div className="text-sm text-gray-400">
                        {entry.content_type} • {entry.pillar}
                      </div>
                    </div>
                    <div
                      className={`px-3 py-1 rounded-full text-xs ${getStatusColor(
                        entry.status
                      )}`}
                    >
                      {entry.status}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Selected Date Modal */}
        {selectedDate && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">
                  {new Date(selectedDate).toLocaleDateString("default", {
                    weekday: "long",
                    month: "long",
                    day: "numeric"
                  })}
                </h2>
                <button
                  onClick={() => setSelectedDate(null)}
                  className="text-gray-400 hover:text-white"
                >
                  ×
                </button>
              </div>
              <div className="space-y-3">
                {getEntriesForDate(new Date(selectedDate)).length > 0 ? (
                  getEntriesForDate(new Date(selectedDate)).map((entry) => (
                    <div key={entry.id} className="bg-gray-700 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span
                          className={`px-2 py-1 rounded text-xs ${getPlatformColor(
                            entry.platform
                          )}`}
                        >
                          {entry.platform}
                        </span>
                        <span className="text-gray-400 text-sm">{entry.content_type}</span>
                      </div>
                      <div className="font-medium">{entry.topic}</div>
                      {entry.hook && (
                        <div className="text-sm text-gray-400 mt-1">"{entry.hook}"</div>
                      )}
                      <div className="text-xs text-gray-500 mt-2">Pillar: {entry.pillar}</div>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500 text-center py-4">No content scheduled</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Stats Summary */}
        <div className="grid grid-cols-4 gap-4 mt-6">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Total Posts</div>
            <div className="text-2xl font-bold">{entries.length}</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Draft</div>
            <div className="text-2xl font-bold text-gray-500">
              {entries.filter((e) => e.status === "draft").length}
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Scheduled</div>
            <div className="text-2xl font-bold text-yellow-500">
              {entries.filter((e) => e.status === "scheduled").length}
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-gray-400 text-sm">Published</div>
            <div className="text-2xl font-bold text-green-500">
              {entries.filter((e) => e.status === "published").length}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
