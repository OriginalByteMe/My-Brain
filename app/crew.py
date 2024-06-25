from modal import App, Function, Image, web_endpoint, Secret, asgi_app
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from typing import Dict
import os

crew_image = Image.debian_slim(python_version="3.10").pip_install(
    "crewai", "crewai[tools]", "langchain-community", "gpt4all"
)
web_app = FastAPI()
app = App("ollama-server", image=crew_image)


@app.function(
    concurrency_limit=1,
    allow_concurrent_inputs=10,
    secrets=[Secret.from_name("ollama-secret")],
)
@web_app.post("/prd_note")
async def prd_note_making(request: Request):
    from .crews.note_taking_crew import NoteTakingCrew
    from langchain_community.chat_models import ChatOllama

    body = await request.json()
    transcript = body["transcript"]
    ollama_url = Function.lookup("the_brain", "ollama_api").web_url
    llm = ChatOllama(model="llama3:8b", base_url=ollama_url)
    response = NoteTakingCrew(llm=llm, transcript=transcript)

    return response.prd_note()

@web_app.post("/normal_note", response_class=HTMLResponse)
async def normal_note_making(request: Request):
    from .crews.note_taking_crew import NoteTakingCrew
    from langchain_community.chat_models import ChatOllama

    body = await request.json()
    transcript = body["transcript"]
    ollama_url = Function.lookup("the_brain", "ollama_api").web_url
    llm = ChatOllama(model="llama3:8b", base_url=ollama_url)
    response = NoteTakingCrew(llm=llm, transcript=transcript)

    return response.normal_note()


