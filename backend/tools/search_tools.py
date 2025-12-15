"""
Search tools for finding tourist attractions using OpenTripMap API
"""
import json
import requests
from typing import Dict, Any
from langchain_core.tools import tool
from geopy.geocoders import Nominatim
from core.config import settings
import logging

logger = logging.getLogger(__name__)
geolocator = Nominatim(user_agent="trip_planner_production")


@tool
def search_attractions(city: str, limit: int = 15) -> str:
    """
    Search for real tourist attractions using OpenTripMap API.
    
    Args:
        city: Name of the city to search
        limit: Maximum number of attractions to return (default: 15)
    
    Returns:
        JSON string with attractions data including names, ratings, and descriptions
    """
    try:
        logger.info(f"Searching attractions for {city}")
        
        # Get city coordinates
        location = geolocator.geocode(city, timeout=10)
        if not location:
            logger.warning(f"City not found: {city}")
            return json.dumps({"error": f"City '{city}' not found", "success": False})
        
        logger.info(f"Found coordinates for {city}: {location.latitude}, {location.longitude}")
        
        # Search for attractions using OpenTripMap
        url = "https://api.opentripmap.com/0.1/en/places/radius"
        params = {
            "radius": settings.SEARCH_RADIUS_KM * 1000,  # Convert to meters
            "lon": location.longitude,
            "lat": location.latitude,
            "kinds": "museums,theatres,architecture,historic,monuments,cultural,interesting_places",
            "limit": limit,
            "apikey": settings.OPENTRIPMAP_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"OpenTripMap API error: {response.status_code}")
            return json.dumps({"error": f"API error: {response.status_code}", "success": False})
        
        data = response.json()
        logger.info(f"Found {len(data)} attractions")
        
        # Get detailed info for top attractions
        attractions = []
        for place in data[:limit]:
            xid = place.get("xid")
            if xid:
                try:
                    detail_url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
                    detail_params = {"apikey": settings.OPENTRIPMAP_API_KEY}
                    detail_response = requests.get(detail_url, params=detail_params, timeout=10)
                    
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        
                        name = detail_data.get("name", "Unknown")
                        if name != "Unknown":
                            attraction = {
                                "name": name,
                                "rating": detail_data.get("rate", 0),
                                "description": detail_data.get("wikipedia_extracts", {}).get("text", "No description available")[:200],
                                "kinds": detail_data.get("kinds", "").split(",")[:3],
                                "coordinates": {
                                    "lat": detail_data.get("point", {}).get("lat"),
                                    "lon": detail_data.get("point", {}).get("lon")
                                }
                            }
                            attractions.append(attraction)
                except Exception as e:
                    logger.warning(f"Error fetching details for {xid}: {e}")
                    continue
        
        result = {
            "city": city,
            "total_found": len(attractions),
            "attractions": attractions,
            "success": True
        }
        
        logger.info(f"Successfully retrieved {len(attractions)} detailed attractions")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error searching attractions: {e}")
        return json.dumps({"error": str(e), "success": False})
