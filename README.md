# ✈️ Airline Passenger Policy & Baggage Rule Explainer

An AI-powered Streamlit chatbot that explains airline baggage, check-in, boarding, and travel policies using Google Gemini Flash.

The chatbot explains airline policies only. It cannot book flights, cancel bookings, process refunds, or quote prices.

## Tech Stack

- Google Gemini via the official `google-genai` SDK
- Streamlit for the chat interface
- Python for application logic
- Custom retry logic for transient API errors

## Architecture

User → Streamlit UI → `get_answer()` → Gemini Flash → Response

The policy document is included in the system prompt to provide context for answering user queries without requiring a separate vector store at runtime.

## Setup

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your API key:

   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

3. Run the application:

   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py` — Streamlit frontend
- `src/config.py` — Configuration
- `src/document_loader.py` — Policy document loader
- `src/vector_store.py` — FAISS vector store from an earlier RAG iteration
- `src/chain.py` — LLM wrapper and system prompt
- `data/` — Policy data
- `tests/` — Test files

## Guardrails

- Explains airline policies only.
- Refuses booking, cancellation, refund, and pricing requests.
- Advises users to verify policies with the relevant airline.

## Limitations

- Uses a limited set of policy documents.
- Airline policies may change over time.
- Does not perform bookings or transactions.
- Gemini API availability and rate limits may affect responses.