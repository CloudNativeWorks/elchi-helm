{{/*
Expand the name of the chart.
*/}}
{{- define "elchi-backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "elchi-backend.fullname" -}}
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
{{- define "elchi-backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "elchi-backend.labels" -}}
helm.sh/chart: {{ include "elchi-backend.chart" . }}
{{ include "elchi-backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: elchi
{{- end }}

{{/*
Selector labels
*/}}
{{- define "elchi-backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "elchi-backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Registry labels
*/}}
{{- define "elchi-backend.registry.labels" -}}
helm.sh/chart: {{ include "elchi-backend.chart" . }}
{{ include "elchi-backend.registry.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: registry
app.kubernetes.io/part-of: elchi
{{- end }}

{{/*
Registry selector labels
*/}}
{{- define "elchi-backend.registry.selectorLabels" -}}
app.kubernetes.io/name: elchi-registry
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Controller labels
*/}}
{{- define "elchi-backend.controller.labels" -}}
helm.sh/chart: {{ include "elchi-backend.chart" . }}
{{ include "elchi-backend.controller.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: controller
app.kubernetes.io/part-of: elchi
{{- end }}

{{/*
Controller selector labels
*/}}
{{- define "elchi-backend.controller.selectorLabels" -}}
app.kubernetes.io/name: elchi-controller
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Control Plane labels
*/}}
{{- define "elchi-backend.controlplane.labels" -}}
helm.sh/chart: {{ include "elchi-backend.chart" . }}
{{ include "elchi-backend.controlplane.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: control-plane
app.kubernetes.io/part-of: elchi
{{- end }}

{{/*
Control Plane selector labels
*/}}
{{- define "elchi-backend.controlplane.selectorLabels" -}}
app.kubernetes.io/name: elchi-controlplane
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
