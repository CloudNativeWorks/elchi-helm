# Grafana Dashboard Generator

This directory contains tools to automatically generate Grafana dashboards for Elchi Envoy metrics.

## Overview

We provide two dashboards for different monitoring needs:

| Dashboard | Purpose | Metrics | Panels | Size | Use Case |
|-----------|---------|---------|--------|------|----------|
| **Elchi Dashboard** | Comprehensive analysis | 577 | 244 | 832 KB | Deep debugging, incident investigation |
| **Elchi Minimal Dashboard** | Essential monitoring | 25 | 26 | 67 KB | Daily monitoring, health checks |

## Files

### Source Files
- **`metrics-source.json`**: Simplified source for comprehensive dashboard
- **`metrics-source-minimal.json`**: Simplified source for minimal dashboard with critical metrics

### Generator
- **`generate_dashboard.py`**: Python script to generate dashboard JSON from source

### Generated Dashboards
- **`elchi-dashboard.json`**: Full Grafana dashboard JSON (auto-generated)
- **`elchi-minimal-dashboard.json`**: Minimal Grafana dashboard JSON (auto-generated)

### Documentation
- **`README.md`**: This file - comprehensive guide
- **`QUICK_START.md`**: Quick start guide
- **`MINIMAL_DASHBOARD_PLAN.md`**: Implementation plan for minimal dashboard

## Quick Start

### Generate Comprehensive Dashboard

```bash
cd charts/elchi-stack/charts/grafana/dashboards
python3 generate_dashboard.py
```

### Generate Minimal Dashboard

```bash
cd charts/elchi-stack/charts/grafana/dashboards
python3 generate_dashboard.py -s metrics-source-minimal.json -o elchi-minimal-dashboard.json
```

### Generate Both Dashboards

```bash
# Generate comprehensive dashboard
python3 generate_dashboard.py

# Generate minimal dashboard
python3 generate_dashboard.py -s metrics-source-minimal.json -o elchi-minimal-dashboard.json
```

## Minimal Dashboard Structure

The minimal dashboard focuses on 25 critical Envoy metrics organized into 5 rows:

### Row 1: Health & Status (5 metrics)
- Server Live Status
- Uptime
- Worker Thread Concurrency
- Memory Allocated
- Heap Size

### Row 2: Cluster Health (4 metrics)
- Active Clusters
- Total Members
- Healthy Members
- Degraded Members

### Row 3: Downstream - Client to Envoy (8 metrics)
- Active Connections
- Request Rate
- Active Requests
- Response Time (p95, p99)
- Success Rate (2xx)
- Client Error Rate (4xx)
- Server Error Rate (5xx)

### Row 4: Upstream - Envoy to Backend (5 metrics)
- Active Connections
- Request Rate
- Active Requests
- Request Timeouts
- Request Retries

### Row 5: Circuit Breakers & Resilience (4 metrics)
- Ejected Hosts
- Connection Circuit Breaker Opens
- Request Circuit Breaker Opens
- Connection Pool Overflow

## Adding New Metrics

### 1. Edit Source File

Edit `metrics-source.json` (comprehensive) or `metrics-source-minimal.json` (minimal) and add your metric:

```json
{
  "title": "Panel Title",
  "description": "Panel description",
  "metric_names": ["metric1", "metric2"],
  "unit": "reqps",
  "panel_type": "timeseries",
  "width": 12,
  "queries": [
    {
      "metric": "metric_name",
      "legend": "{{label}}",
      "type": "rate",
      "group_by": "label_name"
    }
  ]
}
```

### 2. Regenerate Dashboard

```bash
# For comprehensive dashboard
python3 generate_dashboard.py

# For minimal dashboard
python3 generate_dashboard.py -s metrics-source-minimal.json -o elchi-minimal-dashboard.json
```

The script will automatically generate the complete Grafana dashboard JSON.

## Source JSON Format

### Dashboard Information

```json
{
  "dashboard_info": {
    "title": "Dashboard Title",
    "uid": "dashboard-uid",
    "tags": ["tag1", "tag2"],
    "refresh": "10s"
  }
}
```

### Metric Definitions

Each metric group creates a **row** containing multiple **panels**:

```json
{
  "metrics": [
    {
      "row_title": "Row Title",
      "is_collapsed": false,
      "panels": [
        {
          "title": "Panel Title",
          "description": "Panel description",
          "metric_names": ["metric1", "metric2"],
          "unit": "reqps",
          "panel_type": "timeseries",
          "width": 12,
          "queries": [...]
        }
      ]
    }
  ]
}
```

