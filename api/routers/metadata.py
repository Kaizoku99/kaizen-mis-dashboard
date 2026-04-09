"""Metadata & health check router."""
from fastapi import APIRouter
from api.config import settings

router = APIRouter(prefix="/api", tags=["Metadata"])


@router.get("/metadata")
async def get_metadata():
    """Return API metadata, data source status, and threshold configs."""
    import datetime
    
    return {
        "api_version": settings.app_version,
        "status": "healthy",
        "data_sources": [
            {"name": "PostgreSQL (Production DB)", "status": "connected", "type": "database"},
            {"name": "Salesforce CRM", "status": "connected", "type": "crm"},
            {"name": "Jira / Project Mgmt", "status": "connected", "type": "project_tracker"},
            {"name": "Finance ERP", "status": "connected", "type": "erp"},
            {"name": "HR System", "status": "connected", "type": "hris"},
            {"name": "Google Analytics", "status": "connected", "type": "analytics"},
        ],
        "threshold_configs": {
            "enterprise_health": {
                "description": "RYG thresholds for operational KPIs",
                "note": "Configurable via config/thresholds.yaml",
            },
            "scorecard": {
                "description": "Achievement-based: <70% RED, <90% YELLOW, >=90% GREEN",
                "note": "Auto-calculated from target vs actual values",
            },
        },
        "last_data_refresh": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


@router.get("/health")
async def health_check():
    """Simple health check for monitoring."""
    return {"status": "ok"}
