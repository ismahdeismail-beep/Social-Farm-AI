/**
 * Content Strategy Store
 * 
 * Zustand store for managing content strategy state.
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ==================== TYPES ====================

export interface Strategy {
  strategy_id: string;
  name: string;
  vision: string;
  mission: string;
  goals: Array<{ name: string; metric: string; target_value: number }>;
  kpis: Array<{ metric: string; target: number; unit: string }>;
  content_pillars: Array<{ name: string; description: string }>;
  content_mix: Record<string, number>;
  platform_strategies: Array<{ platform: string; strategy: string }>;
  audience_segments: Array<{ name: string; description: string }>;
  themes: Array<{ name: string; keywords: string[] }>;
  recommendations: Array<{ title: string; description: string }>;
  confidence_score: number;
  status: string;
  created_at: string;
}

export interface Campaign {
  campaign_id: string;
  name: string;
  campaign_type: string;
  objectives: Array<{ type: string; target: number; metric: string }>;
  content_plan: Record<string, any>;
  platform_strategy: Record<string, any>;
  timeline: Array<{ week: number; phase: string; focus: string }>;
  budget_allocation: Record<string, number>;
  kpis: Array<{ metric: string; target: number; current: number }>;
}

export interface CalendarEntry {
  id: string;
  date: string;
  platform: string;
  content_type: string;
  topic: string;
  pillar: string;
  status: 'draft' | 'scheduled' | 'published';
  hook?: string;
}

export interface Opportunity {
  id: string;
  title: string;
  description: string;
  opportunity_type: string;
  priority_score: number;
  suggested_formats: string[];
  suggested_platforms: string[];
  status: 'new' | 'reviewing' | 'approved' | 'rejected';
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  recommendation_type: string;
  content_idea: string;
  hook: string;
  target_platforms: string[];
  relevance_score: number;
}

export interface Forecast {
  id: string;
  name: string;
  forecast_type: string;
  predicted_value: number;
  confidence_level: number;
  best_case: number;
  worst_case: number;
}

// ==================== STORE STATE ====================

interface StrategyState {
  // Strategies
  strategies: Strategy[];
  selectedStrategy: Strategy | null;
  strategiesLoading: boolean;
  strategiesError: string | null;

  // Campaigns
  campaigns: Campaign[];
  selectedCampaign: Campaign | null;
  campaignsLoading: boolean;
  campaignsError: string | null;

  // Calendar
  calendarEntries: CalendarEntry[];
  calendarLoading: boolean;
  calendarError: string | null;

  // Opportunities
  opportunities: Opportunity[];
  opportunitiesLoading: boolean;
  opportunitiesError: string | null;

  // Recommendations
  recommendations: Recommendation[];
  recommendationsLoading: boolean;
  recommendationsError: string | null;

  // Forecasts
  forecasts: Forecast[];
  forecastsLoading: boolean;
  forecastsError: string | null;

  // UI State
  currentView: 'dashboard' | 'campaigns' | 'calendar' | 'opportunities';
  generateModalOpen: boolean;
}

// ==================== STORE ACTIONS ====================

interface StrategyActions {
  // Strategy Actions
  setStrategies: (strategies: Strategy[]) => void;
  setSelectedStrategy: (strategy: Strategy | null) => void;
  addStrategy: (strategy: Strategy) => void;
  updateStrategy: (strategyId: string, updates: Partial<Strategy>) => void;
  removeStrategy: (strategyId: string) => void;
  setStrategiesLoading: (loading: boolean) => void;
  setStrategiesError: (error: string | null) => void;

  // Campaign Actions
  setCampaigns: (campaigns: Campaign[]) => void;
  setSelectedCampaign: (campaign: Campaign | null) => void;
  addCampaign: (campaign: Campaign) => void;
  updateCampaign: (campaignId: string, updates: Partial<Campaign>) => void;
  removeCampaign: (campaignId: string) => void;
  setCampaignsLoading: (loading: boolean) => void;
  setCampaignsError: (error: string | null) => void;

  // Calendar Actions
  setCalendarEntries: (entries: CalendarEntry[]) => void;
  addCalendarEntry: (entry: CalendarEntry) => void;
  updateCalendarEntry: (entryId: string, updates: Partial<CalendarEntry>) => void;
  removeCalendarEntry: (entryId: string) => void;
  setCalendarLoading: (loading: boolean) => void;
  setCalendarError: (error: string | null) => void;

  // Opportunity Actions
  setOpportunities: (opportunities: Opportunity[]) => void;
  updateOpportunity: (opportunityId: string, updates: Partial<Opportunity>) => void;
  removeOpportunity: (opportunityId: string) => void;
  setOpportunitiesLoading: (loading: boolean) => void;
  setOpportunitiesError: (error: string | null) => void;

  // Recommendation Actions
  setRecommendations: (recommendations: Recommendation[]) => void;
  setRecommendationsLoading: (loading: boolean) => void;
  setRecommendationsError: (error: string | null) => void;

  // Forecast Actions
  setForecasts: (forecasts: Forecast[]) => void;
  setForecastsLoading: (loading: boolean) => void;
  setForecastsError: (error: string | null) => void;

  // UI Actions
  setCurrentView: (view: StrategyState['currentView']) => void;
  setGenerateModalOpen: (open: boolean) => void;

  // Reset
  reset: () => void;
}

// ==================== INITIAL STATE ====================

const initialState: StrategyState = {
  strategies: [],
  selectedStrategy: null,
  strategiesLoading: false,
  strategiesError: null,

  campaigns: [],
  selectedCampaign: null,
  campaignsLoading: false,
  campaignsError: null,

  calendarEntries: [],
  calendarLoading: false,
  calendarError: null,

  opportunities: [],
  opportunitiesLoading: false,
  opportunitiesError: null,

  recommendations: [],
  recommendationsLoading: false,
  recommendationsError: null,

  forecasts: [],
  forecastsLoading: false,
  forecastsError: null,

  currentView: 'dashboard',
  generateModalOpen: false,
};

// ==================== STORE ====================

export const useStrategyStore = create<StrategyState & StrategyActions>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Strategy Actions
      setStrategies: (strategies) => set({ strategies }),
      setSelectedStrategy: (strategy) => set({ selectedStrategy: strategy }),
      addStrategy: (strategy) =>
        set((state) => ({ strategies: [...state.strategies, strategy] })),
      updateStrategy: (strategyId, updates) =>
        set((state) => ({
          strategies: state.strategies.map((s) =>
            s.strategy_id === strategyId ? { ...s, ...updates } : s
          ),
          selectedStrategy:
            state.selectedStrategy?.strategy_id === strategyId
              ? { ...state.selectedStrategy, ...updates }
              : state.selectedStrategy,
        })),
      removeStrategy: (strategyId) =>
        set((state) => ({
          strategies: state.strategies.filter((s) => s.strategy_id !== strategyId),
          selectedStrategy:
            state.selectedStrategy?.strategy_id === strategyId
              ? null
              : state.selectedStrategy,
        })),
      setStrategiesLoading: (loading) => set({ strategiesLoading: loading }),
      setStrategiesError: (error) => set({ strategiesError: error }),

      // Campaign Actions
      setCampaigns: (campaigns) => set({ campaigns }),
      setSelectedCampaign: (campaign) => set({ selectedCampaign: campaign }),
      addCampaign: (campaign) =>
        set((state) => ({ campaigns: [...state.campaigns, campaign] })),
      updateCampaign: (campaignId, updates) =>
        set((state) => ({
          campaigns: state.campaigns.map((c) =>
            c.campaign_id === campaignId ? { ...c, ...updates } : c
          ),
          selectedCampaign:
            state.selectedCampaign?.campaign_id === campaignId
              ? { ...state.selectedCampaign, ...updates }
              : state.selectedCampaign,
        })),
      removeCampaign: (campaignId) =>
        set((state) => ({
          campaigns: state.campaigns.filter((c) => c.campaign_id !== campaignId),
          selectedCampaign:
            state.selectedCampaign?.campaign_id === campaignId
              ? null
              : state.selectedCampaign,
        })),
      setCampaignsLoading: (loading) => set({ campaignsLoading: loading }),
      setCampaignsError: (error) => set({ campaignsError: error }),

      // Calendar Actions
      setCalendarEntries: (entries) => set({ calendarEntries: entries }),
      addCalendarEntry: (entry) =>
        set((state) => ({ calendarEntries: [...state.calendarEntries, entry] })),
      updateCalendarEntry: (entryId, updates) =>
        set((state) => ({
          calendarEntries: state.calendarEntries.map((e) =>
            e.id === entryId ? { ...e, ...updates } : e
          ),
        })),
      removeCalendarEntry: (entryId) =>
        set((state) => ({
          calendarEntries: state.calendarEntries.filter((e) => e.id !== entryId),
        })),
      setCalendarLoading: (loading) => set({ calendarLoading: loading }),
      setCalendarError: (error) => set({ calendarError: error }),

      // Opportunity Actions
      setOpportunities: (opportunities) => set({ opportunities }),
      updateOpportunity: (opportunityId, updates) =>
        set((state) => ({
          opportunities: state.opportunities.map((o) =>
            o.id === opportunityId ? { ...o, ...updates } : o
          ),
        })),
      removeOpportunity: (opportunityId) =>
        set((state) => ({
          opportunities: state.opportunities.filter((o) => o.id !== opportunityId),
        })),
      setOpportunitiesLoading: (loading) => set({ opportunitiesLoading: loading }),
      setOpportunitiesError: (error) => set({ opportunitiesError: error }),

      // Recommendation Actions
      setRecommendations: (recommendations) => set({ recommendations }),
      setRecommendationsLoading: (loading) => set({ recommendationsLoading: loading }),
      setRecommendationsError: (error) => set({ recommendationsError: error }),

      // Forecast Actions
      setForecasts: (forecasts) => set({ forecasts }),
      setForecastsLoading: (loading) => set({ forecastsLoading: loading }),
      setForecastsError: (error) => set({ forecastsError: error }),

      // UI Actions
      setCurrentView: (view) => set({ currentView: view }),
      setGenerateModalOpen: (open) => set({ generateModalOpen: open }),

      // Reset
      reset: () => set(initialState),
    }),
    {
      name: 'strategy-storage',
      partialize: (state) => ({
        strategies: state.strategies,
        selectedStrategy: state.selectedStrategy,
        campaigns: state.campaigns,
        selectedCampaign: state.selectedCampaign,
        calendarEntries: state.calendarEntries,
        opportunities: state.opportunities,
        currentView: state.currentView,
      }),
    }
  )
);

// ==================== SELECTORS ====================

export const selectStrategies = (state: StrategyState) => state.strategies;
export const selectSelectedStrategy = (state: StrategyState) => state.selectedStrategy;
export const selectCampaigns = (state: StrategyState) => state.campaigns;
export const selectSelectedCampaign = (state: StrategyState) => state.selectedCampaign;
export const selectCalendarEntries = (state: StrategyState) => state.calendarEntries;
export const selectOpportunities = (state: StrategyState) => state.opportunities;
export const selectRecommendations = (state: StrategyState) => state.recommendations;
export const selectForecasts = (state: StrategyState) => state.forecasts;
export const selectCurrentView = (state: StrategyState) => state.currentView;
export const selectGenerateModalOpen = (state: StrategyState) => state.generateModalOpen;

// Loading selectors
export const selectStrategiesLoading = (state: StrategyState) => state.strategiesLoading;
export const selectCampaignsLoading = (state: StrategyState) => state.campaignsLoading;
export const selectCalendarLoading = (state: StrategyState) => state.calendarLoading;
export const selectOpportunitiesLoading = (state: StrategyState) => state.opportunitiesLoading;

// Error selectors
export const selectStrategiesError = (state: StrategyState) => state.strategiesError;
export const selectCampaignsError = (state: StrategyState) => state.campaignsError;
export const selectCalendarError = (state: StrategyState) => state.calendarError;
export const selectOpportunitiesError = (state: StrategyState) => state.opportunitiesError;

// Computed selectors
export const selectApprovedStrategies = (state: StrategyState) =>
  state.strategies.filter((s) => s.status === 'approved');

export const selectActiveCampaigns = (state: StrategyState) =>
  state.campaigns.filter((c) => c.kpis.some((kpi) => kpi.current < kpi.target));

export const selectHighPriorityOpportunities = (state: StrategyState) =>
  state.opportunities.filter((o) => o.priority_score >= 0.8 && o.status === 'new');

export const selectPendingOpportunities = (state: StrategyState) =>
  state.opportunities.filter((o) => o.status === 'reviewing');
