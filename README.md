# 🏢 KAIZEN MIS Executive Dashboard

> Management Information System dashboard for KAIZEN leadership — real-time business intelligence with **RYG (Red/Yellow/Green)** threshold indicators.

## 📋 Overview

Executive-level dashboard that aggregates data from multiple sources into a unified view with two priority tabs:

1. **🟢 Enterprise Health** — Operational KPIs (uptime, users, revenue, support, AI models)
2. **📊 Company Scorecard** — Strategic metrics across 6 categories (Financial, Client Success, Delivery, Sales, People, Innovation)

Each metric is automatically color-coded:
- 🟢 **GREEN** = On track / Healthy
- 🟡 **YELLOW** = Warning / At risk
- 🔴 **RED** = Critical / Off track

## 🏗️ Architecture

```
Data Sources (SQL, APIs, CRM, ERP, HRIS)
         ↓
   FastAPI Backend (Port 8000)
   ├── Data fetching & transformation
   ├── RYG threshold calculation
   └── RESTful JSON endpoints
         ↓
   Streamlit Frontend (Port 8501)
   ├── Enterprise Health tab
   ├── Company Scorecard tab
   └── Interactive charts & tables
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or uv

### Setup

```bash
# Clone the repo
git clone https://github.com/Kaizoku99/kaizen-mis-dashboard.git
cd kaizen-mis-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env  # (or create .env from template)
```

### Run

**Terminal 1 — FastAPI Backend:**
```bash
cd api
uvicorn main:app --reload --port 8000
```
→ API docs available at http://localhost:8000/docs

**Terminal 2 — Streamlit Dashboard:**
```bash
cd dashboard
streamlit run app.py --server.port 8501
```
→ Dashboard opens at http://localhost:8501

## 📁 Project Structure

```
kaizen-mis-dashboard/
├── api/                        # FastAPI backend
│   ├── main.py                 # App entry point, CORS, router registration
│   ├── config.py               # Settings & environment config
│   ├── routers/
│   │   ├── enterprise_health.py    # /api/enterprise-health endpoints
│   │   ├── scorecard.py            # /api/scorecard endpoints
│   │   └── metadata.py             # /api/metadata + health check
│   ├── services/
│   │   ├── ryg_calculator.py       # RYG threshold logic engine
│   │   └── mock_data.py            # Mock data generator (replace with real DB)
│   └── models/
│       └── schemas.py              # Pydantic response models
│
├── dashboard/                  # Streamlit frontend
│   ├── app.py                  # Main entry, tab navigation, header
│   ├── pages/
│   │   ├── enterprise_health.py    # Enterprise Health tab renderer
│   │   └── scorecard.py            # Scorecard tab renderer
│   ├── components/
│   │   ├── kpi_cards.py            # RYG KPI card components
│   │   ├── charts.py               # Plotly chart components
│   │   └── tables.py               # Styled data tables
│   └── utils/
│       └── api_client.py           # FastAPI client helper
│
├── config/                     # Config files (thresholds, etc.)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info & endpoint list |
| `GET /api/enterprise-health` | Full Enterprise Health data (KPIs + charts) |
| `GET /api/enterprise-health/summary` | Lightweight health summary |
| `GET /api/scorecard` | Full Company Scorecard (all categories) |
| `GET /api/scorecard?category=Financial` | Filter scorecard by category |
| `GET /api/scorecard/summary` | Scorecard overview (scores per category) |
| `GET /api/metadata` | Data source status, threshold configs |
| `GET /api/health` | Health check |
| `GET /docs` | Swagger UI (interactive API docs) |

## 🎯 RYG Threshold System

Thresholds are defined per-metric with direction:

```yaml
system_uptime:
  red: 95        # Below 95% = RED
  yellow: 98.5   # Below 98.5% = YELLOW  
  direction: "lower_is_worse"  # Higher uptime is better

support_tickets_open:
  red: 45        # Above 45 = RED
  yellow: 28     # Above 28 = YELLOW
  direction:higher_is_worse"   # Fewer tickets is better
```

For the **Scorecard**, status is auto-calculated from achievement %:
- ≥90% → GREEN
- 70-89% → YELLOW
- <70% → RED

## 🛣️ Roadmap to End of April

- [x] Project scaffold & architecture
- [x] FastAPI backend with mock data
- [x] Streamlit dashboard prototype
- [ ] Connect real data sources (PostgreSQL, CRM, ERP, Jira, HRIS)
- [ ] Replace mock_data.py with actual database queries
- [ ] Configure real RYG thresholds with Elsy/stakeholders
- [ ] Add authentication (if needed for internal deployment)
- [ ] Mobile responsiveness testing
- [ ] Deploy to internal server / cloud
- [ ] User acceptance testing with Elsy

## 🤝 Collaboration

Built by Abdelrahman Saifeldin (AI Solutions Delivery Specialist) in collaboration with a Data Analyst colleague.

**Target Deadline:** End of April 2026 🎯

---

*Powered by FastAPI + Streamlit + Plotly*
