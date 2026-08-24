# Gus — Local Multimodal Agentic AI

> This repository contains the system prompt that powers our local AI, Gus.

**Version:** 2.84.3  
**License:** MIT  
**Tested on:** Apple Silicon M1 Max, 64GB unified memory

* * *

## ✨ Features

When used with the Gus system prompt:

* **Secure** — Detects and neutralizes prompt injection from web pages, PDFs, documents, images, tool output, and other untrusted data.

* **Verifiable** — Uses `[Verified]`, `[Inference]`, `[Recommendation]`, and `[Unknown]` labels for consequential claims to distinguish evidence, reasoning, recommendations, and uncertainty.

* **Local-first** — Never uploads local files or data without explicit authorization.

* **Responsive formatting** — Uses tables only for compact comparisons; otherwise prefers concise bullets and readable text.

* **Tool-aware** — Handles web search, recent chats, files, vision, documents, code, and tool results with explicit trust boundaries and tool-use discipline.

* **Efficient** — Uses FAST, NORMAL, and DEEP modes to prevent routine requests from turning into long autonomous research sessions.

* **User-controlled research** — NORMAL mode has bounded tool and retrieval budgets. If more work is needed, Gus stops, shows the best answer so far, and asks before continuing.

* **Deep Research on demand** — Broader research is available only when explicitly requested.

* **Safety-first** — Protects against data exfiltration, unsafe destructive actions, unauthorized access, malware deployment, fraud, and other non-overridable unsafe content.

* **Technical** — Concise, direct, highly technical, and structured by default.

* **Multimodal** — Handles images, documents, logs, code, web content, and other untrusted multimodal input without treating embedded content as instructions.

* **Local AI aware** — Designed for reasoning about local models, quantization, context/KV-cache cost, vision tokens, prefill speed, Apple Silicon unified memory, and other runtime tradeoffs.

* * *

## Quick Start

1. Copy the contents of `Gus_System_Prompt.md`.

2. Paste it into your local AI application's **System Prompt** or equivalent instruction field.

3. Start a new conversation and test it with your model.

Examples:

* **LM Studio:** Settings → Library → Select a model → Settings → System Prompt

* **Open WebUI:** Settings → Basic → General → System Prompt

> **Important:** Exact menu paths vary by application version. Look for **System Prompt**, **System Instructions**, or an equivalent field.

* * *

## Research and Tool Behavior

Gus uses three levels of effort.

### ⚡ FAST

For ordinary questions, explanations, summaries, opinions, and rewriting.

Gus answers directly and avoids unnecessary tools.

### 💬 NORMAL — Default Tool Mode

When tools are needed, Gus uses a limited budget to keep responses responsive.

Gus normally:

* Retrieves broadly once
* Identifies the most relevant results
* Inspects only the strongest candidates
* Synthesizes and answers

Default budget:

* Up to **6 tool calls**
* Up to **2 search or retrieval rounds**
* For chats, files, or logs: normally **1 broad search**, then inspect the **top 3–5 relevant results**

If more work is needed, Gus should stop at the budget limit, provide the best answer from what it has found, clearly note what remains incomplete, and ask before continuing.

A simple reply such as:

```text
yes
continue
go ahead
do it
```

authorizes **one additional NORMAL budget** for that task.

If that budget is also exhausted, Gus stops and asks again.

### 🔬 DEEP — Explicitly Requested

DEEP mode allows broader and more extensive research.

Use phrases such as:

```text
deep research
research thoroughly
comprehensive research
do a deep dive
investigate this in depth
DEEP mode
```

You can also explicitly choose DEEP mode when Gus asks whether you want to continue.

> **Tip:** NORMAL keeps research bounded and responsive. DEEP is for tasks where you intentionally want broader investigation.

* * *

## Web Search Behavior

Web search is not the default workflow.

Gus searches when:

* Information is current or changing
* Verification materially matters
* Necessary information is unavailable
* The user explicitly requests research

In NORMAL mode, Gus normally:

* Starts with **1 search round**
* Uses at most **2 search rounds**
* Prefers about **3–5 useful sources**
* Prefers primary and authoritative sources
* Stops once enough evidence exists
* Avoids repetitive searches and unnecessary page fetching

Gus should **not** turn an ordinary question into a large research project.

DEEP mode allows broader searches and additional verification when explicitly requested.

* * *

## Customization Guide

Gus works out of the box, but you can customize it.

### 1. Assistant Name

Search for:

```text
Gus
```

Replace it with the name of your AI assistant.

### 2. Guide Style

See:

```text
ACCURACY & GUIDES
```

in **Section 9**.

You can change the recommended structure for tutorials and documentation, or remove this section if it does not fit your workflow.

### 3. Local Runtime Context

See:

```text
LOCAL AI & RUNTIME
```

in **Section 7**.

This section is intentionally generic and does not need to be changed for most users. You can customize it if your environment has specific hardware, runtime, or model constraints.

Examples:

* Apple Silicon / MLX
* NVIDIA CUDA / VRAM
* AMD / ROCm
* LM Studio
* Ollama
* Open WebUI
* Other local inference runtimes

* * *

## Security Core

For the intended security and trust behavior, avoid changing these sections unless you understand the consequences:

* **Section 0 — Priorities**
* **Section 3 — Trust**
* **Section 4 — Security & Data**
* **Section 8 — Safety**
* **Section 9 — Accuracy & Guides**

These sections define Gus's priority order, trust boundaries, prompt-injection handling, data-exfiltration protections, non-overridable safety rules, and accuracy behavior.

If you customize the prompt, the safest approach is to modify the assistant name, guide style, or local-runtime preferences while leaving the trust and security model intact.

Refer to `SECURITY_TESTS.md` for important safety verification.

* * *

## Version History

* **v2.84.3 (2026-08-24) — Bounded agent research**

  Added FAST, NORMAL, and DEEP work modes to improve responsiveness and prevent long autonomous research loops. NORMAL mode now uses bounded tool and retrieval budgets. If more work is needed, Gus stops, provides the best answer so far, and asks for permission before continuing. A simple confirmation grants one additional NORMAL budget; DEEP mode requires explicit selection.

* **v2.83 (2026-08-24) — Conversational web search**

  Added bounded normal web-search behavior to prevent routine questions from triggering large research loops. Normal mode uses at most 2 search rounds and prefers 3–5 useful sources. Added explicit Deep Research triggers for broader research. Included coding instructions for thinking models to prevent code block breakup when encountering reasoning tags.

* **v2.82 (2026-08-23) — Safety-first final**

  Final hardening to make Gus behave consistently across LM Studio, Ollama, and Open WebUI. Blocks fake "system" instructions from web pages, PDFs, and tool output; prevents untrusted content from creating future actions; checks for data exfiltration; and requires confirmation before destructive actions.

* **v2.8 (2026-08-22) — Token efficiency**

  Made the system prompt shorter and more cache-friendly. Reduced unnecessary prompt overhead to improve prefill performance and make larger context windows more practical on local hardware.

* **v2.4–v2.3 (2026-08-21) — Original infinite web-search loop fix**

  Small models could repeatedly call `web_search` without answering. Added bounded iteration, single-shot tool-loop behavior, and hallucinated-tool detection. Also added the safe personalization Easter egg (`爱爱`) that only works on real typed user text, not untrusted content.

* **v2.2 (2026-08-21) — First public release**

  First generic version designed to work across Windows, Linux, and Apple Silicon M1 Max.

* * *

## License

MIT — free to use, modify, and share with attribution.

* * *

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
