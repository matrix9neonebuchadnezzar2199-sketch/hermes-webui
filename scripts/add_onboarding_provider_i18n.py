#!/usr/bin/env python3
"""Add onboarding provider labels and server-note i18n keys to all locales."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
I18N = REPO / "static" / "i18n.js"

LOCALE_ORDER = [
    "en", "it", "ja", "ru", "es", "de", "zh", "zh-Hant", "pt", "ko", "fr", "tr", "pl", "vi",
]

NEW_EN: dict[str, str] = {
    "onboarding_provider_openrouter": "OpenRouter",
    "onboarding_provider_anthropic": "Anthropic",
    "onboarding_provider_openai": "OpenAI",
    "onboarding_provider_ollama": "Ollama",
    "onboarding_provider_lmstudio": "LM Studio",
    "onboarding_provider_custom": "Custom OpenAI-compatible",
    "onboarding_provider_gemini": "Google Gemini",
    "onboarding_provider_deepseek": "DeepSeek",
    "onboarding_provider_xiaomi": "Xiaomi MiMo",
    "onboarding_provider_zai": "Z.AI / GLM (智谱)",
    "onboarding_provider_nvidia": "NVIDIA NIM",
    "onboarding_provider_mistralai": "Mistral",
    "onboarding_provider_x_ai": "xAI (Grok)",
    "onboarding_oauth_label_anthropic": "Claude Code OAuth",
    "onboarding_server_note_agent_unavailable": (
        "Hermes is not fully importable from the Web UI yet. Finish bootstrap or fix the "
        "agent install before provider setup will work."
    ),
    "onboarding_server_note_needs_provider": (
        "Hermes is installed, but you still need to choose a provider and save working credentials."
    ),
    "onboarding_server_note_ready": "Hermes is minimally configured and ready to chat via {0}.",
    "onboarding_server_note_custom_incomplete": (
        "Hermes has a saved provider/model selection but still needs the "
        "base URL and API key required to chat."
    ),
    "onboarding_server_note_api_key_incomplete": (
        "Hermes has a saved provider/model selection but still needs the "
        "API key required to chat."
    ),
    "onboarding_server_note_oauth_incomplete": (
        "Provider '{0}' is configured but not yet authenticated. "
        "Run 'hermes auth' or 'hermes model' in a terminal to complete "
        "setup, then reload the Web UI."
    ),
    "onboarding_unsupported_provider_note": (
        "Advanced provider flows such as Nous Portal and GitHub Copilot are still "
        "terminal-first. OpenAI Codex and Anthropic Claude Code can be authenticated in this onboarding flow "
        "when your Hermes config selects the corresponding provider."
    ),
    "provider_cost_budget_label": "Monthly budget",
    "provider_cost_budget_save_failed": "Failed to save budget",
    "provider_cost_budget_pct": "{0}% of ${1} budget (monthly pace)",
    "onboarding_api_key_help_anthropic": (
        "Anthropic API key path: paste an Anthropic Console API key here. This is separate from a Claude Code subscription; use the Claude Code OAuth card if you want subscription credentials instead."
    ),
    "onboarding_oauth_codex_pending_body": (
        "This instance is configured to use <strong>openai-codex</strong>, which uses OAuth rather than an API key. Use the button below to authenticate with ChatGPT, then continue once provider status refreshes."
    ),
}

NEW_JA: dict[str, str] = {
    "onboarding_provider_openrouter": "OpenRouter",
    "onboarding_provider_anthropic": "Anthropic",
    "onboarding_provider_openai": "OpenAI",
    "onboarding_provider_ollama": "Ollama",
    "onboarding_provider_lmstudio": "LM Studio",
    "onboarding_provider_custom": "カスタム OpenAI 互換",
    "onboarding_provider_gemini": "Google Gemini",
    "onboarding_provider_deepseek": "DeepSeek",
    "onboarding_provider_xiaomi": "Xiaomi MiMo",
    "onboarding_provider_zai": "Z.AI / GLM（智谱）",
    "onboarding_provider_nvidia": "NVIDIA NIM",
    "onboarding_provider_mistralai": "Mistral",
    "onboarding_provider_x_ai": "xAI (Grok)",
    "onboarding_oauth_label_anthropic": "Claude Code OAuth",
    "onboarding_server_note_agent_unavailable": (
        "Web UI から Hermes をまだ完全にインポートできません。プロバイダ設定の前に "
        "Bootstrap を完了するか、エージェントのインストールを修正してください。"
    ),
    "onboarding_server_note_needs_provider": (
        "Hermes はインストール済みですが、プロバイダを選び、動作する認証情報を保存する必要があります。"
    ),
    "onboarding_server_note_ready": "Hermes は最小構成で設定済みで、{0} 経由でチャットできます。",
    "onboarding_server_note_custom_incomplete": (
        "プロバイダとモデルは保存済みですが、チャットに必要なベース URL と APIキーがまだ不足しています。"
    ),
    "onboarding_server_note_api_key_incomplete": (
        "プロバイダとモデルは保存済みですが、チャットに必要な APIキーがまだ不足しています。"
    ),
    "onboarding_server_note_oauth_incomplete": (
        "プロバイダ「{0}」は設定済みですが、まだ認証されていません。"
        "ターミナルで hermes auth または hermes model を実行してセットアップを完了し、Web UI を再読み込みしてください。"
    ),
    "onboarding_unsupported_provider_note": (
        "Nous Portal や GitHub Copilot などの高度なプロバイダフローは、現状ターミナルでの操作が必要です。"
        "OpenAI Codex と Anthropic Claude Code は、Hermes 設定で該当プロバイダが選ばれている場合、このオンボーディングで認証できます。"
    ),
    "provider_cost_budget_label": "月間予算",
    "provider_cost_budget_save_failed": "予算の保存に失敗しました",
    "provider_cost_budget_pct": "月間予算 ${1} の {0}%",
    "onboarding_api_key_help_anthropic": (
        "Anthropic APIキー: Anthropic Console の APIキーをここに貼り付けます。Claude Code サブスクリプションとは別です。サブスクリプション認証情報を使う場合は Claude Code OAuth を選んでください。"
    ),
    "onboarding_oauth_codex_pending_body": (
        "このインスタンスは <strong>openai-codex</strong>（OAuth、APIキー不要）用に設定されています。下のボタンで ChatGPT 認証を行い、プロバイダ状態が更新されたら続けてください。"
    ),
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


def _js_quote(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def _upsert_keys(src: str, locale: str, mapping: dict[str, str]) -> str:
    end = extract_locale_block_end(src, locale)
    block = src[:end]
    for key, value in mapping.items():
        line = f"    {key}: {_js_quote(value)},"
        pat = re.compile(rf"^\s{{4}}{re.escape(key)}:.*$", re.MULTILINE)
        if pat.search(block):
            block = pat.sub(line, block, count=1)
        else:
            block = block.rstrip() + "\n" + line + "\n"
    return block + src[end:]


def main() -> int:
    src = I18N.read_text(encoding="utf-8")
    for locale in LOCALE_ORDER:
        if locale == "ja":
            src = _upsert_keys(src, locale, NEW_JA)
        elif locale == "en":
            src = _upsert_keys(src, locale, NEW_EN)
        else:
            src = _upsert_keys(src, locale, NEW_EN)
    I18N.write_text(src, encoding="utf-8", newline="\n")
    print(f"Updated {I18N}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
