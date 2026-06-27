import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json([
    { id: 'gpt-4', name: 'GPT-4', provider: 'OpenAI', status: 'available' },
    { id: 'claude-3', name: 'Claude 3', provider: 'Anthropic', status: 'available' },
    { id: 'gemini-pro', name: 'Gemini Pro', provider: 'Google', status: 'available' },
  ])
}
