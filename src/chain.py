import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------- Offline fallback (Ollama) ----------
try:
    from ollama import chat as ollama_chat
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

load_dotenv()

# ---------- Gemini client with 5-second timeout ----------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=5000),
)

with open("data/policies/policy.txt", "r", encoding="utf-8") as f:
    POLICY_TEXT = f.read()

MODEL_NAME = "gemini-3.5-flash-lite"
OLLAMA_MODEL = "llama3.2:latest"

SYSTEM_PROMPT = f"""You are an airline policy explainer bot.

STRICT RULES (follow always):
1. ONLY explain airline policies: baggage, check-in, boarding, and travel guidelines.
2. NEVER book, cancel, refund, or quote prices. If the user asks for ANY of these, respond ONLY with:
   "I can only explain policies. Please contact the airline for bookings or refunds."
3. Answer ONLY using the CONTEXT below. Do not use outside knowledge.
4. If the CONTEXT does not contain the answer, respond:
   "I don't have that information. Please check the airline's official website."
5. Be concise. Use bullet points for lists. Do not invent numbers or rules.

CONTEXT:
{POLICY_TEXT}
"""


def _try_gemini(user_query: str) -> str:
    """Online answer via Gemini. Single attempt with short timeout."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    return response.text


def _try_ollama(user_query: str) -> str:
    """Offline answer via local Ollama model."""
    if not OLLAMA_AVAILABLE:
        raise RuntimeError("Ollama client not installed. Run: pip install ollama")
    response = ollama_chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )
    return response["message"]["content"]


def get_answer(user_query: str, chat_history: list) -> str:
    """Try Gemini with fast timeout; fall back to Ollama if it fails."""
    try:
        return _try_gemini(user_query)
    except Exception as e:
        print(f"[chain] Gemini failed ({type(e).__name__}). Falling back to Ollama...")

    try:
        return _try_ollama(user_query)
    except Exception as e:
        print(f"[chain] Ollama also failed: {type(e).__name__}: {e}")

    return (
        "⚠️ I'm offline and the local model isn't available. "
        "Please check your connection or try again."
    )