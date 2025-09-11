[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/elchi)](https://artifacthub.io/packages/search?repo=elchi)

# Elchi Helm Repository

Official Helm charts for the **Elchi** ecosystem - a comprehensive proxy management platform.

## 📦 Available Charts

| Chart | Description | Version |
|-------|-------------|---------|
| [**elchi-stack**](./charts/elchi-stack/) | Complete proxy management platform | ![Version](https://img.shields.io/badge/version-1.0.0-blue) |
| [**elchi-discovery**](./charts/elchi-discovery/) | Service discovery & registry | ![Version](https://img.shields.io/badge/version-1.0.0-blue) |

## 🚀 Quick Start

### Add Repository
```bash
helm repo add elchi https://charts.elchi.io
helm repo update
```

### Install Charts
```bash
# Complete platform
helm install my-stack elchi/elchi-stack \
  --set global.mainAddress="your-domain.com"

# Discovery service only
helm install my-discovery elchi/elchi-discovery
```

## 📖 Documentation

- **elchi-stack**: [Complete documentation](./charts/elchi-stack/README.md)
- **elchi-discovery**: [Complete documentation](./charts/elchi-discovery/README.md)

## 🛠️ Development

### Local Development
```bash
git clone https://github.com/cloudnativeworks/elchi-helm.git
cd elchi-helm

# Install from local
helm install my-stack charts/elchi-stack/
helm install my-discovery charts/elchi-discovery/
```

## 📋 Requirements

- **Kubernetes**: 1.19+
- **Helm**: 3.0.0+
- **Resources**: 2+ CPU cores, 4GB+ RAM per node

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/cloudnativeworks/elchi-helm/issues)
- **Documentation**: [Official Docs](https://charts.elchi.io)
- **Community**: [Discussions](https://github.com/cloudnativeworks/elchi-helm/discussions)

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.