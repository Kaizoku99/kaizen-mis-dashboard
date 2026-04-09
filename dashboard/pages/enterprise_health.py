"""Enterprise Health tab — operational KPIs with RYG indicators."""
import streamlit as st
from dashboard.utils.api_client import get_enterprise_health
from dashboard.components.kpi_cards import kpi_grid, overall_status_badge, summary_pills
from dashboard.components.charts import line_chart, donut_chart
from dashboard.components.tables import health_summary_table


def render_enterprise_health():
    """Render the full Enterprise Health tab."""
    st.header("🟢 Enterprise Health")
    st.markdown("Real-time operational health across all KAIZEN systems and business metrics.")
    
    # Fetch data with loading state
    with st.spinner("Loading enterprise health data..."):
        data = get_enterprise_health()
    
    if not data:
        return
    
    # Top bar: overall status + last updated + summary pills
    col_status, col_time = st.columns([3, 2])
    
    with col_status:
        overall_status_badge(data["overall_status"])
    
    with col_time:
        st.markdown(f"""
        <div style="text-align:center; padding: 20px; color: #6B7280;">
            <div style="font-size:12px;">Last Updated</div>
            <div style="font-size:14px; font-weight:600; color:#374151;">
                {data['last_updated'][:16].replace('T', ' ')}
            </div>
            <div style="font-size:11px; margin-top:4px;">
                Refresh rate: {data['refresh_rate']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary pills (RYG counts)
    summary_pills(data["summary"])
    
    st.markdown("---")
    
    # ─── KPI CARDS GRID ──────────────────────────────
    st.subheader("Key Performance Indicators")
    kpi_grid(data["kpis"], columns=3)
    
    st.markdown("---")
    
    # ─── CHARTS SECTION ──────────────────────────────
    st.subheader("📈 Trends & Analytics")
    
    charts = data.get("charts", {})
    
    # Row 1: Revenue trend + User growth
    c1, c2 = st.columns(2)
    
    with c1:
        if "revenue_trend" in charts:
            line_chart(charts["revenue_trend"], "💰 Monthly Recurring Revenue Trend", "AED k")
    
    with c2:
        if "user_growth" in charts:
            line_chart(charts["user_growth"], "👥 Daily Active Users", "Users")
    
    # Row 2: Ticket volume + API latency
    c3, c4 = st.columns(2)
    
    with c3:
        if "ticket_volume" in charts:
            line_chart(charts["ticket_volume"], "🎫 Support Ticket Volume", "Count")
    
    with c4:
        if "api_latency" in charts:
            line_chart(charts["api_latency"], "⚡ API Response Time (p95)", "ms")
    
    st.markdown("---")
    
    # ─── DETAILED TABLE VIEW ────────────────────────
    with st.expander("📋 View All KPI Details (Table View)", expanded=False):
        health_summary_table(data["kpis"])
    
    # ─── STATUS DISTRIBUTION DONUT ───────────────────
    c5, c6 = st.columns([1, 3])
    with c5:
        donut_chart(
            values=list(data["summary"].values()),
            labels=[f"{k.title()} ({v})" for k, v in data["summary"].items()],
            title="Status Distribution",
        )
