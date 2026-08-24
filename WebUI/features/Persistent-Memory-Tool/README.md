# Persistent Memory — Local JSONL

> Give your Open WebUI assistant memory that survives restarts. No database, no embeddings, no external services.

**Version:** 2.0  
**License:** MIT  
**Author:** Rolan & Doris Tech

---

## What It Does

By default, Open WebUI forgets everything when a chat ends.

This tool fixes that. It lets your assistant remember facts across chats by saving them to a local `memory.jsonl` file.

It can:
- **Remember** facts you tell it to remember
- **Recall** them later when relevant
- **List** what it currently remembers

## How to Use

This tool has 3 functions. Here's exactly when to use each one.

### 1. To SAVE something: `update_memory`

**When:** Only when the user explicitly says to remember, save, store, or keep something.

Don't auto-save everything. Wait for a direct instruction.

**You say:**
> Remember that my server has an M1 Max with 64GB RAM.

**Assistant does:**
> Calls `update_memory(content="My server has an M1 Max with 64GB RAM", category="hardware/server")`

**More examples of what triggers a save:**
- "Save this: I prefer short, direct answers"
- "Store my project name as HomeLab NAS"
- "Remember I'm working on a YouTube channel called Rolan & Doris Tech"

**Categories:** Keep them simple and organized. Use format `type/detail`
- `personal/name`
- `hardware/M1Max`
- `project/MyProject`
- `preferences/response-style`

### 2. To RECALL something: `search_memory`

**When:** When answering would be better if you knew past information about the user.

This is keyword search, not AI search. Use specific keywords.

**You say:**
> What server do I have?

**Assistant does:**
> Calls `search_memory(query="M1 Max server hardware")` -> finds the saved memory and uses it in the answer.

**More examples:**
- You ask "What is my preferred response style?" -> searches `response preferences`
- You ask "What project am I working on?" -> searches `project name`

### 3. To CHECK what is saved: `list_recent_memories`

**When:** When the user asks what you remember.

**You say:**
> What do you remember about me?

**Assistant does:**
> Calls `list_recent_memories()` and shows the last few saved memories.

---

## Installation

1. In Open WebUI, go to Settings -> Admin -> System -> General -> make sure "Memory" is turned on
2. Settings -> Personal -> Preferences -> Personalization -> turn on "Memory (Experimental)"
3. In Open WebUI, go to **Admin Panel > Tools**
4. Click **Create Tool**
5. Name it: `Persistent Memory`
6. Paste the entire contents of `Persistent_Memory_Local_JSONL.py` into the code box
7. Click **Save** and enable the tool

## Where Memory is Stored

Default file path:

/app/backend/data/persistent-memory/memory.jsonl

You can change this in **Tool Valves**.

Each line in the file is one memory with an ID, content, category, and timestamp. Example:

{"id": "abc123", "content": "My server has an M1 Max with 64GB RAM", "category": "hardware/server", "timestamp": "2026-08-24T10:00:00Z"}

This file survives restarts. No database needed.

## Settings (Valves)

You can adjust these in the tool settings:

**`memory_file`**
Where the JSONL file is saved.

**`max_results`**
How many results search returns. Default: `5`

**`max_memory_length`**
Max characters per memory. Default: `2000`

**`enable_duplicate_check`**
If `True`, it won't save the exact same memory twice. Default: `True`

## Notes

- Local only. Your memories stay on your server.
- Fast and lightweight. Uses keyword matching.
- If you need semantic/vector search for thousands of memories, use a vector database instead. This is designed to be simple.

## License

MIT — free to use, modify, and share with attribution.

## Credits

**Rolan & Doris Tech**
If this helps you, please subscribe to our YouTube channel and star the repo.
