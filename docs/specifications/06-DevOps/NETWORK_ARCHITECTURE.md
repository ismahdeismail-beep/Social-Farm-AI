# Network Architecture

## Traffic Flow
1.  **External Traffic**: Hits CDN/Load Balancer.
2.  **Reverse Proxy**: Terminates SSL and routes traffic.
3.  **Internal Services**: Communicate over private Docker network.

## Firewall
Strict firewall rules allow only necessary traffic (e.g., 80/443 from external, internal ports only accessible within the network).

## Service Communication
Services communicate via internal DNS names provided by Docker/Kubernetes.

## CDN Integration
CDN caches static assets and provides DDoS protection.
