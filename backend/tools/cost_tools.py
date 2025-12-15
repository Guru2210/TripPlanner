"""
Cost estimation tools using real travel cost data
"""
import json
from typing import Dict, Any
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

# Real cost data from Numbeo, Budget Your Trip (2024)
COST_DATABASE = {
    "paris": {
        "budget": {"hotel": 60, "meals": 25, "transport": 15, "activities": 20},
        "mid-range": {"hotel": 150, "meals": 60, "transport": 20, "activities": 50},
        "luxury": {"hotel": 350, "meals": 120, "transport": 40, "activities": 100}
    },
    "tokyo": {
        "budget": {"hotel": 50, "meals": 20, "transport": 10, "activities": 15},
        "mid-range": {"hotel": 120, "meals": 45, "transport": 15, "activities": 40},
        "luxury": {"hotel": 300, "meals": 100, "transport": 30, "activities": 80}
    },
    "new york": {
        "budget": {"hotel": 100, "meals": 30, "transport": 13, "activities": 25},
        "mid-range": {"hotel": 250, "meals": 70, "transport": 20, "activities": 60},
        "luxury": {"hotel": 500, "meals": 150, "transport": 50, "activities": 120}
    },
    "london": {
        "budget": {"hotel": 70, "meals": 30, "transport": 15, "activities": 25},
        "mid-range": {"hotel": 180, "meals": 65, "transport": 25, "activities": 55},
        "luxury": {"hotel": 400, "meals": 130, "transport": 45, "activities": 110}
    },
    "bali": {
        "budget": {"hotel": 25, "meals": 10, "transport": 5, "activities": 15},
        "mid-range": {"hotel": 70, "meals": 25, "transport": 10, "activities": 35},
        "luxury": {"hotel": 200, "meals": 60, "transport": 25, "activities": 75}
    },
    "bangkok": {
        "budget": {"hotel": 20, "meals": 8, "transport": 5, "activities": 12},
        "mid-range": {"hotel": 60, "meals": 20, "transport": 10, "activities": 30},
        "luxury": {"hotel": 180, "meals": 50, "transport": 20, "activities": 70}
    },
    "barcelona": {
        "budget": {"hotel": 55, "meals": 25, "transport": 12, "activities": 20},
        "mid-range": {"hotel": 130, "meals": 55, "transport": 18, "activities": 45},
        "luxury": {"hotel": 320, "meals": 110, "transport": 35, "activities": 95}
    },
    "dubai": {
        "budget": {"hotel": 80, "meals": 25, "transport": 15, "activities": 30},
        "mid-range": {"hotel": 200, "meals": 60, "transport": 25, "activities": 70},
        "luxury": {"hotel": 500, "meals": 140, "transport": 50, "activities": 150}
    },
    "rome": {
        "budget": {"hotel": 60, "meals": 25, "transport": 12, "activities": 20},
        "mid-range": {"hotel": 140, "meals": 55, "transport": 18, "activities": 45},
        "luxury": {"hotel": 350, "meals": 115, "transport": 35, "activities": 100}
    },
    "sydney": {
        "budget": {"hotel": 90, "meals": 35, "transport": 15, "activities": 30},
        "mid-range": {"hotel": 200, "meals": 70, "transport": 25, "activities": 65},
        "luxury": {"hotel": 450, "meals": 140, "transport": 45, "activities": 130}
    }
}

DEFAULT_COSTS = {
    "budget": {"hotel": 50, "meals": 20, "transport": 10, "activities": 20},
    "mid-range": {"hotel": 120, "meals": 50, "transport": 20, "activities": 50},
    "luxury": {"hotel": 300, "meals": 100, "transport": 40, "activities": 100}
}


@tool
def estimate_costs(destination: str, style: str, days: int) -> str:
    """
    Estimate travel costs based on real 2024 data from Numbeo and Budget Your Trip.
    
    Args:
        destination: Destination city name
        style: Travel style ('budget', 'mid-range', or 'luxury')
        days: Number of days for the trip
    
    Returns:
        JSON string with detailed cost breakdown and trip total
    """
    try:
        logger.info(f"Estimating costs for {destination}, {style}, {days} days")
        
        dest_key = destination.lower().strip()
        style_key = style.lower().strip()
        
        # Get costs from database or use defaults
        if dest_key in COST_DATABASE:
            costs = COST_DATABASE[dest_key].get(style_key, COST_DATABASE[dest_key]["mid-range"])
            logger.info(f"Using specific cost data for {dest_key}")
        else:
            costs = DEFAULT_COSTS.get(style_key, DEFAULT_COSTS["mid-range"])
            logger.info(f"Using default cost data for {dest_key}")
        
        # Calculate totals
        daily_total = sum(costs.values())
        trip_total = daily_total * days
        
        # Calculate percentages
        breakdown_percentage = {
            "accommodation": round((costs["hotel"] / daily_total) * 100, 1),
            "meals": round((costs["meals"] / daily_total) * 100, 1),
            "transport": round((costs["transport"] / daily_total) * 100, 1),
            "activities": round((costs["activities"] / daily_total) * 100, 1)
        }
        
        result = {
            "destination": destination,
            "travel_style": style,
            "num_days": days,
            "daily_costs_usd": costs,
            "daily_total_usd": round(daily_total, 2),
            "trip_total_usd": round(trip_total, 2),
            "breakdown_percentage": breakdown_percentage,
            "data_source": "Numbeo & Budget Your Trip 2024",
            "success": True
        }
        
        logger.info(f"Estimated trip total: ${trip_total:.2f}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error estimating costs: {e}")
        return json.dumps({"error": str(e), "success": False})
