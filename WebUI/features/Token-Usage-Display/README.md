# Token Usage Display

> Displays per-response and cumulative token usage in Open WebUI.

**Version:** 2.3  
**License:** MIT  
**Author:** Rolan & Doris Tech

---

## What It Does

`Token_Usage_Display.py` shows:

- Prompt tokens
- Response tokens
- Total tokens
- Prompt and response word counts
- Generation speed
- Total response time
- Cumulative usage for the current chat

Cumulative totals are kept in memory and are designed to continue working through chat compaction.

The display puts cumulative usage first for easier viewing on mobile.

---

## Installation

1. In Open WebUI, create a new **Filter**.
2. Name it:

   `Token Usage Display`

3. Paste in the complete contents of:

   `Token_Usage_Display.py`

4. Enable the filter.

No additional Python packages are required beyond the dependencies normally available in Open WebUI.

---

## How It Works

The filter requests streaming usage data when available.

If LM Studio provides token usage, those values are used.

If usage data is unavailable, the filter estimates tokens from text.

At the end of each response, it displays a status line similar to:

```text
📈 ΣP12.4k(9500w) ΣR3.2k(2400w) Σ15.6k(11900w) |
📊 P1.2k(900w) R420(320w) 18.4s 22.8t/s
```

### Display Labels

- `ΣP` — Cumulative prompt tokens
- `ΣR` — Cumulative response tokens
- `Σ` — Cumulative total tokens
- `P` — Current prompt tokens
- `R` — Current response tokens
- `w` — Word count
- `t/s` — Estimated response generation speed

---

## Notes

- Token values are most accurate when the backend provides usage data.
- The fallback token estimate is approximate.
- Cumulative totals are stored in memory and reset when the Open WebUI process restarts.
- The filter does not modify the conversation content.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
