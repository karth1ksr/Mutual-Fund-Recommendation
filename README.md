# Mutual Fund Recommendation Engine

A full-stack Mutual Fund Recommendation system that helps users analyze their existing investments and receive ranked mutual fund recommendations.

The project consists of:
- A **FastAPI backend** for data processing and recommendations
- A **lightweight static frontend** built with HTML, CSS, and Vanilla JavaScript


## Project Structure

- **backend/**: A Python-based API built with FastAPI. It handles data processing, communicates with the database (MongoDB), and serves recommendation logic.
- **frontend/**: A responsive web interface built with HTML, CSS, and Vanilla JavaScript.

## Prerequisites

- [Docker](https://www.docker.com/get-started) (Recommended for easy deployment)
- Python 3.12+ (If running backend locally without Docker)
- **MongoDB Atlas** account (or compatible MongoDB instance)

## Getting Started

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Configuration:**
   Ensure you have a `.env` file in the `backend/` directory with the required environment variables (e.g., MongoDB connection URI, API keys).

3. **Build the Docker Image:**
   ```bash
   docker build -t mf-backend .
   ```

4. **Run the Container:**
   ```bash
   docker run --env-file .env -p 8000:8000 mf-backend
   ```
   - The API will be accessible at: `http://localhost:8000`
   - Interactive API Docs (Swagger UI): `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Build the Docker Image:**
   ```bash
   docker build -t mf-frontend .
   ```

3. **Run the Container:**
   ```bash
   docker run -p 3000:80 mf-frontend
   ```
   - Access the application in your browser at: `http://localhost:3000`

## Development (Local without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
Simply open `frontend/index.html` in your browser or use a live server extension.

## Tech Stack

- **Backend:** FastAPI, Python, MongoDB, Pydantic
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **DevOps:** Docker