### Panel Fields

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `title` | Panel title | Yes | `"Downstream Request Rate"` |
| `description` | Panel description | Yes | `"Rate of downstream requests"` |
| `metric_names` | List of metric names (shown in title) | Yes | `["downstream_rq_total"]` |
| `unit` | Unit type | Yes | `"reqps"`, `"cps"`, `"ops"`, `"ms"`, `"bytes"`, `"Bps"`, `"short"` |
| `panel_type` | Panel type | No | `"timeseries"` (default), `"stat"` |
| `width` | Panel width (0-24) | No | `12` (default) |
| `queries` | List of Prometheus queries | Yes | See below |

### Query Types

#### 1. Rate Query (for counters)

Measures change rate over time (e.g., requests per second):

```json
{
  "metric": "downstream_rq_total",
  "legend": "{{envoy_http_conn_manager_prefix}}",
  "type": "rate",
  "group_by": "envoy_http_conn_manager_prefix"
}
```

**Generated Prometheus Query:**
```promql
sum by (envoy_http_conn_manager_prefix)(rate({__name__=~"${service}_${project}_.*downstream_rq_total", envoy_http_conn_manager_prefix!="admin", client_name=~"$client"}[1m]))
```

#### 2. Gauge Query (for instantaneous values)

Measures current values (e.g., active connection count):

```json
{
  "metric": "http_downstream_cx_active",
  "legend": "Active: {{envoy_http_conn_manager_prefix}}",
  "type": "gauge",
  "group_by": "envoy_http_conn_manager_prefix"
}
```

**Generated Prometheus Query:**
```promql
sum by (envoy_http_conn_manager_prefix)({__name__="${service}_${project}_http_downstream_cx_active", envoy_http_conn_manager_prefix!="admin", client_name=~"$client"})
```

#### 3. Histogram Query (for distributions)

Measures value distribution with percentiles (e.g., p50, p90, p95, p99):

```json
{
  "metric": "http_downstream_cx_length_ms_bucket",
  "legend": "p95 - HTTP: {{envoy_http_conn_manager_prefix}}",
  "type": "histogram",
  "quantile": 0.95,
  "group_by": "envoy_http_conn_manager_prefix"
}
```

**Generated Prometheus Query:**
```promql
histogram_quantile(0.95, sum by (le, envoy_http_conn_manager_prefix)(rate({__name__=~"${service}_${project}_.*http_downstream_cx_length_ms_bucket", envoy_http_conn_manager_prefix!="admin", client_name=~"$client"}[1m])))
```

### Query Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `metric` | Metric name | Yes | - |
| `legend` | Legend format (Grafana template) | Yes | - |
| `type` | Query type: `rate`, `gauge`, `histogram` | Yes | - |
| `group_by` | Prometheus group by label | No | - |
| `quantile` | Percentile for histogram (0.0-1.0) | No (required for histogram) | - |
| `exclude_cluster` | Cluster name to exclude | No | - |

### Special Cases

#### Upstream Metrics

For upstream metrics, you can add cluster filtering:

```json
{
  "metric": "upstream_cx_total",
  "legend": "{{envoy_cluster_name}}",
  "type": "rate",
  "group_by": "envoy_cluster_name",
  "exclude_cluster": "elchi-control-plane"
}
```

#### Listener Metrics

Grouping by listener address:

```json
{
  "metric": "listener_downstream_cx_total",
  "legend": "{{envoy_listener_address}}",
  "type": "rate",
  "group_by": "envoy_listener_address"
}
```

#### Metric Name Prefix

Some metrics start with a prefix (e.g., `_downstream_cx_destroy_total`). In this case, add `_` at the beginning:

```json
{
  "metric": "_downstream_cx_destroy_total",
  "legend": "{{envoy_http_conn_manager_prefix}}",
  "type": "rate",
  "group_by": "envoy_http_conn_manager_prefix"
}
```

## Unit Types

| Unit | Description | Usage |
|------|-------------|-------|
| `reqps` | Requests per second | Request rates |
| `cps` | Connections per second | Connection rates |
| `ops` | Operations per second | General operation rates |
| `ms` | Milliseconds | Duration metrics |
| `bytes` | Bytes | Data size |
| `Bps` | Bytes per second | Data transfer rate |
| `short` | Short format | General numbers |
| `s` | Seconds | Time duration |

