# Docker Architecture

## 1. Container Architecture
Social Farm AI OS utilizes a microservices-based container architecture. Each service is encapsulated in its own container, ensuring isolation, scalability, and ease of deployment.

### Service Components
*   **Frontend**: Next.js application, optimized for production.
*   **Backend**: Python/FastAPI application, handling API requests and business logic.
*   **AI Workers**: Specialized Python containers for asynchronous AI inference tasks.
*   **Database**: PostgreSQL container (or managed service in production).
*   **Cache**: Redis container for session management and caching.
*   **Reverse Proxy**: Nginx container for traffic routing, SSL termination, and security.

## 2. Networking
Containers communicate over a private, isolated Docker network.
*   **Internal Network**: Only the Reverse Proxy container exposes ports (80/443) to the host/external network.
*   **Service Discovery**: Internal DNS names provided by Docker/Kubernetes are used for inter-service communication.

## 3. Volumes
*   **Persistent Data**: Database and storage volumes are mapped to host-level persistent storage or cloud-native storage solutions (e.g., AWS EBS, Azure Disk).
*   **Logs**: Shared volume for log aggregation, mapped to a centralized logging agent.
*   **Configuration**: Configuration files are mounted as read-only volumes.

## 4. Images
*   **Base Images**: Minimal, hardened base images (e.g., Alpine Linux) are used to reduce attack surface.
*   **Multi-stage Builds**: Used to minimize final image size and exclude build-time dependencies.
*   **Tagging**: Images are tagged with the commit SHA and semantic version.

## 5. Compose Structure
`docker-compose.yml` defines the multi-container application, service dependencies, network configurations, and volume mappings. It is used primarily for local development and testing.

## 6. Workflows
*   **Development**: `docker-compose up` for local development with hot-reloading enabled.
*   **Production**: Images are built in the CI pipeline, pushed to a secure registry, and deployed via container orchestration (e.g., Kubernetes or Docker Swarm).
