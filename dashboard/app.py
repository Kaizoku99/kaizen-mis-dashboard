"""KAIZEN MIS Executive Dashboard — Streamlit Frontend Entry Point."""
import streamlit as st
from dashboard.pages.enterprise_health import render_enterprise_health
from dashboard.pages.scorecard import render_scorecard
from dashboard.utils.api_client import get_metadata

# ─── PAGE CONFIGURATION ─────────────────────────────
st.set_page_config(
    page_title="KAIZEN MIS Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main title styling */
    .main-title {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0;
    }
    
    .main-subtitle {
        font-size: 14px;
        color: #6B7280;
        margin-top: 4px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ─────────────────────────────────────────
col_logo, col_title, col_badge = st.columns([1, 5, 2])

with col_logo:
    st.markdown("## 🏢")

with col_title:
    st.markdown('<div class="main-title">KAIZEN MIS Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Executive Management Information System — Real-time Business Intelligence</div>', unsafe_allow_html=True)

with col_badge:
    # Quick status indicator from metadata
    try:
        meta = get_metadata()
        ds_count = len(meta.get("data_sources", []))
        connected = sum(1 for s in meta.get("data_sources", []) if s.get("status") == "connected")
        
        if ds_count > 0 and connected == ds_count:
            st.success(f"✅ All {ds_count} data sources connected")
        else:
            st.warning(f"⚠️ {connected}/{ds_count} data sources connected")
    except Exception:
        st.info("⏳ Connecting to API...")

# Divider
st.markdown("---")

# ─── TAB NAVIGATION ─────────────────────────────────
tab1, tab2 = st.tabs(["🟢 Enterprise Health", "📊 Company Scorecard"])

with tab1:
    render_enterprise_health()

with tab2:
    render_scorecard()

# ─── FOOTER ─────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#9CA3AF; font-size:11px; padding: 10px;">'
    'KAIZEN MIS Dashboard v0.1.0 — Built with FastAPI + Streamlit | '
    'Data refreshes automatically | End of April 2026 Target 🎯'
    '</div>',
    unsafe_allow_html=True,
)
