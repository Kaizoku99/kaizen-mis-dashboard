"""Company Scorecard API router."""
from fastapi import APIRouter, Query
from api.services.mock_data import get_scorecard_data

router = APIRouter(prefix="/api/scorecard", tags=["Company Scorecard"])


@router.get("")
async def get_scorecard(
    category: str | None = Query(None, description="Filter by category name"),
):
    """
    Return full Company Scorecard with all categories and metrics.
    
    Each metric shows:
    - Target vs Actual values
    - Achievement percentage
    - RYG status based on thresholds
    - Owner assignment
    """
    data = get_scorecard_data()
    
    if category:
        filtered_cats = [c for c in data.categories if c.name.lower() == category.lower()]
        return {
            "last_updated": data.last_updated,
            "categories": filtered_cats,
        }
    
    return data


@router.get("/summary")
async def get_scorecard_summary():
    """Return scorecard overview — overall score and per-category status."""
    data = get_scorecard_data()
    return {
        "overall_score": data.overall_score,
        "overall_status": data.overall_status,
        "summary": data.summary,
        "categories": [
            {"name": c.name, "score": c.category_score, "status": c.category_status}
            for c in data.categories
        ],
        "last_updated": data.last_updated,
    }
