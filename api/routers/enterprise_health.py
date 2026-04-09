"""Enterprise Health API router."""
from fastapi import APIRouter
from api.services.mock_data import get_enterprise_health_data

router = APIRouter(prefix="/api/enterprise-health", tags=["Enterprise Health"])


@router.get("")
async def get_enterprise_health():
    """
    Return all Enterprise Health KPIs with RYG status, trends, and chart data.
    
    This endpoint aggregates operational metrics across:
    - Infrastructure & Systems
    - User Activity & Engagement
    - Support & Operations
    - Revenue & Growth
    """
    return get_enterprise_health_data()


@router.get("/summary")
async def get_health_summary():
    """Return only the summary counts and overall status (lightweight)."""
    data = get_enterprise_health_data()
    return {
        "overall_status": data.overall_status,
        "summary": data.summary,
        "last_updated": data.last_updated,
        "total_kpis": len(data.kpis),
    }
