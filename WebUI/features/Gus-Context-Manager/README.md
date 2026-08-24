# Gus Context Manager

> Lightweight context management, selective file retrieval, and prompt-injection defense for Open WebUI.

**Version:** 7.93.01b Unified  
**License:** MIT  
**Author:** Rolan & Doris Tech

One compactor file for all models. Fail-safe 8K default, explicit 16K overrides.

---

## Quick Setup

### 1. Start compactor (4B, fast on M1 Max)

```bash
source ~/mlx-env/bin/activate
export HF_HOME="/Volumes/YourDrive/huggingface"
python3 -m mlx_vlm.server \
    --model mlx-community/Qwen3.5-4B-4bit \
    --host 127.0.0.1 \
    --port 8081
```

Remove `HF_HOME` if you don't use an external drive.

### 2. Pull sanitizer

```bash
ollama pull qwen3.5:2b-mlx
```

### 3. Install filter

Open WebUI: **Admin Panel → Functions → +**

Paste `Gus_Context_Manager_v7.93.01_unified.py` and enable.

Done. Defaults work for the models below.

---

## Recommended Models

| Role | Model | Endpoint | Ctx |
|---|---|---|---|
| Main | Ornith 35b-a3b-mlx / Gemma 31b / Qwen 27b | Your LM Studio / Ollama | 16384 |
| Main small | qwen3.5:2b / llama3.3:70b | Ollama | 8192 |
| Compactor | `mlx-community/Qwen3.5-4B-4bit` | `http://127.0.0.1:8081/v1/chat/completions` | 8192 |
| Sanitizer | `qwen3.5:2b-mlx` | `http://127.0.0.1:11434/api/chat` | 4096 |

Main model stays separate. Helper models only do background compaction and web sanitization.

---

## What It Does

- Keeps main model focused, no prompt bloat
- Strips historical images, file context, and large web payloads
- Compacts old history async, preserves decisions and facts
- Retrieves files only on explicit intent
- Supports follow-ups like `what about the second section?`
- Checks suspicious web/tool content for injections
- Cancels stale background jobs

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

### Architecture (v7.93.01)

```
current model -> effective_ctx -> file budget -> estimate -> pressure -> async compaction
```

* Unknown models default to 8192 (fail-safe, not 16384)
* Case-insensitive match: `MLX-COMMUNITY/Qwen3.5-4B-4bit` matches `qwen3.5-4b`
* File retrieval budget uses current turn's ctx, not previous turn's stale value

### Files

Triggers on:

```
Read the PDF / Check page 4 / According to the report / What does the document say?
```

* `top_k=3`, cached, dynamically budgeted against current ctx
* Injected context is temporary, removed from next turns unless re-requested
* Full-file intent (`full file`, `entire file`) capped at 8000 chars

### Web Safety

* Only last web payload is sanitized, not entire history
* Capped at 4000 chars, `keep_alive=5m` (not permanent)
* Normal user messages bypass sanitizer

---

## Valves You May Change

In filter Valves UI:

```
context_window: 8192 (conservative default, overridden per model)
prepare_ratio: 0.50
use_ratio: 0.65
emergency_ratio: 0.85

compactor_url, compactor_model, compactor_format
sanitizer_url, sanitizer_model, sanitizer_format

file_top_k: 3
file_max_injected_chars: 6000
web_payload_keep_chars: 600
```

No code edit needed for model changes.

---

## Changelog v7.92a → v7.93.01b

1. One file for all models, dynamic ctx detection
2. Default 8192 fail-safe, explicit 16K map (`ornith`, `gemma-4-31b`, `qwen3.5-4b` etc)
3. `_make_text_snapshot` and `_build_compaction_conversation` both skip `[Compressed historical context]`
4. Sanitizer only scans newest web payload, 5m keep-alive
5. `effective_ctx` passed directly to file retrieval (fixes stale ctx on model switch)
6. Removed unused `MODEL_CTX_MAP_16K`, fixed `key.lower() in low` match
7. Token estimate `chars/3.5` not `/4`, `compactor_max_tokens=512`

---

## Notes

* Local Open WebUI only. Runs fully local.
* File retrieval URL may differ on newer Open WebUI versions. Adjust `retrieval_url` valve if needed.
* For M1 Max 64GB: Ornith 16K ~27GB total, Qwen2b 4K ~2GB. Keep both keep-alive.

---

## License

MIT

---

## Credits

**Rolan & Doris Tech**

If this helps, please subscribe on YouTube and star the repo.
