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
│   ├── config.py                  # Centralized Settings (Env vars)
│   ├── exceptions.py              # Custom Exception Classes
│   ├── handlers.py                # Global Exception Handlers
│   └── logging.py                 # Logging Configuration
├── db/
│   ├── base_class.py              # SQLAlchemy Base
│   ├── mongo.py                   # MongoDB Singleton
│   └── session.py                 # SQL Session Management
├── models/
│   └── mutual_funds.py            # SQLAlchemy Database Models
├── prompts/                   # Externalized LLM Prompts
│   ├── fund_enrichment.txt
│   ├── fund_recommendation.txt
│   └── market_data_fetch.txt
├── schemas/
│   └── fund.py                    # Pydantic Schemas for Validation
├── services/
│   ├── advisor.py                 # Gemini Interaction Logic (with Retry)
│   ├── market_data.py             # Perplexity Interaction Logic (with Retry)
│   ├── portfolio.py               # Portfolio Aggregation Logic
│   └── recommendation.py          # Core Pipeline Orchestrator
├── utils/
│   ├── common.py                  # JSON extraction & misc utils
│   ├── helpers.py                 # Printing helpers
│   ├── prompt_loader.py           # Prompt loading utility
│   └── timer.py                   # Performance timing
├── scripts/
│   └── process_all_users.py       # Batch processing script
└── main.py                        # Application Entry Point
test_concurrency.py                # script to test concurrency
```

## 🚀 Key Improvements

1.  **Modular Service Layer**: Business logic is decoupled from API routes.
    *   `MarketDataService`: Handles Perplexity API calls with **automatic retries**.
    *   `AdvisorService`: Handles Gemini API calls with **automatic retries**.
    *   `RecommendationService`: Orchestrates the pipeline with **fault tolerance**. Logs execution timing for monitoring instead of storing in DB.

2.  **Centralized Configuration**:
    *   `app/core/config.py` manages all environment variables using `pydantic-settings`.
    *   New `LOG_LEVEL` setting controls verbosity dynamically.

3.  **Production-Grade Logging**:
    *   **Unified Format**: JSON-friendly logs with timestamps (`2024-12-17 10:00:00 - app.service - INFO - ...`).
    *   **Configurable**: Controlled via environment variables.
    *   **Startup/Shutdown Tracking**: Logs application lifecycle events.

4.  **Robust Error Handling**:
    *   **Custom Exceptions**: `AppError`, `ExternalServiceError`, `DatabaseError` in `app/core/exceptions.py`.
    *   **Global Handlers**: `app/core/handlers.py` catches all errors and returns standardized JSON responses.
    *   **Safety**: Unhandled exceptions are caught to prevent crashing and return a generic 500 error while logging the stack trace internally.

5.  **Resilience & Reliability**:
    *   **Graceful Degradation**: The recommendation pipeline continues even if fetching details for a single fund fails, ensuring user experience isn't broken by minor glitches.

6.  **Externalized Prompt Management**:
    *   **Separation of Concerns**: LLM prompts are stored as plain text files in `app/prompts/`, separating prompt engineering from code logic.
    *   **PromptLoader**: A utility to load and inject variables into prompts safely, facilitating version control and updates without code changes.

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

### 3. Run Concurrency Test
Stress test the API and Database with simultaneous requests:
```bash
python test_concurrency.py
```
*   Configurable `CONCURRENT_REQUESTS` and `TEST_USER_ID` inside the script.
