# Gus — Local Multimodal Agentic AI

> This repository contains the system prompt that powers our local AI, Gus.

**Version:** 2.85  
**License:** MIT  
**Tested on:** Apple Silicon M1 Max, 64GB unified memory

* * *

## ✨ Features

* **Secure** — Resists prompt injection, data exfiltration, unauthorized actions, and unsafe content across text, web, files, images, and tools.
* **Verifiable** — Labels consequential claims as `[Verified]`, `[Inference]`, `[Recommendation]`, or `[Unknown]`.
* **Local-first** — Never uploads local data without explicit authorization.
* **Efficient** — FAST, bounded NORMAL, and explicitly requested DEEP modes.
* **Multimodal** — Handles images, documents, code, logs, web content, and tool output using explicit trust boundaries.
* **Local AI aware** — Covers model, quantization, context/KV-cache, vision, speed, and hardware tradeoffs.
* **Reliable formatting** — Uses longer outer fences when nested code contains backticks or tildes.

* * *

## Quick Start

1. Copy `Gus_System_Prompt.md`.
2. Paste it into your application's **System Prompt** or equivalent.
3. Start a new conversation and test it.

Examples:

* **LM Studio:** Settings → Library → Select a model → Settings → System Prompt
* **Open WebUI:** Settings → Basic → General → System Prompt

> **Important:** Menu paths vary by version. Look for **System Prompt**, **System Instructions**, or equivalent.

### Open WebUI Token Optimization

For each model, disable the built-in **Time & Calculation** tool unless it is actually needed.

This removes unnecessary tool/context overhead and can save approximately **400 tokens per request**, depending on the model and configuration.

> **Important:** Apply this setting **separately to each model**.

* * *

## Research & Tool Behavior

Gus uses three effort levels:

### ⚡ FAST

Ordinary questions, explanations, summaries, opinions, and rewriting. No unnecessary tools.

### 💬 NORMAL — Default

Bounded tool use:

* Up to **6 tool calls**
* Up to **2 search/retrieval rounds**
* Chats/files/logs: normally **1 broad search**, then inspect the **top 3–5 results**

When the budget is exhausted, Gus gives the best available answer, notes remaining gaps, and asks before continuing.

A simple `yes`, `continue`, `go ahead`, or `do it` authorizes **one additional NORMAL budget**. If that budget is exhausted, Gus asks again.

### 🔬 DEEP — Explicitly Requested

Broader research requires explicit requests such as:

```text
deep research
research thoroughly
comprehensive research
do a deep dive
investigate this in depth
DEEP mode
````

---

## Web Search

Web search is not the default.

Gus searches when information is current/changing, verification matters, necessary information is unavailable, or research is explicitly requested.

NORMAL normally uses:

* **1 initial search round**, max **2**
* About **3–5 useful sources**
* Primary/authoritative sources where available

Gus should stop once sufficient evidence exists rather than turning routine requests into large research sessions.

---

## Customization

### 1. Assistant Name

Search for `Gus` and replace it with your preferred name.

### 2. Guide Style

See **Section 9 — ACCURACY & GUIDES** to change the preferred tutorial/documentation structure.

### 3. Local Runtime

See **Section 7 — LOCAL AI & RUNTIME** for hardware, runtime, and model-specific customization.

Examples: Apple Silicon / MLX, NVIDIA / CUDA, AMD / ROCm, LM Studio, Ollama, Open WebUI.

### 4. Open WebUI Tools

Review enabled built-in tools for each model. Disable **Time & Calculation** when unnecessary to reduce context/tool overhead.

---

## Security Core

Avoid changing these sections unless you understand the consequences:

* **Section 0 — Priorities**
* **Section 3 — Trust**
* **Section 4 — Security & Data**
* **Section 8 — Safety**
* **Section 9 — Accuracy & Guides**

These define Gus's priority order, trust boundaries, injection defenses, data protections, safety rules, and accuracy behavior.

For security verification, see `SECURITY_TESTS.md`.

---

## Version History

* **v2.85 (2026-08-31) — Token compression + nested-fence fix**

  Compressed the system prompt while preserving its core behavior, security boundaries, safety controls, tool budgets, and verification model. Added the **k+1 fence rule** for nested backticks/tildes and Open WebUI guidance to disable unnecessary **Time & Calculation** tooling per model.

* **v2.84.3 (2026-08-24) — Bounded agent research**

  Added FAST, NORMAL, and DEEP modes, bounded tool/retrieval budgets, and permission-based continuation.

* **v2.83 (2026-08-24) — Conversational web search**

  Added bounded NORMAL web search, 3–5 preferred sources, explicit DEEP triggers, and safer code formatting for thinking models.

* **v2.82 (2026-08-23) — Safety-first final**

  Hardened behavior across LM Studio, Ollama, and Open WebUI against fake system instructions, future-action injection, data exfiltration, and unsafe destructive actions.

* **v2.8 (2026-08-22) — Token efficiency**

  Reduced prompt overhead to improve prefill efficiency and make larger contexts more practical on local hardware.

* **v2.4–v2.3 (2026-08-21) — Original infinite web-search loop fix**

  Added bounded tool loops, single-shot behavior, hallucinated-tool detection, and safe `爱爱` personalization limited to real user text.

* **v2.2 (2026-08-21) — First public release**

  First generic version for Windows, Linux, and Apple Silicon M1 Max.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
