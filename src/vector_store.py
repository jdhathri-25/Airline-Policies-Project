from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.document_loader import load_and_split
from src.config import GEMINI_API_KEY, EMBEDDING_MODEL


def build_vector_store():
    """Build a FAISS vector store from policy chunks."""
    chunks = load_and_split()
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
    )
    store = FAISS.from_documents(chunks, embeddings)
    print(f"[vector_store] Built FAISS index with {len(chunks)} chunks.")
    return store