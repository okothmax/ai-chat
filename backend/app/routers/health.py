"""
Health check router for monitoring API status
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import get_db
from app.models.pydantic_models import HealthResponse
from app.services.llm_service import llm_service
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check endpoint
    
    Returns:
    - API status
    - Database connectivity
    - Available LLM providers
    - System timestamp
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    # Get available LLM providers
    available_providers = [provider.value for provider in llm_service.get_available_providers()]
    
    return HealthResponse(
        status="healthy" if db_status == "healthy" and available_providers else "degraded",
        timestamp=datetime.now(),
        version="1.0.0",
        database_status=db_status,
        llm_providers=available_providers
    )


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with additional system information
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
        db_error = None
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        db_error = str(e)
    
    # Get LLM provider details
    provider_details = {}
    for provider in llm_service.get_available_providers():
        try:
            llm_provider = llm_service.providers[provider]
            provider_details[provider.value] = {
                "status": "available",
                "model": llm_provider.get_model_name()
            }
        except Exception as e:
            provider_details[provider.value] = {
                "status": "error",
                "error": str(e)
            }
    
    return {
        "status": "healthy" if db_status == "healthy" and provider_details else "degraded",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "components": {
            "database": {
                "status": db_status,
                "error": db_error
            },
            "llm_providers": provider_details
        },
        "configuration": {
            "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
            "max_tokens": settings.MAX_TOKENS,
            "temperature": settings.TEMPERATURE
        }
    }
