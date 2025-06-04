from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from type import ActivitiesList
#from tool.trip_advisor_tool import TripAdvisorTool
from tool.location_search_tool import TripAdvisorLocationSearchTool
from tool.nearby_search_tool import TripAdvisorNearbySearchTool
#from tool.location_details_tool import TripAdvisorLocationDetailsTool
load_dotenv()

search_tool = SerperDevTool()
location_search_tool = TripAdvisorLocationSearchTool()
nearby_search_tool = TripAdvisorNearbySearchTool()
#location_details_tool = TripAdvisorLocationDetailsTool()

@CrewBase
class ActivitiesRecommender():
    """Activities Recommender crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    

    @agent
    def city_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['city_expert'],
            tools=[location_search_tool, nearby_search_tool, search_tool],
            llm=self.llm,
            verbose=True
        )


    @agent
    def activities_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['activities_recommender'],
            tools=[nearby_search_tool, search_tool],
            llm=self.llm,
            verbose=True
        )
    

    @task
    def find_places(self) -> Task:
        return Task(
            config=self.tasks_config['find_places'],
        )


    @task
    def make_recommendations(self) -> Task:
        return Task(
            config=self.tasks_config['make_recommendations'], output_pydantic= ActivitiesList
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the activities recommender Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )