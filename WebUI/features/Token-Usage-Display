"""
title: Token Usage Display - LM Studio Accurate Bionic Persistent
author: Rolan & Doris Tech
version: 2.3
description: Real LM Studio usage + persistent Σ that survives chat compaction. Σ first for mobile portrait view. 
"""

from pydantic import BaseModel, Field
import re
import time
import threading
from typing import Optional, Any, Dict, Set, Tuple


WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)

CUMULATIVE: Dict[str, Dict[str, Any]] = {}
LOCK = threading.Lock()


class Filter:
    class Valves(BaseModel):
        priority: int = Field(default=20)

    def __init__(self):
        self.valves = self.Valves()

    @staticmethod
    def extract_text(content: Any) -> str:
        if not content:
            return ""

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []

            for part in content:
                if not isinstance(part, dict):
                    continue

                if part.get("type") != "text":
                    continue

                text = part.get("text", "")

                if isinstance(text, str):
                    parts.append(text)

            return "".join(parts)

        return str(content)

    @staticmethod
    def count_words(text: str) -> int:
        if not text:
            return 0

        return len(WORD_RE.findall(text))

    @staticmethod
    def estimate_tokens(text: str) -> int:
        if not text:
            return 0

        count = len(TOKEN_RE.findall(text))

        return max(0, int(round(count * 1.3)))

    @staticmethod
    def assistant_text(
        message: Optional[dict],
    ) -> str:
        if not isinstance(message, dict):
            return ""

        content = Filter.extract_text(
            message.get("content", "")
        )

        reasoning = (
            message.get("reasoning")
            or message.get("thinking")
            or ""
        )

        if isinstance(reasoning, dict):
            reasoning = ""

        reasoning = str(reasoning).strip()

        if reasoning:
            visible = THINK_RE.sub(
                "",
                content,
            ).strip()

            if visible:
                return (
                    visible
                    + "\n"
                    + reasoning
                ).strip()

            return reasoning

        return content.strip()

    @staticmethod
    def get_usage(
        message: Optional[dict],
    ) -> Optional[dict]:
        if not isinstance(message, dict):
            return None

        usage = message.get("usage")

        if isinstance(usage, dict):
            return usage

        info = message.get("info")

        if isinstance(info, dict):
            usage = info.get("usage")

            if isinstance(usage, dict):
                return usage

        return None

    @staticmethod
    def get_int(
        data: Optional[dict],
        *keys: str,
    ) -> Optional[int]:
        if not isinstance(data, dict):
            return None

        for key in keys:
            value = data.get(key)

            if value is None:
                continue

            try:
                return int(value)

            except (
                TypeError,
                ValueError,
            ):
                continue

        return None

    @staticmethod
    def get_stream_usage(
        event: Any,
    ) -> Optional[dict]:
        if isinstance(event, dict):
            usage = event.get("usage")

            if isinstance(usage, dict):
                return usage

            return None

        try:
            usage = getattr(
                event,
                "usage",
                None,
            )

            if isinstance(usage, dict):
                return usage

        except Exception:
            pass

        return None

    @staticmethod
    def has_output(event: Any) -> bool:
        if not isinstance(event, dict):
            return False

        choices = event.get("choices")

        if not isinstance(choices, list):
            return False

        for choice in choices:
            if not isinstance(choice, dict):
                continue

            delta = choice.get("delta")

            if not isinstance(delta, dict):
                continue

            if delta.get("content"):
                return True

            for key in (
                "reasoning",
                "thinking",
                "reasoning_content",
            ):
                if delta.get(key):
                    return True

        return False

    @staticmethod
    def make_turn_key(
        chat_id: str,
        assistant_msg: Optional[dict],
        start: Optional[float],
        prompt_tokens: int,
        completion_tokens: int,
        reply_text: str,
    ) -> str:
        if isinstance(assistant_msg, dict):
            message_id = (
                assistant_msg.get("id")
                or assistant_msg.get("message_id")
            )

            if message_id:
                return (
                    f"{chat_id}:msg:{message_id}"
                )

        return str(
            hash(
                (
                    chat_id,
                    start,
                    prompt_tokens,
                    completion_tokens,
                    reply_text,
                )
            )
        )

    async def inlet(
        self,
        body: dict,
        __metadata__: Optional[dict] = None,
        __user__: Optional[dict] = None,
    ) -> dict:
        if __metadata__ is not None:
            __metadata__["_token_start"] = (
                time.perf_counter()
            )

            __metadata__["_token_first"] = None
            __metadata__["_token_stream_usage"] = None

        if body.get("stream") is True:
            stream_options = body.get(
                "stream_options"
            )

            if not isinstance(
                stream_options,
                dict,
            ):
                stream_options = {}

            stream_options["include_usage"] = True

            body["stream_options"] = (
                stream_options
            )

        return body

    async def stream(
        self,
        event: Any,
        __metadata__: Optional[dict] = None,
        __user__: Optional[dict] = None,
        __event_emitter__=None,
    ) -> Any:
        if __metadata__ is None:
            return event

        if (
            __metadata__.get("_token_first")
            is None
            and self.has_output(event)
        ):
            __metadata__["_token_first"] = (
                time.perf_counter()
            )

        usage = self.get_stream_usage(event)

        if isinstance(usage, dict):
            __metadata__[
                "_token_stream_usage"
            ] = usage

        return event

    async def outlet(
        self,
        body: dict,
        __metadata__: Optional[dict] = None,
        __user__: Optional[dict] = None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> dict:
        try:
            messages = body.get(
                "messages",
                [],
            )

            if not isinstance(messages, list):
                messages = []

            metadata = body.get("metadata")

            if not isinstance(metadata, dict):
                metadata = {}

            chat_id = (
                body.get("chat_id")
                or metadata.get("chat_id")
                or metadata.get("conversation_id")
                or "default"
            )

            chat_id = str(chat_id)

            start = (
                __metadata__.get("_token_start")
                if __metadata__
                else None
            )

            first = (
                __metadata__.get("_token_first")
                if __metadata__
                else None
            )

            if start is not None:
                total_elapsed = max(
                    0.0,
                    time.perf_counter() - start,
                )
            else:
                total_elapsed = 0.0

            if first is not None:
                generation_elapsed = max(
                    0.0,
                    time.perf_counter() - first,
                )
            else:
                generation_elapsed = total_elapsed

            assistant_msg = None
            user_msg = None

            for message in reversed(messages):
                if not isinstance(message, dict):
                    continue

                role = message.get("role")

                if (
                    assistant_msg is None
                    and role == "assistant"
                ):
                    assistant_msg = message

                if (
                    user_msg is None
                    and role == "user"
                ):
                    user_msg = message

                if (
                    assistant_msg is not None
                    and user_msg is not None
                ):
                    break

            prompt_text = (
                self.extract_text(
                    user_msg.get("content", "")
                )
                if user_msg
                else ""
            )

            reply_text = (
                self.assistant_text(
                    assistant_msg
                )
                if assistant_msg
                else ""
            )

            prompt_words = self.count_words(
                prompt_text
            )

            reply_words = self.count_words(
                reply_text
            )

            usage = None

            if __metadata__:
                stream_usage = __metadata__.get(
                    "_token_stream_usage"
                )

                if isinstance(
                    stream_usage,
                    dict,
                ):
                    usage = stream_usage

            if usage is None:
                usage = self.get_usage(
                    assistant_msg
                )

            prompt_tokens = self.get_int(
                usage,
                "prompt_tokens",
                "input_tokens",
            )

            completion_tokens = self.get_int(
                usage,
                "completion_tokens",
                "output_tokens",
            )

            total_tokens = self.get_int(
                usage,
                "total_tokens",
            )

            if prompt_tokens is None:
                prompt_tokens = self.estimate_tokens(
                    prompt_text
                )

            if completion_tokens is None:
                completion_tokens = (
                    self.estimate_tokens(
                        reply_text
                    )
                )

            if total_tokens is None:
                total_tokens = (
                    prompt_tokens
                    + completion_tokens
                )

            if (
                generation_elapsed > 0
                and completion_tokens > 0
            ):
                tps = (
                    completion_tokens
                    / generation_elapsed
                )
            else:
                tps = 0.0

            turn_key = self.make_turn_key(
                chat_id=chat_id,
                assistant_msg=assistant_msg,
                start=start,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                reply_text=reply_text,
            )

            with LOCK:
                cum = CUMULATIVE.setdefault(
                    chat_id,
                    {
                        "p_tok": 0,
                        "r_tok": 0,
                        "p_w": 0,
                        "r_w": 0,
                        "seen": set(),
                    },
                )

                seen: Set[str] = cum["seen"]

                if turn_key not in seen:
                    cum["p_tok"] += (
                        prompt_tokens
                    )

                    cum["r_tok"] += (
                        completion_tokens
                    )

                    cum["p_w"] += (
                        prompt_words
                    )

                    cum["r_w"] += (
                        reply_words
                    )

                    seen.add(turn_key)

                cumulative_prompt_tokens = (
                    cum["p_tok"]
                )

                cumulative_reply_tokens = (
                    cum["r_tok"]
                )

                cumulative_prompt_words = (
                    cum["p_w"]
                )

                cumulative_reply_words = (
                    cum["r_w"]
                )

            def fmt(value: int) -> str:
                if value >= 1000:
                    return (
                        f"{value / 1000:.1f}k"
                    )

                return f"{value:,}"

            cumulative_tokens = (
                cumulative_prompt_tokens
                + cumulative_reply_tokens
            )

            cumulative_words = (
                cumulative_prompt_words
                + cumulative_reply_words
            )

            # Σ first for mobile.
            description = (
                f"📈 "
                f"ΣP{fmt(cumulative_prompt_tokens)}"
                f"({cumulative_prompt_words}w) "
                f"ΣR{fmt(cumulative_reply_tokens)}"
                f"({cumulative_reply_words}w) "
                f"Σ{fmt(cumulative_tokens)}"
                f"({cumulative_words}w) | "
                f"📊 "
                f"P{fmt(prompt_tokens)}"
                f"({prompt_words}w) "
                f"R{fmt(completion_tokens)}"
                f"({reply_words}w) "
                f"{total_elapsed:.1f}s "
                f"{tps:.1f}t/s"
            )

            if (
                isinstance(usage, dict)
                and not isinstance(
                    body.get("usage"),
                    dict,
                )
            ):
                body["usage"] = {
                    "prompt_tokens": (
                        prompt_tokens
                    ),
                    "completion_tokens": (
                        completion_tokens
                    ),
                    "total_tokens": (
                        total_tokens
                    ),
                }

            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": description,
                            "done": True,
                        },
                    }
                )

        except Exception as e:
            print(
                "Token Usage Display error: "
                f"{type(e).__name__}: {e}"
            )

        return body
