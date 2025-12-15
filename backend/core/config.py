"""
Configuration management using environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY","AIzaSyB5X7TDJmMTq_T25dnsUGb6s-xao2ufmkY")
    OPENTRIPMAP_API_KEY: str = os.getenv("OPENTRIPMAP_API_KEY", "5ae2e3f221c38a28845f05b667cb80d35f5760ae35c837141e30b083")
    GEOAPIFY_API_KEY: str = os.getenv("GEOAPIFY_API_KEY", "1cc5dc2ea831492d9f9f952fb38ef927")
    
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
