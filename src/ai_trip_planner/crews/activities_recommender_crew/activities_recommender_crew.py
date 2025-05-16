from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

from ...type import ActivitesOutline

search_tool = SerperDevTool()

@CrewBase
class ActivitiesRecommender():
    """Activities Recommender crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o-mini")
    

    @agent
    def city_selector(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selector'],
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )


    @agent
    def activities_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['activities_recommender'],
            tools=[search_tool],
            llm=self.llm,
            verbose=True
        )
    

    @task
    def find_cities(self) -> Task:
        return Task(
            config=self.tasks_config['find_cities'],
        )

    @task
    def find_places(self) -> Task:
        return Task(
            config=self.tasks_config['find_places']
        )

    @task
    def make_recommendations(self) -> Task:
        return Task(
            config=self.tasks_config['make_recommendations'], output_pydantic= ActivitesOutline
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