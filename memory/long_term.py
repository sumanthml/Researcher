import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class MemoryManager:
    def __init__(self, index_name="researcher-memory"):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            self.enabled = False
            print("⚠️ Pinecone API Key missing. Memory disabled.")
            return
        
        # New Pinecone Initialization Pattern
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.enabled = True

        # Check if index exists, if not, create it (Serverless)
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384, # Dimension for 'all-MiniLM-L6-v2'
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        self.index = self.pc.Index(self.index_name)

    def recall(self, query):
        if not self.enabled: return "Memory inactive."
        return "Checking past research..." # Implementation logic

    def commit(self, query, report):
        if not self.enabled: return
        print(f"🧠 Saving research for future learning: {query}")