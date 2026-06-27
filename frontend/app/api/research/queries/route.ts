import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: '1', query: 'Trending topics in sustainable agriculture', status: 'completed', created_at: '2026-06-25T10:00:00Z' },
    { id: '2', query: 'Social media engagement patterns for farm content', status: 'completed', created_at: '2026-06-26T14:30:00Z' },
  ])
}

export async function POST(request: Request) {
  const body = await request.json()
  return NextResponse.json({
    id: String(Date.now()),
    query: body.query,
    status: 'pending',
    created_at: new Date().toISOString(),
  }, { status: 201 })
}
