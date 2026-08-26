"""
title: View Persistent Memory
author: Rolan & Doris Tech
version: 1.1.0
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
                    <td class="time">
                        {timestamp}
                    </td>

                    <td class="category">
                        {memory_path}
                    </td>

                    <td class="tags">
                        {tags}
                    </td>

                    <td class="content">
                        {content}
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
                    overflow-x: auto;
                }}

                table {{
                    width: 100%;
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
                }}

                th {{
                    background: color-mix(
                        in srgb,
                        CanvasText 8%,
                        Canvas
                    );

                    font-weight: 650;
                    white-space: nowrap;
                }}

                tr:nth-child(even) {{
                    background: color-mix(
                        in srgb,
                        CanvasText 3%,
                        Canvas
                    );
                }}

                .time {{
                    white-space: nowrap;
                    opacity: 0.8;
                }}

                .category {{
                    white-space: nowrap;
                    font-weight: 600;
                }}

                .tags {{
                    white-space: nowrap;
                    opacity: 0.75;
                }}

                .content {{
                    min-width: 300px;
                    line-height: 1.45;
                }}

                @media (max-width: 700px) {{

                    body {{
                        padding: 10px;
                    }}

                    th,
                    td {{
                        padding: 7px;
                    }}

                    .content {{
                        min-width: 220px;
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

                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Category</th>
                            <th>Tags</th>
                            <th>Memory</th>
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
