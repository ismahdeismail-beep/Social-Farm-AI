# Reverse Proxy

## Nginx Configuration
*   **Compression**: Gzip enabled for static assets.
*   **Caching**: Static assets cached at the edge and proxy level.
*   **Headers**: Security headers (HSTS, CSP, X-Frame-Options) injected.
*   **Routing**: Path-based routing to backend services.
*   **Security**: Rate limiting and request filtering enabled.
