"""KAIZEN MIS Dashboard — FastAPI Backend Entry Point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import settings
from api.routers.enterprise_health import router as health_router
from api.routers.scorecard import router as scorecard_router
from api.routers.metadata import router as metadata_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## KAIZEN MIS Executive Dashboard API
    
    Management Information System backend for the KAIZEN executive dashboard.
    Provides Enterprise Health KPIs and Company Scorecard data with **RYG (Red/Yellow/Green)** threshold indicators.
    
    ### Features
    - **Enterprise Health Tab**: Operational KPIs (uptime, users, revenue, support, etc.)
    - **Company Scorecard Tab**: Strategic metrics across 6 categories
    - **RYG Threshold System**: Automatic status calculation based on configurable thresholds
    - **Chart Data**: Time-series data for trend visualization
    
    ### Endpoints
    - `/api/enterprise-health` — Full enterprise health data
    - `/api/scorecard` — Full company scorecard data  
    - `/api/metadata` — Data source status & threshold configs
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(scorecard_router)
app.include_router(metadata_router)


@app.get("/")
async def root():
    """Root endpoint — API info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "endpoints": [
            "/api/enterprise-health",
            "/api/enterprise-health/summary",
            "/api/scorecard",
            "/api/scorecard/summary",
            "/api/metadata",
            "/api/health",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
