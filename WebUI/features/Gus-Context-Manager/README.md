# Gus Context Manager
> Lightweight context management, selective file retrieval, and prompt-injection defense for Open WebUI.
**Version:** 7.81
**License:** MIT
**Author:** Rolan & Doris Tech

---

## What It Does

`Gus_Context_Manager.py` helps manage long Open WebUI conversations with lower background memory usage. It provides:

- Text-only context snapshots
- Predictive background compaction
- Active summary consumption to reduce outgoing context
- Stale-job cancellation
- Selective file retrieval
- Short file follow-up support
- Relevant top-k file chunk injection
- Prompt-injection filtering for suspicious retrieved web and tool content
- Local operation with Ollama and OpenAI-compatible local servers

---

## Before You Start

**Requirements:**
- Open WebUI
- `requests` (`pip install requests` if missing)
- A local model server for the **compactor** (OpenAI-compatible)
- Ollama (or another compatible server) for the **sanitizer**

**Recommended models** — small background helpers; your main chat model stays separate and can be larger:

| Role | Model | Endpoint |
|---|---|---|
| Compactor | `mlx-community/Qwen3.5-4B-4bit` | `http://127.0.0.1:8081/v1/chat/completions` |
| Sanitizer | `qwen3.5:2b-mlx` | `http://127.0.0.1:11434/api/chat` |

> **Not mandatory.** You can use other compatible local models. Change any model name or endpoint through the filter's **Valves** in Open WebUI. See [Configuration](#configuration).

---

## Setup

### 1. Start the compactor

Start the MLX server for the recommended compactor (the first launch downloads the model automatically):

    source ~/mlx-env/bin/activate
    export HF_HOME="/Volumes/YourDrive/huggingface"
    python3 -m mlx_vlm.server \
        --model mlx-community/Qwen3.5-4B-4bit \
        --host 127.0.0.1 \
        --port 8081

If you do not use an external drive, remove or change the `HF_HOME` line.

### 2. Download the sanitizer

Make sure Ollama is running, then pull the recommended sanitizer:

    ollama pull qwen3.5:2b-mlx

### 3. Add the compactor connection in Open WebUI

Go to:
    Settings → Admin Settings → AI → Connections → +

Add the local compactor connection with:

- **URL:** `http://127.0.0.1:8081/v1`
- **API key:** leave empty; some Open WebUI versions require a value even when the local server does not need authentication. If so, enter any placeholder such as `not-needed`.
- **Prefix ID:** leave empty unless you specifically need it to avoid duplicate model IDs.

The sanitizer does **not** need a separate connection when using the default Ollama endpoint — the filter talks to Ollama directly.

### 4. Create the filter

1. In Open WebUI, open the **Admin Panel**.
2. Click the **Functions** tab.
3. Click the **+** button to create a new function/filter.
4. Paste the complete contents of:

       Gus_Context_Manager.py

5. Enable the filter.

### 5. Verify the Valves

The filter's defaults already match the recommended models above. If you use different models or server locations, set the matching URLs and model names under [Configuration](#configuration).

---

## How It Works

### Context Compaction

The filter estimates conversation size from text only. When a conversation reaches the configured thresholds, older messages are summarized in the background **after** the current generation completes:

- **60%** — prepare for compaction
- **75%** — eager compaction
- **90%** — immediate compaction

Only text snapshots are retained for background processing. Images, base64 payloads, and other large multimodal content are not intentionally retained in the filter's conversation state, which reduces unnecessary background memory pressure.

### Summary Consumption

In V7.81 the stored summary is actually applied. Before the main model receives a request, the next `inlet()` replaces the older message block that the summary covered with a single compact `[Compressed historical context]` reference message. This is what reduces outgoing context.

- **System messages are preserved verbatim** and are never replaced by a generated summary.
- Only the exact number of messages covered by the summary are removed; the current/newer conversation stays intact.
- The summary remains stored, so it is reapplied on every subsequent `inlet()`. A duplicate check on `[Compressed historical context]` makes re-application idempotent.
- If the conversation no longer contains the full source region, the summary is not applied (no ambiguous partial replacement).

