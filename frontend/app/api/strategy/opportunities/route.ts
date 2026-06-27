import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: '1', title: 'Trending: #UrbanFarming', score: 92, platform: 'TikTok', potential: 'high' },
    { id: '2', title: 'Seasonal: Summer Recipes', score: 85, platform: 'Instagram', potential: 'medium' },
    { id: '3', title: 'Viral: Farm Life Aesthetic', score: 78, platform: 'YouTube', potential: 'high' },
  ])
}
