# ✈️ Airline Passenger Policy & Baggage Rule Explainer

A Streamlit chatbot that explains airline baggage, check-in, boarding, and travel policies.
It **only explains** — it cannot book, cancel, refund, or quote prices.

## Tech Stack
- Google Gemini Flash (`gemini-3.8-flash`) via the official `google-genai` SDK
- Streamlit for the chat UI
- Custom retry logic for transient API errors

## Architecture
User → Streamlit UI → `get_answer()` → Gemini Flash (with system prompt + policy context) → Response

The entire policy document is injected into the system prompt, giving the model grounding
without needing a separate vector store during runtime.

## Setup
1. `pip install -r requirements.txt`
2. Add `GEMINI_API_KEY=...` to `.env`
3. `streamlit run app.py`

## Files
- `app.py` — Streamlit frontend
- `src/config.py` — configuration
- `src/document_loader.py` — policy file loader (used in earlier RAG iteration)
- `src/vector_store.py` — FAISS index (earlier RAG iteration)
- `src/chain.py` — the LLM wrapper + system prompt (guardrails)
- `data/policies/policy.txt` — source policy document
- `tests/test_queries.md` — test log

## Guardrails
The system prompt strictly limits the bot to policy explanation.
Booking, cancellation, refunds, and pricing queries are politely refused.

## Limitations
- Single source document (general airline policies).
- Policies are subject to change — verify with the airline.
- Not a booking or transaction system.
- Free-tier Gemini API may occasionally return 503/429; retries handle most cases.