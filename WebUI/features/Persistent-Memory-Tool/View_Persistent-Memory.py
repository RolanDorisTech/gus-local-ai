"""
title: View Persistent Memory
author: Rolan & Doris Tech
version: 1.2.0
description: One-click viewer for local Persistent Memory JSONL with automatic dark/light mode support.
"""

import html
import json
import os

from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class Action:

    class Valves(BaseModel):
        memory_file: str = "/Volumes/RocketQQ/open-webui-data/qwen-memory/memory.jsonl"
        fallback_file: str = "/app/backend/data/qwen-memory/memory.jsonl"
        priority: int = -100

    def __init__(self):
        self.valves = self.Valves()

    def _get_memory_file(self) -> str:
        if os.path.exists("/Volumes/RocketQQ"):
            return os.path.expanduser(os.path.expandvars(self.valves.memory_file))

        return os.path.expanduser(os.path.expandvars(self.valves.fallback_file))

    def _load(self):
        path = self._get_memory_file()
        memories = []

        if not os.path.exists(path):
            return memories, path

        try:
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    try:
                        entry = json.loads(line)

                        if isinstance(entry, dict):
                            memories.append(entry)

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            return [{"error": str(e)}], path

        memories.sort(
            key=lambda m: str(m.get("timestamp", "")),
            reverse=True,
        )

        return memories, path

    async def action(
        self,
        body: dict,
        __user__=None,
    ):
        memories, path = self._load()

        if not memories:

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">

                <style>
                    :root {{
                        color-scheme: light dark;
                    }}

                    body {{
                        font-family:
                            system-ui,
                            -apple-system,
                            BlinkMacSystemFont,
                            "Segoe UI",
                            sans-serif;

                        background: Canvas;
                        color: CanvasText;

                        padding: 20px;
                        margin: 0;
                    }}

                    .path {{
                        opacity: 0.65;
                        font-size: 0.85em;
                        word-break: break-all;
                    }}
                </style>
            </head>

            <body>
                <h2>Persistent Memory</h2>
                <p>No active memories stored.</p>
                <p class="path">
                    {html.escape(path)}
                </p>
            </body>
            </html>
            """

            return HTMLResponse(
                content=html_content,
                headers={"Content-Disposition": "inline"},
            )

        if len(memories) == 1 and "error" in memories[0]:

            error = html.escape(str(memories[0]["error"]))

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">

                <style>
                    :root {{
                        color-scheme: light dark;
                    }}

                    body {{
                        font-family:
                            system-ui,
                            -apple-system,
                            BlinkMacSystemFont,
                            "Segoe UI",
                            sans-serif;

                        background: Canvas;
                        color: CanvasText;

                        padding: 20px;
                        margin: 0;
                    }}
                </style>
            </head>

            <body>
                <h2>Persistent Memory Error</h2>
                <p>{error}</p>
            </body>
            </html>
            """

            return HTMLResponse(
                content=html_content,
                headers={"Content-Disposition": "inline"},
            )

        rows = []

        for memory in memories:

            timestamp = html.escape(
                str(
                    memory.get(
                        "timestamp",
                        "",
                    )
                )[:19]
            )

            memory_path = html.escape(
                str(
                    memory.get(
                        "path",
                        "uncategorized",
                    )
                )
            )

            tags = memory.get(
                "tags",
                [],
            )

            if isinstance(tags, list):
                tags = ", ".join(str(tag) for tag in tags)
            else:
                tags = str(tags)

            tags = html.escape(tags)

            content = html.escape(
                str(
                    memory.get(
                        "content",
                        "",
                    )
                )
            )

            rows.append(f"""
                <tr>
                    <td class="category">
                        {memory_path}
                    </td>

                    <td class="content">
                        {content}
                    </td>

                    <td class="time">
                        {timestamp}
                    </td>

                    <td class="tags">
                        {tags}
                    </td>
                </tr>
                """)

        table = "".join(rows)

        html_content = f"""
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="utf-8">

            <style>
                :root {{
                    color-scheme: light dark;
                }}

                body {{
                    font-family:
                        system-ui,
                        -apple-system,
                        BlinkMacSystemFont,
                        "Segoe UI",
                        sans-serif;

                    background: Canvas;
                    color: CanvasText;

                    padding: 16px;
                    margin: 0;
                }}

                h2 {{
                    margin: 0 0 8px 0;
                }}

                .meta {{
                    color: color-mix(
                        in srgb,
                        CanvasText 65%,
                        transparent
                    );

                    font-size: 0.85em;
                    margin-bottom: 16px;
                    word-break: break-all;
                }}

                .table-container {{
                    width: 100%;
                    overflow-x: hidden;
                }}

                table {{
                    width: 100%;
                    table-layout: fixed;
                    border-collapse: collapse;
                    font-size: 0.9em;
                }}

                th,
                td {{
                    border: 1px solid color-mix(
                        in srgb,
                        CanvasText 22%,
                        transparent
                    );

                    padding: 9px;
                    text-align: left;
                    vertical-align: top;

                    overflow-wrap: anywhere;
                    word-break: break-word;
                }}

                th {{
                    background: color-mix(
                        in srgb,
                        CanvasText 8%,
                        Canvas
                    );

                    font-weight: 650;
                }}

                tr:nth-child(even) {{
                    background: color-mix(
                        in srgb,
                        CanvasText 3%,
                        Canvas
                    );
                }}

                /* Main readable fields */
                .category {{
                    width: 20%;
                    font-weight: 600;
                }}

                .content {{
                    width: 52%;
                    line-height: 1.45;
                }}

                /* Compact fields on the right */
                .time {{
                    width: 13%;
                    font-size: 0.78em;
                    line-height: 1.35;
                    opacity: 0.75;
                }}

                .tags {{
                    width: 15%;
                    font-size: 0.78em;
                    line-height: 1.35;
                    opacity: 0.75;
                }}

                @media (max-width: 700px) {{

                    body {{
                        padding: 10px;
                    }}

                    table {{
                        font-size: 0.84em;
                    }}

                    th,
                    td {{
                        padding: 7px;
                    }}

                    .category {{
                        width: 21%;
                    }}

                    .content {{
                        width: 49%;
                    }}

                    .time {{
                        width: 14%;
                    }}

                    .tags {{
                        width: 16%;
                    }}
                }}
            </style>
        </head>

        <body>

            <h2>Persistent Memory</h2>

            <div class="meta">
                {len(memories)} active memories
                <br>
                {html.escape(path)}
            </div>

            <div class="table-container">

                <table>

                    <colgroup>
                        <col style="width:20%">
                        <col style="width:52%">
                        <col style="width:13%">
                        <col style="width:15%">
                    </colgroup>

                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Description</th>
                            <th>Time</th>
                            <th>Tags</th>
                        </tr>
                    </thead>

                    <tbody>
                        {table}
                    </tbody>

                </table>

            </div>

            <script>
                function reportHeight() {{
                    const height =
                        document.documentElement.scrollHeight;

                    parent.postMessage(
                        {{
                            type: "iframe:height",
                            height: height
                        }},
                        "*"
                    );
                }}

                window.addEventListener(
                    "load",
                    reportHeight
                );

                new ResizeObserver(
                    reportHeight
                ).observe(document.body);
            </script>

        </body>
        </html>
        """

        return HTMLResponse(
            content=html_content,
            headers={"Content-Disposition": "inline"},
        )
