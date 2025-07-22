"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str = Field(
        ..., 
        min_length=1, 
        max_length=2000,
        description="The question to ask the AI"
    )
    llm_provider: Optional[LLMProvider] = Field(
        None,
        description="Preferred LLM provider (defaults to configured provider)"
    )
    context: Optional[str] = Field(
        None,
        max_length=5000,
        description="Additional context for the question"
    )
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty or just whitespace')
        return v.strip()


class QuestionResponse(BaseModel):
    """Response model for AI answers"""
    question: str
    answer: str
    llm_provider: str
    model_used: str
    response_time: float
    tokens_used: Optional[int] = None
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class QueryHistoryResponse(BaseModel):
    """Response model for query history"""
    id: int
    question: str
    answer: str
    llm_provider: str
    model_used: str
    response_time: Optional[float]
    tokens_used: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    database_status: str
    llm_providers: List[str]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: bool = True
    message: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
