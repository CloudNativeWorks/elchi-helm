#!/usr/bin/env python3
"""
Grafana Dashboard Generator

This script generates a complete Grafana dashboard JSON from a simplified metrics-source.json file.

Usage:
    # Comprehensive dashboard (default)
    python3 generate_dashboard.py

    # Minimal dashboard
    python3 generate_dashboard.py --source metrics-source-minimal.json --output elchi-minimal-dashboard.json

    # Or with short flags
    python3 generate_dashboard.py -s metrics-source-minimal.json -o elchi-minimal-dashboard.json

Input file (default): metrics-source.json (in the same directory as this script)
Output file (default): elchi-dashboard.json (in the same directory as this script)

Source JSON Format:
{
  "dashboard_info": {
    "title": "Dashboard Title",
    "uid": "dashboard-uid",
    "tags": ["tag1", "tag2"],
    "refresh": "10s"
  },
  "datasource": {
    "type": "prometheus",
    "uid": "datasource-uid"
  },
  "metrics": [
    {
      "row_title": "Row Title",
      "panels": [
        {
          "title": "Panel Title",
          "description": "Panel description",
          "metric_names": ["metric1", "metric2"],  # Used for title
          "unit": "short",  # ops, cps, reqps, ms, bytes, Bps, short, etc.
          "queries": [
            {
              "metric": "metric_name",
              "legend": "{{label}}",
              "type": "rate",  # rate, gauge, histogram
              "group_by": "label_name",  # optional
              "quantile": 0.95,  # for histogram only
              "exclude_cluster": "cluster_name"  # optional, for upstream metrics
            }
          ]
        }
      ]
    }
  ]
}

Note: The script automatically generates:
- Panel IDs
- Grid positions (automatic layout)
- Prometheus queries (based on type: rate(), histogram_quantile(), etc.)
- Legend formats
- Thresholds
- Color schemes
- Tooltip settings
- And all other Grafana configurations
"""

import json
import os
import argparse
from typing import Dict, List, Any

# Script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def build_prometheus_query(query_config: Dict[str, Any]) -> str:
    """Builds Prometheus query"""
    metric = query_config["metric"]
    group_by = query_config.get("group_by", "")
    query_type = query_config.get("type", "rate")
    exclude_cluster = query_config.get("exclude_cluster")
    default_value = query_config.get("default_value")  # Value to show if metric doesn't exist
    max_value = query_config.get("max_value")  # Maximum acceptable value

    # Metric name pattern
    metric_pattern = f"${{service}}_${{project}}_{metric}"

    # Filters
    filters = []

    # Exclude admin prefix (for downstream metrics)
    if "downstream" in metric or "http_downstream" in metric:
        filters.append('envoy_http_conn_manager_prefix!="admin"')

    # Cluster exclude
    if exclude_cluster:
        filters.append(f'envoy_cluster_name!="{exclude_cluster}"')

    # Client filter
    filters.append('client_name=~"$client"')

    filter_str = ", ".join(filters)

    # Build query based on query type
    if query_type == "histogram":
        quantile = query_config.get("quantile", 0.95)
        if group_by:
            query = f'histogram_quantile({quantile}, sum by (le, {group_by})(rate({{__name__=~"{metric_pattern}", {filter_str}}}[1m])))'
        else:
            query = f'histogram_quantile({quantile}, sum(rate({{__name__=~"{metric_pattern}", {filter_str}}}[1m])) by (le))'

    elif query_type == "rate":
        if group_by:
            query = f'sum by ({group_by})(rate({{__name__=~"{metric_pattern}", {filter_str}}}[1m]))'
        else:
            query = f'sum(rate({{__name__=~"{metric_pattern}", {filter_str}}}[1m]))'

    elif query_type == "gauge":
        if group_by:
            query = f'sum by ({group_by})({{__name__="${{service}}_${{project}}_{metric}", {filter_str}}})'
        else:
            query = f'sum({{__name__="${{service}}_${{project}}_{metric}", {filter_str}}})'

    else:
        raise ValueError(f"Unknown query type: {query_type}")

    # If max_value is specified, show 0 if value exceeds this threshold
    if max_value is not None:
        query = f'(({query}) < {max_value}) * ({query})'

    # If default_value is specified and metric doesn't exist, show it
    if default_value is not None:
        query = f'({query}) or vector({default_value})'

    return query



def create_target(query_config: Dict[str, Any], ref_id: str) -> Dict[str, Any]:
    """Creates Grafana target (query) object"""
    return {
        "editorMode": "code",
        "expr": build_prometheus_query(query_config),
        "legendFormat": query_config.get("legend", "{{label}}"),
        "range": True,
        "refId": ref_id
    }


