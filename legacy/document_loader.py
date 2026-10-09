import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import POLICY_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_and_split():
    """Load all policy documents and split into chunks."""
    if not os.path.isdir(POLICY_DIR):
        raise FileNotFoundError(f"Policy directory not found: {POLICY_DIR}")

    docs = []
    for filename in sorted(os.listdir(POLICY_DIR)):
        path = os.path.join(POLICY_DIR, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif filename.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")
        else:
            continue
        docs.extend(loader.load())

    if not docs:
        raise ValueError(f"No policy documents found in {POLICY_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"[document_loader] Loaded {len(docs)} doc(s), split into {len(chunks)} chunks.")
    return chunks