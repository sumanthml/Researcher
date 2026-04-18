import os
from dotenv import load_dotenv, find_dotenv

# Force find the .env file
env_path = find_dotenv()
if not env_path:
    raise FileNotFoundError("CRITICAL: .env file not found. Ensure it is in the root directory.")

load_dotenv(env_path)

class Config:
    """Centralized configuration and API key validation."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    
    @classmethod
    def validate(cls):
        """Checks if all essential keys are present."""
        missing = [k for k, v in cls.__dict__.items() if not k.startswith("__") and not v]
        if missing:
            print(f"⚠️ WARNING: Missing API keys for: {', '.join(missing)}")
        else:
            print("✅ All API keys loaded successfully.")

# Run validation on import
Config.validate()