def create_panel(panel_config: Dict[str, Any], panel_id: int, x: int, y: int) -> Dict[str, Any]:
    """Creates Grafana panel object"""

    # Create targets
    targets = []
    ref_ids = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for idx, query in enumerate(panel_config["queries"]):
        targets.append(create_target(query, ref_ids[idx]))

    # Create title with metric names
    metric_names = ", ".join(panel_config.get("metric_names", []))
    full_title = f"{panel_config['title']} ({metric_names})" if metric_names else panel_config['title']

    # Unit
    unit = panel_config.get("unit", "short")

    # Panel width (usually 12, sometimes 24)
    width = panel_config.get("width", 12)

    # Panel type (timeseries or stat)
    panel_type = panel_config.get("panel_type", "timeseries")

    # Special title for stat panel (without metric names)
    if panel_type == "stat":
        full_title = panel_config['title']

    # Base panel structure
    panel = {
        "datasource": {
            "type": "prometheus",
            "uid": "victoriametrics"
        },
        "description": panel_config.get("description", ""),
        "fieldConfig": {
            "defaults": {
                "color": {
                    "mode": "palette-classic" if panel_type == "timeseries" else "thresholds"
                },
                "mappings": [],
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {
                            "color": "green",
                            "value": 0 if panel_type == "timeseries" else None
                        },
                        {
                            "color": "yellow",
                            "value": 80
                        } if panel_type == "stat" else None
                    ]
                },
                "unit": unit
            },
            "overrides": []
        },
        "gridPos": {
            "h": 4 if panel_type == "stat" else 8,
            "w": width,
            "x": x,
            "y": y
        },
        "id": panel_id,
        "pluginVersion": "12.2.1",
        "targets": targets,
        "title": full_title,
        "type": panel_type
    }
    
    # Filter threshold steps (remove None values)
    panel["fieldConfig"]["defaults"]["thresholds"]["steps"] = [
        s for s in panel["fieldConfig"]["defaults"]["thresholds"]["steps"] if s is not None
    ]

    # Special settings based on panel type
    if panel_type == "timeseries":
        panel["fieldConfig"]["defaults"]["custom"] = {
            "axisBorderShow": False,
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "barWidthFactor": 0.6,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "none",
            "hideFrom": {
                "legend": False,
                "tooltip": False,
                "viz": False
            },
            "insertNulls": False,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
                "type": "linear"
            },
            "showPoints": "never",
            "showValues": False,
            "spanNulls": False,
            "stacking": {
                "group": "A",
                "mode": "none"
            },
            "thresholdsStyle": {
                "mode": "off"
            }
        }
        panel["options"] = {
            "legend": {
                "calcs": [
                    "mean",
                    "lastNotNull",
                    "max"
                ],
                "displayMode": "table",
                "placement": "bottom",
                "showLegend": True
            },
            "tooltip": {
                "hideZeros": False,
                "mode": "multi",
                "sort": "desc"
            }
        }
    elif panel_type == "stat":
        panel["options"] = {
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {
                "values": False,
                "calcs": [
                    "lastNotNull"
                ],
                "fields": ""
            },
            "textMode": "auto"
        }

    return panel


def create_row_panel(title: str, row_id: int, y: int, is_collapsed: bool = False) -> Dict[str, Any]:
    """Creates row panel"""
    return {
        "collapsed": is_collapsed,
        "gridPos": {
            "h": 1,
            "w": 24,
            "x": 0,
            "y": y
        },
        "id": row_id,
        "panels": [],
        "title": title,
        "type": "row"
    }


def generate_dashboard(source: Dict[str, Any]) -> Dict[str, Any]:
    """Generates complete Grafana dashboard from source JSON"""

    dashboard_info = source["dashboard_info"]

    # Template variables
    variables = [
        {
            "current": {
                "text": "q3",
                "value": "q3"
            },
            "definition": "label_values(__name__)",
            "description": "Select the service to monitor",
            "label": "Service",
            "name": "service",
            "options": [],
            "query": {
                "qryType": 1,
                "query": "label_values(__name__)",
                "refId": "PrometheusVariableQueryEditor-VariableQuery"
            },
            "refresh": 1,
            "regex": "(.*)_[0-9a-f]{24}_.*",
            "sort": 1,
            "type": "query"
        },
        {
            "current": {
                "text": "68ac8add4d6ae9208b24492b",
                "value": "68ac8add4d6ae9208b24492b"
            },
            "definition": "label_values(__name__)",
            "description": "Select the project ID",
            "label": "Project",
            "name": "project",
            "options": [],
            "query": {
                "qryType": 1,
                "query": "label_values(__name__)",
                "refId": "PrometheusVariableQueryEditor-VariableQuery"
            },
            "refresh": 1,
            "regex": ".*_([0-9a-f]{24,}).*",
            "sort": 1,
            "type": "query"
        },
        {
            "allowCustomValue": False,
            "current": {
                "text": "All",
                "value": [
                    "$__all"
                ]
            },
            "definition": "label_values(client_name)",
            "includeAll": True,
            "label": "Client",
            "multi": True,
            "name": "client",
            "options": [],
            "query": {
                "qryType": 1,
                "query": "label_values(client_name)",
                "refId": "PrometheusVariableQueryEditor-VariableQuery"
            },
            "refresh": 1,
            "regex": "",
            "type": "query"
        }
    ]

    # Create panels
    panels = []
    panel_id = 1
    row_id = 100
    y_position = 0

    for metric_group in source["metrics"]:
        # Add row panel - get is_collapsed value from source (default False)
        is_collapsed = metric_group.get("is_collapsed", False)
        row_panel = create_row_panel(metric_group["row_title"], row_id, y_position, is_collapsed)

        row_id += 1
        y_position += 1

        # Position panels side by side in each row
        x_position = 0
        max_row_height = 0
        row_panels = []  # Panels belonging to this row

        for panel_config in metric_group["panels"]:
            width = panel_config.get("width", 12)

            # If panel doesn't fit in row, move to new row
            if x_position + width > 24:
                x_position = 0
                y_position += max_row_height
                max_row_height = 0

            panel = create_panel(panel_config, panel_id, x_position, y_position)

            # If collapsed row, add panel inside row, otherwise add to main panels
            if is_collapsed:
                row_panels.append(panel)
            else:
                panels.append(panel)

            panel_id += 1
            x_position += width
            max_row_height = max(max_row_height, 8)  # Panel height = 8

        # If collapsed row, put panels inside row
        if is_collapsed:
            row_panel["panels"] = row_panels

        # Add row to main panels
        panels.append(row_panel)
        y_position += max_row_height

    # Dashboard object
    dashboard = {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {
                        "type": "datasource",
                        "uid": "grafana"
                    },
                    "enable": True,
                    "hide": True,
                    "iconColor": "rgba(0, 211, 255, 1)",
                    "name": "Annotations & Alerts",
                    "type": "dashboard"
                }
            ]
        },
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "id": 0,
        "links": [],
        "panels": panels,
        "preload": False,
        "refresh": dashboard_info.get("refresh", "10s"),
        "schemaVersion": 42,
        "tags": dashboard_info.get("tags", []),
        "templating": {
            "list": variables
        },
        "time": {
            "from": "now-30m",
            "to": "now"
        },
        "timepicker": {
            "refresh_intervals": [
                "5s",
                "10s",
                "30s",
                "1m",
                "5m"
            ]
        },
        "timezone": "browser",
        "title": dashboard_info["title"],
        "uid": dashboard_info["uid"],
        "version": 11
    }

    return dashboard


def main():
    """Main function"""
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Grafana Dashboard Generator - Generates Grafana dashboard JSON from simplified source',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate comprehensive dashboard (default)
  %(prog)s

  # Generate minimal dashboard
  %(prog)s --source metrics-source-minimal.json --output elchi-minimal-dashboard.json

  # Using short flags
  %(prog)s -s metrics-source-minimal.json -o elchi-minimal-dashboard.json
        """
    )

    parser.add_argument(
        '-s', '--source',
        default='metrics-source.json',
        help='Source JSON file with simplified metrics (default: metrics-source.json)'
    )

    parser.add_argument(
        '-o', '--output',
        default='elchi-dashboard.json',
        help='Output Grafana dashboard JSON file (default: elchi-dashboard.json)'
    )

    args = parser.parse_args()

    # Create full file paths
    source_file = os.path.join(SCRIPT_DIR, args.source)
    output_file = os.path.join(SCRIPT_DIR, args.output)

    print(f"Reading source file: {source_file}")

    # Read source file
    if not os.path.exists(source_file):
        print(f"ERROR: Source file not found: {source_file}")
        return 1

    with open(source_file, 'r', encoding='utf-8') as f:
        source = json.load(f)

    print("Generating dashboard...")

    # Generate dashboard
    dashboard = generate_dashboard(source)

    # Write output
    print(f"Writing dashboard: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)

    print("✓ Dashboard generated successfully!")
    print(f"  - Source: {args.source}")
    print(f"  - Output: {args.output}")
    print(f"  - Total panels: {len([p for p in dashboard['panels'] if p['type'] != 'row'])}")
    print(f"  - Total rows: {len([p for p in dashboard['panels'] if p['type'] == 'row'])}")

    return 0


if __name__ == "__main__":
    exit(main())
