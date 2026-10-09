import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ---------- Load API key (Streamlit secrets first, then .env) ----------
def _get_gemini_key():
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY")


# ---------- Ollama fallback: only enable locally ----------
def _ollama_enabled():
    # Explicit override via env var
    env_flag = os.getenv("ENABLE_OLLAMA_FALLBACK", "").lower()
    if env_flag == "true":
        return True
    if env_flag == "false":
        return False
    # Auto-detect: enabled only when NOT running on Streamlit Cloud
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets:
            # On Streamlit Cloud, there is no local Ollama
            return False
    except Exception:
        pass
    return True  # local dev → allow fallback


OLLAMA_ENABLED = _ollama_enabled()

try:
    if OLLAMA_ENABLED:
        from ollama import chat as ollama_chat
        OLLAMA_AVAILABLE = True
    else:
        OLLAMA_AVAILABLE = False
except ImportError:
    OLLAMA_AVAILABLE = False


# ---------- Gemini client ----------
client = genai.Client(
    api_key=_get_gemini_key(),
    http_options=types.HttpOptions(timeout=15000),  # 15s; cloud can be slower
)

# ---------- Load policy ----------
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
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    return response.text


def _try_ollama(user_query: str) -> str:
    if not OLLAMA_AVAILABLE:
        raise RuntimeError("Ollama not available on this environment")
    response = ollama_chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )
    return response["message"]["content"]


def get_answer(user_query: str, chat_history: list) -> str:
    """Try Gemini first; fall back to Ollama only when enabled (local dev)."""
    try:
        return _try_gemini(user_query)
    except Exception as e:
        print(f"[chain] Gemini failed ({type(e).__name__}): {e}")

    if OLLAMA_ENABLED:
        try:
            return _try_ollama(user_query)
        except Exception as e:
            print(f"[chain] Ollama also failed: {type(e).__name__}: {e}")

    return (
        "⚠️ The AI service is temporarily unavailable. "
        "Please try again in a moment."
    )