### File Retrieval

Uses `file_handler = True` to take full ownership of retrieval. Normal prompts will NOT trigger retrieval thanks to conservative `FILE_INTENT_RE` gating.

Instead of retrieving file content on every message, the filter retrieves relevant chunks only when the user's message clearly refers to a file or document. Examples:

    Read the PDF.
    What does the document say?
    Check page 4.
    According to the report...
    What about the second section?

Short follow-up questions can continue using recently referenced file context. Relevant content is injected into the current user message, wrapped as:

     [Relevant file context]
     ...
     [/Relevant file context]

Only a limited amount of relevant content is injected.

### Prompt-Injection Filtering

Suspicious web, search, or tool content is checked with a lightweight regex. Only content containing a possible prompt-injection signal is sent to the local sanitizer model, which removes:

- Fake system instructions
- Requests to override instructions
- Requests to reveal secrets
- Attempts to change assistant behavior
- Unrelated commands hidden inside retrieved content

Normal user messages are **not** sent through the sanitizer. The filter also skips its own injected blocks (`[Relevant file context]` and `[Compressed historical context]`). If the sanitizer fails, the original retrieved content is preserved rather than silently deleting potentially useful information.

### Chinese Language Support

The filter includes a small number of Chinese phrases in its file-intent and file-follow-up patterns, so it recognizes common Chinese references to files, documents, reports, pages, and follow-up questions. For example:

    根据这个文件...
    第二个呢？
    里面说什么？

This does **not** change the assistant's language, make the filter Chinese-only, or modify the system prompt or normal conversation behavior. English-only users can leave these patterns exactly as they are.

---

## Configuration

All settings are in the filter's **Valves**. The defaults below match the recommended models.

**Context:**

- `context_window = 32000`
- `prepare_ratio = 0.60`
- `use_ratio = 0.75`
- `emergency_ratio = 0.90`
- `idle_seconds = 8`
- `eager_delay = 2.0`
- `min_messages = 25`
- `compact_ratio = 0.50`

**Compactor:**

- `compactor_url = http://127.0.0.1:8081/v1/chat/completions`
- `compactor_model = mlx-community/Qwen3.5-4B-4bit`
- `compactor_context = 4096`
- `compactor_max_tokens = 256`
- `compactor_temperature = 0.1`
- `compactor_timeout = 90`
- `compactor_max_chars = 8000`

**Web Sanitizer:**

- `sanitizer_url = http://127.0.0.1:11434/api/chat`
- `sanitizer_model = qwen3.5:2b-mlx`
- `sanitizer_context = 4096`
- `enable_web_sanitizer = True`
- `sanitizer_max_tokens = 512`
- `sanitizer_temperature = 0.0`
- `sanitizer_timeout = 20`
- `sanitizer_max_chars = 6000`
- `sanitizer_keep_alive = -1`

**File Retrieval:**

- `file_top_k = 3`
- `retrieval_url = http://127.0.0.1:3000/api/v1/retrieval/query/doc`
- `retrieval_timeout = 15`
- `file_query_cache_size = 32`
- `file_max_injected_chars = 6000`
- `file_followup_turns = 3`
- `enable_injection_defense = True`

**Changing models:** you do not need to edit the filter code. Open the **Valves** and change `compactor_url` / `compactor_model` or `sanitizer_url` / `sanitizer_model`. Each replacement must match the API format that part of the filter expects:

- Compactor — OpenAI-compatible API, default `http://127.0.0.1:8081/v1/chat/completions`
- Sanitizer — Ollama API, default `http://127.0.0.1:11434/api/chat`

---

## Notes

- This filter is designed primarily for local Open WebUI installations.
- The file-retrieval endpoint may need adjustment if your Open WebUI version uses a different internal retrieval API.
- The recommended helper models are intentionally small; your main chat model can remain separate and significantly larger.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
