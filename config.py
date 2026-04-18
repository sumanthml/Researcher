import os
import logging
from dotenv import load_dotenv, find_dotenv

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Neural-Config")

# --- ENVIRONMENT LOADING ---
# find_dotenv() will return an empty string on the cloud, which is fine
env_path = find_dotenv()
if env_path:
    logger.info(f"Local environment detected. Loading from: {env_path}")
    load_dotenv(env_path)
else:
    logger.info("Cloud environment detected. Utilizing System Secrets/Env Variables.")

class Config:
    """
    NEURAL OS v2.5 Centralized Configuration.
    Handles seamless transitions between local development and cloud deployment.
    """
    
    # Reasoning Engine
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Search & Web Intelligence
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    
    # Long-Term Memory (Vector DB)
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
    
    # Specialized Data
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
    SEMANTIC_SCHOLAR_KEY = os.getenv("SEMANTIC_SCHOLAR_KEY")

    @classmethod
    def validate(cls):
        """
        Ensures the system has the minimum intelligence required to function.
        Will NOT crash the app, but will warn the user via logs.
        """
        essential_keys = {
            "GROQ_API_KEY": cls.GROQ_API_KEY,
            "TAVILY_API_KEY": cls.TAVILY_API_KEY
        }
        
        missing = [name for name, val in essential_keys.items() if not val]
        
        if missing:
            logger.warning(f"⚠️ MISSING CRITICAL INTELLIGENCE: {', '.join(missing)}")
            return False
        
        logger.info("✅ Core Neural Systems Optimized and Ready.")
        return True

# Initialize and validate config on module import
Config.validate()
