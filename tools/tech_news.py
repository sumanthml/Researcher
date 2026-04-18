import os
import requests
from newsapi import NewsApiClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class NewsIntelligence:
    def __init__(self):
        # Professional setup using NewsAPI
        self.client = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

    def get_real_world_context(self, query):
        """Scans global news for current events related to the search query."""
        try:
            # We search for the query and filter for the highest relevancy
            response = self.client.get_everything(
                q=query,
                language='en',
                sort_by='relevancy',
                page_size=5
            )
            
            articles = response.get('articles', [])
            if not articles:
                return "No breaking news found for this topic."

            formatted_news = []
            for art in articles:
                entry = f"Source: {art['source']['name']} | Title: {art['title']} | Snippet: {art['description']}"
                formatted_news.append(entry)
            
            return "\n".join(formatted_news)
        except Exception as e:
            return f"TechNews Error: {str(e)}"

def fetch_real_world_news(query):
    """Wrapper for the orchestrator to call the News agent."""
    agent = NewsIntelligence()
    return agent.get_real_world_context(query)