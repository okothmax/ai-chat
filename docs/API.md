# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for this demo application.

## Endpoints

### Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00Z",
  "version": "1.0.0",
  "database_status": "healthy",
  "llm_providers": ["openai", "anthropic"]
}
```

### Ask Question
```http
POST /api/v1/ask
```

**Request Body:**
```json
{
  "question": "What is machine learning?",
  "context": "I am a beginner in AI",
  "llm_provider": "openai"
}
```

**Response:**
```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "llm_provider": "openai",
  "model_used": "gpt-3.5-turbo",
  "response_time": 1.23,
  "tokens_used": 150,
  "timestamp": "2024-01-20T10:30:00Z"
}
```

### Query History
```http
GET /api/v1/history?limit=10&offset=0
```

**Response:**
```json
[
  {
    "id": 1,
    "question": "What is machine learning?",
    "answer": "Machine learning is...",
    "llm_provider": "openai",
    "model_used": "gpt-3.5-turbo",
    "response_time": 1.23,
    "tokens_used": 150,
    "created_at": "2024-01-20T10:30:00Z"
  }
]
```

### Available Providers
```http
GET /api/v1/providers
```

**Response:**
```json
{
  "providers": [
    {
      "name": "openai",
      "model": "gpt-3.5-turbo",
      "status": "available"
    },
    {
      "name": "anthropic",
      "model": "claude-3-haiku-20240307",
      "status": "available"
    }
  ],
  "default": "gpt-3.5-turbo"
}
```

### Usage Statistics
```http
GET /api/v1/stats
```

**Response:**
```json
{
  "total_queries": 42,
  "recent_queries_24h": 5,
  "provider_usage": [
    {"provider": "openai", "count": 30},
    {"provider": "anthropic", "count": 12}
  ]
}
```

## Error Responses

All error responses follow this format:
```json
{
  "error": true,
  "message": "Error description",
  "status_code": 400,
  "timestamp": "2024-01-20T10:30:00Z"
}
```

## Rate Limiting
No rate limiting implemented in this demo version.
