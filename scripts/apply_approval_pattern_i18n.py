#!/usr/bin/env python3
"""Add approval pattern description translations to static/i18n.js."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
I18N = REPO / "static" / "i18n.js"
AGENT_APPROVAL = Path.home() / "AppData/Local/hermes/hermes-agent/tools/approval.py"

LOCALE_ORDER = ["en", "it", "ja", "ru", "es", "de", "zh", "zh-Hant", "pt", "ko", "fr", "tr", "pl", "vi"]

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
    "overwrite project env/config file": "プロジェクト設定ファイルの上書き",
    "xargs with rm": "xargs と rm",
    "find -exec/-execdir rm": "find -exec/-execdir による rm",
    "find -delete": "find -delete",
    "stop/restart hermes gateway (kills running agents)": "Hermes ゲートウェイの停止/再起動（実行中エージェントが終了）",
    "hermes update (restarts gateway, kills running agents)": "hermes update（ゲートウェイ再起動・実行中エージェント終了）",
    "docker compose restart/stop/kill/down (container lifecycle)": "docker compose の再起動/停止/kill/down",
    "docker restart/stop/kill (container lifecycle)": "docker の再起動/停止/kill",
    "start gateway outside systemd (use 'systemctl --user restart hermes-gateway')": "systemd 外でのゲートウェイ起動（systemctl --user restart hermes-gateway を使用）",
    "kill hermes/gateway process (self-termination)": "Hermes/ゲートウェイプロセスの終了（自己終了）",
    "kill process via pgrep/pidof expansion (self-termination)": "pgrep/pidof 展開によるプロセス終了（自己終了）",
    "kill process via backtick pgrep/pidof expansion (self-termination)": "バッククォート pgrep/pidof 展開によるプロセス終了",
    "stop/restart hermes launchd service (kills running agents)": "Hermes launchd サービスの停止/再起動",
    "copy/move file into system config path": "システム設定パスへのコピー/移動",
    "copy/move file into sensitive credential/SSH/shell-rc path": "認証情報/SSH/シェル設定へのコピー/移動",
    "in-place edit of sensitive credential/SSH/shell-rc path": "認証情報/SSH/シェル設定のインプレース編集",
    "in-place edit of sensitive credential/SSH/shell-rc path (long flag)": "認証情報/SSH/シェル設定のインプレース編集（長いフラグ）",
    "in-place edit of sensitive credential/SSH/shell-rc path (perl/ruby)": "認証情報/SSH/シェル設定のインプレース編集（perl/ruby）",
    "in-place edit of system config": "システム設定のインプレース編集",
    "in-place edit of system config (long flag)": "システム設定のインプレース編集（長いフラグ）",
    "in-place edit of Hermes config/env": "Hermes 設定/.env のインプレース編集",
    "in-place edit of Hermes config/env (long flag)": "Hermes 設定/.env のインプレース編集（長いフラグ）",
    "in-place edit of Hermes config/env (perl/ruby)": "Hermes 設定/.env のインプレース編集（perl/ruby）",
    "script execution via heredoc": "ヒアドキュメント経由のスクリプト実行",
    "shell execution via heredoc": "ヒアドキュメント経由のシェル実行",
    "git reset --hard (destroys uncommitted changes)": "git reset --hard（未コミット変更の破棄）",
    "git force push (rewrites remote history)": "git force push（リモート履歴の書き換え）",
    "git force push short flag (rewrites remote history)": "git force push -f（リモート履歴の書き換え）",
    "git clean with force (deletes untracked files)": "git clean -f（未追跡ファイルの削除）",
    "git branch force delete": "git branch の強制削除",
    "git branch force delete (long flags)": "git branch の強制削除（長いフラグ）",
    "git branch force delete (long flags, force-first)": "git branch の強制削除（force 先）",
    "chmod +x followed by immediate execution": "chmod +x 後の即時実行",
    "sudo with privilege flag (stdin/askpass/shell/list)": "sudo 特権フラグ（stdin/askpass/shell/list）",
    "sudo with combined-flag privilege escalation": "sudo 結合フラグによる特権昇格",
    "Dangerous command detected": "危険なコマンドを検出しました",
    "Dangerous command approval": "危険なコマンドの承認",
    "dangerous_command": "危険なコマンド",
    "recursive delete": "再帰的削除",
}


def _slug(desc: str) -> str:
    s = desc.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return ("approval_pattern_" + s.strip("_"))[:96]


def extract_descriptions(path: Path) -> list[str]:
    src = path.read_text(encoding="utf-8")
    marker = "# Pre-compiled variant (same rationale as HARDLINE_PATTERNS_COMPILED above)."
    block = src.split("DANGEROUS_PATTERNS = [", 1)[1].split(marker, 1)[0]
    inline = re.findall(r',\s*"([^"]+)"\s*\),', block)
    multiline = re.findall(r'^\s+"([^"]+)"\s*,?\s*\)\s*,?\s*$', block, re.MULTILINE)
    return sorted(set(inline + multiline))


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


def _js_quote(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def _locale_start(src: str, locale_key: str) -> int:
    match = re.search(_locale_header_pattern(locale_key), src)
    if not match:
        raise ValueError(locale_key)
    return match.start()


def _upsert_keys(src: str, locale: str, mapping: dict[str, str]) -> str:
    start = _locale_start(src, locale)
    end = extract_locale_block_end(src, locale)
    prefix = src[:start]
    block = src[start:end]
    suffix = src[end:]
    for key, value in mapping.items():
        line = f"    {key}: {_js_quote(value)},"
        pat = re.compile(rf"^\s{{4}}{re.escape(key)}:.*$", re.MULTILINE)
        if pat.search(block):
            block = pat.sub(line, block, count=1)
        else:
            block = block.rstrip() + "\n" + line + "\n"
    return prefix + block + suffix


def _build_map(descs: list[str]) -> dict[str, str]:
    return {d: _slug(d) for d in descs}


def _inject_map_constant(src: str, descs: list[str]) -> str:
    lines = ["const APPROVAL_PATTERN_I18N_MAP = {"]
    for d in descs:
        key = _slug(d)
        esc = d.replace("\\", "\\\\").replace("'", "\\'")
        lines.append(f"  '{esc}': '{key}',")
    lines.append("};")
    block = "\n".join(lines)
    if "const APPROVAL_PATTERN_I18N_MAP" in src:
        return re.sub(
            r"const APPROVAL_PATTERN_I18N_MAP = \{[\s\S]*?\};",
            block,
            src,
            count=1,
        )
    anchor = "const ONBOARDING_SERVER_NOTE_MAP = {"
    if anchor not in src:
        raise ValueError("ONBOARDING_SERVER_NOTE_MAP anchor missing")
    insert = block + "\n\n"
    return src.replace(anchor, insert + anchor, 1)


def _inject_functions(src: str) -> str:
    if "function translateApprovalText(" in src:
        return src
    fn = """
