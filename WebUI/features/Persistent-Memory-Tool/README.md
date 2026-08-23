# Persistent Memory — Local JSONL

> Lightweight persistent memory for Open WebUI using a local JSONL file.

**Version:** 2.0  
**License:** MIT  
**Author:** Rolan & Doris Tech

---

## What It Does

`Persistent_Memory_Local_JSONL.py` gives your Open WebUI assistant simple persistent memory.

It can:

- Save user facts, preferences, decisions, and project details
- Search previously saved memories
- List recently saved memories
- Prevent exact duplicate memories
- Survive Open WebUI restarts

Memory is stored locally in a simple JSONL file.

No database, embeddings, or external service is required.

---

## Installation

1. In Open WebUI, create a new **Tool**.
2. Name it:

   `Persistent Memory`

3. Paste in the complete contents of:

   `Persistent_Memory_Local_JSONL.py`

4. Enable the tool.

---

## Memory File Location

The default location is:

```text
/app/backend/data/persistent-memory/memory.jsonl
```

You can change this through the tool's **Valves**.

Each memory is stored as a separate JSON line containing:

- Unique ID
- Memory content
- Category path
- Timestamp

Example:

```text
hardware/M1Max
project/MyProject
preferences/response-style
```

---

## How It Works

### Saving Memory

The assistant should use `update_memory` only when the user explicitly asks it to remember, save, store, or retain information.

Example:

```text
Remember that my server has an M1 Max with 64GB of unified memory.
```

### Searching Memory

`search_memory` uses lightweight keyword matching.

It is useful when previous user-specific information would materially improve the answer.

Example searches:

```text
M1 Max
project name
response preferences
```

This is keyword retrieval, not semantic or vector search.

### Viewing Stored Memory

`list_recent_memories` returns the most recently saved memories.

This is useful when the user asks what the assistant currently remembers.

---

## Important Settings

### `memory_file`

Location of the JSONL memory file.

### `max_results`

Maximum number of search results returned.

Default:

```text
5
```

### `max_memory_length`

Maximum length of a single memory.

Default:

```text
2000 characters
```

### `enable_duplicate_check`

Prevents exact duplicate memories.

Default:

```text
True
```

---

## Notes

- Memory survives Open WebUI restarts.
- Memory is stored locally.
- No embeddings are required.
- Keyword matching is lightweight and fast.
- For larger memory systems or semantic retrieval, a vector database may be more appropriate.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

If this helps you, please consider subscribing to our YouTube channel and starring the repository.
