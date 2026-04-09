"""Company Scorecard tab — strategic metrics across categories."""
import streamlit as st
from dashboard.utils.api_client import get_scorecard, get_scorecard_summary
from dashboard.components.kpi_cards import overall_status_badge, summary_pills
from dashboard.components.charts import gauge_chart, bar_chart, donut_chart
from dashboard.components.tables import scorecard_table


def render_scorecard():
    """Render the full Company Scorecard tab."""
    st.header("📊 Company Scorecard")
    st.markdown("Strategic performance tracking across all business dimensions with target vs actual analysis.")
    
    # Fetch data with loading state
    with st.spinner("Loading scorecard data..."):
        data = get_scorecard()
    
    if not data:
        return
    
    # ─── OVERVIEW SECTION ──────────────────────────
    
    col_score, col_status, col_time = st.columns([2, 2, 2])
    
    with col_score:
        gauge_chart(
            value=data["overall_score"],
            title="Overall Score",
            max_val=100,
            threshold_yellow=85,
            threshold_red=70,
        )
    
    with col_status:
        overall_status_badge(data["overall_status"], "Scorecard Status")
    
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
            <div style="font-size:11px; margin-top:12px; padding-top:12px; border-top:1px solid #E5E7EB;">
                <strong>Total Categories:</strong> {len(data['categories'])}<br/>
                <strong>Total Metrics:</strong> {sum(len(c['metrics']) for c in data['categories'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary pills
    summary_pills(data["summary"])
    
    st.markdown("---")
    
    # ─── CATEGORY SCORES BAR CHART ──────────────────
    cat_names = [c["name"] for c in data["categories"]]
    cat_scores = [c["category_score"] for c in data["categories"]]
    cat_statuses = [c["category_status"] for c in data["categories"]]
    
    bar_chart(
        categories=cat_names,
        values=cat_scores,
        title="📊 Category Performance Scores",
        colors=cat_statuses,
        height=350,
    )
    
    st.markdown("---")
    
    # ─── DETAILED SCORECARD TABLES ─────────────────
    st.subheader("📋 Detailed Scorecard by Category")
    
    scorecard_table(data["categories"])
    
    st.markdown("---")
    
    # ─── BOTTOM SUMMARY ────────────────────────────
    c_left, c_right = st.columns([1, 3])
    
    with c_left:
        donut_chart(
            values=list(data["summary"].values()),
            labels=[f"{k.title()} ({v})" for k, v in data["summary"].items()],
            title="Metric Status",
        )
    
    with c_right:
        st.markdown("""
        ### 📌 How to Read This Scorecard
        
        | Status | Meaning |
        |--------|---------|
        | 🟢 **GREEN** | On track — achievement ≥90% of target |
        | 🟡 **YELLOW** | At risk — achievement 70-89% of target |
        | 🔴 **RED** | Off track — achievement <70% of target |
        
        Each category has a **weight** that contributes to the overall weighted score.
        Click on any category above to see individual metric details including targets, actuals, and owners.
        """)
