# SOCIAL-FARM-AI FRONTEND V2 ARCHITECTURE

## Overview

This document outlines the architecture for the Social Farm AI OS Frontend V2, designed as a premium SaaS application for AI-powered social media management and automation.

## Design Language

### Color System

Primary:
- #0B0F14 - Main background
- #0F172A - Secondary background
- #1A2230 - Surface backgrounds
- #334155 - Borders and dividers
- #64748B - Secondary text
- #94A3B8 - Disabled elements

Accent Gradients:
- Purple to Blue: For primary actions and AI features
- Green to Teal: For success and positive actions
- Orange to Red: For warnings and critical status

### Typography

- **Display**: Inter, 2.5rem, Bold, -0.02em tracking, line-height 1.2
- **H1**: Inter, 2rem, Bold, -0.01em tracking, line-height 1.3
- **H2**: Inter, 1.75rem, Bold, line-height 1.3
- **H3**: Inter, 1.5rem, SemiBold, line-height 1.4
- **H4**: Inter, 1.25rem, SemiBold, line-height 1.4
- **Body**: Inter, 1rem, Regular, line-height 1.5
- **Small**: Inter, 0.875rem, Regular, line-height 1.5
- **Caption**: Inter, 0.75rem, Regular, line-height 1.4

### Spacing System

8px grid system with:
- 0.5rem (8px) - XSmall
- 0.75rem (12px) - Small
- 1rem (16px) - Medium
- 1.5rem (24px) - Large
- 2rem (32px) - XLarge
- 3rem (48px) - XXLarge

### Border Radius

- 0.25rem (4px) - Small
- 0.5rem (8px) - Medium
- 0.75rem (12px) - Large
- 1rem (16px) - XLarge
- 9999px - Pill

### Shadows

- Shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
- Shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
- Shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)
- Shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1)

## Component Library

### Buttons

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}
```

### Cards

```typescript
interface CardProps {
  variant?: 'default' | 'interactive' | 'bordered' | 'glass';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}
```

### Forms

- Input: Text inputs with labels, error states, and helper text
- Select: Dropdown with search and multi-select capabilities
- TextArea: Multi-line text inputs
- Checkbox: Multiple selection inputs
- Radio: Single selection inputs
- Toggle: On/off switches
- Calendar: Date picker components

### Tables

- DataTable: Sortable, filterable, paginated tables
- TableRow: Individual table row with hover states
- TableCell: Customizable table cells
- TableHeader: Sticky header with sorting controls

### Charts

- LineChart: Time series data visualization
- BarChart: Comparative data display
- AreaChart: Cumulative data representation
- DonutChart: Proportional data display
- Heatmap: Correlation and intensity visualization

## Application Shell

### Layout Structure

```
┌─────────────────┐
│ Top Navigation  │
├─────────────────┤
│                 │
│ Left Sidebar    │ Main Content    Right Panel
│ (180px fixed)  │ (flex-grow)    │ (320px fixed)
│                 │                │
└─────────────────┘
```

### Left Sidebar

- Collapsible (180px / 64px icons)
- Icons with grouped sections
- Workspace selector
- User avatar with dropdown
- Primary navigation items (6-8 items)
- Secondary navigation items
- Theme switcher

### Top Navigation

- Global Search with command palette
- Notifications center
- Quick Create button
- AI Assistant button
- Profile menu

### Right Panel

- Contextual AI Assistant
- Suggestions for next actions
- Notifications
- Task Queue
- Recent AI Actions
- Quick insights

## Navigation Structure

The new navigation is workflow-driven:

```
Dashboard
  ├─ Overview
  └─ Analytics

Workspace
  ├─ Team
  ├─ Settings
  └─ Preferences

Content Studio
  ├─ AI Writer
  ├─ Hook Generator
  ├─ Caption Generator
  ├─ Script Writer
  ├─ Carousel Builder
  ├─ Image Studio
  └─ Video Assistant

Publishing
  ├─ Scheduler
  ├─ Calendar
  ├─ Queue
  ├─ Published Posts
  ├─ Drafts
  ├─ Failed Posts
  └─ Approval Queue

Automation
  ├─ Automation Dashboard
  ├─ Automation Rules
  ├─ Auto Publishing
  ├─ Auto Commenting
  ├─ Auto Replies
  ├─ Auto Likes
  ├─ Auto Follow
  ├─ Auto Messaging
  ├─ History
  ├─ Logs
  └─ Approval Queue

Research Center
  ├─ Explorer
  ├─ Collections
  ├─ Knowledge Base
  ├─ Sources
  ├─ Reports
  ├─ Bookmarks
  └─ AI Research

