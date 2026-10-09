# Legacy - RAG Prototype

These files are from an earlier iteration of SkyAssist that used a full
RAG (Retrieval-Augmented Generation) pipeline with:

- **LangChain** for orchestration
- **FAISS** as the vector database
- **Google embeddings** (`gemini-embedding-001`) for chunk vectors
- **RecursiveCharacterTextSplitter** for chunking (500-char chunks, 80-char overlap)

## Why we moved away from RAG

1. **Small corpus:** Our policy document is a single short file. Splitting it
   into 10 chunks and retrieving the top 3 introduced unnecessary latency
   and complexity.

2. **Full-context injection works better:** Injecting the entire policy into
   the system prompt gives the model complete context every time, eliminating
   retrieval errors (chunk boundary issues, missed context).

3. **API fragility:** Google repeatedly deprecated embedding models
   (`models/embedding-001` -> `gemini-embedding-001`), causing pipeline breakage.

4. **Simplicity:** Fewer moving parts = fewer failure modes.

## When RAG *would* be the right choice

- Large knowledge bases (thousands of documents)
- Frequently updated content
- Multi-tenant retrieval
- When context window limits are hit