## Panel Types

| Type | Description | Usage |
|------|-------------|-------|
| `timeseries` | Time series graph (default) | Trends over time |
| `stat` | Single stat panel | Current values, status |

## Example: Adding a New Metric

### 1. Add a new panel

In `metrics-source.json` or `metrics-source-minimal.json`, add to the appropriate row:

```json
{
  "row_title": "Downstream - Request Metrics",
  "is_collapsed": false,
  "panels": [
    {
      "title": "Request Timeout Rate",
      "description": "Rate of requests that timed out",
      "metric_names": ["downstream_rq_timeout"],
      "unit": "reqps",
      "panel_type": "timeseries",
      "width": 12,
      "queries": [
        {
          "metric": "downstream_rq_timeout",
          "legend": "{{envoy_http_conn_manager_prefix}}",
          "type": "rate",
          "group_by": "envoy_http_conn_manager_prefix"
        }
      ]
    }
  ]
}
```

### 2. Regenerate the dashboard

```bash
python3 generate_dashboard.py
# or for minimal:
python3 generate_dashboard.py -s metrics-source-minimal.json -o elchi-minimal-dashboard.json
```

### 3. Deploy with Helm

The dashboard is automatically loaded via ConfigMap when you deploy:

```bash
helm upgrade elchi-stack charts/elchi-stack --values values_dev.yaml
```

## Automatic Features

The script automatically generates:

1. **Panel IDs**: Unique IDs are automatically assigned
2. **Grid Positions**: Panels are automatically positioned
3. **Prometheus Queries**: Correct query format based on type
4. **Legend Format**: With template variables
5. **Thresholds**: Default threshold values
6. **Tooltip**: Multi-series support
7. **Colors**: Palette-classic color scheme
8. **Variables**: Service, Project, Client filters
9. **Annotations**: Grafana annotations support

## Dashboard Variables

Template variables available in all panels:

- `${service}`: Selected service name
- `${project}`: Selected project ID
- `$client`: Selected client (multi-select with "All" option)

## Command Line Options

```bash
# Show help
python3 generate_dashboard.py --help

# Generate with custom source and output
python3 generate_dashboard.py --source SOURCE_FILE --output OUTPUT_FILE

# Using short flags
python3 generate_dashboard.py -s SOURCE_FILE -o OUTPUT_FILE
```

## When to Use Each Dashboard

### Use Minimal Dashboard When:
- Daily monitoring and health checks
- Quick overview of system status
- Monitoring SLIs (Service Level Indicators)
- Dashboard on public displays
- Mobile/tablet viewing
- Performance is critical (smaller size, faster rendering)

### Use Comprehensive Dashboard When:
- Investigating incidents
- Deep performance analysis
- Debugging specific Envoy features
- Analyzing HTTP/network filters
- Troubleshooting TLS, QUIC, or advanced protocols
- Need access to all 577 metrics

## Troubleshooting

### Dashboard not generating

```bash
# Ensure Python 3 is installed
python3 --version

# Give execution permission to the script
chmod +x generate_dashboard.py

# Run manually
python3 generate_dashboard.py
```

### Queries not working

- Verify metric names are correct
- Check if metrics exist in Prometheus: `{__name__=~".*your_metric.*"}`
- Verify labels are correct
- Check template variable values

### Panel not showing

- Ensure `width` does not exceed 24
- Verify JSON syntax is correct
- Check panel_type is valid (`timeseries` or `stat`)

### File too large

If the generated dashboard JSON is too large:
- Use the minimal dashboard instead
- Remove unused metrics from source
- Collapse less important rows

## Contributing

When adding new metrics, please:

1. Use descriptive `title` and `description`
2. Choose the correct `unit`
3. Fill `metric_names` list completely
4. Use meaningful labels in legend format
5. Add to the appropriate row
6. Test the generated dashboard in Grafana

## Dashboard Comparison

| Feature | Comprehensive | Minimal |
|---------|--------------|---------|
| Total Metrics | 577 | 25 |
| Total Panels | 244 | 26 |
| Total Rows | 52 | 5 |
| Expanded Rows | 5 | 5 |
| File Size | 832 KB | 67 KB |
| Load Time | Slower | Faster |
| Use Case | Debugging | Monitoring |

## License

These tools are developed as part of the Elchi project.
