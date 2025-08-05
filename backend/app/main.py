from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.chatbot import CompanyChatbot
import uvicorn
from typing import Optional
import os
from pathlib import Path

# Set environment variables
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Initialize FastAPI with both API and frontend
app = FastAPI(title="Company Chatbot API")

# Serve static files (frontend) - NEW
frontend_dist = Path(__file__).parent.parent / "frontend_dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

# Root endpoint - Modified to serve frontend or API message
@app.get("/")
async def read_root():
    if frontend_dist.exists():
        return FileResponse(frontend_dist / "index.html")
    return {"message": "Chatbot API is running. Frontend not found."}

# Security and rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limiting for static files - NEW
    if request.url.path.startswith('/static/'):
        return await call_next(request)
        
    # Simple rate limiting - 5 requests per minute per IP
    ip = request.client.host
    if hasattr(request.state, 'request_count'):
        request.state.request_count += 1
        if request.state.request_count > 5:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )
    else:
        request.state.request_count = 1
    
    response = await call_next(request)
    return response

# CORS configuration - Updated for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
try:
    chatbot = CompanyChatbot()
except Exception as e:
    raise RuntimeError(f"Failed to initialize chatbot: {str(e)}")

# API Models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[list] = []

# API Endpoints
@app.post("/api/query", response_model=QueryResponse)  # Changed to /api/query
async def process_query(request: QueryRequest):
    try:
        response = chatbot.query(request.question)
        return QueryResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")  # Changed to /api/health
async def health_check():
    return {
        "status": "healthy",
        "frontend_served": frontend_dist.exists()
    }

# Catch-all route for frontend routing - NEW
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    if frontend_dist.exists():
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    return {"error": "Endpoint not found"}, 404

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)