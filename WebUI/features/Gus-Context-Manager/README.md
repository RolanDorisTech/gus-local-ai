# Gus Context Manager

> Lightweight context management, selective file retrieval, and prompt-injection defense for Open WebUI.

**Version:** 7.8  
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
- Local operation with Ollama and OpenAI-compatible local servers

---

## Recommended Models

The filter uses two small helper models.

### Compactor

**Recommended:** `mlx-community/Qwen3.5-4B-4bit`

The compactor summarizes older conversation context in the background.

For Apple Silicon, it can be served with `mlx-vlm`:

    source ~/mlx-env/bin/activate
    export HF_HOME="/Volumes/YourDrive/huggingface"

    python3 -m mlx_vlm.server \
      --model mlx-community/Qwen3.5-4B-4bit \
      --host 127.0.0.1 \
      --port 8081

The first launch downloads the model automatically.

The recommended compactor endpoint is:

    http://127.0.0.1:8081/v1/chat/completions

The recommended model name is:

    mlx-community/Qwen3.5-4B-4bit

### Web Sanitizer

**Recommended:** `qwen3.5:2b-mlx`

The sanitizer checks suspicious retrieved web or tool content for possible prompt injections.

Download it with Ollama:

    ollama pull qwen3.5:2b-mlx

The recommended sanitizer endpoint is:

    http://127.0.0.1:11434/api/chat

The recommended model name is:

    qwen3.5:2b-mlx

---

## Important

The recommended models are **not mandatory**.

You can use other compatible local models if you prefer.

The model names and endpoints can be changed through the filter's **Valves** in Open WebUI.

The recommended setup is:

    Compactor:
    Qwen3.5 4B

    Sanitizer:
    Qwen3.5 2B

Using separate small models for these background tasks helps keep the main chat model focused on normal conversation.

---

## Requirements

- Open WebUI
- `requests`
- A local model server for the compactor
- Ollama or another compatible local server for the sanitizer

The recommended configuration uses:

    Compactor:
    mlx-community/Qwen3.5-4B-4bit

    Sanitizer:
    qwen3.5:2b-mlx

Install `requests` if necessary:

    pip install requests

---

## Installation

### 1. Start the Compactor

Start the recommended Qwen3.5 4B MLX server:

    source ~/mlx-env/bin/activate
    export HF_HOME="/Volumes/YourDrive/huggingface"

    python3 -m mlx_vlm.server \
      --model mlx-community/Qwen3.5-4B-4bit \
      --host 127.0.0.1 \
      --port 8081

If you do not use an external drive, remove or change the `HF_HOME` line.

### 2. Download the Sanitizer

Install the recommended sanitizer model:

    ollama pull qwen3.5:2b-mlx

Make sure Ollama is running.

### 3. Add the Compactor Connection in Open WebUI

Go to:

    Settings
    → Admin Settings
    → AI
    → Connections
    → +

Add the local compactor connection.

Use:

    URL:
    http://127.0.0.1:8081/v1

Some Open WebUI versions may require an API key field even when the local server does not require authentication.

If so, enter any placeholder value, such as:

    not-needed

You do not need to set a Prefix ID for this setup.

Leave Prefix ID empty unless you specifically need it to avoid duplicate model IDs.

The sanitizer does not need to be added as a separate Open WebUI connection when using the default Ollama endpoint. The filter communicates with Ollama directly.

### 4. Create the Filter

Create a new **Filter** in Open WebUI.

Paste the complete contents of:

    Gus_Context_Manager.py

Enable the filter.

### 5. Check the Valves

The filter's recommended defaults are already configured for the recommended models.

If you use different models or server locations, change the corresponding URLs and model names in the filter's **Valves**.

---

## How It Works

### Context Compaction

The filter estimates conversation size using text only.

When the conversation reaches configured thresholds, older messages are summarized in the background.

Default thresholds:

    60%  → Prepare for compaction
    75%  → Eager compaction
    90%  → Immediate compaction

Only text snapshots are retained for background processing.

Images, base64 payloads, and other large multimodal content are not intentionally retained in the filter's conversation state.

This helps reduce unnecessary background memory pressure.

---

## File Retrieval

The filter takes control of attached-file retrieval.

Instead of retrieving file content for every message, it retrieves relevant chunks only when the user's message clearly refers to a file or document.

Examples include:

    Read the PDF.

    What does the document say?

    Check page 4.

    According to the report...

    What about the second section?

Short follow-up questions can continue using recently referenced file context.

Relevant retrieved content is injected into the current user message as:

    [Relevant file context]
    ...
    [/Relevant file context]

Only a limited amount of relevant content is injected.

---

## Prompt-Injection Filtering

Suspicious web, search, or tool content is checked with a lightweight regex.

Only content containing a possible prompt-injection signal is sent to the local sanitizer model.

The sanitizer attempts to remove:

- Fake system instructions
- Requests to override instructions
- Requests to reveal secrets
- Attempts to change assistant behavior
- Unrelated commands hidden inside retrieved content

Normal user messages are not sent through the sanitizer.

If the sanitizer fails, the original retrieved content is preserved rather than silently deleting potentially useful information.

---

## Chinese Language Support

The filter includes a small number of Chinese phrases in its file-intent and file-follow-up patterns.

These patterns simply allow the filter to recognize common Chinese references to files, documents, reports, pages, and follow-up questions.

For example:

    根据这个文件...
    第二个呢？
    里面说什么？

This does **not** change the assistant's language.

It does **not** make the filter Chinese-only.

It does **not** modify the system prompt or normal conversation behavior.

English-only users can leave these patterns exactly as they are.

---

## Important Settings

The main settings are available through the filter's **Valves**.

### Context

    context_window = 32000
    prepare_ratio = 0.60
    use_ratio = 0.75
    emergency_ratio = 0.90

### Compactor

Recommended configuration:

    compactor_url =
    http://127.0.0.1:8081/v1/chat/completions

    compactor_model =
    mlx-community/Qwen3.5-4B-4bit

    compactor_context = 4096
    compactor_max_tokens = 256

### Web Sanitizer

Recommended configuration:

    sanitizer_url =
    http://127.0.0.1:11434/api/chat

    sanitizer_model =
    qwen3.5:2b-mlx

    sanitizer_max_tokens = 512

### File Retrieval

    file_top_k = 3
    file_max_injected_chars = 6000
    file_followup_turns = 3

---

## Changing Models

You do not need to modify the filter code to use different compatible models.

Open the filter's **Valves** and change the relevant settings.

For example:

    Compactor URL
    Compactor Model

    Sanitizer URL
    Sanitizer Model

The replacement model must be compatible with the API format used by that part of the filter.

The recommended configuration is:

    Compactor:
    OpenAI-compatible API
    http://127.0.0.1:8081/v1/chat/completions

    Sanitizer:
    Ollama API
    http://127.0.0.1:11434/api/chat

---

## Notes

This filter is designed primarily for local Open WebUI installations.

The file retrieval endpoint may need adjustment if your Open WebUI version uses a different internal retrieval API.

The recommended models are intentionally small because they are background helper models.

Your main chat model can remain separate and significantly larger.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
