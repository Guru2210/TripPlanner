"""
Configuration management using environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY","")
    OPENTRIPMAP_API_KEY: str = os.getenv("OPENTRIPMAP_API_KEY", "")
    GEOAPIFY_API_KEY: str = os.getenv("GEOAPIFY_API_KEY", "")
    
    # LLM Settings
    LLM_MODEL: str = "gemini-2.5-flash"  # Stable model with good performance
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2048
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:8501", "http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Agent Settings
    MAX_AGENT_ITERATIONS: int = 5
    AGENT_TIMEOUT: int = 300  # seconds
    
    # Tool Settings
    SEARCH_RADIUS_KM: int = 10
    MAX_ATTRACTIONS: int = 15
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
