# Elchi Discovery - Service Discovery & Registry

Lightweight service discovery and registry component for distributed Envoy deployments.

## 🔍 What's Included

- **Discovery API**: Service registration and discovery endpoints
- **Envoy Proxy**: Configured for discovery mode routing
- **Redis Cache**: Fast service data caching
- **Configuration Registry**: Centralized config management

## 🛠️ Installation

```bash
helm repo add elchi https://chart.elchi.io
helm repo update

helm install my-discovery elchi/elchi-discovery \
  --namespace elchi-discovery --create-namespace
```

## ⚙️ Configuration

### Basic Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.namespace` | Deployment namespace | `"elchi-discovery"` |
| `elchi-discovery-api.enabled` | Enable discovery API | `true` |
| `elchi-discovery-api.replicaCount` | API service replicas | `2` |
| `envoy.enabled` | Enable Envoy proxy | `true` |
| `redis.enabled` | Enable Redis cache | `true` |

### Environment-Specific

| Parameter | Description | Dev Default | Prod Default |
|-----------|-------------|-------------|--------------|
| `elchi-discovery-api.replicaCount` | API replicas | `1` | `3` |
| `envoy.replicaCount` | Envoy replicas | `1` | `2` |
| `redis.persistence.enabled` | Redis persistence | `false` | `true` |
| `redis.auth.enabled` | Redis authentication | `false` | `true` |

## 🚀 Usage Examples

### Development Environment
```bash
helm install dev-discovery elchi/elchi-discovery \
  --set elchi-discovery-api.image.tag=latest \
  --set redis.auth.enabled=false \
  --set redis.persistence.enabled=false \
  --namespace elchi-discovery-dev --create-namespace
```

### Production Environment  
```bash
helm install prod-discovery elchi/elchi-discovery \
  --set elchi-discovery-api.replicaCount=3 \
  --set envoy.replicaCount=2 \
  --set redis.auth.enabled=true \
  --set redis.auth.password="secure-password" \
  --set redis.persistence.enabled=true \
  --set redis.persistence.size=20Gi \
  --namespace elchi-discovery --create-namespace
```

### External Redis
```bash
helm install prod-discovery elchi/elchi-discovery \
  --set redis.enabled=false \
  --set elchi-discovery-api.config.redis.host="external-redis.example.com" \
  --set elchi-discovery-api.config.redis.port=6379
```

## 🔧 API Endpoints

After installation, the discovery API provides:

- **Service Registration**: `POST /api/v1/services`
- **Service Discovery**: `GET /api/v1/services/{service-name}`
- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics`

### Example Usage
```bash
# Port forward to access API
kubectl port-forward svc/elchi-discovery-api 8080:8080 -n elchi-discovery

# Register a service
curl -X POST http://localhost:8080/api/v1/services \
  -H "Content-Type: application/json" \
  -d '{"name": "my-service", "endpoints": ["10.1.1.1:8080", "10.1.1.2:8080"]}'

# Discover services
curl http://localhost:8080/api/v1/services/my-service
```

## 📊 Monitoring

Built-in observability:
- **Metrics**: Prometheus format at `/metrics`
- **Health Checks**: Kubernetes probes configured
- **Envoy Admin**: Available at port 9901

## 🐛 Troubleshooting

### Check Components
```bash
# Check all pods
kubectl get pods -n elchi-discovery

# Check API logs
kubectl logs -f deployment/elchi-discovery-api -n elchi-discovery

# Check Envoy logs  
kubectl logs -f deployment/envoy -n elchi-discovery

# Check Redis
kubectl logs -f deployment/redis -n elchi-discovery
```

### Test Connectivity
```bash
# Test API health
kubectl exec -it deployment/elchi-discovery-api -n elchi-discovery -- curl localhost:8080/health

# Test Redis connection
kubectl exec -it deployment/elchi-discovery-api -n elchi-discovery -- redis-cli ping
```

## 🔄 Upgrading

```bash
helm repo update
helm upgrade my-discovery elchi/elchi-discovery
```

## 🗑️ Uninstalling

```bash
helm uninstall my-discovery
kubectl delete namespace elchi-discovery
```

## 🔗 Integration

This chart can be used standalone or integrated with:
- **elchi-stack**: Full proxy management platform
- **External Envoy**: Configure to use this discovery service
- **Service Mesh**: As service discovery backend