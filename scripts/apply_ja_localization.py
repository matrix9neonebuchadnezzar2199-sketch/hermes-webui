#!/usr/bin/env python3
"""Apply Japanese localization batch: add i18n keys, wire t(), server error map."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
I18N = REPO / "static" / "i18n.js"
STATIC = REPO / "static"

LOCALE_ORDER = [
    "en",
    "it",
    "ja",
    "ru",
    "es",
    "de",
    "zh",
    "zh-Hant",
    "pt",
    "ko",
    "fr",
    "tr",
    "pl",
    "vi",
]

# English source strings for new keys.
NEW_KEYS_EN: dict[str, str] = {
    "err_load_session_failed": "Failed to load session",
    "err_load_messages_failed": "Failed to load conversation messages",
    "toast_removed_from_project": "Removed from project",
    "err_unassign_failed": "Unassign failed: ",
    "toast_project_created": "Project created",
    "toast_project_renamed": "Project renamed",
    "toast_project_deleted": "Project deleted",
    "err_project_create_failed": "Project create failed: ",
    "toast_color_updated": "Color updated",
    "err_color_update_failed": "Color update failed: ",
    "toast_created_project_and_moved": 'Created "{0}" and moved session',
    "toast_created_project_move_failed": 'Created "{0}" but move failed: ',
    "err_read_only_rename": "Read-only imported sessions cannot be renamed.",
    "err_read_only_modify": "Read-only imported sessions cannot be modified.",
    "err_read_only_fork": "Read-only sessions cannot be forked.",
    "toast_gateway_sync_fallback": "Gateway sync unavailable — falling back to periodic refresh.",
    "err_new_conversation_failed": "New conversation failed: ",
    "toast_imported_cannot_delete": "Imported sessions cannot be deleted here.",
    "err_finish_turn_before_switch": "Finish the current turn before switching sessions.",
    "err_compression_recovery": "Compression recovery failed: ",
    "toast_compression_exhausted": "This session exhausted context compression. Start a focused continuation, then describe the next narrow task.",
    "toast_compression_action_unavailable": "This conversation already moved on — the focused-continuation action is no longer available.",
    "toast_conversation_refreshed": "Conversation refreshed",
    "toast_force_update_applied": "Force update applied — restarting…",
    "err_request_timeout": "Request timed out. Please try again.",
    "toast_office_preview_only": "This Office document is preview-only.",
    "toast_attachments_queued_removed": "Attachments on queued items will be removed",
    "err_edge_tts": "Edge TTS error: ",
    "err_edge_tts_failed": "Edge TTS failed: ",
    "toast_reasoning_effort_set": "Reasoning effort set to {0}",
    "err_reasoning_effort_failed": "Failed to set effort",
    "err_dashboard_link_save": "Dashboard link settings failed to save.",
    "err_compression_no_response": "No response received after context compression. Please retry.",
    "toast_stream_recovery": "Stream recovery signal received. Restoring transcript...",
    "chat_error_no_response_compression": "**Error:** No response received after context compression. Please retry.",
    "chat_error_generic": "**Error:** An error occurred. Check server logs.",
    "err_approval_not_accepted": "Approval response not accepted.",
    "err_clarify_unavailable": "Clarify endpoint unavailable. Please restart server.",
    "err_compression_failed": "Compression failed: ",
    "err_load_skills_failed": "Failed to load skills: ",
    "toast_unknown_argument": "Unknown argument: {0} — use show|hide|{1}",
    "toast_yolo_prefix": "YOLO: ",
    "toast_stream_inactive": "Stream is no longer active",
    "toast_reconnected_queued": "Current session is still running. Reconnected and queued your message.",
    "toast_model_changed_mismatch": "Model {0} changed to {1} — profile provider mismatch",
    "toast_code_copied": "Code copied",
    "toast_oauth_claude_linked": "Claude Code OAuth linked",
    "err_extension_update_failed": "Failed to update extension: ",
    "err_extension_proxy_consent_failed": "Failed to update extension sidecar proxy consent: ",
    "toast_extension_invalid": "Extension settings contain invalid values.",
    "toast_extension_saved": "Extension settings saved in this browser.",
    "toast_extension_reset": "Extension settings reset in this browser.",
    "toast_extension_cleared": "Extension storage cleared in this browser.",
    "err_extension_install_failed": "Install failed: ",
    "toast_extension_uninstalled": "Extension uninstalled.",
    "err_extension_uninstall_failed": "Uninstall failed: ",
    "err_base_url_required": "Base URL is required",
    "err_model_required": "Model is required",
    "err_connection_test_failed": "Connection test failed: ",
    "err_provider_save_failed": "Failed to save provider",
    "err_passkey_unsupported": "Passkeys require a supported browser and secure context.",
    "toast_passkey_registered": "Passkey registered",
    "err_passkey_register_failed": "Passkey registration failed: ",
    "passkey_remove_title": "Remove passkey?",
    "passkey_remove_message": "This browser/device will no longer be able to sign in with that passkey.",
    "toast_passkey_removed": "Passkey removed",
    "err_passkey_remove_failed": "Failed to remove passkey: ",
    "err_default_model_update_failed": "Failed to update default model — settings saved",
    "toast_password_removed_passkey": "Password removed. Passkey sign-in remains enabled.",
    "passwordless_title": "Go passwordless?",
    "passwordless_message": "This removes the password and keeps passkey sign-in enabled. Keep at least one passkey registered or you could lose access.",
    "passwordless_confirm": "Go passwordless",
    "err_passwordless_failed": "Failed to go passwordless: ",
    "pull_to_refresh": "Pull to refresh",
    "release_to_refresh": "Release to refresh",
    "agent_not_responding": "Hermes agent is not responding",
    "workspace_artifacts_empty": "Open a conversation to see files changed in this workspace during the chat.",
    "terminal_cdn_failed": "Terminal library failed to load. Check your network connection and try again.",
    "login_cannot_reach_server": "Cannot reach server — check your VPN / Tailscale connection.",
    "toast_copy_btn": "Copy",
    "toast_copied_btn": "Copied",
    "toast_dismiss_aria": "Dismiss error toast",
    "force_update_confirm_title": "Force update?",
    "force_update_confirm_message": "This will discard local changes and reset to the latest release.",
    "force_update_confirm_label": "Force update",
    "oauth_login_cancelled": "OAuth login cancelled",
    "oauth_login_claude_code": "Login with Claude Code",
    "oauth_waiting_authorization": "Waiting for authorization...",
    "gateway_service_restart_success": "Gateway service restarted successfully",
    "gateway_service_restart_failed": "Failed to restart gateway service: ",
    "err_unknown": "Unknown error",
    "err_session_no_longer_available": "session no longer available",
}

NEW_KEYS_JA: dict[str, str] = {
    "err_load_session_failed": "セッションの読み込みに失敗しました",
    "err_load_messages_failed": "会話メッセージの読み込みに失敗しました",
    "toast_removed_from_project": "プロジェクトから削除しました",
    "err_unassign_failed": "割り当て解除失敗: ",
    "toast_project_created": "プロジェクトを作成しました",
    "toast_project_renamed": "プロジェクト名を変更しました",
    "toast_project_deleted": "プロジェクトを削除しました",
    "err_project_create_failed": "プロジェクト作成失敗: ",
    "toast_color_updated": "色を更新しました",
    "err_color_update_failed": "色の更新失敗: ",
    "toast_created_project_and_moved": '「{0}」を作成しセッションを移動しました',
    "toast_created_project_move_failed": '「{0}」を作成しましたが移動失敗: ',
    "err_read_only_rename": "読み取り専用のインポートセッションは名前変更できません。",
    "err_read_only_modify": "読み取り専用のインポートセッションは変更できません。",
    "err_read_only_fork": "読み取り専用セッションはフォークできません。",
    "toast_gateway_sync_fallback": "ゲートウェイ同期が利用できません — 定期更新にフォールバックします。",
    "err_new_conversation_failed": "新しい会話の作成失敗: ",
    "toast_imported_cannot_delete": "インポートしたセッションはここでは削除できません。",
    "err_finish_turn_before_switch": "セッションを切り替える前に現在のターンを完了してください。",
    "err_compression_recovery": "圧縮リカバリ失敗: ",
    "toast_compression_exhausted": "このセッションはコンテキスト圧縮の上限に達しました。焦点を絞った続きを開始し、次の狭いタスクを説明してください。",
    "toast_compression_action_unavailable": "この会話は既に進行しています — 焦点を絞った続きのアクションは利用できません。",
    "toast_conversation_refreshed": "会話を更新しました",
    "toast_force_update_applied": "強制更新を適用しました — 再起動中…",
    "err_request_timeout": "リクエストがタイムアウトしました。もう一度お試しください。",
    "toast_office_preview_only": "この Office ドキュメントはプレビューのみです。",
    "toast_attachments_queued_removed": "キュー内アイテムの添付ファイルは削除されます",
    "err_edge_tts": "Edge TTS エラー: ",
    "err_edge_tts_failed": "Edge TTS 失敗: ",
    "toast_reasoning_effort_set": "推論の努力度を {0} に設定しました",
    "err_reasoning_effort_failed": "努力度の設定に失敗しました",
    "err_dashboard_link_save": "ダッシュボードリンク設定の保存に失敗しました。",
    "err_compression_no_response": "コンテキスト圧縮後に応答がありませんでした。もう一度お試しください。",
    "toast_stream_recovery": "ストリーム復旧シグナルを受信しました。トランスクリプトを復元中...",
    "chat_error_no_response_compression": "**エラー:** コンテキスト圧縮後に応答がありませんでした。もう一度お試しください。",
    "chat_error_generic": "**エラー:** エラーが発生しました。サーバーログを確認してください。",
    "err_approval_not_accepted": "承認応答が受け付けられませんでした。",
    "err_clarify_unavailable": "Clarify エンドポイントが利用できません。サーバーを再起動してください。",
    "err_compression_failed": "圧縮失敗: ",
    "err_load_skills_failed": "スキルの読み込み失敗: ",
    "toast_unknown_argument": "不明な引数: {0} — show|hide|{1} を使用してください",
    "toast_yolo_prefix": "YOLO: ",
    "toast_stream_inactive": "ストリームはアクティブではありません",
    "toast_reconnected_queued": "現在のセッションはまだ実行中です。再接続しメッセージをキューに入れました。",
    "toast_model_changed_mismatch": "モデル {0} が {1} に変更されました — プロファイルプロバイダーの不一致",
    "toast_code_copied": "コードをコピーしました",
    "toast_oauth_claude_linked": "Claude Code OAuth をリンクしました",
    "err_extension_update_failed": "拡張機能の更新失敗: ",
    "err_extension_proxy_consent_failed": "拡張機能サイドカープロキシ同意の更新失敗: ",
    "toast_extension_invalid": "拡張機能設定に無効な値が含まれています。",
    "toast_extension_saved": "拡張機能設定をこのブラウザに保存しました。",
    "toast_extension_reset": "拡張機能設定をこのブラウザでリセットしました。",
    "toast_extension_cleared": "拡張機能ストレージをこのブラウザでクリアしました。",
    "err_extension_install_failed": "インストール失敗: ",
    "toast_extension_uninstalled": "拡張機能をアンインストールしました。",
    "err_extension_uninstall_failed": "アンインストール失敗: ",
    "err_base_url_required": "ベース URL が必要です",
    "err_model_required": "モデルが必要です",
    "err_connection_test_failed": "接続テスト失敗: ",
    "err_provider_save_failed": "プロバイダーの保存に失敗しました",
    "err_passkey_unsupported": "パスキーには対応ブラウザとセキュアなコンテキストが必要です。",
    "toast_passkey_registered": "パスキーを登録しました",
    "err_passkey_register_failed": "パスキー登録失敗: ",
    "passkey_remove_title": "パスキーを削除しますか？",
    "passkey_remove_message": "このブラウザ/デバイスではそのパスキーでサインインできなくなります。",
    "toast_passkey_removed": "パスキーを削除しました",
    "err_passkey_remove_failed": "パスキー削除失敗: ",
    "err_default_model_update_failed": "デフォルトモデルの更新に失敗しました — 設定は保存されました",
    "toast_password_removed_passkey": "パスワードを削除しました。パスキーサインインは有効のままです。",
    "passwordless_title": "パスワードレスにしますか？",
    "passwordless_message": "パスワードを削除しパスキーサインインを有効にします。アクセスを失わないよう、少なくとも1つのパスキーを登録したままにしてください。",
    "passwordless_confirm": "パスワードレスにする",
    "err_passwordless_failed": "パスワードレス化失敗: ",
    "pull_to_refresh": "引いて更新",
    "release_to_refresh": "離して更新",
    "agent_not_responding": "Hermes エージェントが応答していません",
    "workspace_artifacts_empty": "会話を開くと、このワークスペースで変更されたファイルが表示されます。",
    "terminal_cdn_failed": "ターミナルライブラリの読み込みに失敗しました。ネットワーク接続を確認して再試行してください。",
    "login_cannot_reach_server": "サーバーに到達できません — VPN / Tailscale 接続を確認してください。",
    "toast_copy_btn": "コピー",
    "toast_copied_btn": "コピー済み",
    "toast_dismiss_aria": "エラートーストを閉じる",
    "force_update_confirm_title": "強制更新しますか？",
    "force_update_confirm_message": "ローカルの変更を破棄し最新リリースにリセットします。",
    "force_update_confirm_label": "強制更新",
    "oauth_login_cancelled": "OAuth ログインがキャンセルされました",
    "oauth_login_claude_code": "Claude Code でログイン",
    "oauth_waiting_authorization": "認証を待機中...",
    "gateway_service_restart_success": "ゲートウェイサービスを再起動しました",
    "gateway_service_restart_failed": "ゲートウェイサービスの再起動失敗: ",
    "err_unknown": "不明なエラー",
    "err_session_no_longer_available": "セッションが利用できなくなりました",
}

SERVER_ERROR_MAP_EN: dict[str, str] = {
    "not found": "server_err_not_found",
    "Auth not enabled": "server_err_auth_not_enabled",
    "Passkey support is disabled.": "server_err_passkey_disabled",
    "Passkey support is disabled. Set HERMES_WEBUI_PASSKEY=1 or webui_passkey_enabled: true to enable.": "server_err_passkey_disabled_full",
    "Too many attempts. Try again in a minute.": "server_err_too_many_attempts",
    "Missing OIDC callback state or code": "server_err_oidc_callback_missing",
    "Cross-origin request rejected": "server_err_cross_origin",
    "session_id is required": "server_err_session_id_required",
    "session_id required": "server_err_session_id_required",
    "name required": "server_err_name_required",
    "stream not found": "server_err_stream_not_found",
    "terminal not running": "server_err_terminal_not_running",
    "job_id required": "server_err_job_id_required",
    "invalid job_id": "server_err_invalid_job_id",
    "offset and limit must be integers": "server_err_offset_limit_integers",
    "job_id and filename required": "server_err_job_id_filename_required",
    "invalid filename": "server_err_invalid_filename",
    "run not found": "server_err_run_not_found",
    "session already has an active stream": "server_err_active_stream",
    "empty message": "server_err_empty_message",
    "no_provider": "server_err_no_provider",
}

SERVER_ERROR_KEYS_EN: dict[str, str] = {
    "server_err_not_found": "Not found",
    "server_err_auth_not_enabled": "Authentication is not enabled",
    "server_err_passkey_disabled": "Passkey support is disabled",
    "server_err_passkey_disabled_full": "Passkey support is disabled. Set HERMES_WEBUI_PASSKEY=1 or webui_passkey_enabled: true to enable.",
    "server_err_too_many_attempts": "Too many attempts. Try again in a minute.",
    "server_err_oidc_callback_missing": "Missing OIDC callback state or code",
    "server_err_cross_origin": "Cross-origin request rejected",
    "server_err_session_id_required": "Session ID is required",
    "server_err_name_required": "Name is required",
    "server_err_stream_not_found": "Stream not found",
    "server_err_terminal_not_running": "Terminal is not running",
    "server_err_job_id_required": "Job ID is required",
    "server_err_invalid_job_id": "Invalid job ID",
    "server_err_offset_limit_integers": "Offset and limit must be integers",
    "server_err_job_id_filename_required": "Job ID and filename are required",
    "server_err_invalid_filename": "Invalid filename",
    "server_err_run_not_found": "Run not found",
    "server_err_active_stream": "Session already has an active stream",
    "server_err_empty_message": "Empty message",
    "server_err_no_provider": "No provider configured",
}

SERVER_ERROR_KEYS_JA: dict[str, str] = {
    "server_err_not_found": "見つかりません",
    "server_err_auth_not_enabled": "認証が有効になっていません",
    "server_err_passkey_disabled": "パスキーサポートが無効です",
    "server_err_passkey_disabled_full": "パスキーサポートが無効です。HERMES_WEBUI_PASSKEY=1 または webui_passkey_enabled: true を設定して有効にしてください。",
    "server_err_too_many_attempts": "試行回数が多すぎます。1分後に再試行してください。",
    "server_err_oidc_callback_missing": "OIDC コールバックの state または code がありません",
    "server_err_cross_origin": "クロスオリジンリクエストが拒否されました",
    "server_err_session_id_required": "セッション ID が必要です",
    "server_err_name_required": "名前が必要です",
    "server_err_stream_not_found": "ストリームが見つかりません",
    "server_err_terminal_not_running": "ターミナルが実行されていません",
    "server_err_job_id_required": "ジョブ ID が必要です",
    "server_err_invalid_job_id": "無効なジョブ ID です",
    "server_err_offset_limit_integers": "offset と limit は整数である必要があります",
    "server_err_job_id_filename_required": "ジョブ ID とファイル名が必要です",
    "server_err_invalid_filename": "無効なファイル名です",
    "server_err_run_not_found": "実行が見つかりません",
    "server_err_active_stream": "セッションには既にアクティブなストリームがあります",
    "server_err_empty_message": "空のメッセージです",
    "server_err_no_provider": "プロバイダーが設定されていません",
}

# Merge server error keys into NEW_KEYS
NEW_KEYS_EN.update(SERVER_ERROR_KEYS_EN)
NEW_KEYS_JA.update(SERVER_ERROR_KEYS_JA)

JS_REPLACEMENTS: list[tuple[str, str]] = [
    # Wire existing keys
    ("showToast('Archive failed: '+(e.message||e))", "showToast(t('session_archive_failed')+(e.message||e))"),
    ("showToast('Delete failed: '+(e.message||e))", "showToast(t('delete_failed')+(e.message||e))"),
    ("showToast('Move failed: '+(e.message||e))", "showToast(t('move_failed')+(e.message||e))"),
    ("showToast('Rename failed: '+(e.message||e))", "showToast(t('rename_failed')+(e.message||e))"),
    ("confirmLabel:'Discard'", "confirmLabel:t('discard')"),
    ("confirmLabel:'Delete'", "confirmLabel:t('delete_title')"),
    ("confirmLabel:'Remove'", "confirmLabel:t('remove')"),
    ("showToast('Gateway service restarted successfully')", "showToast(t('gateway_service_restart_success'))"),
    ("showToast('Failed to restart gateway service: ' + e.message)", "showToast(t('gateway_service_restart_failed') + e.message)"),
    ("showToast('Removed from project')", "showToast(t('toast_removed_from_project'))"),
    ("showToast('Project deleted')", "showToast(t('toast_project_deleted'))"),
    ("showToast('Project created')", "showToast(t('toast_project_created'))"),
    ("showToast('Project renamed')", "showToast(t('toast_project_renamed'))"),
    ("showToast('Color updated')", "showToast(t('toast_color_updated'))"),
    # New keys
    ("showToast('Failed to load session',3000,'error')", "showToast(t('err_load_session_failed'),3000,'error')"),
    ("showToast('Failed to load conversation messages', 3000, 'error')", "showToast(t('err_load_messages_failed'), 3000, 'error')"),
    ("showToast('Unassign failed: '+(e.message||e))", "showToast(t('err_unassign_failed')+(e.message||e))"),
    ("showToast('Project create failed: '+(e.message||e))", "showToast(t('err_project_create_failed')+(e.message||e))"),
    ("showToast('Color update failed: '+(e.message||e))", "showToast(t('err_color_update_failed')+(e.message||e))"),
    ("showToast('Read-only imported sessions cannot be renamed.',3000)", "showToast(t('err_read_only_rename'),3000)"),
    ("showToast('Read-only imported sessions cannot be modified.',3000)", "showToast(t('err_read_only_modify'),3000)"),
    ("showToast('Gateway sync unavailable — falling back to periodic refresh.', 5000)", "showToast(t('toast_gateway_sync_fallback'), 5000)"),
    ("showToast('New conversation failed: '+(err&&err.message||err))", "showToast(t('err_new_conversation_failed')+(err&&err.message||err))"),
    ("showToast('Imported sessions cannot be deleted here.',3000)", "showToast(t('toast_imported_cannot_delete'),3000)"),
    ("showToast('Finish the current turn before switching sessions.',3000)", "showToast(t('err_finish_turn_before_switch'),3000)"),
    ("showToast('Compression recovery failed: '+(e&&e.message||e),5000,'error')", "showToast(t('err_compression_recovery')+(e&&e.message||e),5000,'error')"),
    ("showToast('This session exhausted context compression. Start a focused continuation, then describe the next narrow task.',4500,'warning')", "showToast(t('toast_compression_exhausted'),4500,'warning')"),
    ("showToast('This conversation already moved on — the focused-continuation action is no longer available.',4000,'info')", "showToast(t('toast_compression_action_unavailable'),4000,'info')"),
    ("showToast('Conversation refreshed')", "showToast(t('toast_conversation_refreshed'))"),
    ("showToast('Force update applied — restarting…')", "showToast(t('toast_force_update_applied'))"),
    ("showToast('Request timed out. Please try again.',5000,'error')", "showToast(t('err_request_timeout'),5000,'error')"),
    ("showToast('This Office document is preview-only.', 3000, 'error')", "showToast(t('toast_office_preview_only'), 3000, 'error')"),
    ("showToast('Attachments on queued items will be removed',2600,'warning')", "showToast(t('toast_attachments_queued_removed'),2600,'warning')"),
    ("showToast('Edge TTS error: '+(e&&e.message||e))", "showToast(t('err_edge_tts')+(e&&e.message||e))"),
    ("showToast('Edge TTS failed: '+(e&&e.message||e))", "showToast(t('err_edge_tts_failed')+(e&&e.message||e))"),
    ("showToast('🧠 Failed to set effort')", "showToast('🧠 '+t('err_reasoning_effort_failed'))"),
    ("showToast('Dashboard link settings failed to save.')", "showToast(t('err_dashboard_link_save'))"),
    ("showToast('No response received after context compression. Please retry.',5000,'error')", "showToast(t('err_compression_no_response'),5000,'error')"),
    ("showToast('Stream recovery signal received. Restoring transcript...',3500,'error')", "showToast(t('toast_stream_recovery'),3500,'error')"),
    ("showToast('Compression failed: '+(preflightErr.message||'session no longer available')", "showToast(t('err_compression_failed')+(preflightErr.message||t('err_session_no_longer_available'))"),
    ("showToast('Compression failed: '+e.message)", "showToast(t('err_compression_failed')+e.message)"),
    ("showToast('Failed to load skills: '+e.message)", "showToast(t('err_load_skills_failed')+e.message)"),
    ("showToast('Read-only sessions cannot be forked.',3000)", "showToast(t('err_read_only_fork'),3000)"),
    ("showToast('Stream is no longer active',2000)", "showToast(t('toast_stream_inactive'),2000)"),
    ("showToast('Current session is still running. Reconnected and queued your message.',2600)", "showToast(t('toast_reconnected_queued'),2600)"),
    ("showToast('Code copied')", "showToast(t('toast_code_copied'))"),
    ("showToast('Claude Code OAuth linked')", "showToast(t('toast_oauth_claude_linked'))"),
    ("showToast('Failed to update extension: '+(e&&e.message?e.message:String(e)))", "showToast(t('err_extension_update_failed')+(e&&e.message?e.message:String(e)))"),
    ("showToast('Failed to update extension sidecar proxy consent: '+(e&&e.message?e.message:String(e)))", "showToast(t('err_extension_proxy_consent_failed')+(e&&e.message?e.message:String(e)))"),
    ("showToast('Extension settings contain invalid values.')", "showToast(t('toast_extension_invalid'))"),
    ("showToast('Extension settings saved in this browser.')", "showToast(t('toast_extension_saved'))"),
    ("showToast('Extension settings reset in this browser.')", "showToast(t('toast_extension_reset'))"),
    ("showToast('Extension storage cleared in this browser.')", "showToast(t('toast_extension_cleared'))"),
    ("showToast('Install failed: '+(e&&e.message?e.message:String(e)))", "showToast(t('err_extension_install_failed')+(e&&e.message?e.message:String(e)))"),
    ("showToast('Extension uninstalled.')", "showToast(t('toast_extension_uninstalled'))"),
    ("showToast('Uninstall failed: '+(e&&e.message?e.message:String(e)))", "showToast(t('err_extension_uninstall_failed')+(e&&e.message?e.message:String(e)))"),
    ("showToast('Base URL is required')", "showToast(t('err_base_url_required'))"),
    ("showToast('Model is required')", "showToast(t('err_model_required'))"),
    ("showToast('Connection test failed: '+(e&&e.message||'request error'))", "showToast(t('err_connection_test_failed')+(e&&e.message||t('err_unknown')))"),
    ("showToast('Error: '+(e&&e.message||'Failed to save provider'))", "showToast(t('error_prefix')+(e&&e.message||t('err_provider_save_failed')))"),
    ("showToast('Passkeys require a supported browser and secure context.')", "showToast(t('err_passkey_unsupported'))"),
    ("showToast('Passkey registered')", "showToast(t('toast_passkey_registered'))"),
    ("showToast('Passkey registration failed: '+e.message)", "showToast(t('err_passkey_register_failed')+e.message)"),
    ("showToast('Passkey removed')", "showToast(t('toast_passkey_removed'))"),
    ("showToast('Failed to remove passkey: '+e.message)", "showToast(t('err_passkey_remove_failed')+e.message)"),
    ("showToast('Failed to update default model — settings saved')", "showToast(t('err_default_model_update_failed'))"),
    ("showToast('Password removed. Passkey sign-in remains enabled.')", "showToast(t('toast_password_removed_passkey'))"),
    ("showToast('Failed to go passwordless: '+e.message)", "showToast(t('err_passwordless_failed')+e.message)"),
    ("showToast('Error: '+e.message)", "showToast(t('error_prefix')+translateServerError(e.message))"),
    ("title:'Remove passkey?',message:'This browser/device will no longer be able to sign in with that passkey.'", "title:t('passkey_remove_title'),message:t('passkey_remove_message')"),
    ("title:'Go passwordless?',message:'This removes the password and keeps passkey sign-in enabled. Keep at least one passkey registered or you could lose access.',confirmLabel:'Go passwordless'", "title:t('passwordless_title'),message:t('passwordless_message'),confirmLabel:t('passwordless_confirm')"),
    ("content='**Error:** No response received after context compression. Please retry.'", "content=t('chat_error_no_response_compression')"),
    ("content:'**Error:** No response received after context compression. Please retry.'", "content=t('chat_error_no_response_compression')"),
    ("content:'**Error:** An error occurred. Check server logs.'", "content=t('chat_error_generic')"),
    ("content=`**Error:** ${errMsg}`", "content=t('error_prefix').replace(': ','')+': '+translateServerError(errMsg)"),
    ('"Approval response not accepted."', "t('err_approval_not_accepted')"),
    ('showToast("Clarify endpoint unavailable. Please restart server.", 5000)', "showToast(t('err_clarify_unavailable'), 5000)"),
    ("showToast('YOLO: ' + e.message)", "showToast(t('toast_yolo_prefix') + e.message)"),
    ("showToast('YOLO: '+e.message)", "showToast(t('toast_yolo_prefix')+e.message)"),
    ("btn.textContent='Copied'", "btn.textContent=t('toast_copied_btn')"),
    (">Copy</button>", ">'+t('toast_copy_btn')+'</button>"),
    ('aria-label="Dismiss error toast"', "aria-label=\"'+t('toast_dismiss_aria')+'\""),
    (">Dismiss</button>", ">'+t('dismiss')+'</button>"),
    ("const err=new Error('Request timed out. Please try again.');", "const err=new Error(t('err_request_timeout'));"),
    ("showToast(data.error, 5000, 'error')", "showToast(translateServerError(data.error), 5000, 'error')"),
    ("showToast(t('session_toolsets_failed') + (r && r.error ? r.error : 'Unknown error')", "showToast(t('session_toolsets_failed') + (r && r.error ? translateServerError(r.error) : t('err_unknown'))"),
    ("showToast('Moved to '+p.name)", "showToast(t('moved_to')+p.name)"),
]


def _locale_header_pattern(locale_key: str) -> str:
    if re.match(r"^[A-Za-z_][\w-]*$", locale_key) and "-" in locale_key:
        return rf"\n  '{re.escape(locale_key)}': \{{"
    return rf"\n  {re.escape(locale_key)}: \{{"


def extract_locale_block(src: str, locale_key: str) -> tuple[int, int]:
    """Return (start_index_of_open_brace, end_index_after_close_brace) for locale block."""
    start_match = re.search(_locale_header_pattern(locale_key), src)
    if not start_match:
        raise ValueError(f"Locale block not found: {locale_key}")
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
                return start, i + 1
    raise ValueError(f"Unbalanced braces for {locale_key}")


def js_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def format_key_line(key: str, value: str) -> str:
    return f"    {key}: '{js_escape(value)}',\n"


def add_keys_to_i18n(src: str) -> str:
    for locale in LOCALE_ORDER:
        _, end = extract_locale_block(src, locale)
        if locale == "ja":
            translations = {**NEW_KEYS_EN, **{k: NEW_KEYS_JA.get(k, v) for k, v in NEW_KEYS_EN.items()}}
        else:
            translations = NEW_KEYS_EN
        # Skip keys already present
        block_start_match = re.search(_locale_header_pattern(locale), src)
        block_start = block_start_match.start()
        block_text = src[block_start:end]
        lines = ["\n    // ja localization batch\n"]
        for key, value in translations.items():
            if re.search(rf"^\s{{4}}{re.escape(key)}:", block_text, re.MULTILINE):
                continue
            lines.append(format_key_line(key, value))
        insertion = "".join(lines)
        src = src[: end - 1] + insertion + src[end - 1 :]
    return src


def add_translate_server_error(src: str) -> str:
    if "function translateServerError(" in src:
        return src
    map_entries = ",\n".join(
        f"  {js_escape(k)!r}: {js_escape(v)!r}" for k, v in SERVER_ERROR_MAP_EN.items()
    )
    fn = f"""
