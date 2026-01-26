[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/elchi-stack)](https://artifacthub.io/packages/search?repo=elchi-stack)

# Elchi Proxy Management Platform - Helm Charts

This repository contains Helm charts for deploying the **Elchi** - a comprehensive proxy management platform that provides UI-based configuration management for Envoy proxies.

## 🚀 What is Elchi?

Elchi is a proxy management platform that simplifies Envoy proxy configuration through a web-based interface:

- **UI Frontend**: Web interface for creating and managing proxy configurations
- **Controller**: Receives configurations from UI and stores them in MongoDB
- **Control Plane**: Distributes configuration snapshots to Envoy proxies
- **Registry**: Handles routing and service discovery between components

## Requirements

| Requirement | Minimum Version | Maximum Version | Notes |
|-------------|-----------------|-----------------|-------|
| **Kubernetes** | 1.21 | 1.35+ | Uses `policy/v1` PDB (requires 1.21+) |
| **Helm** | 3.0.0 | 3.x | Chart API v2 |
| **CPU** | 2 cores | - | Per node (1.3 cores for pods + system) |
| **Memory** | 4 GB | - | Per node (2.5 GB for pods + system) |

> **Tested Versions**: Kubernetes 1.21 - 1.35 (current latest)

### API Versions Used

| API | Version | Kubernetes Requirement |
|-----|---------|------------------------|
| `apps/v1` | Stable | 1.9+ |
| `policy/v1` | Stable | 1.21+ |
| `v1` (core) | Stable | 1.0+ |
| `rbac.authorization.k8s.io/v1` | Stable | 1.8+ |

## Available Versions
> Syntax: `<elchiBackendVersion>`-`<goControlPlaneVersion>`-`<envoyVersion>`

- `v0.1.0-v0.13.4-envoy1.36.2`

## Global Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.clusterDomain` | Kubernetes cluster domain suffix | `"cluster.local"` |
| `global.mainAddress` | Base URL for all components | `""` (Required) |
| `global.port` | Port for the Elchi controller API. If empty, uses 80/443 based on TLS | `""` |
| `global.tlsEnabled` | Whether to use HTTPS | `false` |
| `global.timezone` | Timezone for all services (e.g., "Europe/Istanbul", "UTC"). If empty, uses host timezone | `""` |
| `global.timezonePath` | Custom path to timezone file on host (advanced users only) | `"/etc/localtime"` |
| `global.installMongo` | Whether to use self-hosted MongoDB | `true` |
| `global.installVictoriaMetrics` | Whether to use self-hosted Victoria Metrics | `true` |
| `global.installGslb` | Whether to deploy GSLB CoreDNS plugin | `true` |
| `global.internalCommunication` | Enable internal communication between services | `false` |
| `global.storageClass` | Storage class for all PVCs (mongodb, victoriametrics) | `"standard"` |
| `global.versions` | List of Elchi backend versions to deploy | `[{tag: v0.1.0-v0.13.4-envoy1.36.2}]` |
| `global.mongodb.hosts` | MongoDB connection hosts (comma-separated for replica set) | `""` |
| `global.mongodb.username` | MongoDB username | `"elchi"` |
| `global.mongodb.password` | MongoDB password | `"elchi"` |
| `global.mongodb.database` | MongoDB database name | `"elchi"` |
| `global.mongodb.scheme` | Connection scheme (mongodb or mongodb+srv) | `""` |
| `global.mongodb.port` | MongoDB connection port | `""` |
| `global.mongodb.replicaset` | Replica set name (if using replica set) | `""` |
| `global.mongodb.timeoutMs` | Connection timeout in milliseconds | `""` |
| `global.mongodb.tlsEnabled` | Enable TLS connection to MongoDB | `""` |
| `global.mongodb.authSource` | Authentication source database (e.g., admin) | `""` |
| `global.mongodb.authMechanism` | Authentication mechanism | `""` |
| `global.victoriametrics.endpoint` | External Victoria Metrics endpoint (required when installVictoriaMetrics is false). Supports both `http://host:port` and `host:port` formats | `""` |
| `global.elchiBackend.controlPlaneDefaultReplicas` | Default replicas for Control Plane services | `4` |
| `global.elchiBackend.controllerDefaultReplicas` | Default replicas for Controller services | `4` |
| `global.envoy.service.type` | Envoy service type (ClusterIP, NodePort, LoadBalancer) | `"NodePort"` |
| `global.envoy.service.httpNodePort` | Fixed NodePort for HTTP (null for auto-assign) | `null` |
| `global.envoy.service.adminNodePort` | Fixed NodePort for admin interface (null for auto-assign) | `null` |
| `global.envoy.service.annotations` | Service annotations (for cloud provider configurations) | `{}` |
| `global.grafana.user` | Grafana login username | `"elchi"` |
| `global.grafana.password` | Grafana login password | `"elchi"` |
| `global.jwt.secret` | JWT secret key for authentication (minimum 32 characters) | `"xK9mP2sV8nQ4wT6yR3jL5bH7fA0cE1gD9kU2oI6vN8xM4qZ"` |
| `global.jwt.accessTokenDuration` | Access token expiration duration | `"1h"` |
| `global.jwt.refreshTokenDuration` | Refresh token expiration duration | `"5h"` |
| `global.cors.allowedOrigins` | CORS allowed origins (use "*" for all, or comma-separated domains) | `"*"` |
| `global.gslb.zone` | DNS zone for GSLB resolution | `"gslb.elchi"` |
| `global.gslb.secret` | Shared secret for CoreDNS plugin authentication | `"elchi-secret-change-me"` |
| `global.gslb.ttl` | Default TTL for DNS records in seconds | `300` |
| `global.gslb.syncInterval` | Interval for syncing DNS records from backend | `"5m"` |
| `global.gslb.timeout` | HTTP request timeout for backend communication | `"10s"` |
| `global.gslb.fallthrough` | Whether to pass unmatched queries to next plugin | `true` |

## ElchiBackend Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Elchi backend image repository | `"jhonbrownn/elchi-backend"` |
| `image.pullPolicy` | Image pull policy | `"Always"` |
| `resources.controller.requests.memory` | Controller service memory request | `"128Mi"` |
| `resources.controller.requests.cpu` | Controller service CPU request | `"100m"` |
| `resources.controller.limits.memory` | Controller service memory limit | `"2Gi"` |
| `resources.controller.limits.cpu` | Controller service CPU limit | `"2000m"` |
| `resources.controlPlane.requests.memory` | Control Plane service memory request | `"256Mi"` |
| `resources.controlPlane.requests.cpu` | Control Plane service CPU request | `"100m"` |
| `resources.controlPlane.limits.memory` | Control Plane service memory limit | `"4Gi"` |
| `resources.controlPlane.limits.cpu` | Control Plane service CPU limit | `"1000m"` |
| `resources.registry.requests.memory` | Registry service memory request | `"64Mi"` |
| `resources.registry.requests.cpu` | Registry service CPU request | `"50m"` |
| `resources.registry.limits.memory` | Registry service memory limit | `"512Mi"` |
| `resources.registry.limits.cpu` | Registry service CPU limit | `"500m"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.controller.port` | Controller REST service port | `8099` |
| `service.controller.grpcPort` | Controller gRPC service port | `50051` |
| `service.controlPlane.port` | Control Plane service port | `18000` |
| `service.registry.port` | Registry gRPC service port | `9090` |
| `service.registry.metricsPort` | Registry metrics service port | `9091` |
| `config.logging.level` | Logging level | `"info"` |
| `config.logging.formatter` | Log formatter type | `"text"` |
| `config.logging.reportCaller` | Whether to report caller in logs | `"false"` |

## Elchi Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicas` | Number of Elchi replicas | `3` |
| `image.repository` | Elchi image repository | `"jhonbrownn/elchi"` |
| `image.tag` | Elchi image tag | `"v0.1.0"` |
| `image.pullPolicy` | Image pull policy | `"Always"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.port` | Service port | `80` |
| `resources.requests.memory` | Memory request | `"32Mi"` |
| `resources.requests.cpu` | CPU request | `"10m"` |
| `resources.limits.memory` | Memory limit | `"256Mi"` |
| `resources.limits.cpu` | CPU limit | `"200m"` |

## Envoy Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicas` | Number of Envoy replicas | `4` |
| `image.repository` | Envoy image repository | `"envoyproxy/envoy"` |
| `image.tag` | Envoy image tag | `"v1.33.0"` |
| `image.pullPolicy` | Image pull policy | `"Always"` |
| `service.type` | Kubernetes service type | `"NodePort"` |
| `service.httpPort` | HTTP service port | `8080` |
| `service.adminPort` | Admin service port | `9901` |
| `resources.requests.memory` | Memory request | `"64Mi"` |
| `resources.requests.cpu` | CPU request | `"50m"` |
| `resources.limits.memory` | Memory limit | `"1Gi"` |
| `resources.limits.cpu` | CPU limit | `"1000m"` |

## MongoDB Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of MongoDB replicas | `1` |
| `image.repository` | MongoDB image repository | `"mongo"` |
| `image.tag` | MongoDB image tag | `"6.0.12"` |
| `image.pullPolicy` | Image pull policy | `"IfNotPresent"` |
| `persistence.enabled` | Enable persistence | `true` |
| `persistence.size` | PVC size | `"5Gi"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.port` | Service port | `27017` |
| `resources.requests.memory` | Memory request | `"256Mi"` |
| `resources.requests.cpu` | CPU request | `"100m"` |
| `resources.limits.memory` | Memory limit | `"2Gi"` |
| `resources.limits.cpu` | CPU limit | `"1000m"` |

## Victoria Metrics Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Victoria Metrics image repository | `"victoriametrics/victoria-metrics"` |
| `image.tag` | Victoria Metrics image tag | `"v1.93.5"` |
| `image.pullPolicy` | Image pull policy | `"IfNotPresent"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.port` | Service port | `8428` |
| `persistence.size` | Storage size for metrics data | `"5Gi"` |
| `retentionPeriod` | Data retention period | `"15d"` |
| `resources.requests.memory` | Memory request | `"128Mi"` |
| `resources.requests.cpu` | CPU request | `"50m"` |
| `resources.limits.memory` | Memory limit | `"2Gi"` |
| `resources.limits.cpu` | CPU limit | `"1000m"` |

## OpenTelemetry Collector Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | OTEL Collector image repository | `"otel/opentelemetry-collector-contrib"` |
| `image.tag` | OTEL Collector image tag | `"0.89.0"` |
| `image.pullPolicy` | Image pull policy | `"IfNotPresent"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.grpcPort` | gRPC service port | `4317` |
| `service.httpPort` | HTTP service port | `4318` |
| `resources.requests.memory` | Memory request | `"64Mi"` |
| `resources.requests.cpu` | CPU request | `"25m"` |
| `resources.limits.memory` | Memory limit | `"512Mi"` |
| `resources.limits.cpu` | CPU limit | `"500m"` |

## Grafana Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Grafana image repository | `"grafana/grafana"` |
| `image.tag` | Grafana image tag | `"12.2.1"` |
| `image.pullPolicy` | Image pull policy | `"IfNotPresent"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.port` | Service port | `3000` |
| `resources.requests.memory` | Memory request | `"64Mi"` |
| `resources.requests.cpu` | CPU request | `"25m"` |
| `resources.limits.memory` | Memory limit | `"512Mi"` |
| `resources.limits.cpu` | CPU limit | `"500m"` |
| `datasource.name` | Datasource name | `"VictoriaMetrics"` |
| `datasource.type` | Datasource type | `"prometheus"` |
| `datasource.access` | Datasource access mode | `"proxy"` |
| `datasource.isDefault` | Set as default datasource | `true` |

## Usage

### Installation

**Important**: This chart does not create the namespace. You must create it before installation:

```bash
kubectl create namespace elchi-stack
```

Or use the `--create-namespace` flag with Helm install command.

```bash
# Basic installation
helm install my-elchi-stack charts/elchi-stack \
  --namespace elchi-stack \
  --create-namespace

# With custom values file
helm install my-elchi-stack charts/elchi-stack \
  --namespace elchi-stack \
  --create-namespace \
  --values values.yaml
```

### Configuration Examples

#### 1. Default Installation (with self-hosted MongoDB and Victoria Metrics)

```yaml
global:
  mainAddress: "your-domain.com"
  port: ""
  tlsEnabled: false
  installMongo: true
  installVictoriaMetrics: true
  versions:
    - tag: v0.1.0-v0.13.4-envoy1.34.2
    - tag: v0.1.0-v0.13.4-envoy1.33.5
  elchiBackend:
    controlPlaneDefaultReplicas: 4
    controllerDefaultReplicas: 4
  envoy:
    service:
      type: NodePort
      httpNodePort: null      # Auto-assign
      adminNodePort: null     # Auto-assign
```

#### 2. Fixed NodePort Configuration (On-Premises)

```yaml
global:
  mainAddress: "elchi.example.com"
  tlsEnabled: true
  installMongo: false
  installVictoriaMetrics: true
  mongodb:
    hosts: "mongodb.example.com:27017"
    username: "elchi"
    password: "elchi"
    database: "elchi"
    scheme: "mongodb"
    tlsEnabled: "true"
    authSource: "admin"
    authMechanism: "SCRAM-SHA-256"
  envoy:
    service:
      type: NodePort
      httpNodePort: 30080     # Fixed port
      adminNodePort: 30901    # Fixed admin port
```

#### 3. LoadBalancer Configuration (Cloud)

```yaml
global:
  mainAddress: "elchi.cloud.example.com"
  tlsEnabled: true
  installMongo: false
  installVictoriaMetrics: false
  mongodb:
    hosts: "mongodb.example.com:27017"
    username: "elchi"
    password: "elchi"
    database: "elchi"
  victoriametrics:
    endpoint: "http://victoria-metrics.example.com:8428"
  envoy:
    service:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
```

#### 4. Both External MongoDB and Victoria Metrics

```yaml
global:
  mainAddress: "your-domain.com"
  installMongo: false
  installVictoriaMetrics: false
  mongodb:
    hosts: "mongodb.example.com:27017"
    username: "elchi"
    password: "elchi"
    database: "elchi"
  victoriametrics:
    endpoint: "victoria-metrics.example.com:8428"  # or "http://victoria-metrics.example.com:8428"
```

### Install/Upgrade Commands

#### Install with values file
```bash
helm install my-elchi-stack charts/elchi-stack \
  --namespace elchi-stack \
  --create-namespace \
  --values values.yaml
```

#### Upgrade with values file
```bash
helm upgrade my-elchi-stack charts/elchi-stack \
  --namespace elchi-stack \
  --values values.yaml
```

#### Install with command line parameters
```bash
helm install my-elchi-stack charts/elchi-stack \
  --namespace elchi-stack \
  --create-namespace \
  --set-string global.mainAddress="elchi.example.com" \
  --set-string global.port="443" \
  --set global.tlsEnabled=true \
  --set global.installVictoriaMetrics=false \
  --set-string global.victoriametrics.endpoint="external-vm.example.com:8428" \
  --set global.envoy.service.type="LoadBalancer"
```

#### Uninstall
```bash
helm uninstall my-elchi-stack --namespace elchi-stack

# Optionally delete the namespace
kubectl delete namespace elchi-stack
```

### Components:

- **🎨 Elchi UI**: React-based web interface for proxy configuration management
- **🎯 Controller**: Receives configurations from UI and validates/stores them in MongoDB
- **🕹️ Control Plane**: Distributes configuration snapshots to Envoy proxy instances
- **📡 Registry**: Handles service discovery and routing between components
- **🌐 Envoy Proxy**: Load balancer and proxy
- **🗄️ MongoDB**: Database for storing proxy configurations (optional - supports external)
- **📊 VictoriaMetrics**: Time-series database for metrics storage (optional - supports external)
- **📈 OpenTelemetry Collector**: Collects and forwards metrics to VictoriaMetrics
- **📉 Grafana**: Visualization and monitoring dashboards for metrics and analytics
- **🌍 Elchi CoreDNS**: GSLB DNS resolution with CoreDNS plugin (DaemonSet)

## Elchi CoreDNS Chart Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | CoreDNS image repository | `"jhonbrownn/elchi-coredns"` |
| `image.tag` | CoreDNS image tag | `"latest"` |
| `image.pullPolicy` | Image pull policy | `"IfNotPresent"` |
| `service.type` | Kubernetes service type | `"ClusterIP"` |
| `service.dnsPort` | DNS service port | `53` |
| `resources.requests.memory` | Memory request | `"32Mi"` |
| `resources.requests.cpu` | CPU request | `"10m"` |
| `resources.limits.memory` | Memory limit | `"256Mi"` |
| `resources.limits.cpu` | CPU limit | `"200m"` |
| `forwarders` | DNS forwarders for non-GSLB queries | `["8.8.8.8", "8.8.4.4"]` |

## Notes

### Namespace Management
- **This chart does NOT create the namespace.** You must create it manually or use `--create-namespace` flag
- This follows Kubernetes and Helm best practices where namespace lifecycle is managed separately from applications
- All resources will be installed in the namespace specified by `--namespace` flag

### External Services
- When `installMongo: false`, you must provide external MongoDB connection details via `global.mongodb.*` parameters
- When `installVictoriaMetrics: false`, you must provide external Victoria Metrics endpoint via `global.victoriametrics.endpoint`

### GSLB CoreDNS Requirements

⚠️ **Important**: When enabling GSLB (`global.installGslb: true`), the following requirements apply:

- **Port 53 must be available** on all Kubernetes nodes where CoreDNS will run
- The CoreDNS DaemonSet uses `hostPort: 53` to bind directly to the node's DNS port
- If `node-local-dns` or another DNS service is already using port 53, the pods will fail to schedule with error: `didn't have free ports for the requested pod ports`

**Alternative: External GSLB Installation**

If port 53 is not available in your Kubernetes cluster (e.g., `node-local-dns` is running), you can install Elchi GSLB externally:

1. Set `global.installGslb: false` in your values file
2. Download and install the standalone GSLB binary from: https://github.com/CloudNativeWorks/elchi-gslb/releases
3. Configure the external GSLB to connect to your Elchi Registry service

This approach is recommended for:
- Clusters with `node-local-dns` or other DNS caching solutions
- Environments where you need more control over DNS infrastructure
- Multi-cluster GSLB deployments

### Envoy Service Configuration
- **NodePort with auto-assign**: Set `global.envoy.service.httpNodePort: null` for automatic port assignment (default)
- **NodePort with fixed port**: Set `global.envoy.service.httpNodePort: 30080` for stable port across deployments
- **LoadBalancer**: Set `global.envoy.service.type: LoadBalancer` for cloud environments
- Use `global.envoy.service.annotations` for cloud-specific configurations (AWS NLB, GCP internal LB, etc.)

### Multi-Version Support
- The system supports multiple backend versions for rolling updates and canary deployments
- Envoy automatically routes traffic based on version headers and load balancing policies

### Timezone Configuration
- All services support timezone configuration via `global.timezone` parameter
- If not specified, services will use the host system's timezone
- Common values: `"UTC"`, `"Europe/Istanbul"`, `"America/New_York"`, etc.
- Advanced users can customize the timezone file path via `global.timezonePath`

### Grafana Access
- Access Grafana at: `http://<mainAddress>/grafana/`
- Default credentials are configured via `global.grafana.user` and `global.grafana.password`
- Grafana comes pre-configured with:
  - VictoriaMetrics as the default datasource
  - Pre-built dashboards for Envoy/Elchi metrics monitoring
  - Dark theme enabled by default

## Security Considerations

⚠️ **Important**: For production deployments, you **MUST** change the following default values:

- **JWT Secret** (`global.jwt.secret`): Change to a secure, randomly generated value of at least 32 characters. The default value is provided for development purposes only.
- **Grafana Credentials** (`global.grafana.user` and `global.grafana.password`): Change the default credentials for Grafana login. The default values (elchi/elchi) should never be used in production environments.
- **MongoDB Credentials** (`global.mongodb.username` and `global.mongodb.password`): If using the built-in MongoDB, change the default credentials.
- **GSLB Secret** (`global.gslb.secret`): Change to a secure value for CoreDNS plugin authentication.
