import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: '1', title: 'World Food Day Post', date: '2026-10-16', type: 'social', status: 'scheduled' },
    { id: '2', title: 'Harvest Festival Live', date: '2026-09-22', type: 'live', status: 'planning' },
  ])
}
