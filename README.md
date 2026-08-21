# Gus — Local Multimodal Agentic AI

> Gus is our local AI assistant that runs 100% locally. This repo contains the system prompt that powers Gus.
> Works on Apple Silicon, Windows, Linux - via LM Studio + Ollama + Open WebUI

Tested on Apple Silicon M1 Max 64GB | Version: 2.3 | License: MIT

Built by Rolan & Doris Tech for our YouTube community - free for everyone to use.

---

### What is Gus?

Gus is our local multimodal AI assistant - a name for our assistant that runs 100% locally on our machine.

This repo shares the system prompt we use to run Gus - so you can run your own locally and SAFELY too.

### ✨ Features of Gus (when using this prompt): 
- Secure - detects and neutralizes prompt injection from web, PDFs, images
- Verifiable - forces [Verified] / [Inference] / [Unknown] labeling, no hallucinations
- Local-first - never uploads your files without explicit permission
- Tool-aware - transparent search, vision, and code handling
- Technical - concise, direct and methodical

### Quick Start

1. Download Gus_System_Prompt_v2.3.md (the prompt for Gus)
2. Open LM Studio or Open WebUI -> Settings -> Personal -> Basics -> General -> System Prompt -> Paste

### Customization Guide

You don't need to change anything - it works out of the box as Gus. If you want to make it yours, search for these keywords:

1. Your Names (for injection defense):
Search: Rolan & Doris (4 references total)
Replace with your name

2. Name of AI Assistant:
Search: Gus
Change to the name of your AI assistant

3. Hardware Context:
Search: M1 Max
Update for your hardware: M1 Max, RTX 4090, how much VRAM, etc.

4. Guide Style:
See: TECHNICAL STANDARDS (Section 11)
Change structure for your tutorials or docs or remove entirely if not applicable.

5. Date Token:
Search: {{CURRENT_DATE}} - leave as-is if your platform auto-fills, or replace with static date like 2026-08-21

6. Personalization (NEW in v2.3):
Search: Private personalization - Easter egg: if you say "love you" it replies "love you too!" - Keep, change to your own phrase, or delete it. It's HIGH_TRUST only, so web/PDFs can't trigger it.

Tip: Keep Section 0, 2, 3, 9 (Mission, Trust, Security, Safety) as-is - those are the security core of Gus.

### Version History

- v2.3 (2026-08-21) - Public-safe personalization + hardened trust hierarchy + exfil/auto-render guardrail + multi-turn fix
- v2.2 (2026-08-21) - First generic public release, Windows/Linux friendly, clarified priority logic

### License

MIT - Free to use, modify, and share with attribution.

### Credits

Rolan & Doris Tech - YouTube

Star this repo if Gus helps you!
