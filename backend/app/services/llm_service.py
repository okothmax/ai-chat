"""
LLM Service for handling AI interactions with multiple providers
Demonstrates prompt engineering and clean architecture
"""

import time
import logging
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod

import openai
import anthropic
from app.config import settings
from app.models.pydantic_models import LLMProvider
from app.services.demo_llm import DemoLLMProvider

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate_response(self, question: str, context: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """Generate response from the LLM"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name being used"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider with advanced prompt engineering"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            raise ValueError("OpenAI API key not configured. Please add your API key to the .env file")
        
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def _create_system_prompt(self) -> str:
        """Create a well-engineered system prompt"""
        return """You are an expert AI assistant designed to provide helpful, accurate, and comprehensive answers.

Your capabilities include:
- Providing detailed explanations on complex topics
- Breaking down problems into manageable steps
- Offering practical solutions and recommendations
- Adapting your communication style to the user's needs

Guidelines for responses:
1. Be accurate and factual - if uncertain, acknowledge limitations
2. Provide structured, well-organized answers
3. Use examples when helpful
4. Be concise yet comprehensive
5. Maintain a professional but approachable tone
6. If the question is unclear, ask for clarification

Remember: Your goal is to be maximally helpful while maintaining accuracy and clarity."""
    
    def _create_user_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Create a well-structured user prompt"""
        prompt = f"Question: {question}"
        
        if context:
            prompt = f"Context: {context}\n\n{prompt}"
        
        prompt += "\n\nPlease provide a comprehensive and helpful answer."
        return prompt
    
    async def generate_response(self, question: str, context: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """Generate response using OpenAI GPT"""
        try:
            start_time = time.time()
            
            messages = [
                {"role": "system", "content": self._create_system_prompt()},
                {"role": "user", "content": self._create_user_prompt(question, context)}
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            answer = response.choices[0].message.content
            metadata = {
                "tokens_used": response.usage.total_tokens,
                "response_time": response_time,
                "model": self.model,
                "provider": "openai"
            }
            
            logger.info(f"OpenAI response generated in {response_time:.2f}s using {response.usage.total_tokens} tokens")
            
            return answer, metadata
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate response from OpenAI: {str(e)}")
    
    def get_model_name(self) -> str:
        return self.model


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider with optimized prompting"""
    
    def __init__(self):
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
            raise ValueError("Anthropic API key not configured. Please add your API key to the .env file")
        
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL
    
    def _create_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Create Claude-optimized prompt"""
        prompt = """I am an expert AI assistant focused on providing accurate, helpful, and well-structured responses.

I will:
- Provide comprehensive yet concise answers
- Use clear explanations and examples
- Structure information logically
- Acknowledge any limitations or uncertainties
- Ask for clarification if needed

"""
        
        if context:
            prompt += f"Context: {context}\n\n"
        
        prompt += f"Question: {question}\n\nResponse:"
        return prompt
    
    async def generate_response(self, question: str, context: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """Generate response using Anthropic Claude"""
        try:
            start_time = time.time()
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                messages=[
                    {"role": "user", "content": self._create_prompt(question, context)}
                ]
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            answer = response.content[0].text
            metadata = {
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "response_time": response_time,
                "model": self.model,
                "provider": "anthropic"
            }
            
            logger.info(f"Anthropic response generated in {response_time:.2f}s using {metadata['tokens_used']} tokens")
            
            return answer, metadata
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise Exception(f"Failed to generate response from Anthropic: {str(e)}")
    
    def get_model_name(self) -> str:
        return self.model


class LLMService:
    """Main service for managing LLM interactions"""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available LLM providers"""
        try:
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
                self.providers[LLMProvider.OPENAI] = OpenAIProvider()
                logger.info("OpenAI provider initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI provider: {e}")
        
        try:
            if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
                self.providers[LLMProvider.ANTHROPIC] = AnthropicProvider()
                logger.info("Anthropic provider initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Anthropic provider: {e}")
        
        # Add demo provider as fallback if no real providers are configured
        if not self.providers:
            self.providers["demo"] = DemoLLMProvider()
            logger.info("Demo provider initialized (no API keys configured)")
            logger.warning("Using demo mode. Configure API keys in .env for real AI responses.")
    
    def get_available_providers(self) -> list:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    async def generate_answer(
        self, 
        question: str, 
        provider: Optional[LLMProvider] = None,
        context: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Generate answer using specified or default provider"""
        
        # If no real providers available, use demo
        if not any(isinstance(p, str) and p != "demo" for p in self.providers.keys()) and "demo" in self.providers:
            llm_provider = self.providers["demo"]
            answer, metadata = await llm_provider.generate_response(question, context)
            return answer, metadata
        
        # Use specified provider or default
        if provider is None:
            # Get first available real provider
            available_providers = [p for p in self.providers.keys() if p != "demo"]
            if available_providers:
                provider = available_providers[0] if isinstance(available_providers[0], str) else available_providers[0]
            else:
                provider = "demo"
        
        if provider not in self.providers:
            available = ", ".join([str(p) for p in self.providers.keys()])
            raise ValueError(f"Provider {provider} not available. Available: {available}")
        
        llm_provider = self.providers[provider]
        
        try:
            answer, metadata = await llm_provider.generate_response(question, context)
            return answer, metadata
        except Exception as e:
            logger.error(f"Error generating answer with {provider}: {e}")
            raise


# Global service instance
llm_service = LLMService()
