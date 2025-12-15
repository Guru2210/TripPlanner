"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TravelStyle(str, Enum):
    BUDGET = "budget"
    MID_RANGE = "mid-range"
    LUXURY = "luxury"


class AgentType(str, Enum):
    RESEARCHER = "researcher"
    BUDGET = "budget"
    PLANNER = "planner"


class TripRequest(BaseModel):
    """User trip planning request"""
    destination: str = Field(..., description="Destination city", min_length=2)
    num_days: int = Field(..., description="Number of days", ge=1, le=30)
    budget_usd: float = Field(..., description="Budget in USD", ge=100)
    travel_style: TravelStyle = Field(..., description="Travel style preference")
    interests: List[str] = Field(..., description="User interests", min_items=1)
    
    @validator('interests')
    def validate_interests(cls, v):
        if not v:
            raise ValueError("At least one interest is required")
        return [interest.lower().strip() for interest in v]
    
    class Config:
        schema_extra = {
            "example": {
                "destination": "Paris",
                "num_days": 4,
                "budget_usd": 2500,
                "travel_style": "mid-range",
                "interests": ["museums", "landmarks", "food"]
            }
        }


class AgentStatus(BaseModel):
    """Agent execution status"""
    agent: AgentType
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Optional[Dict[str, Any]] = None


class Activity(BaseModel):
    """Single activity in itinerary"""
    name: str
    time: str
    duration_hours: float
    cost_usd: float
    description: str
    reasoning: Optional[str] = None


class DayPlan(BaseModel):
    """Single day itinerary"""
    day: int
    date: Optional[str] = None
    activities: List[Activity]
    daily_cost: float
    summary: str


class Itinerary(BaseModel):
    """Complete trip itinerary"""
    destination: str
    num_days: int
    total_budget: float
    travel_style: str
    day_plans: List[DayPlan]
    total_cost: float
    budget_status: str
    recommendations: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)


class TripResponse(BaseModel):
    """API response for trip planning"""
    request_id: str
    status: str
    itinerary: Optional[Itinerary] = None
    agent_updates: List[AgentStatus] = []
    error: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "request_id": "trip_123456",
                "status": "completed",
                "itinerary": {
                    "destination": "Paris",
                    "num_days": 4,
                    "total_budget": 2500,
                    "travel_style": "mid-range",
                    "day_plans": [],
                    "total_cost": 2400,
                    "budget_status": "within_budget"
                }
            }
        }
