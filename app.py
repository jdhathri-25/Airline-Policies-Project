import streamlit as st
from src.chain import get_answer
import time

# ---------- Page config ----------
st.set_page_config(
    page_title="SkyAssist — Airline Policy Explainer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* -------- Base background -------- */
    .stApp {
        background: #05070d;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(56,189,248,0.25), transparent),
            radial-gradient(ellipse 60% 50% at 100% 100%, rgba(139,92,246,0.15), transparent),
            radial-gradient(ellipse 60% 50% at 0% 100%, rgba(37,99,235,0.15), transparent);
        background-attachment: fixed;
    }

    /* -------- Hide chrome -------- */
    #MainMenu, footer, header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}

    /* -------- Force dark text colors -------- */
    .stMarkdown, .stMarkdown p, .stMarkdown li { color: #cbd5e1; }
    h1, h2, h3, h4 { color: #f1f5f9; font-family: 'Space Grotesk', sans-serif; }

    /* ==================== HERO ==================== */
    .hero-wrap {
        position: relative;
        padding: 3rem 3rem 3rem 3rem;
        border-radius: 28px;
        background:
            linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0c4a6e 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow:
            0 30px 80px -20px rgba(56, 189, 248, 0.35),
            0 0 0 1px rgba(255,255,255,0.03) inset;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -200px; left: -100px;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(56,189,248,0.35), transparent 60%);
        animation: float1 12s ease-in-out infinite;
    }
    .hero-wrap::after {
        content: '';
        position: absolute;
        bottom: -200px; right: -100px;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(139,92,246,0.3), transparent 60%);
        animation: float2 15s ease-in-out infinite;
    }
    @keyframes float1 {
        0%,100% { transform: translate(0,0); }
        50% { transform: translate(40px, 30px); }
    }
    @keyframes float2 {
        0%,100% { transform: translate(0,0); }
        50% { transform: translate(-40px, -30px); }
    }

    .hero-inner { position: relative; z-index: 2; }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(56,189,248,0.1);
        border: 1px solid rgba(56,189,248,0.3);
        padding: 0.4rem 0.9rem;
        border-radius: 100px;
        color: #7dd3fc;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1.25rem;
    }
    .hero-badge .pulse {
        width: 6px; height: 6px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 12px #22c55e;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%,100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.3); }
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -1.5px;
        color: #ffffff;
        margin: 0 0 1rem 0;
        background: linear-gradient(180deg, #ffffff 0%, #94a3b8 120%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-title .accent {
        background: linear-gradient(90deg, #38bdf8 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 580px;
        line-height: 1.6;
        margin: 0;
    }

    /* ==================== BADGES ==================== */
    .pill-row {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin: 1rem 0 1.75rem 0;
    }
    .pill {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 0.45rem 1rem;
        border-radius: 100px;
        font-size: 0.8rem;
        color: #cbd5e1;
        font-weight: 500;
        transition: all 0.25s ease;
        backdrop-filter: blur(10px);
    }
    .pill:hover {
        border-color: rgba(56, 189, 248, 0.5);
        color: #7dd3fc;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px -8px rgba(56,189,248,0.4);
    }

    /* ==================== SIDEBAR ==================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #05070d 0%, #0b1120 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.1);
    }
    section[data-testid="stSidebar"] * { color: #cbd5e1; }
    section[data-testid="stSidebar"] h2 {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(90deg, #38bdf8, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.3rem;
        font-weight: 700;
    }
    section[data-testid="stSidebar"] h3 {
        color: #64748b;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(15, 23, 42, 0.6);
        color: #e2e8f0;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        text-align: left;
        padding: 0.85rem 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    section[data-testid="stSidebar"] .stButton button::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #38bdf8, #a78bfa);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(30, 58, 138, 0.35);
        border-color: rgba(56, 189, 248, 0.4);
        color: white;
        transform: translateX(6px);
        box-shadow: 0 10px 30px -10px rgba(56,189,248,0.5);
    }
    section[data-testid="stSidebar"] .stButton button:hover::before {
        opacity: 1;
    }

    /* ==================== STATS ==================== */
    .stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
    }
    .stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 14px;
        padding: 0.9rem 0.75rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.25s ease;
    }
    .stat-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }
    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(180deg, #38bdf8, #0284c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.65rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.35rem;
        font-weight: 600;
    }

    /* ==================== CHAT ==================== */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 18px;
        padding: 1rem 1.25rem;
        backdrop-filter: blur(12px);
        animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, #38bdf8, #2563eb) !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, #a78bfa, #7c3aed) !important;
    }

    /* Chat input */
    .stChatInput textarea {
        background: rgba(15, 23, 42, 0.9) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important;
        font-size: 0.95rem !important;
        padding: 1rem 1.25rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }
    .stChatInput textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15), 0 8px 30px -10px rgba(56,189,248,0.5) !important;
    }
    .stChatInput textarea::placeholder { color: #64748b !important; }

    /* ==================== DISCLAIMER ==================== */
    .disclaimer {
        background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(245,158,11,0.03));
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        color: #cbd5e1;
        font-size: 0.82rem;
        margin-top: 1.5rem;
        line-height: 1.6;
    }
    .disclaimer b { color: #fbbf24; }

    /* ==================== FOOTER ==================== */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.75rem;
        margin: 1.5rem 0 0.5rem 0;
        padding-top: 1.25rem;
        border-top: 1px solid rgba(56, 189, 248, 0.1);
        letter-spacing: 0.3px;
    }
    .footer .grad {
        background: linear-gradient(90deg, #38bdf8, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }

    /* ==================== CAPABILITY CARD ==================== */
    .cap-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 14px;
        padding: 1rem;
        font-size: 0.8rem;
        line-height: 1.7;
        color: #cbd5e1;
        backdrop-filter: blur(10px);
    }
    .cap-can { color: #4ade80; font-weight: 600; }
    .cap-cant { color: #f87171; font-weight: 600; }

    /* Response time chip */
    .rt-chip {
        display: inline-block;
        background: rgba(56,189,248,0.1);
        border: 1px solid rgba(56,189,248,0.2);
        color: #7dd3fc;
        font-size: 0.7rem;
        padding: 0.2rem 0.6rem;
        border-radius: 100px;
        margin-top: 0.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "refusal_count" not in st.session_state:
    st.session_state.refusal_count = 0

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ✈️ SkyAssist")
    st.caption("Your airline policy co-pilot")
    st.divider()

    st.markdown("### 💬 Quick Questions")
    for q in [
        "Explain cabin baggage rules",
        "What is the check-in time process?",
        "Summarize boarding group rules",
        "Explain excess baggage concept",
    ]:
        if st.button(q, use_container_width=True, key=f"btn_{q}"):
            st.session_state.pending_query = q

    st.divider()
    st.markdown("### 📊 Session Stats")
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-value">{st.session_state.query_count}</div>
            <div class="stat-label">Queries</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{st.session_state.refusal_count}</div>
            <div class="stat-label">Blocked</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️  Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.refusal_count = 0
        st.rerun()

    st.divider()
    st.markdown("### ℹ️ Capabilities")
    st.markdown("""
    <div class="cap-card">
        <span class="cap-can">✔ Can</span><br>
        Explain baggage, check-in, boarding & travel rules<br><br>
        <span class="cap-cant">✘ Cannot</span><br>
        Booking, refunds, or pricing
    </div>
    """, unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-inner">
        <div class="hero-badge">
            <span class="pulse"></span> LIVE · POWERED BY GEMINI FLASH
        </div>
        <h1 class="hero-title">
            Airline policies,<br>
            <span class="accent">explained instantly.</span>
        </h1>
        <p class="hero-sub">
            Ask about baggage allowances, check-in timelines, boarding rules, or travel guidelines.
            Clear answers, grounded in policy — no bookings, no guesswork.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Clickable topic pills ----------
st.markdown('<div class="pill-row">', unsafe_allow_html=True)
pill_cols = st.columns(5)
topics = [
    ("🧳 Baggage", "Explain cabin baggage rules"),
    ("⏰ Check-in", "What is the check-in time process?"),
    ("🎫 Boarding", "Summarize boarding group rules"),
    ("⚖️ Excess Baggage", "Explain excess baggage concept"),
    ("🛫 Travel Guidelines", "Explain general travel guidelines"),
]
for col, (label, query) in zip(pill_cols, topics):
    with col:
        if st.button(label, key=f"pill_{label}", use_container_width=True):
            st.session_state.pending_query = query
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Empty greeting ----------
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🧑‍✈️"):
        st.markdown(
            "Hi there! 👋 I'm your airline policy assistant.\n\n"
            "Ask me anything about **baggage rules, check-in timelines, boarding, or excess baggage**. "
            "Click a quick question on the left to get started."
        )

# ---------- Chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍✈️" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

# ---------- Query handling ----------
prompt = None
if "pending_query" in st.session_state:
    prompt = st.session_state.pop("pending_query")

chat_input = st.chat_input("Ask about baggage, check-in, or boarding...")
if chat_input:
    prompt = chat_input

REFUSAL_KEYWORDS = ["book", "cancel", "refund", "fare", "price", "cheapest", "reschedule"]

if prompt:
    st.session_state.query_count += 1

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧑‍✈️"):
        start = time.time()
        with st.spinner("Checking the policy…"):
            try:
                response = get_answer(prompt, st.session_state.messages[:-1])
            except Exception as e:
                response = f"⚠️ Something went wrong: `{type(e).__name__}`. Please try again."
        elapsed = time.time() - start

        if any(k in prompt.lower() for k in REFUSAL_KEYWORDS):
            st.session_state.refusal_count += 1

        st.markdown(response)
        st.markdown(f'<span class="rt-chip">⚡ {elapsed:.2f}s</span>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------- Disclaimer & footer ----------
st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Disclaimer:</b> Policies are subject to change. Always verify with the airline before travel.
    SkyAssist does not perform bookings, refunds, or pricing.
</div>
<div class="footer">
    <span class="grad">SkyAssist</span> · Gemini Flash · Streamlit
</div>
""", unsafe_allow_html=True)