"""
Demo LLM provider for testing without API keys
"""

import time
import asyncio
from typing import Dict, Any, Optional, Tuple


class DemoLLMProvider:
    """Demo LLM provider that works without API keys for testing"""
    
    def __init__(self):
        self.model = "demo-model-v1.0"
    
    async def generate_response(self, question: str, context: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """Generate a demo response"""
        start_time = time.time()
        
        # Simulate API call delay
        await asyncio.sleep(1.5)
        
        # Generate contextual demo response
        demo_responses = {
            "capital": f"The capital of Kenya is Nairobi. It's a vibrant city and the economic hub of East Africa.",
            "python": f"Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
            "ai": f"Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. It includes machine learning, natural language processing, and computer vision.",
            "fastapi": f"FastAPI is a modern, fast web framework for building APIs with Python. It's built on standard Python type hints and provides automatic API documentation.",
            "nextjs": f"Next.js is a React framework that enables functionality such as server-side rendering and generating static websites. It's great for building modern web applications.",
            "default": f"Thank you for your question: '{question}'. This is a demo response from the AI Q&A system. In production, this would be powered by advanced language models like GPT or Claude."
        }
        
        # Find appropriate response based on question content
        question_lower = question.lower()
        response_key = "default"
        
        for key in demo_responses:
            if key in question_lower:
                response_key = key
                break
        
        answer = demo_responses[response_key]
        
        # Add context if provided
        if context:
            answer = f"Based on the context you provided: '{context}'\n\n{answer}"
        
        # Add demo disclaimer
        answer += f"\n\n---\n*Note: This is a demo response. To get real AI-powered answers, please configure your OpenAI or Anthropic API keys in the backend/.env file.*"
        
        end_time = time.time()
        response_time = end_time - start_time
        
        metadata = {
            "tokens_used": len(answer.split()) * 2,  # Rough token estimate
            "response_time": response_time,
            "model": self.model,
            "provider": "demo"
        }
        
        return answer, metadata
    
    def get_model_name(self) -> str:
        return self.model
