# Accessibility — Social Farm AI OS

## Overview

This document outlines accessibility standards and best practices for Social Farm AI OS, ensuring WCAG 2.1 AA compliance.

## WCAG 2.1 Compliance

### Level A Requirements

#### 1. Non-text Content
- All images have descriptive `alt` text
- Decorative images use `alt=""`
- Icons have accessible labels

```tsx
// ✅ Good
<Image src="/logo.png" alt="Social Farm AI logo" />
<Icon aria-label="Close menu" />

// ❌ Bad
<Image src="/logo.png" />
<Icon />
```

#### 2. Time-based Media
- Videos have captions
- Audio has transcripts
- No auto-playing media

#### 3. Adaptable Content
- Semantic HTML elements
- Proper heading hierarchy
- ARIA landmarks

```tsx
// ✅ Good
<header role="banner">
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/home">Home</a></li>
    </ul>
  </nav>
</header>

<main role="main">
  <h1>Page Title</h1>
  <section aria-labelledby="section1">
    <h2 id="section1">Section Title</h2>
  </section>
</main>

<footer role="contentinfo">
  <p>&copy; 2026 Social Farm AI</p>
</footer>
```

#### 4. Distinguishable
- Color contrast ratio ≥ 4.5:1 (normal text)
- Color contrast ratio ≥ 3:1 (large text)
- Text can be resized up to 200%

### Level AA Requirements

#### 1.4.3 Contrast (Minimum)
```css
/* ✅ Good - meets 4.5:1 ratio */
.text-primary { color: #1f2937; } /* Gray 800 */
.text-secondary { color: #6b7280; } /* Gray 500 */

/* ❌ Bad - doesn't meet contrast ratio */
.text-light { color: #9ca3af; } /* Gray 400 */
```

#### 2.1 Keyboard Accessible
- All interactive elements are keyboard accessible
- Focus order is logical
- No keyboard traps

```tsx
// ✅ Good - keyboard accessible
<button onClick={handleClick}>Click me</button>
<a href="/page">Link</a>
<input type="text" onChange={handleChange} />

// ❌ Bad - not keyboard accessible
<div onClick={handleClick}>Click me</div>
<span onClick={handleClick}>Click me</span>
```

#### 2.4.1 Bypass Blocks
- Skip navigation link
- Landmark regions

```tsx
// Skip navigation
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

<main id="main-content">
  {/* Page content */}
</main>
```

#### 2.4.3 Focus Order
- Logical tab order
- Visible focus indicators

```css
/* Focus styles */
:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Remove default outline for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

#### 2.4.7 Focus Visible
- Clear focus indicators
- Minimum 2px outline

## Component Accessibility

### Buttons

```tsx
// ✅ Accessible button
<button
  type="button"
  onClick={handleClick}
  aria-label="Close dialog"
  className="focus:outline-none focus:ring-2 focus:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// Button with loading state
<button
  type="button"
  disabled={isLoading}
  aria-busy={isLoading}
  aria-live="polite"
>
  {isLoading ? 'Loading...' : 'Submit'}
</button>
```

### Forms

```tsx
// ✅ Accessible form
<form onSubmit={handleSubmit}>
  <div>
    <label htmlFor="email">Email address</label>
    <input
      type="email"
      id="email"
      name="email"
      aria-required="true"
      aria-invalid={errors.email ? 'true' : 'false'}
      aria-describedby={errors.email ? 'email-error' : undefined}
    />
    {errors.email && (
      <p id="email-error" role="alert" className="text-red-500">
        {errors.email}
      </p>
    )}
  </div>
  
  <button type="submit">Submit</button>
</form>
```

### Modals

```tsx
// ✅ Accessible modal
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>
  
  <button onClick={onConfirm}>Confirm</button>
  <button onClick={onCancel}>Cancel</button>
</div>
```

### Navigation

```tsx
// ✅ Accessible navigation
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <a
        href="/dashboard"
        role="menuitem"
        aria-current={isActive ? 'page' : undefined}
      >
        Dashboard
      </a>
    </li>
    <li role="none">
      <a
        href="/settings"
        role="menuitem"
        aria-current={isActive ? 'page' : undefined}
      >
        Settings
      </a>
    </li>
  </ul>
