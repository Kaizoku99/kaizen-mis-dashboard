"""Pydantic response schemas for KAIZEN MIS Dashboard."""
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RYGStatus(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class ThresholdConfig(BaseModel):
    """RYG threshold configuration for a metric."""
    red: float
    yellow: float
    direction: str  # "higher_is_worse" or "lower_is_worse"


class KPI(BaseModel):
    """A single KPI metric with status."""
    name: str
    value: float
    unit: str = ""
    status: str  # "green", "yellow", "red"
    threshold: ThresholdConfig
    trend: str  # "up", "down", "stable"
    change_percent: Optional[float] = None
    description: str = ""


class ChartDataPoint(BaseModel):
    """Single data point for charts."""
    label: str
    value: float


class ChartSeries(BaseModel):
    """A chart series (line/bar data)."""
    name: str
    data: list[ChartDataPoint]


class EnterpriseHealthResponse(BaseModel):
    """Full Enterprise Health tab response."""
    last_updated: str
    refresh_rate: str
    overall_status: str
    summary: dict[str, int]  # {"green": X, "yellow": Y, "red": Z}
    kpis: list[KPI]
    charts: dict[str, list[ChartSeries]]


class ScorecardMetric(BaseModel):
    """Company Scorecard metric row."""
    category: str
    metric: str
    target: float
    actual: float
    achievement_pct: float
    status: str
    owner: str = ""
    due_date: str = ""


class ScorecardCategory(BaseModel):
    """A scorecard category with its metrics."""
    name: str
    weight: float
    metrics: list[ScorecardMetric]
    category_score: float
    category_status: str


class ScorecardResponse(BaseModel):
    """Full Company Scorecard tab response."""
    last_updated: str
    refresh_rate: str
    overall_score: float
    overall_status: str
    categories: list[ScorecardCategory]
    summary: dict[str, int]


class MetadataResponse(BaseModel):
    """API metadata — thresholds info, health check, etc."""
    api_version: str
    status: str
    data_sources: list[dict]
    threshold_configs: dict
    last_data_refresh: str
