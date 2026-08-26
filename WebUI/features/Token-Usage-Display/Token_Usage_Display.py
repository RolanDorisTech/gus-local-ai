"""  
title: Token Usage Display - LM Studio Accurate Bionic Persistent  
author: Rolan & Doris Tech  
version: 2.4.06 TIME FORMAT FIX  
description: Time format: <60s => decimal seconds, >=60s => H:MM:SS.  
"""  
  
from pydantic import BaseModel, Field  
import re, time, threading, hashlib  
from collections import OrderedDict  
from typing import Optional, Any, Dict  
  
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)  
TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)  
THINK_RE = re.compile(  
    r"<" + "think[^>]*>.*?" + "<" + "/think>", re.DOTALL | re.IGNORECASE  
)  
REASONING_RE = re.compile(  
    r"<" + "(?:reasoning|thought)[^>]*>.*?" + "<" + "/(?:reasoning|thought)>",  
    re.DOTALL | re.IGNORECASE,  
)  
  
MAX_CHATS = 500  
CUMULATIVE: OrderedDict[str, Dict[str, Any]] = OrderedDict()  
LOCK = threading.Lock()  
  
  
class Filter:  
    class Valves(BaseModel):  
        priority: int = Field(default=20)  
  
    def __init__(self):  
        self.valves = self.Valves()  
  
    @staticmethod  
    def fmt(n: int) -> str:  
        if n >= 1_000_000:  
            return f"{n/1e6:.1f}M"  
        if n >= 1000:  
            return f"{n/1e3:.1f}k"  
        return str(int(n))  
  
    @staticmethod  
    def fmt_w(n: int) -> str:  
        return f"{Filter.fmt(n)}w"  
  
    @staticmethod  
    def fmt_time(seconds: float) -> str:  
        """
        < 60s  => '18.3s'
        60-3599s => 'MM:SS'
        >= 3600s => 'H:MM:SS'
        """  
        s = int(seconds)
        if s < 60:
            return f"{seconds:.1f}s"
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        if h > 0:
            return f"{h}:{m:02d}:{sec:02d}"
        return f"{m}:{sec:02d}"

    @staticmethod
    def extract_text(content: Any) -> str:
        if not content:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "".join(
                [
                    p.get("text", "")
                    for p in content
                    if isinstance(p, dict)
                    and p.get("type") == "text"
                    and isinstance(p.get("text"), str)
                ]
            )
        return str(content)

    @staticmethod
    def count_words(t: str) -> int:
        return len(WORD_RE.findall(t)) if t else 0

    @staticmethod
    def estimate_tokens(t: str) -> int:
        return max(0, int(round(len(TOKEN_RE.findall(t)) * 1.3))) if t else 0

    @staticmethod
    def assistant_text(m: Optional[dict]) -> str:
        if not isinstance(m, dict):
            return ""
        raw = Filter.extract_text(m.get("content", ""))
        visible = THINK_RE.sub("", raw)
        visible = REASONING_RE.sub("", visible)
        return visible.strip()

    @staticmethod
    def get_usage(m: Optional[dict]) -> Optional[dict]:
        if not isinstance(m, dict):
            return None
        u = m.get("usage")
        if isinstance(u, dict):
            return u
        info = m.get("info")
        if isinstance(info, dict):
            u = info.get("usage")
            if isinstance(u, dict):
                return u
        return None

    @staticmethod
    def get_int(d: Optional[dict], *keys: str) -> Optional[int]:
        if not isinstance(d, dict):
            return None
        for k in keys:
            v = d.get(k)
            if v is None:
                continue
            try:
                return int(v)
            except:
                continue
        return None

    @staticmethod
    def get_stream_usage(e: Any) -> Optional[dict]:
        if isinstance(e, dict):
            u = e.get("usage")
            if isinstance(u, dict):
                return u
            return None
        try:
            u = getattr(e, "usage", None)
            if isinstance(u, dict):
                return u
        except:
            pass
        return None

    @staticmethod
    def has_output(e: Any) -> bool:
        if not isinstance(e, dict):
            return False
        choices = e.get("choices")
        if not isinstance(choices, list):
            return False
        for c in choices:
            if not isinstance(c, dict):
                continue
            d = c.get("delta")
            if not isinstance(d, dict):
                continue
            if d.get("content"):
                return True
            for k in ("reasoning", "thinking", "reasoning_content"):
                if d.get(k):
                    return True
        return False

    @staticmethod
    def make_turn_key(chat_id: str, user_msg: Optional[dict], prompt_text: str) -> str:
        if isinstance(user_msg, dict):
            mid = user_msg.get("id") or user_msg.get("message_id")
            if mid:
                return f"{chat_id}:u:{mid}"
        h = hashlib.md5(prompt_text.encode("utf-8")).hexdigest()[:16]
        return f"{chat_id}:h:{h}"

    async def inlet(
        self,
        body: dict,
        user: Optional[dict] = None,
        metadata: Optional[dict] = None,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        meta = (
            metadata
            or __metadata__
            or kwargs.get("metadata")
            or kwargs.get("__metadata__")
        )
        if isinstance(meta, dict):
            meta["_token_start"] = time.perf_counter()
            meta["_token_first"] = None
            meta["_token_stream_usage"] = None
        if body.get("stream") is True:
            so = body.get("stream_options")
            if not isinstance(so, dict):
                so = {}
            so["include_usage"] = True
            body["stream_options"] = so
        return body

    async def stream(
        self,
        event: Any,
        user: Optional[dict] = None,
        metadata: Optional[dict] = None,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
        **kwargs,
    ) -> Any:
        meta = (
            metadata
            or __metadata__
            or kwargs.get("metadata")
            or kwargs.get("__metadata__")
        )
        if not isinstance(meta, dict):
            return event
        if meta.get("_token_first") is None and self.has_output(event):
            meta["_token_first"] = time.perf_counter()
        u = self.get_stream_usage(event)
        if isinstance(u, dict):
            meta["_token_stream_usage"] = u
        return event

    async def outlet(
        self,
        body: dict,
        user: Optional[dict] = None,
        metadata: Optional[dict] = None,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
        __event_emitter__=None,
        __event_call__=None,
        **kwargs,
    ) -> dict:
        try:
            messages = body.get("messages", [])
            if not isinstance(messages, list):
                messages = []
            body_meta = body.get("metadata") or {}
            chat_id = str(
                body.get("chat_id")
                or body_meta.get("chat_id")
                or body_meta.get("conversation_id")
                or "default"
            )
            meta = (
                metadata
                or __metadata__
                or kwargs.get("metadata")
                or kwargs.get("__metadata__")
                or {}
            )
            emitter = (
                __event_emitter__
                or kwargs.get("__event_emitter__")
                or kwargs.get("event_emitter")
            )

            start = meta.get("_token_start")
            first = meta.get("_token_first")
            su = meta.get("_token_stream_usage")

            total_elapsed = max(0.0, time.perf_counter() - start) if start else 0.0
            generation_elapsed = (
                max(0.0, time.perf_counter() - first) if first else total_elapsed
            )

            assistant_msg = None
            user_msg = None
            for m in reversed(messages):
                if not isinstance(m, dict):
                    continue
                r = m.get("role")
                if assistant_msg is None and r == "assistant":
                    assistant_msg = m
                if user_msg is None and r == "user":
                    user_msg = m
                if assistant_msg and user_msg:
                    break

            prompt_text = (
                self.extract_text(user_msg.get("content", "")) if user_msg else ""
            )
            reply_text = self.assistant_text(assistant_msg) if assistant_msg else ""

            prompt_words = self.count_words(prompt_text)
            reply_words = self.count_words(reply_text)
            usage = su if isinstance(su, dict) else self.get_usage(assistant_msg)
            prompt_tokens = self.get_int(usage, "prompt_tokens", "input_tokens")
            completion_tokens = self.get_int(
                usage, "completion_tokens", "output_tokens"
            )
            total_tokens = self.get_int(usage, "total_tokens")
            if prompt_tokens is None:
                prompt_tokens = self.estimate_tokens(prompt_text)
            if completion_tokens is None:
                completion_tokens = self.estimate_tokens(reply_text)
            if total_tokens is None:
                total_tokens = prompt_tokens + completion_tokens
            tps = (
                (completion_tokens / generation_elapsed)
                if generation_elapsed > 0 and completion_tokens > 0
                else 0.0
            )

            turn_key = self.make_turn_key(chat_id, user_msg, prompt_text)
            with LOCK:
                cum = CUMULATIVE.get(chat_id)
                if cum is None:
                    cum = {"p_tok": 0, "r_tok": 0, "p_w": 0, "r_w": 0, "turns": {}}
                    CUMULATIVE[chat_id] = cum
                else:
                    CUMULATIVE.move_to_end(chat_id)
                turns = cum["turns"]
                if turn_key in turns:
                    old = turns[turn_key]
                    cum["p_tok"] -= old["p_tok"]
                    cum["r_tok"] -= old["r_tok"]
                    cum["p_w"] -= old["p_w"]
                    cum["r_w"] -= old["r_w"]
                turns[turn_key] = {
                    "p_tok": prompt_tokens,
                    "r_tok": completion_tokens,
                    "p_w": prompt_words,
                    "r_w": reply_words,
                }
                cum["p_tok"] += prompt_tokens
                cum["r_tok"] += completion_tokens
                cum["p_w"] += prompt_words
                cum["r_w"] += reply_words
                while len(CUMULATIVE) > MAX_CHATS:
                    CUMULATIVE.popitem(last=False)
                cp_tok, cr_tok = cum["p_tok"], cum["r_tok"]
                cp_w, cr_w = cum["p_w"], cum["r_w"]
            ct_tok = cp_tok + cr_tok
            ct_w = cp_w + cr_w

            time_str = self.fmt_time(total_elapsed)
            description = f"🚀{tps:.1f}t/s({time_str}) 🪟Σ{self.fmt(ct_tok)}({self.fmt_w(ct_w)}) 👇P{self.fmt(prompt_tokens)}·{self.fmt_w(prompt_words)}|R{self.fmt(completion_tokens)}·{self.fmt_w(reply_words)} 📈ΣP{self.fmt(cp_tok)}·{self.fmt_w(cp_w)}|ΣR{self.fmt(cr_tok)}·{self.fmt_w(cr_w)}"

            if isinstance(usage, dict) and not isinstance(body.get("usage"), dict):
                body["usage"] = {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                }

            # DEBUG
            print(
                f"[TokenFilter] chat={chat_id} has_meta={isinstance(meta,dict)} has_emitter={emitter is not None} desc={description} kwargs_keys={list(kwargs.keys())}"
            )

            if emitter:
                await emitter(
                    {
                        "type": "status",
                        "data": {"description": description, "done": True},
                    }
                )
            else:
                print("[TokenFilter] NO EMITTER - filter won't show!")
        except Exception as e:
            print(f"Token Usage Display error: {type(e).__name__}: {e}")
        return body
