# Token Usage Display — LM Studio Accurate Bionic Persistent

> A lightweight Open WebUI Filter that displays per-response and cumulative token usage, word counts, elapsed time, and generation speed.

**Version:** 2.3
**License:** MIT
**Designed for:** Open WebUI + LM Studio
**Built by:** Rolan & Doris Tech

Built for our YouTube community — free for everyone to use.

---

## ✨ Features

* **Real LM Studio usage** — Uses token usage returned by the inference backend when available.
* **Streaming usage support** — Requests `stream_options.include_usage` and captures usage from the stream when provided.
* **Fallback estimation** — Estimates token counts when the backend does not return usage data.
* **Persistent cumulative totals** — Tracks cumulative prompt tokens, reply tokens, and words for each chat during the running Open WebUI process.
* **Compaction-friendly** — The cumulative `Σ` totals are stored independently of the visible chat history, so normal chat compaction does not reset them while the Filter process remains running.
* **Mobile-first layout** — Cumulative `Σ` statistics are displayed before the current-turn statistics.
* **Generation speed** — Displays approximate generation speed in tokens per second.
* **Word counts** — Shows prompt and response word counts alongside token counts.
* **Duplicate protection** — Attempts to avoid counting the same completed assistant turn twice.
* **Reasoning-aware** — Includes assistant reasoning/thinking content when available for fallback text-based estimation.

---

## Quick Start

1. Open `Token_Usage_Display.py`.
2. Copy the **entire file**.
3. Open **Open WebUI**.
4. Go to **Workspace -> Functions** or **Workspace -> Filters** depending on your Open WebUI version.
5. Create a new Filter.
6. Paste the entire Python code.
7. Save the Filter.
8. Enable the Filter for your model or conversation.

> **Important:** Exact Open WebUI menu paths may vary by version.

The code should be copied exactly, including the header at the top of the file.

---

## What It Displays

After a response completes, the Filter displays a status line similar to:

```text
📈 ΣP12.4k(9,540w) ΣR3.1k(2,380w) Σ15.5k(11,920w) | 📊 P1,250(960w) R420(320w) 4.8s 87.5t/s
```

### Cumulative Statistics

The first section begins with:

```text
📈
```

and displays cumulative totals for the current chat:

```text
ΣP
```

Cumulative prompt tokens.

```text
ΣR
```

Cumulative reply tokens.

```text
Σ
```

Combined cumulative token total.

Word counts are displayed in parentheses.

Example:

```text
ΣP12.4k(9,540w)
```

means approximately:

* 12,400 cumulative prompt tokens
* 9,540 cumulative prompt words

---

### Current-Turn Statistics

The second section begins with:

```text
📊
```

and displays statistics for the most recent completed response.

```text
P
```

Current prompt token count.

```text
R
```

Current response token count.

The Filter also displays:

```text
4.8s
```

Approximate total elapsed time for the request.

And:

```text
87.5t/s
```

Approximate generation speed in tokens per second.

---

## Example

A completed turn may display:

```text
📈 ΣP8.2k(6,300w) ΣR2.4k(1,850w) Σ10.6k(8,150w) | 📊 P1,120(850w) R310(240w) 3.6s 86.1t/s
```

This means:

### Cumulative

* Prompt tokens: approximately 8,200
* Prompt words: 6,300
* Response tokens: approximately 2,400
* Response words: 1,850
* Total tokens: approximately 10,600
* Total words: 8,150

### Current Turn

* Prompt tokens: approximately 1,120
* Prompt words: 850
* Response tokens: approximately 310
* Response words: 240
* Total elapsed time: 3.6 seconds
* Generation speed: approximately 86.1 tokens per second

---

## LM Studio Usage Accuracy

When LM Studio returns usage information, the Filter uses the backend-provided values for:

* `prompt_tokens`
* `completion_tokens`
* `total_tokens`

The Filter first checks usage captured from the streaming response.

If streaming usage is unavailable, it checks the completed assistant message.

This makes the Filter more accurate than estimating all token counts directly from text.

---

## Token Estimation Fallback

Some backends or configurations may not return token usage information.

When real usage data is unavailable, the Filter estimates tokens from text using:

```text
Estimated tokens = token-like units × 1.3
```

This is an approximation.

Different model tokenizers can produce different token counts for the same text.

Therefore:

> Backend-reported token usage should be considered more accurate than the Filter's fallback estimate.

---

## Word Counting

