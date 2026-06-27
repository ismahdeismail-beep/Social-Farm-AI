import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: '1', name: 'Sustainable Farming Trends', description: 'Research on sustainable agriculture trends', query_count: 5 },
    { id: '2', name: 'Social Media Best Practices', description: 'Content strategy research for farm accounts', query_count: 3 },
  ])
}
