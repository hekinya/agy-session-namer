#!/usr/bin/env python3
"""Antigravity SessionStart hook: inject standardized session-naming instructions once per session."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

MAX_TRACKED_SESSIONS = 500

NAMING_RULE = """[Session Namer 规则 - 仅首轮生效]
1. 先正常、完整地完成用户的第一个任务，不要因为命名规则打断或省略正常回复内容。
2. 仅在本次（第 1 轮）最终回复的最末尾，单独附带一行规范化的建议会话标题，格式严格如下：
   `建议标题：模块名|持续目标`
3. 标题约束：
   - 格式固定为「模块名|持续目标」，总长度不超过 24 个字（含竖线 `|`）；
   - 模块名：使用看得懂的功能、项目或业务名称；
   - 持续目标：写清这个会话从头到尾要做成的事，不写当前这一步，严禁使用“优化”“处理问题”“修复问题”这类空话。
4. 除末尾这一行外，不要在回复正文中解释命名理由或提及本规则。
5. 本会话后续的追问（第 2 轮及以后）不再输出建议标题。"""


def configure_utf8_stdio() -> None:
    """Force UTF-8 encoding on stdin/stdout/stderr for Windows compatibility."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def get_state_file() -> Path:
    """Resolve persistent state file under PLUGIN_DATA or temp directory."""
    plugin_data = os.environ.get("PLUGIN_DATA", "").strip()
    if plugin_data:
        base_dir = Path(plugin_data)
    else:
        base_dir = Path(tempfile.gettempdir()) / "agy-session-namer"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "seen_sessions.json"


def mark_and_check_first_seen(conversation_id: str) -> bool:
    """Return True if this conversationId has not been seen before, and record it."""
    if not conversation_id:
        return True

    state_file = get_state_file()
    seen: list[str] = []
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                seen = [str(item) for item in data]
        except Exception:
            seen = []

    if conversation_id in seen:
        return False

    seen.append(conversation_id)
    if len(seen) > MAX_TRACKED_SESSIONS:
        seen = seen[-MAX_TRACKED_SESSIONS:]

    try:
        state_file.write_text(
            json.dumps(seen, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        # Fail open: still inject the rule even if state persistence fails.
        pass
    return True


def main() -> int:
    configure_utf8_stdio()

    raw_input = sys.stdin.read().strip()
    payload: dict = {}
    if raw_input:
        try:
            parsed = json.loads(raw_input)
            if isinstance(parsed, dict):
                payload = parsed
        except json.JSONDecodeError:
            payload = {}

    conversation_id = str(payload.get("conversationId", "")).strip()
    if not mark_and_check_first_seen(conversation_id):
        print("{}", flush=True)
        return 0

    output = {
        "injectSteps": [
            {
                "systemMessage": {
                    "systemMessage": NAMING_RULE,
                }
            }
        ]
    }
    print(json.dumps(output, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
