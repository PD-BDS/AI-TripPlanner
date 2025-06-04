import datetime
import json
import logging
import os
from dotenv import load_dotenv
from typing import Any, Optional, Type, List
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

load_dotenv()
logger = logging.getLogger(__name__)

class NearbySearchSchema(BaseModel):
    latitude: float = Field(..., description="Latitude of the center point")
    longitude: float = Field(..., description="Longitude of the center point")
    category: str = Field(..., description="Type of location to search: 'attractions', 'hotels', or 'restaurants'")
    radius: int = Field(30, description="Search radius in kilometers (max 200)")

class TripAdvisorNearbySearchTool(BaseTool):
    name: str = "TripAdvisor Nearby Location Explorer"
    description: str = "Searches for nearby attractions, hotels, or restaurants from a specific coordinate on TripAdvisor and returns detailed information."
    args_schema: Type[BaseModel] = NearbySearchSchema

    def _run(self, **kwargs: Any) -> Any:
        latitude = kwargs.get("latitude")
        longitude = kwargs.get("longitude")
        category = kwargs.get("category", "attractions").lower()
        radius = kwargs.get("radius", 30)

        if category not in {"attractions", "hotels", "restaurants"}:
            return f"Invalid category: '{category}'. Must be 'attractions', 'hotels', or 'restaurants'."

        api_key = os.getenv("TRIPADVISOR_API_KEY")
        if not api_key:
            return "TripAdvisor API key not found. Please set TRIPADVISOR_API_KEY in environment variables."

        headers = {
            "accept": "application/json"
        }

        nearby_url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"
        all_locations = []
        seen_ids = set()

        try:
            response = requests.get(
                nearby_url,
                params={
                    "key": api_key,
                    "latLong": f"{latitude},{longitude}",
                    "category": category,
                    "radius": radius,
                    "radiusUnit": "km",
                    "language": "en",
                },
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            for loc in data:
                loc_id = loc.get("location_id")
                if loc_id and loc_id not in seen_ids:
                    seen_ids.add(loc_id)
                    all_locations.append(loc)
        except Exception as e:
            logger.error(f"Error fetching nearby {category}: {e}")
            return f"Failed to search nearby {category}: {e}"

        if not all_locations:
            return f"No nearby {category} found for coordinates ({latitude}, {longitude})."

        location_ids = [loc["location_id"] for loc in all_locations]

        details_list = []
        for loc_id in location_ids:
            try:
                details_url = f"https://api.content.tripadvisor.com/api/v1/location/{loc_id}/details"
                response = requests.get(
                    details_url,
                    params={"key": api_key, "language": "en"},
                    headers=headers,
                    timeout=15
                )
                response.raise_for_status()
                detail = response.json()
                details_list.append({
                    "name": detail.get("name"),
                    "address": detail.get("address_obj", {}).get("address_string"),
                    "latitude": detail.get("latitude"),
                    "longitude": detail.get("longitude"),
                    "ranking_data": detail.get("ranking_data"),
                    "rating": detail.get("rating"),
                    "review_rating_count": detail.get("review_rating_count"),
                    "num_reviews": detail.get("num_reviews"),
                    "trip_types": detail.get("trip_types")
                })
            except Exception as e:
                logger.warning(f"Skipping location ID {loc_id} due to error: {e}")
                continue

        return details_list