// Map known English server error strings to i18n keys (client-side, no backend change).
const SERVER_ERROR_I18N_MAP = {{
{map_entries}
}};

/**
 * Translate a server-returned error message using the active locale when possible.
 * @param {{string|undefined|null}} msg
 * @returns {{string}}
 */
function translateServerError(msg) {{
  const raw = String(msg == null ? '' : msg).trim();
  if (!raw) return raw;
  const key = SERVER_ERROR_I18N_MAP[raw];
  if (key) {{
    const translated = t(key);
    if (translated && translated !== key) return translated;
  }}
  for (const [prefix, i18nKey] of Object.entries(SERVER_ERROR_I18N_MAP)) {{
    if (raw.startsWith(prefix) && prefix.length > 3) {{
      const translated = t(i18nKey);
      if (translated && translated !== i18nKey) return translated;
    }}
  }}
  return raw;
}}

"""
    anchor = "function t(key, ...args) {"
    return src.replace(anchor, fn + anchor, 1)


def apply_js_replacements(content: str, filename: str) -> str:
    for old, new in JS_REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
    # Special dynamic replacements
    if filename == "sessions.js":
        content = content.replace(
            "showToast('Created \"'+res.project.name+'\" and moved session')",
            "showToast(t('toast_created_project_and_moved', res.project.name))",
        )
        content = content.replace(
            "showToast('Created \"'+res.project.name+'\" but move failed: '+(e&&e.message||'try again'))",
            "showToast(t('toast_created_project_move_failed', res.project.name)+(e&&e.message||t('err_unknown')))",
        )
    if filename == "ui.js":
        content = content.replace(
            "showToast('🧠 Reasoning effort set to '+((st&&st.reasoning_effort)||effort))",
            "showToast('🧠 '+t('toast_reasoning_effort_set', (st&&st.reasoning_effort)||effort))",
        )
        content = content.replace(
            "message=j.error||j.message||text;",
            "message=translateServerError(j.error||j.message||text);",
        )
    if filename == "workspace.js":
        content = content.replace(
            "message=j.error||j.message||text;",
            "message=translateServerError(j.error||j.message||text);",
        )
        content = content.replace(
            '"Open a conversation to see files changed in this workspace during the chat."',
            "t('workspace_artifacts_empty')",
        )
    if filename == "commands.js":
        content = content.replace(
            "showToast('Unknown argument: '+arg+' \\u2014 use show|hide|'+EFFORTS.join('|'))",
            "showToast(t('toast_unknown_argument', arg, EFFORTS.join('|')))",
        )
    if filename == "messages.js":
        content = content.replace(
            "showToast('Model '+_sentModel+' changed to '+startData.effective_model+' — profile provider mismatch', 5000)",
            "showToast(t('toast_model_changed_mismatch', _sentModel, startData.effective_model), 5000)",
        )
    return content


def main() -> int:
    i18n_src = I18N.read_text(encoding="utf-8")
    i18n_src = add_keys_to_i18n(i18n_src)
    i18n_src = add_translate_server_error(i18n_src)
    I18N.write_text(i18n_src, encoding="utf-8")
    print(f"Updated {I18N}")

    for js_file in STATIC.glob("*.js"):
        if js_file.name == "i18n.js":
            continue
        text = js_file.read_text(encoding="utf-8")
        updated = apply_js_replacements(text, js_file.name)
        if updated != text:
            js_file.write_text(updated, encoding="utf-8")
            print(f"Updated {js_file.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
