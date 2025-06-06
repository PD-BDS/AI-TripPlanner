from typing import List, Optional
import re
import json
from pydantic import BaseModel

from crews.activities_recommender_crew.activities_recommender_crew import ActivitiesRecommender
from crews.trip_planner_crew.trip_planner_crew import TripPlanner
from type import UserProfile,TripDetails, ActivitesOutline, ActivitiesList, UserSelectionOutline, PlanOutline,TripPlan



class TripPlanState(BaseModel):
    userprofile: UserProfile
    tripdetails: TripDetails
    activities_outline: List[ActivitesOutline] = []
    selected_activities: List[ActivitesOutline] = []
    plan_outline: List[PlanOutline] = []  



def generate_recommendations(userprofile: UserProfile, tripdetails: TripDetails) -> List[ActivitesOutline]:
    crew = ActivitiesRecommender().crew()
    output = crew.kickoff(inputs={
        "userprofile": userprofile.model_dump(mode="json"),
        "tripdetails": tripdetails.model_dump(mode="json"),
        "activities_outline": "title, short_description, location, approximate_expense, recommendation_rating, latitude, longitude, ranking_data, rating, review_rating_count, num_reviews"
    })

    return output["activities"]


def generate_plan(userprofile: UserProfile, tripdetails: TripDetails, selected_activities: List[dict]) -> List[PlanOutline]:
    crew = TripPlanner().crew()
    output = crew.kickoff(inputs={
        "userprofile": userprofile.model_dump(mode="json"),
        "tripdetails": tripdetails.model_dump(mode="json"),
        "selected_activities": selected_activities,
        "plan_outline": "day_wise_plan, weather_condition, packing_and_clothing_tips, expense_breakdown, hotel_suggestions, restaurents_suggestions, special_notes"
    })

    return output["plan"]