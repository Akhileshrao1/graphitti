import os
from dotenv import load_dotenv

load_dotenv() #for loading variables from .env file.


MODEL_PROVIDER = "groq"
MODEL_NAME = "llama-3.3-70b-versatile"


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")