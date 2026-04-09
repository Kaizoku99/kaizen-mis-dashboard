"""Mock data generator for KAIZEN MIS Dashboard prototype.
Replace this with real data source connections when ready."""
import random
import datetime
from api.models.schemas import (
    KPI, ThresholdConfig, ChartDataPoint, ChartSeries,
    EnterpriseHealthResponse,
    ScorecardMetric, ScorecardCategory, ScorecardResponse
)
from api.services.ryg_calculator import calculate_status


def _random_trend() -> str:
    return random.choices(["up", "down", "stable"], weights=[40, 30, 30])[0]


def _generate_time_series(days: int = 30, base_value: float = 100,
                           variance: float = 15) -> list[ChartDataPoint]:
    """Generate realistic time series data with some noise."""
    data = []
    value = base_value
    for i in range(days):
        value += random.uniform(-variance, variance)
        value = max(base_value * 0.5, min(base_value * 1.5, value))
        date = (datetime.date.today() - datetime.timedelta(days=days - i)).isoformat()
        data.append(ChartDataPoint(label=date, value=round(value, 1)))
    return data


# ─── ENTERPRISE HEALTH MOCK DATA ────────────────────────────────────────

ENTERPRISE_HEALTH_KPI_CONFIGS = [
    {
        "name": "System Uptime",
        "unit": "%",
        "base_value": 99.5,
        "variance": 0.3,
        "threshold": ThresholdConfig(red=95.0, yellow=98.5, direction="lower_is_worse"),
        "description": "Overall platform and infrastructure availability",
    },
    {
        "name": "Active Users (Daily)",
        "unit": "",
        "base_value": 1250,
        "variance": 120,
        "threshold": ThresholdConfig(red=800, yellow=1000, direction="higher_is_worse"),
        "description": "Unique daily active users across all platforms",
    },
    {
        "name": "API Response Time",
        "unit": "ms",
        "base_value": 220,
        "variance": 50,
        "threshold": ThresholdConfig(red=500, yellow=350, direction="higher_is_worse"),
        "description": "Average API response time (p95)",
    },
    {
        "name": "Support Tickets Open",
        "unit": "",
        "base_value": 32,
        "variance": 12,
        "threshold": ThresholdConfig(red=45, yellow=28, direction="higher_is_worse"),
        "description": "Unresolved support tickets",
    },
    {
        "name": "Avg Resolution Time",
        "unit": "hrs",
        "base_value": 8.5,
        "variance": 3,
        "threshold": ThresholdConfig(red=16, yellow=10, direction="higher_is_worse"),
        "description": "Average time to resolve support tickets",
    },
    {
        "name": "Revenue MRR",
        "unit": "AED k",
        "base_value": 485,
        "variance": 25,
        "threshold": ThresholdConfig(red=350, yellow=420, direction="lower_is_worse"),
        "description": "Monthly Recurring Revenue (thousands AED)",
    },
    {
        "name": "Client NPS Score",
        "unit": "",
        "base_value": 72,
        "variance": 6,
        "threshold": ThresholdConfig(red=40, yellow=55, direction="lower_is_worse"),
        "description": "Net Promoter Score from client surveys",
    },
    {
        "name": "Project Delivery On-Time %",
        "unit": "%",
        "base_value": 88,
        "variance": 7,
        "threshold": ThresholdConfig(red=70, yellow=82, direction="lower_is_worse"),
        "description": "Percentage of projects delivered by deadline",
    },
    {
        "name": "Employee Utilization",
        "unit": "%",
        "base_value": 78,
        "variance": 6,
        "threshold": ThresholdConfig(red=60, yellow=70, direction="lower_is_worse"),
        "description": "Billable hours / total available hours",
    },
    {
        "name": "New Leads This Month",
        "unit": "",
        "base_value": 45,
        "variance": 14,
        "threshold": ThresholdConfig(red=20, yellow=30, direction="lower_is_worse"),
        "description": "Qualified sales leads generated this month",
    },
    {
        "name": "Conversion Rate",
        "unit": "%",
        "base_value": 24,
        "variance": 5,
        "threshold": ThresholdConfig(red=10, yellow=17, direction="lower_is_worse"),
        "description": "Lead-to-client conversion percentage",
    },
    {
        "name": "AI Model Accuracy (Avg)",
        "unit": "%",
        "base_value": 94.2,
        "variance": 2.5,
        "threshold": ThresholdConfig(red=85, yellow=90, direction="lower_is_worse"),
        "description": "Average accuracy of deployed AI models",
    },
]


