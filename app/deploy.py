from .ollama import ollama_app
from .stable_diffusion_xl import app as stable_diffusion_app
from modal import App

app = App("the_brain") 
app.include(ollama_app)
app.include(stable_diffusion_app)