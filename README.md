# RAG Demo — IPCC AR6 (Ollama + LangChain)

This is a Retrieval-Augmented Generation (RAG) demo application that allows you to ask questions about the IPCC AR6 reports. The application uses:

- **Ollama** for embeddings and LLM.
- **LangChain** for RAG pipeline.
- **Chroma** as vector database.
- **FastAPI** backend for serving queries.
- **Streamlit** frontend for interactive UI.

---
# Launch RAG Demo — All-in-One Script

```bash
# 1. Start Ollama server
ollama serve

# 2. Ingest PDFs into chunks
python ingest.py

# 3. Embed chunks and build vector store
python embedding.py

# 4. Start FastAPI backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 5. Start Streamlit frontend
streamlit run ui_streamlit.py

