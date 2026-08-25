# Token Usage Display

> Displays per-response and cumulative token usage in Open WebUI — real LM Studio usage + persistent Σ.

**Version:** 2.4.05 DEBUG FIX  
**License:** MIT  
**Author:** Rolan & Doris Tech

---

## Display Format

    🚀22.8t/s(1.2s) 🪟Σ15.6k(11.9kw) 👇P1.2k·900w|R420·320w 📈ΣP12.4k·9.5kw|ΣR3.2k·2.4kw

- `🚀 t/s(s)` — generation speed (token/second) + total time (second)
- `🪟Σ` — context window total tokens (words)
- `👇 P·w|R·w` — current turn
- `📈 ΣP·w|ΣR·w` — cumulative
- `P` - Prompt
- `R` - Reply
- `w` - words

## What It Does

- Uses real `prompt_tokens` / `completion_tokens` from LM Studio, Ollama, OpenAI when available
- Falls back to text estimate (`\w+|[^\w\s] * 1.3`) + word count
- Shows t/s generation speed and total elapsed
- Keeps persistent cumulative ΣP / ΣR / Σ per chat_id (500 chats LRU)
- Stable turn dedup via md5(prompt) or message_id — survives compaction / regen
- Strips `<think>` and `<reasoning>` blocks from count

## Installation

1. Open WebUI > Admin > Functions > Filters > New Filter
2. Name: `Token Usage Display`
3. Paste full `Token_Usage_Display.py` V2.4.05
4. Save > Toggle OFF then ON > Restart Open WebUI container > Start **New Chat**

No extra packages required.

## How It Works

- **inlet(body, user, metadata):** sets `_token_start`, `_token_first`, forces `stream_options.include_usage=True`
- **stream(event, user, metadata):** captures first output token time, captures final `usage` from stream
- **outlet(body, user, metadata, __event_emitter__):** prefers stream usage, else `message.usage`, else estimate; builds status line and emits via `__event_emitter__`
- Compatibility: accepts both `metadata` and `__metadata__`, `user` and `__user__`, `__event_emitter__`

## Notes

- Most accurate when backend provides usage
- Cumulative is in-memory, resets on OWUI restart
- Does not modify conversation content
- Fixed: real `__init__` dunders, split `</think>` to avoid template bug, stable `metadata` param name

## Troubleshooting

If line doesn't show: use New Chat (old chats cache old filter), check filter ON, `docker logs open-webui | grep TokenFilter` — should show `has_emitter=True` and `has_meta=True`. Test with plain model, not QwenDaily tool assistant.

## License

MIT — free to use, modify, share with attribution.

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
