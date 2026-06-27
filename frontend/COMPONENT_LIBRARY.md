# SOCIAL-FARM-AI FRONTEND V2 COMPONENT LIBRARY

## Overview

This document serves as a comprehensive reference for all UI components used throughout the Social Farm AI OS Frontend V2. Each component includes implementation details, props, and usage examples.

## Component Index

1. [Avatar](#avatar)
2. [Breadcrumb](#breadcrumb)
3. [Button](#button)
4. [Card](#card)
5. [Checkbox](#checkbox)
6. [Chip](#chip)
7. [Drawer](#drawer)
8. [DropdownMenu](#dropdownmenu)
9. [EmptyState](#emptystate)
10. [Hero](#hero)
11. [Input](#input)
12. [KpiCard](#kpCard)
13. [List](#list)
14. [Modal](#modal)
15. [NavItem](#navitem)
16. [Progress](#progress)
17. [ProgressBar](#progressBar)
18. [RadioButton](#radiobutton)
19. [SearchBar](#searchbar)
20. [Select](#select)
21. [Skeleton](#skeleton)
22. [StatusBadge](#statusBadge)
23. [Table](#table)
24. [Tabs](#tabs)
25. [Tag](#tag)
26. [TextArea](#textarea)
27. [Timeline](#timeline)
28. [Toast](#toast)
29. [Toggle](#toggle)
30. [Tooltip](#tooltip)

## Avatar

A user avatar component that supports images, initials, and fallback icons.

### Props

```typescript
interface AvatarProps {
  src?: string;
  alt?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  fallback?: string;
  status?: 'online' | 'offline' | 'busy' | 'away';
  className?: string;
}
```

### Size Options

- `xs`: 24px
- `sm`: 32px  
- `md`: 40px
- `lg`: 48px
- `xl`: 64px

### Usage Example

```tsx
<Avatar 
  src="/avatars/user.jpg"
  alt="John Doe"
  size="md"
  status="online"
/>

<Avatar 
  fallback="JD"
  size="lg"
/>
```

## Breadcrumb

Navigation breadcrumb trail for hierarchical navigation.

### Props

```typescript
interface BreadcrumbProps {
  items: BreadcrumbItem[];
  separator?: React.ReactNode;
  className?: string;
}

interface BreadcrumbItem {
  label: string;
  href?: string;
  onClick?: () => void;
  isCurrent?: boolean;
}
```

### Usage Example

```tsx
<Breadcrumb
  items=[
    { label: 'Dashboard', href: '/' },
    { label: 'Accounts', href: '/accounts' },
    { label: 'Facebook', isCurrent: true }
  ]
/>
```

## Button

A versatile button component with multiple variants and sizes.

### Props

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success' | 'warning';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  asChild?: boolean;
}
```

### Variants

- `primary`: Gradient blue/purple button (default)
- `secondary`: Solid gray button
- `outline`: Border-only button
- `ghost`: Text-only button
- `danger`: Red gradient button
- `success`: Green gradient button
- `warning`: Orange gradient button

### Usage Example

```tsx
<Button variant="primary" size="md">
  Create Post
</Button>

<Button variant="outline" leftIcon={<PlusIcon />}>
  Add Account
</Button>

<Button isLoading={loading} disabled={isDisabled}>
  Save Changes
</Button>
```

## Card

A flexible container component for grouping related content.

### Props

```typescript
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'interactive' | 'bordered' | 'glass' | 'elevated';
  padding?: 'none' | 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}
```

### Variants

- `default`: Standard card with surface background
- `interactive`: Hoverable with cursor pointer
- `bordered`: Card with emphasis border
- `glass`: Frosted glass effect
- `elevated`: Higher elevation shadow

### Usage Example

```tsx
<Card padding="lg">
  <CardHeader>
    <CardTitle>Connected Accounts</CardTitle>
    <CardDescription>Manage your social media accounts</CardDescription>
  </CardHeader>
  <CardContent>
    // Content goes here
  </CardContent>
  <CardFooter>
    // Footer actions
  </CardFooter>
</Card>
```

## Checkbox

Checkbox component for multiple selection.

### Props

```typescript
interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  description?: string;
  error?: string;
  indeterminate?: boolean;
}
```

### Usage Example

```tsx
<Checkbox
  id="notifications"
  label="Email Notifications"
  description="Receive email alerts for important events"
/>

<Checkbox
  id="terms"
  label="I agree to the terms and conditions"
  error="You must accept the terms to continue"
/>
```

## Chip

A small component for displaying tags or status.

### Props

```typescript
interface ChipProps {
  label: string;
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'outline';
  size?: 'sm' | 'md';
  avatar?: React.ReactNode;
  onDelete?: () => void;
  clickable?: boolean;
  active?: boolean;
}
```

### Usage Example

```tsx
<Chip label="Active" variant="success" size="sm" />
<Chip label="Pending" variant="warning" size="md" />
<Chip label="John Doe" avatar={<Avatar fallback="JD" size="xs" />} onDelete={() => {}} />
```

## Drawer

A slide-out drawer component for panels and menus.

### Props

```typescript
interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  position?: 'left' | 'right';
  overlay?: boolean;
}
```

### Usage Example

```tsx
<Drawer
  isOpen={isDrawerOpen}
  onClose={() => setIsDrawerOpen(false)}
  title="Automation Rules"
  size="lg"
  position="right"
>
  // Drawer content
</Drawer>
```

## DropdownMenu

Context menu button with dropdown list of options.

### Props

```typescript
interface DropdownMenuProps {
  trigger: React.ReactNode;
  items: DropdownMenuItem[];
  align?: 'start' | 'end' | 'center';
  side?: 'top' | 'bottom' | 'left' | 'right';
}

interface DropdownMenuItem {
  label: string;
  icon?: React.ReactNode;
  onClick: () => void;
  divider?: boolean;
  disabled?: boolean;
  destructive?: boolean;
}
```

### Usage Example

```tsx
<DropdownMenu
  trigger={<Button variant="ghost" size="sm">⋮</Button>}
  items={menuItems}
  align="end"
>
  Items displayed here
</DropdownMenu>
```

## EmptyState

A component shown when there is no data to display.

### Props

```typescript
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}
```

### Usage Example

```tsx
<EmptyState
  icon={<InboxIcon className="w-12 h-12 text-gray-400" />}
  title="No posts scheduled"
  description="Create your first post to start publishing"
  action={<Button>Create Post</Button>}
/>
```

## Hero

Large section hero with title, subtitle, and actions.

### Props

```typescript
interface HeroProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  background?: 'gradient' | 'image' | 'dark';
  className?: string;
}
```

### Usage Example

```tsx
<Hero
  title="AI-Powered Social Media Management"
  subtitle="Create, schedule, and automate your social media posts with AI"
  background="gradient"
  actions={
    <Button size="lg" variant="primary">
      Get Started
    </Button>
  }
/>
```

## Input

Text input field with label, error handling, and helper text.

### Props

```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}
```

### Usage Example

```tsx
<Input
  type="email"
  label="Email Address"
  placeholder="john@example.com"
  error="Please enter a valid email"
  helperText="We'll never share your email."
/>

<Input
  type="password"
  label="Password"
  placeholder="Enter your password"
  leftIcon={<LockIcon />}
/>
```

## KpiCard

Card component specifically for displaying Key Performance Indicators.

### Props

```typescript
interface KpiCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'increase' | 'decrease' | 'neutral';
  icon?: React.ReactNode;
  trend?: number[];
  format?: 'number' | 'percent' | 'currency' | 'short';
  className?: string;
}
```

### Usage Example

```tsx
<KpiCard
  title="Total Followers"
  value={12547}
  change="+12%"
  changeType="increase"
  icon={<UsersIcon className="w-8 h-8" />}
  format="number"
/>

<KpiCard
  title="Engagement Rate"
  value={3.8}
  change="-0.2%"
  changeType="decrease"
  icon={<TrendingUpIcon className="w-8 h-8" />}
  format="percent"
/>
```

## List

List component for displaying collections of items.

### Props

```typescript
interface ListProps {
  items: ListItem[];
  renderItem: (item: ListItem, index: number) => React.ReactNode;
  className?: string;
  emptyState?: React.ReactNode;
}

interface ListItem {
  id: string;
  [key: string]: any;
}
```

### Usage Example

```tsx
<List
  items={accounts}
  renderItem={(account) => (
    <ListItem key={account.id}>
      <div>{account.name}</div>
      <div>{account.followers} followers</div>
    </ListItem>
  )}
/>
```

## Modal

A centered modal dialog for user confirmations, forms, or detailed views.

### Props

```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlay?: boolean;
  closeOnEsc?: boolean;
}
```

### Usage Example

```tsx
<Modal
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  title="Create New Post"
  description="Fill in the details for your social media post"
  size="lg"
>
  <div>Modal content goes here</div>
</Modal>
```

## NavItem

Single item in a navigation tree.

### Props

```typescript
interface NavItemProps {
  label: string;
  href?: string;
  icon?: React.ReactNode;
  badge?: string | number;
  isActive?: boolean;
  onClick?: () => void;
  subItems?: NavItem[];
}
```

### Usage Example

```tsx
<NavItem
  label="Dashboard"
  href="/dashboard"
  icon={<HomeIcon />}
  isActive={isActive}
/>

<NavItem
  label="Analytics"
  icon={<ChartBarIcon />}
  subItems={subNavItems}
/>
```

## Progress

Circular progress indicator with percentage and label.

### Props

```typescript
interface ProgressProps {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'default' | 'success' | 'warning' | 'error';
  showValue?: boolean;
  label?: string;
}
```

### Usage Example

```tsx
<Progress value={75} size="lg" variant="success" showValue label="API Health" />
```

## ProgressBar

Linear progress bar for multi-step processes.

### Props

```typescript
interface ProgressBarProps {
  value: number;
  max?: number;
  steps?: ProgressStep[];
  showValue?: boolean;
  color?: string;
  className?: string;
}

interface ProgressStep {
  label: string;
  value?: number;
}
```

### Usage Example

```tsx
<ProgressBar 
  value={3} 
  max={5} 
  steps={[{label: 'Connected'}, {label: 'Drafted'}, {label: 'Scheduled'}, {label: 'Published'}, {label: 'Analyzed'}]} 
/>
```

## RadioButton

Single selection radio button group.

### Props

```typescript
interface RadioButtonProps {
  id: string;
  value: string;
  label: string;
  description?: string;
  groupName: string;
  checked?: boolean;
  onChange?: (value: string) => void;
}
```

### Usage Example

```tsx
<RadioButton
  id="frequency-daily"
  value="daily"
  label="Daily"
  description="Post once every day"
  groupName="frequency"
/>

<RadioButton
  id="frequency-weekly"
  value="weekly"
  label="Weekly"
  description="Post once every week"
  groupName="frequency"
/>
```

## SearchBar

Search input with suggestions, filters, and clear functionality.

### Props

```typescript
interface SearchBarProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (value: string) => void;
  onClear?: () => void;
  suggestions?: string[];
  filter?: boolean;
  recentSearches?: string[];
}
```

### Usage Example

```tsx
<SearchBar
  placeholder="Search for posts, topics, or accounts..."
  suggestions={['automation', 'ai tools', 'marketing tips']}
  recentSearches={['dashboard', 'analytics', 'schedules']}
/>
```

## Select

Dropdown select with search functionality.

### Props

```typescript
interface SelectProps<T> {
  value?: T;
  onValueChange?: (value: T) => void;
  options: SelectOption<T>[];
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  searchable?: boolean;
  multiSelect?: boolean;
  clearable?: boolean;
}

interface SelectOption<T> {
  value: T;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}
```

### Usage Example

```tsx
<Select
  placeholder="Select an account"
  options={accounts.map(acc => ({ value: acc.id, label: acc.name }))}
/>

<Select
  placeholder="Select multiple platforms"
  options={platforms}
  multiSelect
/>
```

## Skeleton

Loading skeleton components for better UX during data fetching.

### Props

```typescript
interface SkeletonProps {
  className?: string;
  animation?: 'pulse' | 'wave' | 'none';
  variant?: 'text' | 'rect' | 'circle';
}
```

### Usage Example

```tsx
<Skeleton variant="rect" className="w-full h-32 rounded-lg" />
<Skeleton variant="text" className="w-3/4 h-4" />
<Skeleton variant="circle" className="w-10 h-10" />
```

## StatusBadge

A non-interactive badge for displaying status.

### Props

```typescript
interface StatusBadgeProps {
  status: 'success' | 'warning' | 'danger' | 'info' | 'neutral' | 'processing';
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  rounded?: boolean;
  dot?: boolean;
}
```

### Usage Example

```tsx
<StatusBadge status="success" label="Online" />
<StatusBadge status="warning" label="Degraded" dot />
<StatusBadge status="danger" label="Failed" size="lg" />
```

## Table

Data table with sorting, searching, and pagination.

### Props

```typescript
interface TableProps<T> {
  columns: TableColumn<T>[];
  data: T[];
  keyExtractor?: (item: T) => string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  onSort?: (key: string) => void;
  pagination?: PaginationProps;
  rowActions?: (row: T) => TableAction[];
  emptyState?: React.ReactNode;
}

interface TableColumn<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
  className?: string;
}

interface TableAction {
  label: string;
  icon?: React.ReactNode;
  onClick: (row: T) => void;
  variant?: 'default' | 'danger' | 'success';
}

interface PaginationProps {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
}
```

### Usage Example

```tsx
<Table
  columns={columns}
  data={posts}
  sortBy="scheduledAt"
  sortOrder="desc"
  pagination={{ page: 1, pageSize: 10, total: 100, onPageChange: setPage }}
  rowActions={(row) => [
    { label: 'Edit', onClick: () => editPost(row.id) },
    { label: 'Delete', onClick: () => deletePost(row.id), variant: 'danger' }
  ]}
/>
```

## Tabs

Tab navigation for switching between views.

### Props

```typescript
interface TabsProps<T> {
  tabs: Tab<T>[];
  value?: T;
  onValueChange?: (value: T) => void;
  defaultValue?: T;
  variant?: 'default' | 'pills' | 'underline';
}

interface Tab<T> {
  value: T;
  label: string;
  icon?: React.ReactNode;
  content: React.ReactNode;
}
```

### Usage Example

```tsx
<Tabs
  tabs={[
    { value: 'analytics', label: 'Analytics', content: <Analytics /> },
    { value: 'traffic', label: 'Traffic', content: <Traffic /> },
    { value: 'engagement', label: 'Engagement', content: <Engagement /> }
  ]}
/>
```

## Tag

Tag component for filtering and categorization.

### Props

```typescript
interface TagProps {
  label: string;
  onRemove?: () => void;
  removable?: boolean;
  variant?: 'default' | 'filled' | 'outlined';
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple' | 'gray';
}
```

### Usage Example

```tsx
<Tag label="Marketing" color="blue" variant="filled" />
<Tag label="Q1 2024" color="green" variant="outlined" onRemove={() => {}} />
```

## TextArea

Multi-line text input for longer content.

### Props

```typescript
interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  maxLength?: number;
  showCount?: boolean;
}
```

### Usage Example

```tsx
<TextArea
  label="Post Content"
  placeholder="Write your post content here..."
  rows={5}
  maxLength={280}
  showCount
/>
```

## Timeline

Chronological timeline for displaying sequential events.

### Props

```typescript
interface TimelineProps {
  events: TimelineEvent[];
  className?: string;
}

interface TimelineEvent {
  id: string;
  title: string;
  description?: string;
  date: Date;
  status?: 'success' | 'warning' | 'error' | 'info';
  icon?: React.ReactNode;
  action?: React.ReactNode;
}
```

### Usage Example

```tsx
<Timeline
  events={[
    { id: '1', title: 'Post Scheduled', date: new Date(), status: 'success' },
    { id: '2', title: 'AI Analysis Complete', date: new Date(Date.now() - 86400000), status: 'info' },
  ]}
/>
```

## Toast

Notification toast component for user feedback.

### Props

```typescript
interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose?: () => void;
}
```

### Usage Example

```tsx
<Toast
  message="Post created successfully!"
  type="success"
  duration={3000}
/>
```

## Toggle

Switch component for toggling between two states.

### Props

```typescript
interface ToggleProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  label?: string;
  description?: string;
}
```

### Usage Example

```tsx
<Toggle
  checked={notificationsEnabled}
  onChange={setNotificationsEnabled}
  label="Push Notifications"
  description="Receive notifications for important events"
/>
```

## Tooltip

Small contextual tooltip on hover or focus.

### Props

```typescript
interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactNode;
  placement?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
}
```

### Usage Example

```tsx
<Tooltip content="This field is required">
  <Input placeholder="Required field" />
</Tooltip>
```

## Installation

To use the component library, install the base components:

```bash
npm install @social-farm-ai/ui
```

Or import individual components:

```tsx
import { Button, Card, Input, Modal, Tabs } from '@social-farm-ai/ui';
```

## Theme Provider

Wrap your application with the ThemeProvider to ensure consistent theming:

```tsx
import { ThemeProvider } from '@social-farm-ai/ui';

<ThemeProvider>
  <App />
</ThemeProvider>
```

## Accessibility

All components are built with accessibility in mind:
- Proper ARIA labels
- Keyboard navigation support
- Focus management
- Screen reader compatibility
- Color contrast compliance

## Contributing

1. Fork the repository
2. Make your changes
3. Run tests: `npm test`
4. Run lint: `npm run lint`
5. Commit with conventional commits
6. Push and create a pull request