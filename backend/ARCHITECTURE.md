# Production-Grade Architecture Refactoring

The codebase has been completely refactored into a scalable, maintainable, and production-ready architecture using FastAPI and best practices.

## 📂 New Directory Structure (`app/`)

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   └── recommendation.py  # API Routes
│   │   └── router.py              # Router configuration
│   └── deps.py                    # Dependency Injection (DB session)
├── core/
│   └── config.py                  # Centralized Settings (Env vars)
├── db/
│   ├── base_class.py              # SQLAlchemy Base
│   ├── mongo.py                   # MongoDB Singleton
│   └── session.py                 # SQL Session Management
├── models/
│   └── mutual_funds.py            # SQLAlchemy Database Models
├── schemas/
│   └── fund.py                    # Pydantic Schemas for Validation
├── services/
│   ├── advisor.py                 # Gemini Interaction Logic
│   ├── market_data.py             # Perplexity Interaction Logic
│   ├── portfolio.py               # Portfolio Aggregation Logic
│   └── recommendation.py          # Core Pipeline Orchestrator
├── utils/
│   ├── common.py                  # JSON extraction & misc utils
│   ├── helpers.py                 # Printing helpers
│   └── timer.py                   # Performance timing
├── scripts/
│   └── process_all_users.py       # Batch processing script
└── main.py                        # Application Entry Point
```

## 🚀 Key Improvements

1.  **Modular Service Layer**: Business logic is decoupled from API routes.
    *   `MarketDataService`: Handles all Perplexity API calls.
    *   `AdvisorService`: Handles all Gemini API calls.
    *   `PortfolioService`: Manages complex SQL queries for portfolio aggregation.
    *   `RecommendationService`: Orchestrates the full recommendation pipeline.

2.  **Centralized Configuration**:
    *   `app/core/config.py` manages all environment variables using `pydantic-settings`.
    *   Database URIs and API keys are strictly typed and validated.

3.  **Dependency Injection**:
    *   Database sessions are injected into API endpoints using `Depends(deps.get_db)`, ensuring proper connection closing/pooling.

4.  **Robust Error Handling & Logging**:
    *   Services use Python's built-in `logging` instead of `print` statements.
    *   API endpoints return proper HTTP 404/500 errors.
    *   JSON parsing from LLMs is robust with fallback mechanisms.

5.  **Validation**:
    *   Pydantic models in `app/schemas` ensure data integrity for inputs and outputs.

## 🛠️ How to Run

### 1. Run the API Server
Start the FastAPI server for real-time recommendations:
```bash
uvicorn app.main:app --reload
```
*   **Swagger UI**: Visit `http://127.0.0.1:8000/docs` to test endpoints interactively.

### 2. Run Batch Job
Process recommendations for **ALL** users in the database:
```bash
python -m app.scripts.process_all_users
```
*(Make sure to run this from the project root)*
