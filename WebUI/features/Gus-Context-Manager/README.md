# Gus Context Manager

> Lightweight context management, selective file retrieval, and prompt-injection defense for Open WebUI.

**Version:** 7.94.00 Ollama Unified
**License:** MIT
**Author:** Rolan & Doris Tech

One compactor file for all models. Fail-safe 8K default, explicit 16K overrides. Helper models run through Ollama.

---

## Quick Setup

### 1. Pull compactor (4B MLX 8-bit)

```bash
ollama pull qwen3.5:4b-mlx
```

### 2. Pull sanitizer

```bash
ollama pull qwen3.5:2b-mlx
```

### 3. Install filter

Open WebUI: **Admin Panel → Functions → +**

Paste `Gus_Context_Manager_v7.94.00_Ollama.py` and enable.

Done. Defaults work for the models below.

---

## Recommended Models

| Role       | Model                                     | Endpoint                          | Ctx   |
| ---------- | ----------------------------------------- | --------------------------------- | ----- |
| Main       | Ornith 35b-a3b-mlx / Gemma 31b / Qwen 27b | Your LM Studio / Ollama           | 16384 |
| Main small | qwen3.5:2b / llama3.3:70b                 | Ollama                            | 8192  |
| Compactor  | `qwen3.5:4b-mlx`                          | `http://127.0.0.1:11434/api/chat` | 16384 |
| Sanitizer  | `qwen3.5:2b-mlx`                          | `http://127.0.0.1:11434/api/chat` | 4096  |

Main model stays separate. Helper models only do background compaction and web sanitization.

The compactor uses Ollama with `keep_alive=24h` to avoid repeated model reloads and reduce compaction latency.

---

## What It Does

* Keeps main model focused, no prompt bloat
* Strips historical images, file context, and large web payloads
* Compacts old history async, preserves decisions and facts
* Retrieves files only on explicit intent
* Supports follow-ups like `what about the second section?`
* Checks suspicious web/tool content for injections
* Cancels stale background jobs

---

## How It Works

### Normal chat

Almost no-op. Lightweight CPU only.

### Long chat (3-stage, model-aware)

Pressure = `estimated_tokens / effective_ctx`

* **50%** - prepare (wait for idle 6s)
* **65%** - eager (wait 1.5s)
* **85%** - immediate

Example: 8K model compacts at ~4096 tokens, 16K model at ~8192.

Summary replaces first 60% of history, keeps last 40% raw. Old summary is never re-summarized.

### Architecture (v7.94.00)

```text
current model -> effective_ctx -> file budget -> estimate -> pressure -> async compaction
```

* Unknown models default to 8192 (fail-safe, not 16384)
* Case-insensitive model matching is used for known context sizes
* File retrieval budget uses the current turn's ctx, not a previous turn's stale value
* Compactor and sanitizer both use Ollama's `/api/chat` endpoint

---

## Files

Triggers on:

```text
Read the PDF / Check page 4 / According to the report / What does the document say?
```

* `top_k=3`, cached, dynamically budgeted against current ctx
* Injected context is temporary, removed from next turns unless re-requested
* Full-file intent (`full file`, `entire file`) capped at 8000 chars

---

## Web Safety

* Only last web payload is sanitized, not entire history
* Capped at 4000 chars
* Sanitizer uses `keep_alive=5m`
* Normal user messages bypass sanitizer

---

## Valves You May Change

In filter Valves UI:

```text
context_window: 8192 (conservative default, overridden per model)
prepare_ratio: 0.50
use_ratio: 0.65
emergency_ratio: 0.85

compactor_url: http://127.0.0.1:11434/api/chat
compactor_model: qwen3.5:4b-mlx
compactor_format: ollama
compactor_context: 16384
compactor_keep_alive: 24h

sanitizer_url: http://127.0.0.1:11434/api/chat
sanitizer_model: qwen3.5:2b-mlx
sanitizer_format: ollama
sanitizer_context: 4096
sanitizer_keep_alive: 5m

file_top_k: 3
file_max_injected_chars: 6000
web_payload_keep_chars: 600
```

No code edit needed for model changes.

---

## Changelog v7.93.01b → v7.94.00

1. Replaced the separate HF MLX compactor server with Ollama
2. Replaced `mlx-community/Qwen3.5-4B-4bit` with `qwen3.5:4b-mlx`
3. Compactor endpoint changed from port `8081` OpenAI-compatible API to Ollama `/api/chat` on port `11434`
4. Compactor format changed from `openai` to `ollama`
5. Compactor context increased to 16384
6. Added `compactor_keep_alive` to the actual Ollama compactor request
7. Compactor keep-alive set to `24h` to avoid repeated model loading
8. Removed the need for a separate Python virtual environment and `mlx_vlm.server`
9. Removed `HF_HOME` setup for the compactor
10. Sanitizer remains `qwen3.5:2b-mlx` on Ollama with `keep_alive=5m`
11. Existing dynamic context detection, file retrieval, summary handling, and injection defense remain unchanged

---

## Notes

* Local Open WebUI and local Ollama only. Runs fully local.
* No separate HF model server is required for the compactor.
* The compactor remains loaded for up to 24 hours after use, reducing reload latency during repeated compaction.
* On a 64GB unified-memory M1 Max, keeping the 4B compactor loaded is intended to prioritize responsiveness over unloading helper-model memory.
* File retrieval URL may differ on newer Open WebUI versions. Adjust `retrieval_url` valve if needed.
* The sanitizer uses a shorter 5-minute keep-alive because it is only needed when suspicious web/tool content requires cleaning.

---

## License

MIT

---

## Credits

**Rolan & Doris Tech**

If this helps, please subscribe on YouTube and star the repo.
