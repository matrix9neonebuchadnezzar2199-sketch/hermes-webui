from pathlib import Path
import re


REPO = Path(__file__).resolve().parent.parent


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_spanish_locale_block_exists():
    src = read(REPO / "static" / "i18n.js")
    assert "\n  es: {" in src
    assert "_label: 'Español'" in src
    assert "_speech: 'es-ES'" in src


def test_spanish_locale_includes_representative_translations():
    src = read(REPO / "static" / "i18n.js")
    expected = [
        "settings_title: 'Configuración'",
        "login_title: 'Iniciar sesión'",
        "approval_heading: 'Se requiere aprobación'",
        "tab_tasks: 'Tareas'",
        "tab_skills: 'Habilidades'",
        "tab_memory: 'Memoria'",
    ]
    for entry in expected:
        assert entry in src


def extract_locale_block(src: str, locale_key: str) -> str:
    if locale_key == "zh-Hant":
        start_match = re.search(r"\n  'zh-Hant': \{", src)
    else:
        start_match = re.search(rf"\n  {re.escape(locale_key)}: \{{", src)
    assert start_match, f"{locale_key} locale block not found"

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
            continue
        if ch == "}":
            depth -= 1
            if depth == 0:
                return src[start + 1 : i]

    raise AssertionError(f"{locale_key} locale block braces are not balanced")


def test_spanish_locale_covers_english_keys():
    src = read(REPO / "static" / "i18n.js")
    key_pattern = re.compile(r"^\s{4}([a-zA-Z0-9_]+):", re.MULTILINE)
    en_keys = set(key_pattern.findall(extract_locale_block(src, "en")))
    es_keys = set(key_pattern.findall(extract_locale_block(src, "es")))

    missing = sorted(en_keys - es_keys)
    assert not missing, f"Spanish locale missing keys: {missing}"
