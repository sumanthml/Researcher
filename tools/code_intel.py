import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CodeIntelAgent:
    def __init__(self):
        # GitHub token is optional but recommended for higher rate limits
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    def scan_github_trends(self, query):
        """Finds trending codebases and framework updates on GitHub."""
        search_url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
        
        try:
            response = requests.get(search_url, headers=self.headers)
            if response.status_code == 200:
                repos = response.json().get('items', [])[:3]
                if not repos: return "No major open-source projects found."
                
                results = []
                for r in repos:
                    results.append(f"Repo: {r['full_name']} | Stars: {r['stargazers_count']} | Updates: {r['updated_at']}")
                return "\n".join(results)
            return "GitHub Intel currently limited."
        except Exception as e:
            return f"CodeIntel Error: {str(e)}"

def get_dev_trends(query):
    """Wrapper for the orchestrator to call the Code agent."""
    agent = CodeIntelAgent()
    return agent.scan_github_trends(query)