import time
from src.chain import get_answer

queries = [
    "Explain cabin baggage rules",
    "What is the check-in time process?",
    "Summarize boarding group rules",
    "Explain excess baggage concept",
    "Book me a ticket to Delhi",
    "Cancel my booking",
    "What's the cheapest fare to Mumbai?",
    "Refund my cancelled flight",
    "What's the weather in Delhi?",
]

for i, q in enumerate(queries):
    print("=" * 60)
    print(f"Q{i+1}:", q)
    print("-" * 60)
    print(get_answer(q, []))
    print()
    if i < len(queries) - 1:
        time.sleep(15)
