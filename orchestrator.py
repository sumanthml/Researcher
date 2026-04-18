import os
import json
from groq import Groq
from dotenv import load_dotenv, find_dotenv
from tools.web_search import research_tool_manager
from memory.long_term import MemoryManager

load_dotenv(find_dotenv())

class ResearchOrchestrator:
    def __init__(self):
        # Using the stable 'versatile' model to stop connection crashes[cite: 326, 481, 502].
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.memory = MemoryManager()
        self.model = "llama-3.3-70b-versatile" 

    def run_full_loop(self, user_query, mode="General Intelligence"):
        # 1. Gather live intel from the 8+ APIs you collected[cite: 120, 145, 218].
        web_intel = research_tool_manager(user_query)
        past_memories = self.memory.recall(user_query) # [cite: 55, 208, 266]

        # 2. DYNAMIC DATA SYNTHESIS: We force a JSON response
        system_msg = f"""
        You are a Data Intelligence Architect. 
        Analyze this raw data: {web_intel[:3000]}
        
        TASK: Return ONLY a JSON object with this exact structure:
        {{
            "metrics": {{"Relevancy": "XX%", "Volatility": "High/Low", "Growth": "+XX%"}},
            "chart_data": {{"Label": ["A", "B", "C"], "Value": [10, 20, 30]}},
            "report": "Clean, short, professional analysis with bold headings."
        }}
        RULES: 
        - The 'Value' in chart_data must represent actual stats found in the data.
        - The 'report' must be under 200 words. NO RAMBLING.
        """
        
        try:
            # We call the Brain to generate the structured dashboard data
            completion = self.client.chat.completions.create(
                messages=[{"role": "system", "content": system_msg},
                          {"role": "user", "content": user_query}],
                model=self.model,
                temperature=0.1, # Factual precision[cite: 479].
                response_format={"type": "json_object"} # FORCES JSON FORMAT
            )
            
            # Parse the JSON so the UI can use it
            dashboard_data = json.loads(completion.choices[0].message.content)
            dashboard_data["raw_intel"] = web_intel
            
            # Commit to long-term learning database[cite: 54, 161, 305, 504].
            self.memory.commit(user_query, dashboard_data["report"])
            
            return dashboard_data
            
        except Exception as e:
            return {"report": f"System Error: {str(e)}", "metrics": {}, "chart_data": {}}