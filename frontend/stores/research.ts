import { create } from 'zustand'

interface ResearchQuery {
  id: string
  query: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  result?: string
  created_at: string
}

interface ResearchState {
  queries: ResearchQuery[]
  currentQuery: ResearchQuery | null
  loading: boolean
  error: string | null
  setQueries: (queries: ResearchQuery[]) => void
  setCurrentQuery: (query: ResearchQuery | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useResearchStore = create<ResearchState>((set) => ({
  queries: [],
  currentQuery: null,
  loading: false,
  error: null,
  setQueries: (queries) => set({ queries }),
  setCurrentQuery: (query) => set({ currentQuery: query }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}))
