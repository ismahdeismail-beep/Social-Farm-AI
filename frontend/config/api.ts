export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  wsURL: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080',
  endpoints: {
    posts: '/api/automation/posts',
    replies: '/api/automation/replies',
    comments: '/api/automation/comments',
    executions: '/api/automation/executions'
  }
};
