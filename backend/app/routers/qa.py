"""
Q&A router for handling AI-powered question answering
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.database import get_db
from app.models.pydantic_models import (
    QuestionRequest, 
    QuestionResponse, 
    QueryHistoryResponse,
    LLMProvider
)
from app.models.database_models import QueryHistory
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    """
    Ask a question to the AI and get a comprehensive answer
    
    This endpoint demonstrates:
    - Input validation and sanitization
    - LLM integration with multiple providers
    - Response time tracking
    - Query history storage
    - Proper error handling
    """
    try:
        logger.info(f"Processing question: {request.question[:100]}...")
        
        # Generate AI response
        answer, metadata = await llm_service.generate_answer(
            question=request.question,
            provider=request.llm_provider,
            context=request.context
        )
        
        # Create response object
        response = QuestionResponse(
            question=request.question,
            answer=answer,
            llm_provider=metadata["provider"],
            model_used=metadata["model"],
            response_time=metadata["response_time"],
            tokens_used=metadata.get("tokens_used"),
            timestamp=datetime.now()
        )
        
        # Save to database
        try:
            query_record = QueryHistory(
                question=request.question,
                answer=answer,
                llm_provider=metadata["provider"],
                model_used=metadata["model"],
                response_time=metadata["response_time"],
                tokens_used=metadata.get("tokens_used")
            )
            db.add(query_record)
            db.commit()
            logger.info(f"Query saved to database with ID: {query_record.id}")
        except Exception as e:
            logger.error(f"Failed to save query to database: {e}")
            # Don't fail the request if database save fails
            db.rollback()
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process your question. Please try again."
        )


@router.get("/history", response_model=List[QueryHistoryResponse])
async def get_query_history(
    limit: int = Query(default=10, ge=1, le=100, description="Number of queries to return"),
    offset: int = Query(default=0, ge=0, description="Number of queries to skip"),
    db: Session = Depends(get_db)
):
    """
    Get query history with pagination
    
    Returns recent questions and answers with metadata
    """
    try:
        queries = db.query(QueryHistory)\
            .order_by(QueryHistory.created_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        return [QueryHistoryResponse.from_orm(query) for query in queries]
        
    except Exception as e:
        logger.error(f"Error fetching query history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch query history"
        )


@router.get("/history/{query_id}", response_model=QueryHistoryResponse)
async def get_query_by_id(
    query_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific query by ID
    """
    try:
        query = db.query(QueryHistory).filter(QueryHistory.id == query_id).first()
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Query not found"
            )
        
        return QueryHistoryResponse.from_orm(query)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching query {query_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch query"
        )


@router.delete("/history/{query_id}")
async def delete_query(
    query_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific query from history
    """
    try:
        query = db.query(QueryHistory).filter(QueryHistory.id == query_id).first()
        
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Query not found"
            )
        
        db.delete(query)
        db.commit()
        
        return {"message": "Query deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting query {query_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete query"
        )


@router.get("/providers")
async def get_available_providers():
    """
    Get list of available LLM providers and their models
    """
    try:
        providers = []
        for provider in llm_service.get_available_providers():
            llm_provider = llm_service.providers[provider]
            providers.append({
                "name": provider.value,
                "model": llm_provider.get_model_name(),
                "status": "available"
            })
        
        return {
            "providers": providers,
            "default": llm_service.providers[LLMProvider(llm_service.providers.__iter__().__next__())].get_model_name() if providers else None
        }
        
    except Exception as e:
        logger.error(f"Error fetching providers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch available providers"
        )


@router.get("/stats")
async def get_usage_stats(db: Session = Depends(get_db)):
    """
    Get usage statistics
    """
    try:
        total_queries = db.query(QueryHistory).count()
        
        # Get provider usage stats
        provider_stats = db.query(
            QueryHistory.llm_provider,
            db.func.count(QueryHistory.id).label('count')
        ).group_by(QueryHistory.llm_provider).all()
        
        # Get recent activity (last 24 hours)
        from datetime import timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_queries = db.query(QueryHistory)\
            .filter(QueryHistory.created_at >= yesterday)\
            .count()
        
        return {
            "total_queries": total_queries,
            "recent_queries_24h": recent_queries,
            "provider_usage": [
                {"provider": stat[0], "count": stat[1]} 
                for stat in provider_stats
            ]
        }
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch usage statistics"
        )
