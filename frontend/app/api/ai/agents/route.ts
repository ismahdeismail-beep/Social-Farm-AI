import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: '1', name: 'Content Creator', status: 'active', type: 'content' },
    { id: '2', name: 'Research Analyst', status: 'active', type: 'research' },
    { id: '3', name: 'Trend Monitor', status: 'idle', type: 'analytics' },
    { id: '4', name: 'Strategy Planner', status: 'active', type: 'strategy' },
  ])
}
