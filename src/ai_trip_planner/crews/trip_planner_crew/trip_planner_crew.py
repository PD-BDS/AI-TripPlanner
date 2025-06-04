from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from type import PlanOutline, TripPlan
#from tool.trip_advisor_tool import TripAdvisorTool
from dotenv import load_dotenv
from tool.location_search_tool import TripAdvisorLocationSearchTool
from tool.nearby_search_tool import TripAdvisorNearbySearchTool
#from tool.location_details_tool import TripAdvisorLocationDetailsTool

load_dotenv()

search_tool = SerperDevTool()
location_search_tool = TripAdvisorLocationSearchTool()
nearby_search_tool = TripAdvisorNearbySearchTool()
#location_details_tool = TripAdvisorLocationDetailsTool()

@CrewBase
class TripPlanner():
    """Trip Planner crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    

    @agent
    def travel_activities_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_activities_expert'],
            tools=[nearby_search_tool, search_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def travel_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_planner'],
            tools=[],
            llm=self.llm,
            verbose=True
        )


    @task
    def gathering_info_activities(self) -> Task:
        return Task(
            config=self.tasks_config['gathering_info_activities'],
        )

    @task
    def planning_trip(self) -> Task:
        return Task(
            config=self.tasks_config['planning_trip'], output_pydantic= TripPlan
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the trip planner Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )