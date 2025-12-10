import os
import json
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# ----- CONFIG -----
CHUNKS_DIR = "chunks"
PERSIST_DIR = "vectordb"
MODEL_NAME = "nomic-embed-text:latest"
OLLAMA_URL = "http://localhost:11434"  # Make sure your Ollama server is running here

# ----- FUNCTIONS -----
def test_ollama_connection(embedder):
    """Quick test to make sure Ollama server is reachable and embeddings work."""
    try:
        result = embedder.embed_documents(["Hello world"])
        print("Ollama embedding test succeeded:", result)
    except Exception as e:
        raise RuntimeError(
            f"Failed to connect to Ollama server at {OLLAMA_URL}. "
            f"Check that the server is running and the model '{MODEL_NAME}' is available."
        ) from e

def embed_and_store(chunks_dir=CHUNKS_DIR, persist_directory=PERSIST_DIR):
    # Initialize Ollama embeddings client
    embedder = OllamaEmbeddings(model=MODEL_NAME, base_url=OLLAMA_URL)

    # Test connection before processing all documents
    test_ollama_connection(embedder)

    # Load documents from JSON chunks
    documents = []
    for fn in os.listdir(chunks_dir):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(chunks_dir, fn), "r", encoding="utf8") as f:
            items = json.load(f)
        for it in items:
            documents.append({
                "page_content": it["page_content"],
                "metadata": it.get("metadata", {})
            })

    if not documents:
        raise ValueError(f"No documents found in {chunks_dir}")

    # Create or load Chroma vector store
    vectordb = Chroma.from_texts(
        texts=[doc["page_content"] for doc in documents],
        embedding=embedder,
        metadatas=[doc["metadata"] for doc in documents],
        persist_directory=persist_directory
    )

    vectordb.persist()
    print(f"Vector store persisted to '{persist_directory}' with {len(documents)} documents.")
    return vectordb

# ----- MAIN -----
if __name__ == "__main__":
    embed_and_store()

