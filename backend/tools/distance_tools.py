"""
Distance and duration calculation tools using GeoPy
"""
import json
from typing import Dict, Any
from langchain_core.tools import tool
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import logging

logger = logging.getLogger(__name__)
geolocator = Nominatim(user_agent="trip_planner_production")


@tool
def calculate_distance(origin: str, destination: str) -> str:
    """
    Calculate distance and estimated travel duration between two locations.
    
    Args:
        origin: Starting location name
        destination: Destination location name
    
    Returns:
        JSON string with distance in km/miles and duration estimates for different transport modes
    """
    try:
        logger.info(f"Calculating distance from {origin} to {destination}")
        
        # Geocode both locations
        origin_loc = geolocator.geocode(origin, timeout=10)
        dest_loc = geolocator.geocode(destination, timeout=10)
        
        if not origin_loc or not dest_loc:
            missing = []
            if not origin_loc:
                missing.append(origin)
            if not dest_loc:
                missing.append(destination)
            logger.warning(f"Could not find locations: {missing}")
            return json.dumps({
                "error": f"Could not find location(s): {', '.join(missing)}",
                "success": False
            })
        
        # Calculate geodesic distance
        origin_coords = (origin_loc.latitude, origin_loc.longitude)
        dest_coords = (dest_loc.latitude, dest_loc.longitude)
        
        distance_km = geodesic(origin_coords, dest_coords).kilometers
        distance_miles = distance_km * 0.621371
        
        # Estimate durations for different transport modes
        # Average speeds: Walking 5 km/h, Cycling 15 km/h, Driving 50 km/h, Public transport 30 km/h
        durations = {
            "walking_hours": round(distance_km / 5, 2),
            "cycling_hours": round(distance_km / 15, 2),
            "driving_hours": round(distance_km / 50, 2),
            "public_transport_hours": round(distance_km / 30, 2)
        }
        
        result = {
            "origin": origin,
            "destination": destination,
            "distance_km": round(distance_km, 2),
            "distance_miles": round(distance_miles, 2),
            "estimated_durations": durations,
            "success": True
        }
        
        logger.info(f"Distance: {distance_km:.2f} km")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error calculating distance: {e}")
        return json.dumps({"error": str(e), "success": False})
