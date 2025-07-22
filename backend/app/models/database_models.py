"""
Database models for the AI Q&A application
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.database import Base


class QueryHistory(Base):
    """Model for storing Q&A history"""
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    llm_provider = Column(String(50), nullable=False)
    model_used = Column(String(100), nullable=False)
    response_time = Column(Float, nullable=True)  # in seconds
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_session = Column(String(255), nullable=True)  # For future user sessions
    
    def __repr__(self):
        return f"<QueryHistory(id={self.id}, question='{self.question[:50]}...')>"


class APIUsage(Base):
    """Model for tracking API usage statistics"""
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    def __repr__(self):
        return f"<APIUsage(id={self.id}, endpoint='{self.endpoint}', status={self.status_code})>"
