"""
AI Q&A Interview Project - FastAPI Backend
A professional-grade API for handling AI-powered Q&A interactions
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging
from typing import List, Optional

from app.config import settings
from app.database import engine, Base
from app.routers import qa, health
from app.models import database_models

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Q&A API...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Q&A API...")


# Initialize FastAPI app
app = FastAPI(
    title="AI Q&A Interview Project",
    description="""
    A professional AI-powered Q&A API built with FastAPI.
    
    This API demonstrates:
    - Clean architecture and code organization
    - Proper error handling and validation
    - LLM integration with multiple providers
    - Query history management
    - Comprehensive documentation
    
    Built by:Orain The Cloud Architect | DevOps Engineer | AI & Software Engineer
    """,
    version="1.0.0",
    contact={
        "name": "Maxwell Okoth",
        "url": "https://github.com/okothmax",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(qa.router, prefix="/api/v1", tags=["Q&A"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Q&A Interview Project API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "author": "Maxwell Okoth - Cloud Architect | DevOps Engineer | AI & Software Engineer"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
