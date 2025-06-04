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

class TripAdvisorSchema(BaseModel):
    location_query: str = Field(..., description="City or destination to search on TripAdvisor")
    category: str = Field(..., description="Type of location to search: 'attraction', 'hotels', or 'restaurants'")
    max_results: int = Field(50, description="Maximum number of results to retrieve (in batches of 10)")

class TripAdvisorTool(BaseTool):
    name: str = "TripAdvisor Location Explorer"
    description: str = "Searches a destination on TripAdvisor and returns details about attractions, hotels, or restaurants."
    args_schema: Type[BaseModel] = TripAdvisorSchema

    def _run(self, **kwargs: Any) -> Any:
        location_query = kwargs.get("location_query")
        category = kwargs.get("category", "attraction").lower()
        max_results = kwargs.get("max_results", 30)

        if category not in {"attraction", "hotels", "restaurants"}:
            return f"Invalid category: '{category}'. Must be 'attraction', 'hotels', or 'restaurants'."

        api_key = os.getenv("TRIPADVISOR_API_KEY")
        if not api_key:
            return "TripAdvisor API key not found. Please set TRIPADVISOR_API_KEY in environment variables."

        headers = {
            "accept": "application/json"
        }

        search_url = "https://api.content.tripadvisor.com/api/v1/location/search"
        nearby_url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"

        all_locations = []
        seen_ids = set()

        try:
            # Primary paginated location search
            for offset in range(0, max_results, 10):
                response = requests.get(
                    search_url,
                    params={
                        "key": api_key,
                        "searchQuery": location_query,
                        "language": "en",
                        "category": category,
                        "radius": 100,
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

                        # Nearby search for each base result
                        lat = loc.get("latitude")
                        lon = loc.get("longitude")
                        if lat and lon:
                            try:
                                nearby_resp = requests.get(
                                    nearby_url,
                                    params={
                                        "key": api_key,
                                        "latitude": lat,
                                        "longitude": lon,
                                        "language": "en",
                                        "category": category,
                                        "radius": 30,
                                        "radiusUnit": "km"
                                    },
                                    headers=headers,
                                    timeout=15
                                )
                                nearby_resp.raise_for_status()
                                nearby_data = nearby_resp.json().get("data", [])
                                for nearby_loc in nearby_data:
                                    nearby_id = nearby_loc.get("location_id")
                                    if nearby_id and nearby_id not in seen_ids:
                                        seen_ids.add(nearby_id)
                                        all_locations.append(nearby_loc)
                            except Exception as ne:
                                logger.warning(f"Skipping nearby search for {loc_id} due to error: {ne}")

                if len(data) < 10:
                    break
        except Exception as e:
            logger.error(f"Error fetching locations: {e}")
            return f"Failed to search {category}s: {e}"

        if not all_locations:
            return f"No {category}s found for '{location_query}'."

        location_ids = [loc["location_id"] for loc in all_locations[:max_results]]

        # Step 3: Fetch detailed info for each location ID
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
