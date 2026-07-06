#!/usr/bin/env python3
"""Generate approval pattern i18n keys from hermes-agent tools/approval.py."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENT_APPROVAL = Path.home() / "AppData/Local/hermes/hermes-agent/tools/approval.py"
if len(sys.argv) > 1:
    AGENT_APPROVAL = Path(sys.argv[1])

# Manual JA translations for common patterns (fallback: keep EN in other locales).
JA: dict[str, str] = {
    "delete in root path": "ルートパスへの削除",
    "recursive delete": "再帰的削除",
    "recursive delete (long flag)": "再帰的削除（長いフラグ）",
    "Windows cmd destructive delete": "Windows cmd による破壊的削除",
    "Windows PowerShell destructive delete": "Windows PowerShell による破壊的削除",
    "PowerShell encoded command execution": "PowerShell エンコードコマンドの実行",
    "world/other-writable permissions": "全員書き込み可能なパーミッション",
    "recursive world/other-writable (long flag)": "再帰的な全員書き込み可能パーミッション",
    "recursive chown to root": "root への再帰的 chown",
    "recursive chown to root (long flag)": "root への再帰的 chown（長いフラグ）",
    "format filesystem": "ファイルシステムのフォーマット",
    "disk copy": "ディスクコピー（dd）",
    "write to block device": "ブロックデバイスへの書き込み",
    "SQL DROP": "SQL DROP",
    "SQL DELETE without WHERE": "WHERE 句なしの SQL DELETE",
    "SQL TRUNCATE": "SQL TRUNCATE",
    "overwrite system config": "システム設定の上書き",
    "stop/restart system service": "システムサービスの停止/再起動",
    "kill all processes": "全プロセスの強制終了",
    "force kill processes": "プロセスの強制終了",
    "force kill processes (killall -KILL)": "プロセスの強制終了（killall -KILL）",
    "force kill processes (killall -s KILL)": "プロセスの強制終了（killall -s KILL）",
    "kill processes by regex (killall -r)": "正規表現によるプロセス終了（killall -r）",
    "fork bomb": "フォークボム",
    "shell command via -c/-lc flag": "シェル -c/-lc 経由のコマンド実行",
    "script execution via -e/-c flag": "スクリプト -e/-c 経由の実行",
    "pipe remote content to shell": "リモート内容をシェルへパイプ",
    "execute remote script via process substitution": "プロセス置換でリモートスクリプト実行",
    "execute remote content via command substitution": "コマンド置換でリモート内容を実行",
    "pipe decoded content to shell (possible command obfuscation)": "デコード結果をシェルへパイプ（難読化の可能性）",
    "pipe xxd-decoded content to shell (possible command obfuscation)": "xxd デコード結果をシェルへパイプ",
    "pipe tr-transformed output to shell (possible command obfuscation)": "tr 変換結果をシェルへパイプ",
    "pipe openssl-decoded content to shell (possible command obfuscation)": "openssl デコード結果をシェルへパイプ",
    "overwrite system file via tee": "tee によるシステムファイル上書き",
    "overwrite system file via redirection": "リダイレクトによるシステムファイル上書き",
    "overwrite project env/config via tee": "tee によるプロジェクト設定の上書き",
    "overwrite project env/config via redirection": "リダイレクトによるプロジェクト設定の上書き",
    "xargs with rm": "xargs と rm",
    "find -exec/-execdir rm": "find -exec/-execdir による rm",
    "dangerous_command": "危険なコマンド",
    "Dangerous command detected": "危険なコマンドを検出しました",
    "Dangerous command approval": "危険なコマンドの承認",
}


def _slug(desc: str) -> str:
    s = desc.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s[:80] or "unknown"


def extract_descriptions(path: Path) -> list[str]:
    src = path.read_text(encoding="utf-8")
    marker = "# Pre-compiled variant (same rationale as HARDLINE_PATTERNS_COMPILED above)."
    block = src.split("DANGEROUS_PATTERNS = [", 1)[1].split(marker, 1)[0]
    inline = re.findall(r',\s*"([^"]+)"\s*\),', block)
    multiline = re.findall(r'^\s+"([^"]+)"\s*,?\s*\)\s*,?\s*$', block, re.MULTILINE)
    return sorted(set(inline + multiline))


def main() -> int:
    if not AGENT_APPROVAL.exists():
        print(f"missing {AGENT_APPROVAL}", file=sys.stderr)
        return 1
    descs = extract_descriptions(AGENT_APPROVAL)
    print(f"// {len(descs)} approval patterns")
    print("const APPROVAL_PATTERN_I18N_MAP = {")
    for d in descs:
        key = "approval_pattern_" + _slug(d)
        esc = d.replace("\\", "\\\\").replace("'", "\\'")
        print(f"  '{esc}': '{key}',")
    print("};")
    print("\n// JA locale entries:")
    for d in descs:
        key = "approval_pattern_" + _slug(d)
        ja = JA.get(d, d)  # untranslated keep EN for now
        esc = ja.replace("\\", "\\\\").replace("'", "\\'")
        print(f"    {key}: '{esc}',")
    return 0


if __name__ == "__main__":
    sys.exit(main())
