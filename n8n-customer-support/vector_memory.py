import chromadb
from datetime import datetime

class CustomerMemory:
    def __init__(self):
        self.client = chromadb.Client()
        try:
            self.collection = self.client.create_collection(
                name="customer_memory",
                metadata={"description": "Customer conversation history"}
            )
        except:
            self.collection = self.client.get_collection(name="customer_memory")
    
    def store_conversation(self, user_id: str, conversation_summary: str, conversation_id: str):
        self.collection.add(
            documents=[conversation_summary],
            metadatas=[{
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }],
            ids=[conversation_id]
        )
    
    def retrieve_memory(self, user_id: str, query: str, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id}
        )
        return results

# Initialize
memory = CustomerMemory()
