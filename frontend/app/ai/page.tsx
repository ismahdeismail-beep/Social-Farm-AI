"use client";

import { useState, useEffect, useRef } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  model?: string;
  tokens?: number;
}

export default function AICommandCenter() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchSystemStatus();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch("/api/ai/health");
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error("Failed to fetch system status:", error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: data.request_id,
        role: "assistant",
        content: data.content || "No response generated",
        timestamp: new Date(),
        model: data.model,
        tokens: data.tokens_used,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">AI Command Center</h1>
            <p className="text-gray-400 text-sm">Master AI Orchestrator</p>
          </div>
          <div className="flex items-center gap-4">
            <StatusBadge
              label="Gateway"
              status={systemStatus?.components?.gateway || "unknown"}
            />
            <StatusBadge
              label="Router"
              status={systemStatus?.components?.router || "unknown"}
            />
            <StatusBadge
              label="Memory"
              status={systemStatus?.components?.memory || "unknown"}
            />
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-4 grid grid-cols-12 gap-4 h-[calc(100vh-80px)]">
        {/* Sidebar */}
        <aside className="col-span-3 bg-gray-800 rounded-lg p-4 overflow-y-auto">
          <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
          <div className="space-y-2">
            <QuickAction
              title="Trend Analysis"
              description="Analyze current trends"
              onClick={() =>
                setInput("Analyze current trends in social media")
              }
            />
            <QuickAction
              title="Content Creation"
              description="Generate content ideas"
              onClick={() =>
                setInput("Generate 5 content ideas for our brand")
              }
            />
            <QuickAction
              title="Research"
              description="Research a topic"
              onClick={() => setInput("Research competitors in our industry")}
            />
            <QuickAction
              title="Quality Review"
              description="Review content quality"
              onClick={() => setInput("Review this content for quality")}
            />
          </div>

          <div className="mt-6">
            <h3 className="text-md font-semibold mb-2">System Metrics</h3>
            <div className="space-y-2 text-sm">
              <MetricItem label="Total Executions" value="-" />
              <MetricItem label="Success Rate" value="-" />
              <MetricItem label="Total Cost" value="-" />
            </div>
          </div>
        </aside>

        {/* Main Chat Area */}
        <main className="col-span-9 bg-gray-800 rounded-lg flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-20">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-xl font-semibold">AI Command Center</h3>
                <p className="mt-2">
                  Ask anything or use quick actions to get started
                </p>
              </div>
            )}
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex items-center gap-2 text-gray-400">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-700 p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                placeholder="Type your message..."
                className="flex-1 bg-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                Send
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

function StatusBadge({ label, status }: { label: string; status: string }) {
  const color =
    status === "healthy"
      ? "bg-green-500"
      : status === "degraded"
        ? "bg-yellow-500"
        : "bg-red-500";

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${color}`}></div>
      <span className="text-sm text-gray-400">{label}</span>
    </div>
  );
}

function QuickAction({
  title,
  description,
  onClick,
}: {
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
    >
      <div className="font-semibold">{title}</div>
      <div className="text-sm text-gray-400">{description}</div>
    </button>
  );
}

function MetricItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between">
      <span className="text-gray-400">{label}</span>
      <span className="font-mono">{value}</span>
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[70%] rounded-lg p-4 ${
          isUser ? "bg-blue-600" : "bg-gray-700"
        }`}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>
        <div className="mt-2 text-xs text-gray-400 flex gap-4">
          <span>{message.timestamp.toLocaleTimeString()}</span>
          {message.model && <span>Model: {message.model}</span>}
          {message.tokens && <span>Tokens: {message.tokens}</span>}
        </div>
      </div>
    </div>
  );
}
