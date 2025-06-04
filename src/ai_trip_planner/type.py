from typing import List, Optional

from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    age: int
    marital_status: str
    occupation: str
    email: str
    nationality: str
    interests: List[str]

class TripDetails(BaseModel):
    from_location: str 
    to_location: str 
    from_date: str
    to_date: str
    purpose: str
    companions: List[str]
    budget_type: str
    budget: int
    travelers: int
    travel_preferences: List[str]
    hotel_preferences: List[str]
    food_preferences: List[str]
    special_requirements: Optional[str] = None

class ActivitesOutline(BaseModel):
    title: str
    short_description: str
    location: str
    approximate_expense: str
    recommendation_rating: str
    latitude: float
    longitude: float
    ranking_data: List[str]
    rating: str
    review_rating_count: str
    num_reviews: str

    
class ActivitiesList(BaseModel):
    activities: List[ActivitesOutline]

class UserSelectionOutline(BaseModel):
    selected: List[ActivitesOutline]

class PlanOutline(BaseModel):
    day_wise_plan: str
    weather_condition: str
    packing_and_clothing_tips: str
    expense_breakdown: str
    hotel_suggestions: str
    restaurants_suggestions: str
    special_notes: str

class TripPlan(BaseModel):
    plan: List[PlanOutline]