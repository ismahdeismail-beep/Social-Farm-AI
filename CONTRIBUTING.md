# Contributing to Social Farm AI OS

Thank you for your interest in contributing to Social Farm AI OS! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Git

### Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Social-Farm-AI.git
   cd Social-Farm-AI
   ```

2. **Start development environment**
   ```bash
   docker-compose up -d
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names with prefixes:

- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `ci/` - CI/CD changes

Example: `feat/add-user-authentication`

### Development Process

1. Create a new branch from `develop`
2. Make your changes
3. Write or update tests
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all public functions
- Use async/await for asynchronous operations
- Maximum line length: 88 characters (Black formatter)

### TypeScript/React (Frontend)

- Follow ESLint configuration
- Use functional components with hooks
- Write TypeScript types for all props
- Use proper error boundaries
- Follow Next.js best practices

### General

- Write meaningful variable and function names
- Keep functions small and focused
- Add comments for complex logic
- Remove unused code and imports

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```
feat(auth): add JWT authentication

- Implement JWT token generation
- Add login/logout endpoints
- Create authentication middleware

Closes #123
```

## Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git checkout develop
   git merge upstream/develop
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feat/your-feature-name
   ```

5. **Create a Pull Request**
   - Use the PR template
   - Link related issues
   - Add screenshots if applicable
   - Request review from maintainers

### PR Review Checklist

- [ ] Code follows project standards
- [ ] Tests are added/updated
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] All CI checks pass

## Reporting Issues

### Bug Reports

Use the Bug Report template when creating issues. Include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

### Feature Requests

Use the Feature Request template. Include:

- Problem description
- Proposed solution
- Alternatives considered
- Additional context

## Development Tools

### Recommended VS Code Extensions

- Python
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- Docker

### Useful Commands

```bash
# Backend
cd backend
ruff check .          # Linting
ruff format .         # Formatting
pytest -v             # Run tests

# Frontend
cd frontend
npm run lint          # Linting
npm run build         # Build
npm test              # Run tests
```

## Questions?

If you have questions, feel free to:

- Open a discussion
- Join our community chat
- Reach out to maintainers

Thank you for contributing!