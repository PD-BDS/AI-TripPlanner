from typing import List, Optional

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from src.ai_trip_planner.crews.activities_recommender_crew.activities_recommender_crew import ActivitiesRecommender
from src.ai_trip_planner.crews.trip_planner_crew.trip_planner_crew import TripPlanner
from type import UserProfile,TripDetails, ActivitesOutline, UserSelectionOutline, PlanOutline



class TripPlanState(BaseModel):
    userprofile: UserProfile
    tripdetails: TripDetails
    activities_outline: List[ActivitesOutline] = []
    user_selected_activities: List[UserSelectionOutline] = []
    plan_outline: Optional[PlanOutline] = None  # Make it optional



def generate_recommendations(userprofile: UserProfile, tripdetails: TripDetails):
    crew = ActivitiesRecommender().crew()
    output = crew.kickoff(inputs={
        "userprofile": userprofile.model_dump(mode="json"),
        "tripdetails": tripdetails.model_dump(mode="json"),
        "activities_outline": "### Title, Description, Location, Cost, Rating"
    })
    return ActivitesOutline()

def generate_plan(userprofile: UserProfile, tripdetails: TripDetails, user_selected_activities: UserSelectionOutline):
    crew = TripPlanner().crew()
    output = crew.kickoff(inputs={
        "userprofile": userprofile.model_dump(mode="json"),
        "tripdetails": tripdetails.model_dump(mode="json"),
        "user_selected_activities": user_selected_activities.model_dump(mode="json"),
        "plan_outline": """
        ### Plan Outline:
        - Day-wise schedule
        - Grouped activities
        - Tips and Notes
        - Packing and weather
        - Expenses
        """
    })
    return output["plan_outline"]

#async def kickoff(self):
#    await self.create_recommendations()
#    await self.create_plan()
#    return self.state.plan_outline

