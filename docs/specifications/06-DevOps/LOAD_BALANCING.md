# Load Balancing

## Design
A reverse proxy (Nginx/Traefik) acts as the load balancer.

## Health Checks
Active health checks monitor service availability. Unhealthy instances are automatically removed from the rotation.

## Sticky Sessions
Sticky sessions are disabled by default to ensure statelessness.

## Scaling
Load balancer scales horizontally based on traffic demand.

## Traffic Routing
Traffic is routed based on path-based rules (e.g., `/api` -> Backend, `/` -> Frontend).
