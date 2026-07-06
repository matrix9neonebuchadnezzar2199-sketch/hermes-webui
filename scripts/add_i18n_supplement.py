#!/usr/bin/env python3
"""Add supplemental i18n keys for remaining hardcoded strings."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
I18N = REPO / "static" / "i18n.js"

LOCALE_ORDER = [
    "en", "it", "ja", "ru", "es", "de", "zh", "zh-Hant", "pt", "ko", "fr", "tr", "pl", "vi",
]

EXTRA_EN = {
    "err_force_update_failed": "Force update failed: ",
    "force_update_confirm_title_target": "Force update {0}?",
    "force_update_confirm_message_target": "This will discard all local changes and delete untracked files in the {0} repo, then reset to the latest remote version. This cannot be undone.",
    "force_update_btn": "Force update",
    "force_updating": "Force updating…",
    "oauth_start_again": "Start again whenever you're ready.",
    "err_clarify_not_accepted": "Clarification response not accepted — the agent may have already proceeded.",
    "err_clarify_expired": "Clarification prompt expired or not found.",
    "err_clarify_deliver_failed": "Failed to deliver clarification response.",
    "terminal_cdn_failed_jsdelivr": "Terminal library failed to load. Check network access to cdn.jsdelivr.net.",
    "chat_error_prefix": "**Error:** ",
    "conn_unreachable": "Cannot reach server — check your VPN / Tailscale connection.",
}

EXTRA_JA = {
    "err_force_update_failed": "強制更新失敗: ",
    "force_update_confirm_title_target": "{0} を強制更新しますか？",
    "force_update_confirm_message_target": "ローカルの変更をすべて破棄し、{0} リポジトリの未追跡ファイルを削除してから、最新のリモート版にリセットします。元に戻せません。",
    "force_update_btn": "強制更新",
    "force_updating": "強制更新中…",
    "oauth_start_again": "準備ができたらいつでも再開できます。",
    "err_clarify_not_accepted": "明確化応答が受け付けられませんでした — エージェントは既に進行している可能性があります。",
    "err_clarify_expired": "明確化プロンプトの期限切れ、または見つかりません。",
    "err_clarify_deliver_failed": "明確化応答の送信に失敗しました。",
    "terminal_cdn_failed_jsdelivr": "ターミナルライブラリの読み込みに失敗しました。cdn.jsdelivr.net へのネットワークアクセスを確認してください。",
    "chat_error_prefix": "**エラー:** ",
    "conn_unreachable": "サーバーに到達できません — VPN / Tailscale 接続を確認してください。",
}


def _locale_header_pattern(locale_key: str) -> str:
    if re.match(r"^[A-Za-z_][\w-]*$", locale_key) and "-" in locale_key:
        return rf"\n  '{re.escape(locale_key)}': \{{"
    return rf"\n  {re.escape(locale_key)}: \{{"


def extract_locale_block_end(src: str, locale_key: str) -> int:
    start_match = re.search(_locale_header_pattern(locale_key), src)
    if not start_match:
        raise ValueError(locale_key)
    start = start_match.end() - 1
    depth = 0
    in_single = in_double = in_backtick = False
    escape = False
    for i in range(start, len(src)):
        ch = src[i]
        if escape:
            escape = False
            continue
        if in_single:
            if ch == "\\":
                escape = True
            elif ch == "'":
                in_single = False
            continue
        if in_double:
            if ch == "\\":
                escape = True
            elif ch == '"':
                in_double = False
            continue
        if in_backtick:
            if ch == "\\":
                escape = True
            elif ch == "`":
                in_backtick = False
            continue
        if ch == "'":
            in_single = True
            continue
        if ch == '"':
            in_double = True
            continue
        if ch == "`":
            in_backtick = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"unbalanced {locale_key}")


def js_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def main() -> int:
    src = I18N.read_text(encoding="utf-8")
    for locale in LOCALE_ORDER:
        end = extract_locale_block_end(src, locale)
        translations = EXTRA_EN if locale != "ja" else {**EXTRA_EN, **EXTRA_JA}
        block_start = re.search(_locale_header_pattern(locale), src).start()
        block_text = src[block_start:end]
        lines = ["\n    // ja localization batch (supplement)\n"]
        for key, value in translations.items():
            if re.search(rf"^\s{{4}}{re.escape(key)}:", block_text, re.MULTILINE):
                continue
            lines.append(f"    {key}: '{js_escape(value)}',\n")
        if len(lines) > 1:
            src = src[:end] + "".join(lines) + src[end:]
    I18N.write_text(src, encoding="utf-8")
    print("Supplemental keys added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
