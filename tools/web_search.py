import os
from tavily import TavilyClient
from duckduckgo_search import DDGS
from config import Config

def research_tool_manager(query):
    """
    Strategically manages search requests to optimize API usage.
    Uses DuckDuckGo for general checks and Tavily for deep research.
    """
    print(f"🔍 Researching: {query}")
    
    # 1. Try DuckDuckGo (Unlimited/Free) first
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            if results:
                return "\n".join(results)
    except Exception as e:
        print(f"DuckDuckGo error: {e}")

    # 2. Use Tavily if DDG fails or for complex queries
    if not Config.TAVILY_API_KEY:
        return "Error: Tavily API Key is missing. Check your .env file."
        
    client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    try:
        search_result = client.search(query=query, search_depth="advanced")
        return "\n".join([r['content'] for r in search_result['results']])
    except Exception as e:
        return f"Research failed: {str(e)}"