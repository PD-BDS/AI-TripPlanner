from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from type import PlanOutline, TripPlan

search_tool = SerperDevTool()

@CrewBase
class TripPlanner():
    """Trip Planner crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o-mini")
    

    @agent
    def travel_activities_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_activities_expert'],
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def travel_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_planner'],
            tools=[search_tool],
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