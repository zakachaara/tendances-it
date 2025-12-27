from fastapi import FastAPI
from pydantic import BaseModel
from vector_memory import memory

app = FastAPI()

class MemoryStore(BaseModel):
    user_id: str
    summary: str
    conversation_id: str

class MemoryQuery(BaseModel):
    user_id: str
    query: str

@app.post("/memory/store")
def store_memory(data: MemoryStore):
    memory.store_conversation(data.user_id, data.summary, data.conversation_id)
    return {"status": "stored"}

@app.post("/memory/retrieve")
def retrieve_memory(data: MemoryQuery):
    results = memory.retrieve_memory(data.user_id, data.query)
    return {"memories": results}
