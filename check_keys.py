import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

tavily_key = os.getenv("TAVILY_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print(f"Tavily Key Found: {tavily_key is not None}")
print(f"Groq Key Found: {groq_key is not None}")