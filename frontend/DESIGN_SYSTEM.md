# SOCIAL-FARM-AI FRONTEND V2 DESIGN SYSTEM

## Design Tokens

### Colors

```css
/* Primary Backgrounds */
--bg-primary: #0B0F14;
--bg-secondary: #121822;
--bg-surface: #1A2230;
--bg-hover: #1E293B;
--bg-active: #334155;

/* Text Colors */
--text-primary: #F1F5F9;
--text-secondary: #94A3B8;
--text-muted: #64748B;
--text-disabled: #475569;
--text-error: #F43F5E;
--text-success: #10B981;
--text-warning: #FBBF24;
--text-info: #38BDF8;

/* Border Colors */
--border-primary: #334155;
--border-secondary: #1E293B;
--border-muted: #0F172A;

/* Accent Colors */
--accent-purple: #8B5CF6;
--accent-blue: #3B82F6;
--accent-teal: #14B8A6;
--accent-green: #10B981;
--accent-orange: #F97316;
--accent-red: #EF4444;

/* Gradients */
--gradient-primary: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
--gradient-secondary: linear-gradient(135deg, #14B8A6 0%, #10B981 100%);
--gradient-success: linear-gradient(135deg, #10B981 0%, #84CC16 100%);
--gradient-warning: linear-gradient(135deg, #F97316 0%, #FBBF24 100%);
--gradient-danger: linear-gradient(135deg, #EF4444 0%, #F43F5E 100%);
```

### Typography

```css
/* Font Families */
--font-display: 'Inter', system-ui, sans-serif;
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Font Sizes - Responsive */
--text-display: clamp(2rem, 4vw, 3rem);
--text-h1: clamp(1.75rem, 3vw, 2.5rem);
--text-h2: clamp(1.5rem, 2.5vw, 2rem);
--text-h3: clamp(1.25rem, 2vw, 1.75rem);
--text-h4: clamp(1.125rem, 1.5vw, 1.5rem);
--text-body: 1rem;
--text-small: 0.875rem;
--text-caption: 0.75rem;

/* Font Weights */
--weight-thin: 100;
--weight-extralight: 200;
--weight-light: 300;
--weight-normal: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
--weight-extrabold: 800;
--weight-black: 900;

/* Line Heights */
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;

/* Letter Spacing */
--tracking-tighter: -0.05em;
--tracking-tight: -0.025em;
--tracking-normal: 0;
--tracking-wide: 0.025em;
--tracking-wider: 0.05em;
--tracking-widest: 0.1em;
```

### Spacing (8px Grid)

```css
--space-0: 0;
--space-1: 0.25rem; /* 4px */
--space-2: 0.5rem; /* 8px */
--space-3: 0.75rem; /* 12px */
--space-4: 1rem; /* 16px */
--space-5: 1.25rem; /* 20px */
--space-6: 1.5rem; /* 24px */
--space-7: 1.75rem; /* 28px */
--space-8: 2rem; /* 32px */
--space-9: 2.5rem; /* 40px */
--space-10: 3rem; /* 48px */
--space-11: 3.5rem; /* 56px */
--space-12: 4rem; /* 64px */
```

### Border Radius

```css
--radius-none: 0;
--radius-sm: 0.25rem; /* 4px */
--radius-md: 0.5rem; /* 8px */
--radius-lg: 0.75rem; /* 12px */
--radius-xl: 1rem; /* 16px */
--radius-2xl: 1.5rem; /* 24px */
--radius-full: 9999px;
```

### Shadows

```css
--shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
--shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
--shadow-none: none;
```

### Animations

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
--easing-ease: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--easing-ease-in: cubic-bezier(0.42, 0, 1, 1);
--easing-ease-out: cubic-bezier(0, 0, 0.58, 1);
--easing-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
```

## ComponentStyles

### Button

```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition-property: all;
  transition-duration: var(--transition-fast);
  focus:outline-none;
  focus:ring-2;
  focus:ring-offset-2;
  focus:ring-offset-gray-900;
  disabled:opacity-50;
  disabled:cursor-not-allowed;
}

.button-primary {
  background-image: var(--gradient-primary);
  color: white;
  box-shadow: var(--shadow-sm);
}

.button-primary:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.button-secondary {
  background-color: var(--bg-surface);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
}

.button-secondary:hover {
  background-color: var(--bg-hover);
  border-color: var(--accent-blue);
}

.button-ghost {
  color: var(--text-secondary);
}

.button-ghost:hover {
  color: var(--text-primary);
  background-color: var(--bg-hover);
}

.button-outline {
  background-color: transparent;
  border: 1px solid var(--border-primary);
  color: var(--text-primary);
}

