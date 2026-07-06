#!/usr/bin/env python3
"""Add conn_unreachable to _LOGIN_LOCALE in routes.py."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROUTES = REPO / "api" / "routes.py"

JA = "サーバーに到達できません — VPN / Tailscale 接続を確認してください。"
EN = "Cannot reach server — check your VPN / Tailscale connection."


def main() -> None:
    src = ROUTES.read_text(encoding="utf-8")
    block_start = src.index("_LOGIN_LOCALE = {")
    block_end = src.index("\n\ndef _resolve_login_locale_key", block_start)
    block = src[block_start:block_end]
    if "conn_unreachable" in block:
        print("already patched")
        return

    def repl(match: re.Match[str]) -> str:
        line = match.group(0)
        if '"ja"' in src[max(0, match.start() - 200) : match.start()] or "接続失敗" in line:
            extra = JA
        else:
            # Use Japanese only for ja block - detect by scanning backwards for "ja": {
            window = block[max(0, match.start() - 400) : match.start()]
            extra = JA if re.search(r'"ja"\s*:\s*\{', window) else EN
        escaped = extra.replace("\\", "\\\\").replace('"', '\\"')
        return f'{line}\n        "conn_unreachable": "{escaped}",'

    block2 = re.sub(r'"conn_failed": "[^"]+",', repl, block)
    ROUTES.write_text(src[:block_start] + block2 + src[block_end:], encoding="utf-8")
    print("patched routes.py")


if __name__ == "__main__":
    main()
