import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: '1', name: 'Summer Harvest Campaign', status: 'active', platform: 'Instagram', start_date: '2026-06-01', end_date: '2026-08-31' },
    { id: '2', name: 'Farm-to-Table Stories', status: 'planning', platform: 'TikTok', start_date: '2026-07-01', end_date: '2026-09-30' },
  ])
}
