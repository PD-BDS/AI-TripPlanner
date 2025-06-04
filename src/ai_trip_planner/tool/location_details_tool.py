import os
import logging
from dotenv import load_dotenv
from typing import Any, Type
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

load_dotenv()
logger = logging.getLogger(__name__)

class LocationDetailsSchema(BaseModel):
    location_id: str = Field(..., description="TripAdvisor location_id to get details for")

class TripAdvisorLocationDetailsTool(BaseTool):
    name: str = "TripAdvisor Location Details"
    description: str = "Fetches detailed info for a location by ID."
    args_schema: Type[BaseModel] = LocationDetailsSchema

    def _run(self, **kwargs: Any) -> Any:
        loc_id = kwargs.get("location_id")

        api_key = os.getenv("TRIPADVISOR_API_KEY")
        if not api_key:
            return "Missing TRIPADVISOR_API_KEY."

        headers = {"accept": "application/json"}
        url = f"https://api.content.tripadvisor.com/api/v1/location/{loc_id}/details"

        try:
            response = requests.get(url, params={
                "key": api_key,
                "language": "en"
            }, headers=headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Details fetch failed for {loc_id}: {e}")
            return f"Details fetch error: {e}"
