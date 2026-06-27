import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    service: 'social-farm-ai-backend',
    version: '0.3.0-preview',
    timestamp: new Date().toISOString(),
    components: {
      database: 'mock',
      redis: 'mock',
      ai: 'mock',
    },
  })
}
