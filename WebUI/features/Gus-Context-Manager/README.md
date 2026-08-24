# Gus Context Manager

> Lightweight context management, selective file retrieval, and prompt-injection defense for Open WebUI.

**Version:** 7.92a  
**License:** MIT  
**Author:** Rolan & Doris Tech

---

## Quick Setup

### 1. Start the compactor

```bash
source ~/mlx-env/bin/activate
export HF_HOME="/Volumes/YourDrive/huggingface"
python3 -m mlx_vlm.server \
    --model mlx-community/Qwen3.5-4B-4bit \
    --host 127.0.0.1 \
    --port 8081
```

If you do not use an external drive, remove or change the `HF_HOME` line.

### 2. Download the sanitizer

```bash
ollama pull qwen3.5:2b-mlx
```

### 3. Create the filter

In Open WebUI:

**Admin Panel → Functions → +**

Paste the complete contents of:

```text
Gus_Context_Manager_v7.92_Predictive_Intent.py
```

Then enable the filter.

### 4. Done

The default settings are already configured for the recommended local models below. You normally do not need to change anything.

---

## Recommended Models

| Role | Model | Endpoint |
|---|---|---|
| Main AI | Your preferred chat model | Open WebUI |
| Compactor | `mlx-community/Qwen3.5-4B-4bit` | `http://127.0.0.1:8081/v1/chat/completions` |
| Sanitizer | `qwen3.5:2b-mlx` | `http://127.0.0.1:11434/api/chat` |

Your main AI model remains separate. The two small helper models only handle background context compaction and suspicious web content.

---

## What It Does

Gus Context Manager keeps long conversations smooth and efficient by:

- Reducing unnecessary historical context
- Compacting older conversation history in the background
- Preserving important decisions and conclusions
- Removing historical images and large raw payloads
- Retrieving file content only when the user asks for it
- Supporting short file follow-up questions
- Checking suspicious web/search content for prompt injection
- Cancelling stale background compaction jobs

The goal is simple: **keep the main model focused on useful context without unnecessary prompt growth, slowdown, truncation, or forgetting.**

---

## How It Works

### Normal Conversation

For ordinary conversation, the filter does almost nothing. It uses lightweight CPU operations and adds minimal latency.

### Long Conversations

As the conversation grows, older history can be compacted in the background:

- **60%** — prepare for compaction
- **75%** — eager compaction
- **90%** — immediate compaction

The summary preserves important facts, decisions, preferences, settings, constraints, and unresolved issues.

### Files

File content is retrieved only when clearly needed, for example:

```text
Read the PDF.
What does the document say?
Check page 4.
According to the report...
What about the second section?
```

Relevant file content is temporary and is removed from later history unless retrieved again.

### Web Safety

Suspicious web, search, or tool content is checked for possible prompt injection.

Normal user messages are not sent through the sanitizer.

---

## Changing Models

You normally do not need to edit the code.

Open the filter's **Valves** and change:

```text
compactor_url
compactor_model
compactor_format

sanitizer_url
sanitizer_model
sanitizer_format
```

The defaults are:

```text
Compactor:
URL:    http://127.0.0.1:8081/v1/chat/completions
Model:  mlx-community/Qwen3.5-4B-4bit
Format: openai

Sanitizer:
URL:    http://127.0.0.1:11434/api/chat
Model:  qwen3.5:2b-mlx
Format: ollama
```

---

## Notes

- Designed primarily for local Open WebUI installations.
- Runs entirely with local helper models.
- The file retrieval endpoint may need adjustment if your Open WebUI version uses a different internal API.
- The recommended helper models are intentionally small to minimize impact on the main chat model.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
