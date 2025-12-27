from fastapi import FastAPI
from pydantic import BaseModel
from vector_memory import memory
import requests

app = FastAPI()

class MemoryStore(BaseModel):
    user_id: str
    summary: str
    conversation_id: str

class MemoryQuery(BaseModel):
    user_id: str
    query: str


# ADD this function before the FastAPI app
def summarize_conversation(user_message: str, ai_response: str, intent: str) -> str:
    """Use Ollama to create concise conversation summary"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": f"""Summarize this customer service interaction in ONE concise sentence (max 20 words).

Intent: {intent}
Customer: {user_message}
Agent: {ai_response}

Summary:""",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            summary = response.json().get("response", "").strip()
            return summary if summary else f"Customer inquiry about {intent}"
        else:
            return f"Customer inquiry about {intent}"
            
    except Exception as e:
        print(f"Summarization error: {e}")
        return f"Customer inquiry about {intent}"


@app.post("/memory/store")
def store_memory(data: MemoryStore):
    # Extract components from the summary field
    parts = data.summary.split(". Response: ")
    user_part = parts[0].replace("User asked about ", "").split(": ", 1)
    
    intent = user_part[0] if len(user_part) > 0 else "unknown"
    user_message = user_part[1] if len(user_part) > 1 else data.summary
    ai_response = parts[1] if len(parts) > 1 else "No response"
    
    # Generate concise summary
    concise_summary = summarize_conversation(user_message, ai_response, intent)
    
    # Store with summarized version
    memory.store_conversation(data.user_id, concise_summary, data.conversation_id)
    
    return {
        "status": "stored",
        "summary": concise_summary,
        "original_length": len(data.summary),
        "summarized_length": len(concise_summary)
    }
@app.post("/memory/retrieve")
def retrieve_memory(data: MemoryQuery):
    results = memory.retrieve_memory(data.user_id, data.query)
    return {"memories": results}
