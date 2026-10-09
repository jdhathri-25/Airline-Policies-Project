# Test Queries — Airline Policy Explainer Bot

## Required Queries

| # | Query | Expected | Result |
|---|-------|----------|--------|
| 1 | Explain cabin baggage rules | 7kg, 55×35×25 cm, personal item | ✅ Pass |
| 2 | What is the check-in time process? | Domestic 2h, international 3h, bag drop 45 min before | ✅ Pass |
| 3 | Summarize boarding group rules | Groups by row/fare class, gate closes 20 min before | ✅ Pass |
| 4 | Explain excess baggage concept | Per-kg charge, cheaper pre-purchased online | ✅ Pass |

## Refusal Queries

| # | Query | Expected | Result |
|---|-------|----------|--------|
| 5 | Book me a ticket to Delhi | Refusal message | ✅ Pass |
| 6 | Cancel my booking | Refusal message | ✅ Pass |
| 7 | What's the cheapest fare? | Refusal message | ✅ Pass |
| 8 | Refund my cancelled flight | Refusal message | ✅ Pass |

## Off-Topic Queries

| # | Query | Expected | Result |
|---|-------|----------|--------|
| 9 | What's the weather in Delhi? | Only explains policies | ✅ Pass |
| 10 | Tell me a joke | Only explains policies | ✅ Pass |

## Notes
- Run `python test_run.py` to reproduce.
- Model: gemini-3.8-flash (with retry logic for 503/429)
- Free tier rate-limited; retries handle temporary errors.