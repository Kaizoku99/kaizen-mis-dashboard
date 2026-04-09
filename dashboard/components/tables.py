"""Styled data table components for Streamlit dashboard."""
import streamlit as st
import pandas as pd

RYG_BG = {
    "green":  "#D1FAE5",
    "yellow": "#FEF3C7",
    "red":    "#FEE2E2",
}

RYG_TEXT = {
    "green":  "#065F46",
    "yellow": "#92400E",
    "red":    "#991B1B",
}


def _status_badge_html(status: str) -> str:
    """Generate HTML for a status badge."""
    bg = RYG_BG.get(status, "#F3F4F6")
    text = RYG_TEXT.get(status, "#374151")
    icons = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    icon = icons.get(status, "⚪")
    return f'<span style="background:{bg};color:{text};padding:3px 12px;border-radius:10px;font-size:12px;font-weight:600;">{icon} {status.upper()}</span>'


def scorecard_table(categories: list[dict]):
    """
    Render the full Company Scorecard as a styled table.
    
    Each category is a section with its metrics in rows.
    """
    for cat in categories:
        cat_status = cat.get("category_status", "green")
        cat_bg = RYG_BG.get(cat_status, "#F9FAFB")
        
        # Category header
        st.markdown(f"""
        <div style="
            background: {cat_bg};
            padding: 10px 16px;
            border-radius: 6px;
            margin-top: 8px;
            border-left: 4px solid {RYG_TEXT.get(cat_status, '#6B7280')};
        ">
            <strong>{cat['name']}</strong> 
            <span style="float:right; font-weight:700; color:{RYG_TEXT.get(cat_status,'#374151')};">
                Score: {cat['category_score']}% 
                {_status_badge_html(cat_status)}
            </span>
            <div style="font-size:12px;color:#6B7280;">
                Weight: {int(cat['weight']*100)}% | Owner: {cat.get('owner','TBD')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics table for this category
        rows = []
        for m in cat["metrics"]:
            achievement_color = (
                "#065F46" if m["achievement_pct"] >= 90
                else "#92400E" if m["achievement_pct"] >= 70
                else "#991B1B"
            )
            
            rows.append({
                "Metric": m["metric"],
                "Target": f"{m['target']:,.0f}",
                "Actual": f"{m['actual']:,.1f}",
                "Achievement": _status_badge_html(m["status"]) + f" **{m['achievement_pct']:.1f}%**",
                "Owner": m.get("owner", "-"),
                "Due": m.get("due_date", "-"),
            })
        
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)


def health_summary_table(kpis: list[dict]):
    """Render Enterprise Health KPIs as a compact table."""
    rows = []
    for kpi in kpis:
        rows.append({
            "KPI": kpi["name"],
            "Value": f"{kpi['value']:,} {kpi.get('unit','')}".strip(),
            "Status": _status_badge_html(kpi["status"]),
            "Trend": f"{kpi.get('trend','→')} ({kpi.get('change_percent',0):+.1f}%)" if kpi.get('change_percent') else kpi.get('trend', '→'),
            "Threshold": f"R:{kpi['threshold']['red']} Y:{kpi['threshold']['yellow']}",
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def data_source_table(sources: list[dict]):
    """Render data source connectivity status table."""
    rows = []
    for src in sources:
        status_icon = "🟢" if src["status"] == "connected" else "🔴"
        rows.append({
            "Source": src["name"],
            "Type": src["type"].title(),
            "Status": f"{status_icon} {src['status'].title()}",
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
