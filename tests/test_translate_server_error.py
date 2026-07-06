"""Tests for translateServerError() and ja localization batch keys."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_translate_server_error_function_exists():
    src = read(REPO / "static" / "i18n.js")
    assert "function translateServerError(msg)" in src
    assert "SERVER_ERROR_I18N_MAP" in src
    assert "'Auth not enabled': 'server_err_auth_not_enabled'" in src


def test_server_error_keys_present_in_all_locales():
    src = read(REPO / "static" / "i18n.js")
    required = [
        "server_err_auth_not_enabled",
        "server_err_not_found",
        "server_err_active_stream",
    ]
    for key in required:
        count = len(re.findall(rf"^\s{{4}}{re.escape(key)}:", src, re.MULTILINE))
        assert count >= 14, f"{key} expected in all locales, found {count}"


def test_ja_localization_batch_keys_have_japanese_values():
    """Spot-check new toast/error keys are translated in ja, not left as English."""
    src = read(REPO / "static" / "i18n.js")
    ja_expected = [
        "err_load_session_failed: 'セッションの読み込みに失敗しました'",
        "pull_to_refresh: '引いて更新'",
        "agent_not_responding: 'Hermes エージェントが応答していません'",
        "server_err_auth_not_enabled: '認証が有効になっていません'",
        "chat_error_prefix: '**エラー:** '",
    ]
    for entry in ja_expected:
        assert entry in src, f"Missing ja translation: {entry}"


def test_onboarding_server_note_translation_helpers_exist():
    src = read(REPO / "static" / "i18n.js")
    assert "function translateOnboardingServerNote(msg)" in src
    assert "function onboardingProviderLabel(id, fallback)" in src
    assert "onboarding_server_note_needs_provider" in src


def test_onboarding_js_uses_server_note_translation():
    src = read(REPO / "static" / "onboarding.js")
    assert "translateOnboardingServerNote(system.provider_note)" in src
    assert "onboardingProviderLabel(p.id,p.label)" in src


def test_ja_onboarding_server_notes_translated():
    src = read(REPO / "static" / "i18n.js")
    assert "onboarding_server_note_needs_provider: 'Hermes はインストール済みですが" in src


def test_workspace_api_uses_translate_server_error():
    src = read(REPO / "static" / "workspace.js")
    assert "translateServerError(j.error||j.message||text)" in src


def test_ui_toast_error_buttons_use_i18n():
    src = read(REPO / "static" / "ui.js")
    assert "${t('toast_copy_btn')}" in src
    assert "${t('dismiss')}" in src