Trend Intelligence
  ├─ Trend Dashboard
  ├─ Discovery
  ├─ Score
  ├─ Comparison
  ├─ Competitors
  ├─ Forecast
  └─ War Room

Accounts
  ├─ Facebook
  ├─ Instagram
  ├─ TikTok
  ├─ Threads
  ├─ LinkedIn
  ├─ X
  ├─ Pinterest
  └─ YouTube

Analytics
  ├─ Executive Dashboard
  ├─ Reach
  ├─ Engagement
  ├─ Followers
  ├─ ROI
  ├─ Growth
  ├─ Conversions
  └─ AI Performance

AI Center
  ├─ Provider Manager
  ├─ Gateway
  ├─ Prompt Library
  ├─ Token Usage
  ├─ Costs
  ├─ Agent Monitor
  ├─ AI Logs
  ├─ Provider Health
  └─ Settings

Team
  ├─ Members
  ├─ Permissions
  ├─ Roles
  ├─ Audit Logs
  └─ Activity

Settings
  ├─ General
  ├─ Profile
  ├─ Billing
  ├─ API Keys
  ├─ Notifications
  ├─ Security
  ├─ Workspace
  └─ Preferences
```

## Key Pages

### Dashboard

Overview with:
- Analytics cards (Connected Accounts, Scheduled Posts, Published Today, AI Tasks, Active Automations)
- Publishing Calendar (drag and drop)
- AI Suggestions (trending topics, best posting time, hashtags)
- Recent Activity timeline

### Content Studio

AI-powered content creation tools:
- AI Writer with templates
- Hook Generator
- Caption Generator
- Script Writer
- Media library and editor
- Draft library with version control

### Automation

The heart of Social Farm AI:
- Real-time automation dashboard
- Rule builder with visual interface
- Execution monitor with logs
- Error queue and retry controls
- Success rate monitoring
- Worker status and health

### Trend Intelligence

- Real-time trend discovery
- Trend scoring algorithm
- Competitive analysis
- Future predictions
- Alert system for trend changes
- War room for crisis management

### AI Center

- Multi-provider management
- Token usage optimization
- Prompt library management
- AI agent monitoring
- Cost tracking and alerts
- System health monitoring

## Performance & Accessibility

### Performance Optimizations

- Code splitting with dynamic imports
- Image optimization (next/image)
- Lazy loading for off-screen content
- Virtualized tables for large datasets
- Caching strategies
- Bundle analyzer for optimization

### Accessibility Standards

- WCAG 2.1 AA compliance
- Keyboard navigation
- ARIA labels and roles
- High contrast mode
- Screen reader support
- Focus management
- Semantic HTML

## Animation & Micro-interactions

- Page transitions (slide fade)
- Hover effects on cards and buttons
- Loading states with skeleton screens
- Modal animations
- Sidebar collapse animations
- Progress indicators
- Success/error notifications

## Technology Stack

### Frontend Framework
- Next.js 14 (App Router)
- React 18
- TypeScript

### Styling
- Tailwind CSS 3.x
- Headless UI for dropdowns, modals, etc.

### State Management
- Zustand (lightweight, no boilerplate)

### HTTP Client
- TanStack Query (formerly React Query)
- Axios for API calls

### Icons
- lucide-react

### Charts
- Recharts
- Chart.js

### Form Library
- React Hook Form

### Date Library
- date-fns
- React DayPicker

### HTTP Cache
- SWR

## State Management

### Stores

- `uiStore`: UI state (modals, notifications, theme)
- `authStore`: Authentication state
- `workspaceStore`: Workspace management
- `accountStore`: Connected social accounts
- `contentStore`: Content creation state
- `automationStore`: Automation rules and execution
- `analyticsStore`: Dashboard analytics and metrics
- `aiStore`: AI provider and agent state

### Global State Management

- Zustand for lightweight state
- Context providers for React
- Local storage for persistence

## API Integration

### Data Fetching

- Server-side rendering for critical paths
- Incremental Static Regeneration (ISR)
- SWR for real-time data
- Server components for static content

### Error Handling

- Global error boundaries
- Retry logic with exponential backoff
- Graceful degradation
- User-friendly error messages

### Auth

- JWT with HTTP-only cookies
- OAuth for social media accounts
- Multi-factor authentication
- Session management

## Responsive Design

Support for:
- Desktop (1280px+)
- Laptop (1024-1280px)
- Tablet (768-1024px)
- Mobile (480-768px)
- Large screens (1600px+)

Mobile-first approach with responsive breakpoints.