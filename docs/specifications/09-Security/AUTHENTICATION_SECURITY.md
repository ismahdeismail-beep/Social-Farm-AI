# Authentication Security

## 1. Password Policy
*   Minimum 12 characters.
*   Must include uppercase, lowercase, numbers, and special characters.
*   Password history check (cannot reuse last 5 passwords).

## 2. Password Hashing
*   Algorithm: Argon2id.
*   Cost factors: Configurable based on hardware.

## 3. JWT Security
*   Algorithm: RS256 (Asymmetric).
*   Short-lived access tokens (15 minutes).
*   Long-lived refresh tokens (stored in secure, HttpOnly, SameSite=Strict cookies).

## 4. Session Security
*   Session timeout after 30 minutes of inactivity.
*   Session invalidation on logout or password change.

## 5. MFA Readiness
*   Architecture supports TOTP (Time-based One-Time Password) via feature flag.

## 6. Rate Limiting & Account Lockout
*   5 failed attempts -> 15-minute lockout.
*   IP-based rate limiting on login endpoints.