.button-outline:hover {
  background-color: var(--bg-surface);
}

.button-danger {
  background-image: var(--gradient-danger);
  color: white;
  box-shadow: var(--shadow-sm);
}

.button-danger:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
```

### Card

```css
.card {
  background-color: var(--bg-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-secondary);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-interactive {
  cursor: pointer;
}

.card-interactive:hover {
  border-color: var(--accent-blue);
  box-shadow: var(--shadow-lg);
}

.card-glass {
  background: rgba(26, 34, 48, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--border-secondary);
}

.card-content {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--border-secondary);
}
```

### Input

```css
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: var(--text-body);
  transition: all var(--transition-fast);
}

.input:focus {
  outline: none;
  border-color: var(--accent-blue);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input::placeholder {
  color: var(--text-muted);
}

.input-error {
  border-color: var(--text-error);
}

.input-error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-label {
  display: block;
  margin-bottom: var(--space-2);
  font-size: var(--text-small);
  font-weight: 500;
  color: var(--text-secondary);
}

.input-helper {
  margin-top: var(--space-2);
  font-size: var(--text-caption);
  color: var(--text-muted);
}

.input-error-text {
  margin-top: var(--space-2);
  font-size: var(--text-caption);
  color: var(--text-error);
}
```

### Modal

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  opacity: 0;
  animation: modal-fade-in var(--transition-normal);
}

.modal-content {
  background-color: var(--bg-secondary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-2xl);
  width: 100%;
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  transform: scale(0.95);
  animation: modal-scale-in var(--transition-normal);
}

.modal-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--border-secondary);
}

.modal-body {
  padding: var(--space-6);
}

.modal-footer {
  padding: var(--space-6);
  border-top: 1px solid var(--border-secondary);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-4);
}
```

### Table

```css
.table-container {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-secondary);
  overflow: hidden;
  background-color: var(--bg-surface);
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  background-color: var(--bg-primary);
  position: sticky;
  top: 0;
  z-index: 10;
}

.table-header-cell {
  padding: var(--space-4) var(--space-6);
  text-align: left;
  font-size: var(--text-small);
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.table-row {
  transition: background-color var(--transition-fast);
}

.table-row:hover {
  background-color: var(--bg-hover);
}

.table-cell {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--border-secondary);
  font-size: var(--text-body);
}
```

### Timeline

```css
.timeline {
  position: relative;
  padding-left: var(--space-8);
}

.timeline::before {
  content: '';
  position: absolute;
  left: var(--space-4);
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--gradient-primary);
}

.timeline-item {
  position: relative;
  margin-bottom: var(--space-8);
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -32px;
  top: 8px;
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
  background: var(--gradient-primary);
  border: 3px solid var(--bg-secondary);
  z-index: 1;
}
```

### Notifications

```css
.notification {
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: flex-start;
  animation: slide-in var(--transition-normal);
}

.notification-success {
  background-color: rgba(16, 185, 129, 0.1);
  border-left: 4px solid var(--text-success);
  color: var(--text-success);
}

.notification-error {
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 4px solid var(--text-error);
  color: var(--text-error);
}

.notification-warning {
  background-color: rgba(245, 158, 11, 0.1);
  border-left: 4px solid var(--text-warning);
  color: var(--text-warning);
}

.notification-info {
  background-color: rgba(59, 130, 246, 0.1);
  border-left: 4px solid var(--text-info);
  color: var(--text-info);
}
```

## Animation Keyframes

```css
@keyframes modal-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modal-scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
```

## Theme Variables

The design system uses CSS custom properties for theming. Override these variables to change the theme:

```css
html {
  --bg-primary: #0B0F14;
  --bg-secondary: #121822;
  --bg-surface: #1A2230;
  --text-primary: #F1F5F9;
  --text-secondary: #94A3B8;
  --accent-blue: #3B82F6;
  --accent-purple: #8B5CF6;
}
```

## Usage Guidelines

### When to Use Components

- **Button**: Any action that triggers a state change
- **Card**: Grouping related information
- **Modal**: Short-term focused tasks
- **Table**: Displaying tabular data
- **Timeline**: Showing chronological events
- **Notifications**: User feedback

### Component Composition

- Combine cards with headers, content, and footers
- Use buttons within forms
- Group related inputs in card layouts
- Use tables for data display with pagination
- Chain notifications for feedback

### Best Practices

- Keep consistent spacing and alignment
- Use meaningful color combinations
- Ensure adequate contrast ratios
- Maintain visual hierarchy with size and weight
- Use subtle animations to guide attention
- Provide feedback for all user interactions