def get_enterprise_health_data() -> EnterpriseHealthResponse:
    """Generate complete Enterprise Health response with mock data."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    kpis = []
    summary = {"green": 0, "yellow": 0, "red": 0}
    
    for config_dict in ENTERPRISE_HEALTH_KPI_CONFIGS:
        # Generate slightly randomized current value
        value = round(config_dict["base_value"] + random.uniform(
            -config_dict["variance"], config_dict["variance"]
        ), 1)
        
        status = calculate_status(value, config_dict["threshold"])
        trend = _random_trend()
        change_pct = round(random.uniform(-8, 12), 1) if trend != "stable" else 0
        
        kpi = KPI(
            name=config_dict["name"],
            value=value,
            unit=config_dict["unit"],
            status=status,
            threshold=config_dict["threshold"],
            trend=trend,
            change_percent=change_pct,
            description=config_dict["description"],
        )
        kpis.append(kpi)
        summary[status] += 1
    
    # Generate chart data
    charts = {
        "revenue_trend": [
            ChartSeries(name="MRR (AED k)", data=_generate_time_series(30, 485, 25))
        ],
        "user_growth": [
            ChartSeries(name="Daily Active Users", data=_generate_time_series(30, 1250, 120))
        ],
        "ticket_volume": [
            ChartSeries(name="Tickets Open", data=_generate_time_series(30, 32, 12)),
            ChartSeries(name="Tickets Resolved", data=_generate_time_series(30, 30, 10)),
        ],
        "api_latency": [
            ChartSeries(name="p95 Response Time (ms)", data=_generate_time_series(30, 220, 50))
        ],
    }
    
    from api.services.ryg_calculator import get_overall_status
    overall = get_overall_status(summary)
    
    return EnterpriseHealthResponse(
        last_updated=now,
        refresh_rate="hourly",
        overall_status=overall,
        summary=summary,
        kpis=kpis,
        charts=charts,
    )


# ─── COMPANY SCORECARD MOCK DATA ────────────────────────────────────────

SCORECARD_CATEGORIES = [
    {
        "name": "Financial Performance",
        "weight": 0.25,
        "metrics": [
            {"metric": "Monthly Revenue Target", "target": 500, "actual": 485, "higher_better": True},
            {"metric": "Gross Margin %", "target": 45, "actual": 42.3, "higher_better": True},
            {"metric": "Accounts Receivable Days", "target": 30, "actual": 38, "higher_better": False},
            {"metric": "Cost per Acquisition", "target": 2500, "actual": 2300, "higher_better": False},
        ],
        "owner": "Finance Team",
    },
    {
        "name": "Client Success",
        "weight": 0.20,
        "metrics": [
            {"metric": "NPS Score", "target": 70, "actual": 72, "higher_better": True},
            {"metric": "Client Retention Rate %", "target": 92, "actual": 89, "higher_better": True},
            {"metric": "CSAT Score", "target": 4.5, "actual": 4.3, "higher_better": True},
            {"metric": "Upsell Revenue (AED k)", "target": 80, "actual": 65, "higher_better": True},
        ],
        "owner": "Client Success Lead",
    },
    {
        "name": "Delivery & Operations",
        "weight": 0.20,
        "metrics": [
            {"metric": "Projects Delivered On-Time %", "target": 90, "actual": 88, "higher_better": True},
            {"metric": "Budget Variance %", "target": 5, "actual": 7.2, "higher_better": False},
            {"metric": "Resource Utilization %", "target": 80, "actual": 78, "higher_better": True},
            {"metric": "Defect Escape Rate %", "target": 2, "actual": 1.5, "higher_better": False},
        ],
        "owner": "Delivery Manager",
    },
    {
        "name": "Sales & Growth",
        "weight": 0.15,
        "metrics": [
            {"metric": "New Clients Acquired", "target": 8, "actual": 6, "higher_better": True},
            {"metric": "Pipeline Value (AED k)", "target": 2000, "actual": 1850, "higher_better": True},
            {"metric": "Lead Conversion %", "target": 25, "actual": 24, "higher_better": True},
            {"metric": "Sales Cycle Length (days)", "target": 45, "actual": 52, "higher_better": False},
        ],
        "owner": "Sales Director",
    },
    {
        "name": "People & Culture",
        "weight": 0.10,
        "metrics": [
            {"metric": "Employee Satisfaction eNPS", "target": 40, "actual": 35, "higher_better": True},
            {"metric": "Attrition Rate %", "target": 10, "actual": 8, "higher_better": False},
            {"metric": "Training Hours/Employee", "target": 20, "actual": 18, "higher_better": True},
            {"metric": "Open Positions Filled %", "target": 80, "actual": 75, "higher_better": True},
        ],
        "owner": "HR Lead",
    },
    {
        "name": "Innovation & AI",
        "weight": 0.10,
        "metrics": [
            {"metric": "AI Models Deployed", "target": 5, "actual": 4, "higher_better": True},
            {"metric": "Model Accuracy Avg %", "target": 95, "actual": 94.2, "higher_better": True},
            {"metric": "R&D Budget Utilization %", "target": 90, "actual": 85, "higher_better": True},
            {"metric": "Patents/IP Filed", "target": 2, "actual": 1, "higher_better": True},
        ],
        "owner": "CTO / Tech Lead",
    },
]


def get_scorecard_data() -> ScorecardResponse:
    """Generate complete Company Scorecard response with mock data."""
    from api.services.ryg_calculator import (
        calculate_achievement, get_status_from_achievement, get_overall_status
    )
    
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    categories = []
    total_weighted_score = 0
    summary = {"green": 0, "yellow": 0, "red": 0}
    
    for cat_config in SCORECARD_CATEGORIES:
        metrics = []
        category_total_achievement = 0
        
        for m in cat_config["metrics"]:
            achievement = calculate_achievement(m["actual"], m["target"])
            status = get_status_from_achievement(achievement, m.get("higher_better", True))
            
            metric = ScorecardMetric(
                category=cat_config["name"],
                metric=m["metric"],
                target=float(m["target"]),
                actual=float(m["actual"]),
                achievement_pct=achievement,
                status=status,
                owner=cat_config.get("owner", ""),
                due_date="2026-04-30",
            )
            metrics.append(metric)
            category_total_achievement += achievement
            summary[status] += 1
        
        category_avg = round(category_total_achievement / len(metrics), 1)
        category_status = get_status_from_achievement(category_avg, higher_is_better=True)
        
        category = ScorecardCategory(
            name=cat_config["name"],
            weight=cat_config["weight"],
            metrics=metrics,
            category_score=category_avg,
            category_status=category_status,
        )
        categories.append(category)
        total_weighted_score += category_avg * cat_config["weight"]
    
    overall_score = round(total_weighted_score, 1)
    overall_status = get_status_from_achievement(overall_score, higher_is_better=True)
    
    return ScorecardResponse(
        last_updated=now,
        refresh_rate="daily",
        overall_score=overall_score,
        overall_status=overall_status,
        categories=categories,
        summary=summary,
    )
