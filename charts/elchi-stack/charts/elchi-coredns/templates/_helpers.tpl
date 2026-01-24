{{/*
Expand the name of the chart.
*/}}
{{- define "elchi-coredns.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "elchi-coredns.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "elchi-coredns.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "elchi-coredns.labels" -}}
helm.sh/chart: {{ include "elchi-coredns.chart" . }}
{{ include "elchi-coredns.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: dns
app.kubernetes.io/part-of: elchi
{{- end }}

{{/*
Selector labels
*/}}
{{- define "elchi-coredns.selectorLabels" -}}
app.kubernetes.io/name: {{ include "elchi-coredns.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
