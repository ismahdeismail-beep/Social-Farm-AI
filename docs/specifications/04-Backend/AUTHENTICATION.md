# AUTHENTICATION

## Purpose
Secure identification and session management.

## Strategy
- **JWT (JSON Web Token):** Stateless authentication.
- **Refresh Tokens:** Persistent token management.
- **Login Flow:** Validate credentials -> Sign JWT -> Create Refresh Token session.
- **Password:** Argon2 hashing algorithm.

| Flow | Status | Security |
| :--- | :--- | :--- |
| Login | Verified | TLS / Hashing |
| Token Refresh | Verified | Secure Storage |
