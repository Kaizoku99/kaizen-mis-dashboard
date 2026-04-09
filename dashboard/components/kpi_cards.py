"""RYG KPI Card components for Streamlit dashboard."""
import streamlit as st

# RYG color palette
RYG_COLORS = {
    "green":  ("#10B981", "#D1FAE5", "#065F46"),  # bg, light, text
    "yellow": ("#F59E0B", "#FEF3C7", "#92400E"),
    "red":    ("#EF4444", "#FEE2E2", "#991B1B"),
}

STATUS_ICONS = {
    "green": "🟢",
    "yellow": "🟡",
    "red":    "🔴",
}

TREND_ICONS = {
    "up":     "↑",
    "down":   "↓",
    "stable": "→",
}

TREND_COLORS = {
    "up":   "#10B981",
    "down": "#EF4444",
    "stable": "#6B7280",
}


def kpi_card(kpi: dict, key: str | None = None):
    """
    Render a single KPI card with RYG status indicator.
    
    Shows: metric name, value + unit, status badge, trend arrow,
           change %, and description.
    """
    status = kpi.get("status", "green")
    bg_color, light_bg, text_color = RYG_COLORS[status]
    
    # Format value
    value = kpi["value"]
    unit = kpi.get("unit", "")
    if unit == "%":
        display_value = f"{value:.1f}%"
    elif unit:
        display_value = f"{value:,.1f} {unit}"
    else:
        display_value = f"{value:,.0f}" if isinstance(value, float) else str(value)
    
    # Trend
    trend = kpi.get("trend", "stable")
    change_pct = kpi.get("change_percent")
    if change_pct is not None:
        trend_text = f"{TREND_ICONS[trend]} {abs(change_pct):+.1f}%"
        trend_color = TREND_COLORS[trend]
    else:
        trend_text = f"{TREND_ICONS[trend]}"
        trend_color = TREND_COLORS[trend]
    
    st.markdown(f"""
    <div style="
        background: white;
        border-left: 4px solid {bg_color};
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 8px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="font-size: 13px; color: #6B7280; font-weight: 500;">
                    {kpi['name']}
                </div>
                <div style="font-size: 28px; font-weight: 700; color: #111827; margin-top: 4px;">
                    {display_value}
                </div>
            </div>
            <div style="text-align: right;">
                <span style="
                    background: {light_bg};
                    color: {text_color};
                    padding: 2px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                ">
                    {STATUS_ICONS[status]} {status.upper()}
                </span>
                <div style="color: {trend_color}; font-weight: 600; font-size: 14px; margin-top: 6px;">
                    {trend_text}
                </div>
            </div>
        </div>
        {f'<div style="font-size: 11px; color: #9CA3AF; margin-top: 8px;">{kpi.get(\"description\", \"\")}</div>' if kpi.get('description') else ''}
    </div>
    """, unsafe_allow_html=True)


def kpi_grid(kpis: list[dict], columns: int = 3):
    """Render a grid of KPI cards."""
    for row_start in range(0, len(kpis), columns):
        cols = st.columns(columns)
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx < len(kpis):
                with col:
                    kpi_card(kpis[idx], key=f"kpi_{idx}")


def overall_status_badge(status: str, label: str = "Overall Status"):
    """Render a large overall status badge."""
    bg_color, light_bg, text_color = RYG_COLORS[status]
    icon = STATUS_ICONS[status]
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 20px;
        background: {light_bg};
        border-radius: 12px;
        border: 2px solid {bg_color};
        margin: 16px 0;
    ">
        <div style="font-size: 48px;">{icon}</div>
        <div style="font-size: 22px; font-weight: 700; color: {text_color};">
            {label}: {status.upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)


def summary_pills(summary: dict[str, int]):
    """Render RYG summary count pills."""
    cols = st.columns(3)
    labels = {"green": "🟢 Healthy", "yellow": "🟡 Warning", "red": "🔴 Critical"}
    
    for i, (col, (status, count)) in enumerate(zip(cols, summary.items())):
        _, light_bg, text_color = RYG_COLORS[status]
        with col:
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 12px;
                background: {light_bg};
                border-radius: 8px;
            ">
                <div style="font-size: 24px; font-weight: 700; color: {text_color};">
                    {count}
                </div>
                <div style="font-size: 12px; color: {text_color};">
                    {labels[status]}
                </div>
            </div>
            """, unsafe_allow_html=True)
