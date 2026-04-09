"""Streamlit → FastAPI client helper."""
import requests
import streamlit as st

API_BASE = st.session_get("api_base") or "http://localhost:8000"


def _get(endpoint: str, params: dict | None = None) -> dict:
    """Make a GET request to the FastAPI backend."""
    url = f"{API_BASE}{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        st.error(f"⚠️ Cannot connect to API at {url}. Is the backend running?")
        st.stop()
    except requests.HTTPError as e:
        st.error(f"⚠️ API error: {e}")
        return {}


def get_enterprise_health() -> dict:
    """Fetch full Enterprise Health data."""
    return _get("/api/enterprise-health")


def get_health_summary() -> dict:
    """Fetch lightweight health summary."""
    return _get("/api/enterprise-health/summary")


def get_scorecard(category: str | None = None) -> dict:
    """Fetch Company Scorecard data."""
    params = {"category": category} if category else None
    return _get("/api/scorecard", params=params)


def get_scorecard_summary() -> dict:
    """Fetch scorecard overview."""
    return _get("/api/scorecard/summary")


def get_metadata() -> dict:
    """Fetch API metadata and data source status."""
    return _get("/api/metadata")