Word counts are calculated separately from token counts.

The Filter uses a Unicode-aware regular expression to count word-like sequences.

Word counts are useful for quickly comparing the visible amount of text with the number of model tokens used.

However, words and tokens are not equivalent.

A single word may contain:

* One token
* Multiple tokens
* Less than one token on average across a larger text sample

The exact relationship depends on the tokenizer and language.

---

## Reasoning and Thinking Models

Some models expose hidden or separate reasoning content through fields such as:

* `reasoning`
* `thinking`
* `reasoning_content`

The Filter detects reasoning or thinking content when available.

This is primarily used for fallback text extraction and token estimation when backend usage statistics are unavailable.

If the backend provides real token usage statistics, those values are preferred.

---

## Persistent Σ Totals

The cumulative totals are stored in the Filter's Python process using an in-memory dictionary.

Totals are organized by chat ID.

This means normal conversation compaction does not automatically reset the cumulative totals, because the totals are not calculated solely from the currently visible chat history.

### Important

The cumulative totals are persistent only for the lifetime of the running Open WebUI Python process.

They may reset when:

* Open WebUI is restarted
* The Open WebUI backend process restarts
* The Filter is reloaded
* The server is redeployed
* The Python process is replaced

They are not currently written to disk.

---

## Duplicate Protection

The Filter creates a turn key for each completed assistant response.

When a turn has already been counted for a chat, it is not added to the cumulative totals again.

This helps prevent duplicate counting if the Filter lifecycle causes the same completed turn to be processed more than once.

When an assistant message ID is available, it is used as part of the turn key.

If no message ID is available, the Filter falls back to a hash based on the chat, timing, token counts, and reply text.

---

## Generation Speed

Generation speed is calculated approximately as:

```text
completion tokens / generation elapsed time
```

The Filter attempts to detect the time at which the first output token arrives.

Generation elapsed time is then measured from first output until completion.

This is intended to better represent generation speed than dividing output tokens by the entire request duration.

If first-output timing is unavailable, the Filter falls back to the total elapsed request time.

Actual performance can vary depending on:

* Model
* Quantization
* Hardware
* Context size
* Prompt prefill time
* KV cache state
* Batch settings
* Streaming behavior
* Backend implementation

---

## Priority

The default Filter priority is:

```text
20
```

This can be changed through the Filter valves if your Open WebUI setup requires a different execution order.

---

## Requirements

The Filter requires:

* Open WebUI with Python Filter support
* Python
* Pydantic

It is designed to work with LM Studio-compatible API responses and can also fall back to estimation when usage fields are unavailable.

---

## Supported Usage Fields

The Filter looks for common usage field names including:

```text
prompt_tokens
```

```text
input_tokens
```

```text
completion_tokens
```

```text
output_tokens
```

```text
total_tokens
```

This improves compatibility with different OpenAI-compatible backends.

---

## Limitations

### Cumulative Totals Are In-Memory

The `Σ` totals are not written to disk.

They survive normal chat compaction while the Filter process remains running, but they reset when the relevant Python process restarts.

### Fallback Token Counts Are Estimates

If the backend does not provide usage information, token counts are estimated.

These estimates will not exactly match every model tokenizer.

### Generation Speed Is Approximate

The displayed tokens-per-second value depends on the timing information available from the stream.

It should be considered an approximate generation speed measurement.

### Long-Running Servers

The Filter stores turn identifiers in memory to avoid duplicate counting.

On a very long-running server with a very large number of chats and responses, the in-memory cumulative tracking data can grow over time.

For typical personal or local Open WebUI use, this is generally small.

---

## Best Use Cases

This Filter is especially useful for:

* Monitoring local model token usage
* Comparing models
* Comparing quantizations
* Measuring generation speed
* Tracking long conversations
* Monitoring context growth
* Testing chat compaction
* Comparing prompt efficiency
* Measuring local AI performance
* LM Studio and Open WebUI benchmarking

---

## Version History

* **v2.3 — LM Studio Accurate Bionic Persistent**
  Added real LM Studio usage support, streaming usage capture, persistent cumulative totals across chat compaction, duplicate protection, mobile-first cumulative display, and improved fallback estimation.

---

## License

MIT — free to use, modify, and share with attribution.

---

## Credits

**Rolan & Doris Tech**

Created for our YouTube community and released for everyone to use.

If this Filter helps your local AI setup, consider subscribing to our YouTube channel and starring the repository.
