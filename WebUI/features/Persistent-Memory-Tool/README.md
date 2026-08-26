# Persistent Memory — Local JSONL

> Fast, private, recoverable memory for Open WebUI. Local JSONL only — no database, embeddings, or cloud services.

**Version:** 3.1.00
**License:** MIT
**Author:** Rolan & Doris Tech

---

## Quick Start

### 1. Disable Open WebUI Memory

Go to:

**Admin → System → General → Memories**

Turn **Memories OFF**.

This tool should be your **only persistent-memory system**. Using both systems can duplicate memory and add unnecessary context/token overhead.

### 2. Install the Tool

Go to:

**Admin Panel → Tools → Create Tool**

Paste the entire `Persistent_Memory_Local_JSONL.py`, save it, and enable it for your models.

### 3. Install the Viewer Action

Enable the separate **View Persistent Memory** Action.

After an assistant response, hover over the response and use the Action in the message toolbar to see your active memories in a table.

---

## What It Does

* **Save** durable information with `update_memory`
* **Recall** relevant information with `search_memory`
* **Update** memories with `replace_memory`
* **Delete** safely with `delete_memory`
* **Restore** deleted memories with `restore_memory`

Normal chats do **not** load the entire memory file.

---

## Why Use This Instead of Open WebUI Memory?

This tool is designed for:

* **No automatic memory injection**
* **Lower token usage**
* **Local-only storage**
* **Keyword + tag retrieval**
* **No embeddings or vector database**
* **Recoverable deletion**
* **Version history**
* **Simple JSONL files and backups**

---

## How to Use

### Save: `update_memory`

Only save when the user explicitly says to remember, save, store, or keep something.

Keep memories short and specific.

Example:

> Remember that my server has an M1 Max with 64GB RAM.

Use a few useful tags such as:

`hardware,m1max,local-ai`

### Recall: `search_memory`

Search only when previous user-specific information would materially improve the answer.

Examples:

> What Mac are we using?

> What did we decide for the Gus compactor?

Use tags when useful:

`hardware`

`project,gus`

`preferences`

Do **not** search for greetings, generic questions, or information already in the current chat.

### Update: `replace_memory`

Use when the user explicitly asks to change or correct an existing memory.

The old version is automatically saved to:

`memory_history.jsonl`

### Delete: `delete_memory`

Use only when the user explicitly asks to delete or forget something.

The memory is removed from active memory and moved to:

`memory_deleted.jsonl`

It is **not permanently destroyed**.

### Restore: `restore_memory`

Use when the user asks to restore a deleted memory.

---

## Memory Files

```text
qwen-memory/
├── memory.jsonl          Active memories
├── memory_history.jsonl  Previous versions
└── memory_deleted.jsonl  Recoverable deleted memories
```

Only `memory.jsonl` is searched during normal retrieval.

Default location:

`/Volumes/RocketQQ/open-webui-data/qwen-memory/memory.jsonl`

Docker fallback:

`/app/backend/data/qwen-memory/memory.jsonl`

Your hourly backup system provides an additional recovery layer.

---

## Memory Tips

Keep memories:

* Short
* Specific
* One fact or decision per entry
* Tagged with a few useful keywords

Example:

```text
Path: project/Gus
Tags: project,gus,compactor
Memory: Gus uses Qwen3.5-4B as the dedicated context compactor.
```

Do not store code, READMEs, transcripts, drafts, or temporary task context.

---

## Settings (Valves)

**`memory_file`** — active memory location
**`fallback_file`** — Docker fallback location
**`max_results`** — search results, default `5`
**`max_memory_length`** — memory size, default `2000` characters
**`max_tags`** — tags per memory, default `6`
**`enable_duplicate_check`** — prevents exact duplicates, default `True`

---

## License

MIT — free to use, modify, and share with attribution.

## Credits

**Rolan & Doris Tech**
If this helps you, please subscribe to our YouTube channel and star the repo.
