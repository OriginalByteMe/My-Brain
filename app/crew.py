from modal import App, Function, Image, web_endpoint, Secret

from typing import Dict
import os

crew_image = Image.debian_slim(python_version="3.10").pip_install(
    "crewai", "crewai[tools]", "langchain-community", "gpt4all"
)

app = App("ollama-server", image=crew_image)


@app.function(
    concurrency_limit=1,
    allow_concurrent_inputs=10,
    secrets=[Secret.from_name("ollama-secret")],
)
@web_endpoint(method="POST")
def crew(inputs: Dict):
    from .crews.note_taking_crew import NoteTakingCrew
    from langchain_community.chat_models import ChatOllama

    ollama_url = Function.lookup("the_brain", "ollama_api").web_url
    llm = ChatOllama(model="llama3:8b", base_url=ollama_url)
    response = NoteTakingCrew(llm=llm, transcript=inputs["transcript"])

    return response.kickoff()


# def crew():
#   from crewai import Agent, Crew, Process, Task
#   from crewai_tools import SerperDevTool
#   llm = ChatOllama(
#     model = "llama3:8b",
#     base_url = "https://originalbyteme-dev--the-brain-ollama-api.modal.run")
#   # Creating a senior researcher agent with memory and verbose mode
#   researcher = Agent(
#     role='Senior Researcher',
#     goal='Uncover groundbreaking technologies in {topic}',
#     verbose=True,
#     # memory=True,
#     backstory=(
#       "Driven by curiosity, you're at the forefront of"
#       "innovation, eager to explore and share knowledge that could change"
#       "the world."
#     ),
#     allow_delegation=True,
#     llm=llm
#   )

#   # Creating a writer agent with custom tools and delegation capability
#   writer = Agent(
#     role='Writer',
#     goal='Narrate compelling tech stories about {topic}',
#     verbose=True,
#     # memory=True,
#     backstory=(
#       "With a flair for simplifying complex topics, you craft"
#       "engaging narratives that captivate and educate, bringing new"
#       "discoveries to light in an accessible manner."
#     ),
#     allow_delegation=False,
#     llm=llm
#   )

#   # Research task
#   research_task = Task(
#     description=(
#       "Identify the next big trend in {topic}."
#       "Focus on identifying pros and cons and the overall narrative."
#       "Your final report should clearly articulate the key points,"
#       "its market opportunities, and potential risks."
#     ),
#     expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
#     agent=researcher,
#   )

#   # Writing task with language model configuration
#   write_task = Task(
#     description=(
#       "Compose an insightful article on {topic}."
#       "Focus on the latest trends and how it's impacting the industry."
#       "This article should be easy to understand, engaging, and positive."
#     ),
#     expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
#     agent=writer,
#     async_execution=False,
#     output_file='new-blog-post.md'  # Example of output customization
#   )

#   crew = Crew(
#     agents=[researcher, writer],
#     tasks=[research_task, write_task],
#     process=Process.sequential,  # Optional: Sequential task execution is default
#     # memory=True,
#     cache=True,
#     max_rpm=100,
#     share_crew=True
#   )

#   # Starting the task execution process with enhanced feedback
#   result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
#   return result
