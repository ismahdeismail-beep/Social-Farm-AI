/**
 * TypeScript type definitions for Social Farm AI OS
 */

// ============================================================
// API Types
// ============================================================

export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

// ============================================================
// Authentication Types
// ============================================================

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  confirm_password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// ============================================================
// AI Types
// ============================================================

export type AIProvider = 'openai' | 'anthropic' | 'google' | 'xai' | 'deepseek';

export type AITaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface AIAgent {
  id: string;
  name: string;
  provider: AIProvider;
  model: string;
  status: 'active' | 'inactive';
  capabilities: string[];
}

export interface AITask {
  id: string;
  agent_id: string;
  status: AITaskStatus;
  input: string;
  output?: string;
  error?: string;
  created_at: string;
  completed_at?: string;
}

export interface AIChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface AIChatRequest {
  messages: AIChatMessage[];
  provider?: AIProvider;
  model?: string;
  temperature?: number;
  max_tokens?: number;
}

export interface AIChatResponse {
  message: AIChatMessage;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

// ============================================================
// Research Types
// ============================================================

export interface ResearchQuery {
  id: string;
  query: string;
  status: 'pending' | 'processing' | 'completed';
  results?: ResearchResult[];
  created_at: string;
}

export interface ResearchResult {
  id: string;
  title: string;
  content: string;
  source: string;
  relevance_score: number;
  metadata?: Record<string, unknown>;
}

export interface Trend {
  id: string;
  topic: string;
  score: number;
  change: number;
  category: string;
  timestamp: string;
}

// ============================================================
// Strategy Types
// ============================================================

export type StrategyStatus = 'draft' | 'active' | 'paused' | 'completed';

export interface Strategy {
  id: string;
  name: string;
  description: string;
  status: StrategyStatus;
  goals: StrategyGoal[];
  campaigns: Campaign[];
  created_at: string;
  updated_at: string;
}

export interface StrategyGoal {
  id: string;
  name: string;
  target: number;
  current: number;
  unit: string;
}

export interface Campaign {
  id: string;
  name: string;
  strategy_id: string;
  status: 'draft' | 'scheduled' | 'active' | 'completed';
  start_date: string;
  end_date: string;
  platforms: Platform[];
  content: ContentItem[];
}

export type Platform = 'twitter' | 'linkedin' | 'facebook' | 'instagram' | 'tiktok' | 'youtube';

export interface ContentItem {
  id: string;
  campaign_id: string;
  platform: Platform;
  content: string;
  media_urls?: string[];
  scheduled_at?: string;
  published_at?: string;
  status: 'draft' | 'scheduled' | 'published' | 'failed';
}

export interface Recommendation {
  id: string;
  type: 'content' | 'timing' | 'audience' | 'platform';
  title: string;
  description: string;
  confidence: number;
  impact: 'low' | 'medium' | 'high';
}

// ============================================================
// Workspace Types
// ============================================================

export interface Workspace {
  id: string;
  name: string;
  description: string;
  owner_id: number;
  members: WorkspaceMember[];
  created_at: string;
}

export interface WorkspaceMember {
  user_id: number;
  role: 'owner' | 'admin' | 'member' | 'viewer';
  joined_at: string;
}

// ============================================================
// Organization Types
// ============================================================

export interface Organization {
  id: string;
  name: string;
  description: string;
  website?: string;
  industry: string;
  size: 'startup' | 'small' | 'medium' | 'large' | 'enterprise';
  created_at: string;
}

// ============================================================
// UI Types
// ============================================================

export type Theme = 'light' | 'dark' | 'system';

export interface NavItem {
  label: string;
  href: string;
  icon?: string;
  badge?: number;
}

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}