</nav>
```

### Tables

```tsx
// ✅ Accessible table
<table>
  <caption>Recent transactions</caption>
  <thead>
    <tr>
      <th scope="col">Date</th>
      <th scope="col">Description</th>
      <th scope="col">Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2026-01-15</td>
      <td>Payment received</td>
      <td>$100.00</td>
    </tr>
  </tbody>
</table>
```

## ARIA Patterns

### Live Regions

```tsx
// Announce dynamic updates
<div aria-live="polite" aria-atomic="true">
  {notification && <p>{notification}</p>}
</div>

// Assertive announcements
<div aria-live="assertive" role="alert">
  {error && <p>{error}</p>}
</div>
```

### Expanded/Collapsed

```tsx
// ✅ Expandable section
<button
  aria-expanded={isExpanded}
  aria-controls="section-content"
  onClick={toggle}
>
  Section Title
</button>
<div
  id="section-content"
  role="region"
  aria-labelledby="section-button"
  hidden={!isExpanded}
>
  {/* Content */}
</div>
```

### Listbox

```tsx
// ✅ Custom listbox
<div
  role="listbox"
  aria-label="Select an option"
  aria-activedescendant={activeOption}
>
  <div
    role="option"
    id="option-1"
    aria-selected={selectedOption === 'option-1'}
  >
    Option 1
  </div>
  <div
    role="option"
    id="option-2"
    aria-selected={selectedOption === 'option-2'}
  >
    Option 2
  </div>
</div>
```

## Testing

### Automated Testing

```bash
# Install axe-core
npm install @axe-core/react

# Use in React components
import { useEffect } from 'react';
import axe from 'axe-core';

useEffect(() => {
  axe.run().then(results => {
    if (results.violations.length > 0) {
      console.error('Accessibility violations:', results.violations);
    }
  });
}, []);
```

### Manual Testing

1. **Keyboard Navigation**
   - Tab through all interactive elements
   - Verify focus order is logical
   - Check focus indicators are visible

2. **Screen Reader Testing**
   - Test with NVDA (Windows)
   - Test with VoiceOver (macOS)
   - Test with TalkBack (Android)

3. **Color Contrast**
   - Use WebAIM Contrast Checker
   - Verify text is readable
   - Check for color-blindness

4. **Zoom Testing**
   - Zoom to 200%
   - Verify content is readable
   - Check no content is cut off

## Common Issues

### 1. Missing Alt Text
```tsx
// ❌ Bad
<img src="chart.png" />

// ✅ Good
<img src="chart.png" alt="Sales chart showing 20% growth in Q4" />
```

### 2. Missing Labels
```tsx
// ❌ Bad
<input type="email" />

// ✅ Good
<label htmlFor="email">Email</label>
<input type="email" id="email" />
```

### 3. Low Contrast
```css
/* ❌ Bad - contrast ratio 2.5:1 */
.text { color: #9ca3af; background: #f3f4f6; }

/* ✅ Good - contrast ratio 7:1 */
.text { color: #1f2937; background: #ffffff; }
```

### 4. Keyboard Traps
```tsx
// ❌ Bad - keyboard trap
<div tabIndex={0}>
  <input type="text" />
</div>

// ✅ Good - proper tab order
<div>
  <input type="text" tabIndex={0} />
</div>
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [React Accessibility](https://reactjs.org/docs/accessibility.html)

## Checklist

### Semantic HTML
- [ ] Use proper heading hierarchy (h1-h6)
- [ ] Use landmark regions (header, nav, main, footer)
- [ ] Use lists for navigation
- [ ] Use tables for tabular data

### Forms
- [ ] All inputs have labels
- [ ] Required fields are marked
- [ ] Error messages are descriptive
- [ ] Form validation is accessible

### Keyboard
- [ ] All interactive elements are focusable
- [ ] Focus order is logical
- [ ] Focus indicators are visible
- [ ] No keyboard traps

### Color & Contrast
- [ ] Text meets contrast ratios
- [ ] Information not conveyed by color alone
- [ ] Focus states have sufficient contrast

### ARIA
- [ ] ARIA labels for interactive elements
- [ ] Live regions for dynamic content
- [ ] Proper roles and states
- [ ] No ARIA overuse