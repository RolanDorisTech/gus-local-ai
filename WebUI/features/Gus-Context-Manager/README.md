# Gus Context Manager

> Lightweight context management, selective file retrieval, and prompt-injection defense for Open WebUI.

**Version:** 7.7  
**License:** MIT  
**Author:** Rolan & Doris Tech

---

## What It Does

`Gus_Context_Manager.py` helps manage long Open WebUI conversations with lower background memory usage.

It provides:

- Text-only context snapshots
- Predictive background compaction
- Stale-job cancellation
- Selective file retrieval
- Short file follow-up support
- Relevant top-k file chunk injection
- Prompt-injection filtering for suspicious retrieved web and tool content
- Local operation with Ollama

---

## Requirements

- Open WebUI
- Ollama
- `requests`
- Default model: `qwen3:1.7b`

Install the model:

```bash
ollama pull qwen3:1.7b
```

---

## Installation

1. Save the filter as:

   `Gus_Context_Manager.py`

2. In Open WebUI, create a new **Filter**.

3. Paste in the complete contents of the Python file.

4. Install `requests` if necessary:

   ```bash
   pip install requests
   ```

5. Make sure Ollama is running.

6. Enable the filter.

The default Ollama endpoint is:

`http://127.0.0.1:11434/api/chat`

---

## How It Works

### Context Compaction

The filter estimates conversation size using text only.

When the conversation reaches configured thresholds, older messages are summarized in the background using `qwen3:1.7b`.

Default thresholds:

- **60%** — prepare for compaction
- **75%** — eager compaction
- **90%** — immediate compaction

Only text snapshots are retained for background processing. Images and base64 payloads are not retained in conversation state.

### File Retrieval

The filter takes control of attached-file retrieval and retrieves relevant chunks only when the user's message clearly refers to a file or document.

Short follow-up questions can continue using recently referenced file context.

Retrieved context is injected into the current user message as:

```text
[Relevant file context]
...
[/Relevant file context]
```

### Prompt-Injection Filtering

Suspicious web, search, or tool content is checked with a lightweight regex.

Only content containing a possible injection signal is sent to the local sanitizer model.

Normal user messages are not modified.

---

## Important Settings

The main settings are available through the filter's **Valves**.

### Context

```text
context_window = 32000
prepare_ratio = 0.60
use_ratio = 0.75
emergency_ratio = 0.90
```

### Compactor

```text
compactor_model = "qwen3:1.7b"
compactor_context = 4096
compactor_max_tokens = 256
```

### File Retrieval

```text
file_top_k = 3
file_max_injected_chars = 6000
file_followup_turns = 3
```

### Web Sanitizer

```text
enable_web_sanitizer = True
sanitizer_max_tokens = 512
```

---

## Notes

This filter is designed for local Open WebUI installations.

The retrieval endpoint may need adjustment if your Open WebUI version uses a different internal API.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