/**
 * Translate hermes-agent approval pattern descriptions for the active locale.
 * @param {string|undefined|null} text
 * @returns {string}
 */
function translateApprovalText(text) {
  const raw = String(text == null ? '' : text).trim();
  if (!raw) return raw;
  const key = APPROVAL_PATTERN_I18N_MAP[raw];
  if (key) {
    const translated = t(key);
    if (translated && translated !== key) return translated;
  }
  return raw;
}

/**
 * Build localized approval card description from pending approval payload.
 * @param {object} pending
 * @returns {string}
 */
function formatApprovalDescription(pending) {
  const rawDesc = String((pending && pending.description) || '').trim();
  const keys = (pending && (pending.pattern_keys || (pending.pattern_key ? [pending.pattern_key] : []))) || [];
  const descPart = translateApprovalText(rawDesc);
  const keyLabels = keys.map((k) => translateApprovalText(String(k || '').trim())).filter(Boolean);
  const uniqueKeys = keyLabels.filter((k, idx) => k && k !== descPart && keyLabels.indexOf(k) === idx);
  if (descPart && uniqueKeys.length) return descPart + ' [' + uniqueKeys.join(', ') + ']';
  if (descPart) return descPart;
  if (keyLabels.length) return keyLabels.filter((k, i) => keyLabels.indexOf(k) === i).join(', ');
  return t('approval_desc_prefix');
}

"""
    return src.replace(
        "function translateOnboardingServerNote(msg) {",
        fn + "function translateOnboardingServerNote(msg) {",
        1,
    )


def main() -> int:
    agent = AGENT_APPROVAL
    if len(sys.argv) > 1:
        agent = Path(sys.argv[1])
    descs = extract_descriptions(agent)
    extra = ["Dangerous command detected", "Dangerous command approval", "dangerous_command"]
    for e in extra:
        if e not in descs:
            descs.append(e)
    descs = sorted(set(descs))

    src = I18N.read_text(encoding="utf-8")
    src = _inject_map_constant(src, descs)
    src = _inject_functions(src)

    key_to_en = {_slug(d): d for d in descs}
    key_to_ja = {_slug(d): JA.get(d, d) for d in descs}
    key_to_ja["approval_counter_pending"] = "{0} / {1} 件（承認待ち）"
    key_to_en["approval_counter_pending"] = "{0} of {1} pending"

    for locale in LOCALE_ORDER:
        if locale == "ja":
            src = _upsert_keys(src, locale, key_to_ja)
        elif locale == "en":
            mapping = dict(key_to_en)
            src = _upsert_keys(src, locale, mapping)
        else:
            src = _upsert_keys(src, locale, key_to_en)

    I18N.write_text(src, encoding="utf-8", newline="\n")
    print(f"Updated {len(descs)} approval patterns in {I18N}")
    missing_ja = [d for d in descs if d not in JA]
    if missing_ja:
        print(f"warning: {len(missing_ja)} patterns use English fallback in ja", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
