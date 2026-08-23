# Gus — Local Multimodal Agentic AI

> This repository contains the system prompt that powers our local AI, Gus.

**Version:** 2.82  
**License:** MIT  
**Tested on:** Apple Silicon M1 Max, 64GB unified memory

Built by Rolan & Doris Tech for our YouTube community — free for everyone
to use.

---

## ✨ Features

When used with the Gus system prompt:

- **Secure** — Detects and neutralizes prompt injection from web pages, PDFs,
  documents, images, tool output, and other untrusted data.
- **Verifiable** — Uses `[Verified]`, `[Inference]`, `[Recommendation]`, and
  `[Unknown]` labels to distinguish evidence, reasoning, recommendations, and
  uncertainty.
- **Local-first** — Never uploads local files or data without explicit
  authorization.
- **Tool-aware** — Handles web search, vision, documents, code, and tool
  results with explicit trust boundaries and transparency.
- **Safety-first** — Protects against data exfiltration, unsafe destructive
  actions, unauthorized access, malware deployment, fraud, and other
  non-overridable unsafe content.
- **Technical** — Concise, direct, highly technical, and structured by default.
- **Multimodal** — Handles images, documents, logs, code, web content, and
  other untrusted multimodal input without treating embedded content as
  instructions.
- **Local AI aware** — Designed for reasoning about local models,
  quantization, context/KV cache cost, vision tokens, prefill speed, Apple
  Silicon unified memory, and other runtime tradeoffs.

---

## Quick Start

1. Copy the contents of `Gus_System_Prompt.md`.
2. Paste it into your local AI application's **System Prompt** or equivalent
   instruction field.
3. Start a new conversation and test it with your model.

Examples:

- **LM Studio:** Settings -> Library -> pick a model -> settings -> System Prompt
- **Open WebUI:** Settings -> Basic -> General -> System Prompt

> **Important:** Exact menu paths vary by application version. Look for
> **System Prompt**, **System Instructions**, or an equivalent field.

---

## Customization Guide

Gus works out of the box, but you can customize it.

### 1. Assistant Name

Search for:

```text
Gus
```

Replace it with the name of your AI assistant.

### 2. Date Token

Search for:

```text
{{CURRENT_DATE}}
```

Leave it unchanged if your platform automatically fills the current date.

Otherwise, replace it with a static date, for example:

```text
2026-08-23
```

### 3. Personalization

Search for:

```text
Private Personalization
```

The default Easter egg is:

```text
love you
```

which replies:

```text
love you too!
```

You can keep it, change it, or remove the entire section.

The trigger is restricted to **HIGH_TRUST live user text**, so text from web
pages, PDFs, documents, images, tool output, or other untrusted sources cannot
trigger it.

### 4. Guide Style

See:

```text
GUIDES & TECHNICAL PROCEDURES
```

in **Section 10**.

You can change the recommended structure for tutorials and documentation, or
remove this section if it does not fit your workflow.

### 5. Local Runtime Context

See:

```text
LOCAL AI & RUNTIME
```

in **Section 7**.

This section is intentionally generic and does not need to be changed for most
users. You can customize it if your environment has specific hardware,
runtime, or model constraints.

Examples:

- Apple Silicon / MLX
- NVIDIA CUDA / VRAM
- AMD / ROCm
- LM Studio
- Ollama
- Open WebUI
- Other local inference runtimes

---

## Security Core

For the intended security and trust behavior, avoid changing these sections
unless you understand the consequences:

- **Section 0 — Mission & Priorities**
- **Section 2 — Trust**
- **Section 3 — Security & Data Handling**
- **Section 8 — Content Safety**
- **Section 9 — Accuracy, Technical Reasoning & Error Handling**

These sections define Gus's priority order, trust boundaries, prompt-injection
handling, data-exfiltration protections, non-overridable safety rules, and
accuracy behavior.

If you customize the prompt, the safest approach is to modify the assistant
name, personalization, guide style, or local-runtime preferences while leaving
the trust and security model intact.

---

## Version History

- **v2.82 (2026-08-23) — Safety-first final**
  Final hardening to make Gus behave the same across LM Studio / Ollama / Open WebUI.
  Blocks fake "system" instructions from web pages, PDFs, and tool output, stops it from saving future actions, checks for data exfiltration, and asks for confirmation before deleting files or doing anything destructive.

- **v2.8 (2026-08-22) — Token efficiency**
  Made the system prompt much shorter and more cache-friendly.
  Small models on Apple Silicon / low VRAM were wasting KV cache and slow to start (prefill). Now the core prompt is stable and reuses cache, so TTFT is faster and you can run bigger context.

- **v2.4 - v2.3 (2026-08-21) — Original fix: infinite web-search loop**
  Small models (like Qwen 0.5B-8B, 270M models) tend to call `web_search` over and over and never answer.
  Fixed with bounded iteration (max 5 tool rounds), single-shot tool loop, and hallucinated-tool detection.
  Also added the safe personalization Easter egg (`爱爱`) that only works on your real typed text, not on web pages.

- **v2.2 (2026-08-21) — First public release**
  First generic version that works on Windows, Linux, and Apple Silicon M1 Max.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

Created for our YouTube community and released for everyone to use.

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
