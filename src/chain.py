import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


# ---------- Load API key (Streamlit secrets → .env) ----------
def _get_gemini_key():
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY")


# ---------- Ollama toggle ----------
def _ollama_enabled():
    env_flag = os.getenv("ENABLE_OLLAMA_FALLBACK", "").lower()
    if env_flag == "true":
        return True
    if env_flag == "false":
        return False
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets:
            return False
    except Exception:
        pass
    return True


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
    http_options=types.HttpOptions(timeout=15000),
)

# ---------- Load policy ----------
with open("data/policies/policy.txt", "r", encoding="utf-8") as f:
    POLICY_TEXT = f.read()

MODEL_NAME = "gemini-3.5-flash-lite"
OLLAMA_MODEL = "llama3.2:latest"

SYSTEM_PROMPT = f"""You are an airline policy explainer bot.

STRICT RULES (follow always):
1. ONLY explain airline policies: baggage, check-in, boarding, and travel guidelines.
2. NEVER book, cancel, refund, or quote prices. If the user asks for ANY of these,
   respond ONLY with:
   "I can only explain policies. Please contact the airline for bookings or refunds."
3. Answer ONLY using the CONTEXT below. Do not use outside knowledge.
4. If the CONTEXT does not contain the answer, respond:
   "I don't have that information. Please check the airline's official website."
5. Be concise. Use bullet points for lists. Do not invent numbers or rules.
6. If you are refusing a request under rule 2, START your response with the exact
   tag [REFUSED] on its own line, then the refusal message on the next line.

CONTEXT:
{POLICY_TEXT}
"""


def _build_gemini_contents(user_query: str, chat_history: list) -> list:
    """Convert chat history + new query into Gemini Content objects."""
    contents = []
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])],
            )
        )
    contents.append(
        types.Content(role="user", parts=[types.Part(text=user_query)])
    )
    return contents


def _try_gemini(user_query: str, chat_history: list) -> str:
    contents = _build_gemini_contents(user_query, chat_history)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1024,
        ),
    )
    return response.text


def _try_ollama(user_query: str, chat_history: list) -> str:
    if not OLLAMA_AVAILABLE:
        raise RuntimeError("Ollama not available")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_query})
    response = ollama_chat(model=OLLAMA_MODEL, messages=messages)
    return response["message"]["content"]


def get_answer(user_query: str, chat_history: list) -> str:
    """Try Gemini first; fall back to Ollama when enabled (local only)."""
    try:
        return _try_gemini(user_query, chat_history)
    except Exception as e:
        print(f"[chain] Gemini failed ({type(e).__name__}): {e}")

    if OLLAMA_ENABLED:
        try:
            return _try_ollama(user_query, chat_history)
        except Exception as e:
            print(f"[chain] Ollama also failed: {type(e).__name__}: {e}")

    return (
        "⚠️ The AI service is temporarily unavailable. "
        "Please try again in a moment."
    )