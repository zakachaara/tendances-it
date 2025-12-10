from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

app = FastAPI()

# Load vector DB and set up retriever
embedding_fn = OllamaEmbeddings(model="nomic-embed-text:latest")
vectordb = Chroma(
    persist_directory="vectordb",
    embedding_function=embedding_fn
)

retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# LLM
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.0
)

prompt = PromptTemplate.from_template(
    "Use the following context to answer the question. "
    "If the answer is not in the context, say 'I don’t know.'\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}"
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)


class QueryIn(BaseModel):
    question: str


@app.post("/ask")
def ask(q: QueryIn):
    result = qa({"query": q.question})

    # Prepare sources with page info
    sources = []
    for doc in result.get("source_documents", []):
        # Assuming metadata contains 'page' or 'page_number'
        page = doc.metadata.get("page", "unknown")
        sources.append({"page": page, "content": doc.page_content[:200]})  # truncate for preview

    return {
        "ans": result["result"],      # frontend expects 'ans'
        "sources": sources
    }


