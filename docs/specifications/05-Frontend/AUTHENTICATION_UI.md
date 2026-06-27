# Frontend Specification: AUTHENTICATION_UI

## Purpose
Manage user identification and session lifecycle.

## Components
- LoginForm, RegisterForm, ForgotPasswordForm.
- ProfileSwitch, LogoutAction.

## Flow
- AuthGuard (HOC/Wrapper) to protect routes.
- JWT storage in secure HttpOnly cookies (preferred) or secure local storage.
- Session lifecycle handled by Auth Store.
