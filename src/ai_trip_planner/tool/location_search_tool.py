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

class LocationSearchSchema(BaseModel):
    location_query: str = Field(..., description="City or destination to search on TripAdvisor")
    category: str = Field(..., description="Type of location to search: 'attraction'")
    max_results: int = Field(50, description="Maximum number of results to retrieve (in batches of 10)")

class TripAdvisorLocationSearchTool(BaseTool):
    name: str = "TripAdvisor Location Explorer"
    description: str = "Searches a destination on TripAdvisor and returns details about attractions."
    args_schema: Type[BaseModel] = LocationSearchSchema

    def _run(self, **kwargs: Any) -> Any:
        location_query = kwargs.get("location_query")
        category = kwargs.get("category", "attraction").lower()
        max_results = kwargs.get("max_results", 50)

        if category not in {"attraction", "hotels", "restaurants"}:
            return f"Invalid category: '{category}'. Must be 'attraction', 'hotels', or 'restaurants'."

        api_key = os.getenv("TRIPADVISOR_API_KEY")
        if not api_key:
            return "TripAdvisor API key not found. Please set TRIPADVISOR_API_KEY in environment variables."

        headers = {
            "accept": "application/json"
        }

        search_url = "https://api.content.tripadvisor.com/api/v1/location/search"
        all_locations = []
        seen_ids = set()

        try:
            for offset in range(0, max_results, 10):
                response = requests.get(
                    search_url,
                    params={
                        "key": api_key,
                        "searchQuery": location_query,
                        "language": "en",
                        "category": category,
                        "radius": 200,
                        "radiusUnit": "km",
                        "offset": offset
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
                if len(data) < 10:
                    break
        except Exception as e:
            logger.error(f"Error fetching {category} locations: {e}")
            return f"Failed to search {category}s: {e}"

        if not all_locations:
            return f"No {category}s found for '{location_query}'."

        location_ids = [loc["location_id"] for loc in all_locations[:max_results]]

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
