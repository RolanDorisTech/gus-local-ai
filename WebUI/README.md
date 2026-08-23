# Gus — Open WebUI Features

> Small, practical tools and filters for local Open WebUI setups.

**Author:** Rolan & Doris Tech  
**License:** MIT

---

## What's Here

```text
WebUI/
└── features/
    ├── gus-context-manager/
    ├── persistent-memory/
    └── token-usage-display/
```

Each folder contains the feature's Python file and its own README.

### Token Usage Display

Displays usage information for each response.

- Prompt and response tokens
- Word counts
- Generation speed
- Response time
- Cumulative chat totals

### Persistent Memory — Local JSONL

Simple local memory that survives restarts.

- Save facts, preferences, and project details
- Search stored memories
- List recent memories
- No database or embeddings required

### Gus Context Manager

Low-memory context management for long conversations.

- Background context compaction
- Selective file retrieval
- File follow-up support
- Prompt-injection filtering for suspicious retrieved content
- Local helper-model support

---

## Installation

The features are independent. You do **not** need all three.

Open the folder for the feature you want and follow its README.

In Open WebUI:

- **Filters:** Gus Context Manager, Token Usage Display
- **Tools:** Persistent Memory — Local JSONL

Exact menu locations may vary by Open WebUI version.

---

## Designed for Local AI

These were built primarily for our own local setup using combinations of:

- Apple Silicon
- Open WebUI
- LM Studio
- Ollama
- MLX
- OpenAI-compatible local servers

Other compatible local setups may work as well.

---

## A Small Note About Personalization

These tools were originally built for personal use before being released publicly.

We cleaned them up, but you may still find occasional:

- Personal names or references
- Hardware or model preferences
- Local paths
- Chinese examples or language patterns

Don't worry if you find something like that.

You can **delete it, change it, leave it alone, or tell us about it**.

Some Chinese language patterns are intentional and simply help recognize common file or follow-up references. They do not change the assistant's language or affect normal English use.

---

## Before You Use Them

Check the feature-specific README for how to use. If you have additional questions, feel free to reach out. 
  

We recommend testing each feature before using it in an important workflow.

---

## Feedback

These tools are still evolving.

If you find a bug, compatibility issue, leftover personalization, or have an improvement idea, let us know.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

Built for our local AI project and released for the community.

If these tools help you, please consider subscribing to our YouTube channel and starring the repository.
