#!/usr/bin/env python
# coding: utf-8
"""
scripts/utils/ux.py
-------------------
Módulo compartilhado de UX para scripts de terminal do PulseFlat.
Fornece cores ANSI, ícones, helpers visuais, logger colorido e CLI comum.
"""

import argparse
import os
import sys
import logging
from typing import Optional, Iterator

# ── Detecção de Ambiente ──────────────────────────────────────────────
_CI = os.environ.get("CI", "")
_NO_COLOR = os.environ.get("NO_COLOR", "")
_TERM = os.environ.get("TERM", "")

IS_TTY = sys.stdout.isatty()
USE_COLOR = (IS_TTY or bool(_CI)) and not _NO_COLOR and _TERM != "dumb"

# Detecta suporte a Unicode (emoji) no terminal
try:
    USE_UNICODE = IS_TTY and sys.stdout.encoding and "UTF" in sys.stdout.encoding.upper()
except Exception:
    USE_UNICODE = False


def configure(*, use_color: Optional[bool] = None, use_unicode: Optional[bool] = None) -> None:
    """Override runtime de USE_COLOR / USE_UNICODE (útil em testes)."""
    global USE_COLOR, USE_UNICODE, ICON
    if use_color is not None:
        USE_COLOR = use_color
    if use_unicode is not None:
        USE_UNICODE = use_unicode
    if use_unicode is not None:
        _rebuild_icons()


def _rebuild_icons() -> None:
    """Reconstrói ICON com base no USE_UNICODE atual."""
    global ICON
    u = USE_UNICODE
    ICON.clear()
    ICON.update({
        "success": "✔" if u else "[OK]",
        "fail":    "✖" if u else "[FAIL]",
        "warn":    "⚠" if u else "[WARN]",
        "info":    "ℹ" if u else "[INFO]",
        "skip":    "⏭" if u else "[SKIP]",
        "file":    "📄" if u else "[FILE]",
        "package": "📦" if u else "[PKG]",
        "refresh": "🔄" if u else "[REFRESH]",
        "clean":   "🧹" if u else "[CLEAN]",
        "chart":   "📊" if u else "[CHART]",
        "clock":   "⏱" if u else "[TIME]",
        "folder":  "📁" if u else "[DIR]",
        "search":  "🔍" if u else "[SEARCH]",
        "gear":    "⚙"  if u else "[GEAR]",
        "rocket":  "🚀" if u else "[ROCKET]",
    })


# ── Códigos ANSI Core ─────────────────────────────────────────────────
def _c(code: str, text: str) -> str:
    """Aplica código ANSI se cores estiverem habilitadas."""
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


# Paleta básica
def bold(t: str) -> str:    return _c("1", t)
def dim(t: str) -> str:     return _c("2", t)
def red(t: str) -> str:     return _c("31", t)
def green(t: str) -> str:   return _c("32", t)
def yellow(t: str) -> str:  return _c("33", t)
def blue(t: str) -> str:    return _c("34", t)
def magenta(t: str) -> str: return _c("35", t)
def cyan(t: str) -> str:    return _c("36", t)
def white(t: str) -> str:   return _c("97", t)

# Paleta brilhante (bold + cor)
def b_red(t: str) -> str:     return _c("1;31", t)
def b_green(t: str) -> str:   return _c("1;32", t)
def b_yellow(t: str) -> str:  return _c("1;33", t)
def b_blue(t: str) -> str:    return _c("1;34", t)
def b_magenta(t: str) -> str: return _c("1;35", t)
def b_cyan(t: str) -> str:    return _c("1;36", t)
def b_white(t: str) -> str:   return _c("1;97", t)


# ── Ícones ────────────────────────────────────────────────────────────
ICON: dict[str, str] = {}
_rebuild_icons()

GROUP_ICON = {
    "anbima":  "🟡",
    "b3":      "🔵",
    "bcb":     "🟢",
    "cvm":     "🟣",
    "ibge":    "🔴",
    "ratings": "⚪",
    "misc":    "🟤",
}

GROUP_COLOR = {
    "anbima":  yellow,
    "b3":      cyan,
    "bcb":     green,
    "cvm":     magenta,
    "ibge":    red,
    "ratings": white,
    "misc":    blue,
}


# ── Helpers Visuais ───────────────────────────────────────────────────
def _line(char: str = "─", width: int = 72) -> str:
    """Retorna uma linha decorativa."""
    return dim(char * width)


def _progress_bar(done: int, total: int, width: int = 30) -> str:
    """Retorna uma barra de progresso ASCII colorida."""
    if total == 0:
        return ""
    filled = int(width * done / total)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(100 * done / total)
    return cyan(bar) + dim(f"  {pct:3d}%  ({done}/{total})")


def _spinner(frames: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏") -> Iterator[str]:
    """Generator infinito de frames de spinner."""
    i = 0
    while True:
        yield frames[i % len(frames)]
        i += 1


# ── Funções de Status (prints coloridos) ──────────────────────────────
def print_start(msg: str, icon: str = "refresh") -> None:
    """Indica início de operação."""
    print(f"  {ICON[icon]}  {msg}")


def print_done(msg: str, elapsed: Optional[float] = None, icon: str = "success") -> None:
    """Indica operação concluída com sucesso."""
    time_str = f"  {dim(f'{elapsed:.1f}s')}" if elapsed is not None else ""
    print(f"  {green(ICON[icon])}  {msg}{time_str}")


def print_fail(msg: str, elapsed: Optional[float] = None, icon: str = "fail") -> None:
    """Indica operação falhou."""
    time_str = f"  {dim(f'{elapsed:.1f}s')}" if elapsed is not None else ""
    print(f"  {red(ICON[icon])}  {msg}{time_str}")


def print_warn(msg: str, icon: str = "warn") -> None:
    """Indica aviso."""
    print(f"  {yellow(ICON[icon])}  {msg}")


def print_skip(msg: str, icon: str = "skip") -> None:
    """Indica item pulado."""
    print(f"  {dim(ICON[icon])}  {msg}")


def print_info(msg: str, icon: str = "info") -> None:
    """Indica informação."""
    print(f"  {cyan(ICON[icon])}  {msg}")


def print_summary(
    title: str,
    total: int,
    success: int,
    failed: int,
    skipped: int = 0,
    elapsed: float = 0.0,
    details: list[tuple[str, str, str]] = None,
) -> None:
    """Imprime tabela de resumo final."""
    details = details or []
    print()
    print(_line("═"))
    print(f"  {bold(title)}")
    print(_line("─"))

    parts = [
        f"  {bold('Total')}: {white(str(total))}",
        b_green(f"✔ {success} ok"),
    ]
    if failed:
        parts.append(b_red(f"✖ {failed} erro(s)"))
    else:
        parts.append(dim("0 erros"))
    if skipped:
        parts.append(yellow(f"⏭ {skipped} pulado(s)"))
    parts.append(cyan(f"⏱ {elapsed:.1f}s"))
    print("  │  ".join(parts))

    if details:
        print()
        print(dim("  Detalhes:"))
        for icon_key, label, value in details:
            icon_char = ICON.get(icon_key, "•")
            print(f"    {icon_char}  {label}: {white(value)}")

    print(_line("═"))
    print()


# ── Logger Colorido (wrapper sobre stdlib logging) ────────────────────
class ColorLogger:
    """Logger que usa cores ANSI nos níveis."""

    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)
            self._logger.propagate = False

    def _log(self, level: int, msg: str, color_fn) -> None:
        if USE_COLOR:
            self._logger.log(level, color_fn(msg))
        else:
            self._logger.log(level, msg)

    def debug(self, msg: str) -> None:
        self._log(logging.DEBUG, msg, dim)

    def info(self, msg: str) -> None:
        self._log(logging.INFO, msg, white)

    def success(self, msg: str) -> None:
        self._log(logging.INFO, msg, green)

    def warning(self, msg: str) -> None:
        self._log(logging.WARNING, msg, yellow)

    def error(self, msg: str) -> None:
        self._log(logging.ERROR, msg, red)

    def critical(self, msg: str) -> None:
        self._log(logging.CRITICAL, msg, b_red)

    def setLevel(self, level: int) -> None:
        self._logger.setLevel(level)


# ── CLI Helpers ───────────────────────────────────────────────────────
def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Adiciona argumentos comuns a todos os scripts."""
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suprime output não-essencial (apenas erros e resumo final)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra output detalhado (debug/info)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Desabilita cores ANSI (equivalente a NO_COLOR=1)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula execução sem gravar arquivos"
    )


def apply_common_args(args: argparse.Namespace) -> None:
    """Aplica efeitos dos argumentos comuns (chamar após parse_args)."""
    global USE_COLOR
    if args.no_color:
        USE_COLOR = False
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)


# ── Banner e Seção (versões simplificadas para scripts menores) ───────
def banner(title: str, subtitle: str = "") -> None:
    """Imprime cabeçalho padrão."""
    print()
    print(_line("═"))
    print(f"  {bold(title)}")
    if subtitle:
        print(f"  {dim(subtitle)}")
    print(_line("═"))
    print()


def section(title: str, icon: str = "gear") -> None:
    """Imprime separador de seção."""
    print()
    print(_line())
    print(f"  {ICON[icon]}  {bold(title)}")
    print(_line())
    print()


__all__ = [
    "USE_COLOR", "USE_UNICODE", "IS_TTY",
    "_c", "bold", "dim", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "b_red", "b_green", "b_yellow", "b_blue", "b_magenta", "b_cyan", "b_white",
    "ICON", "GROUP_ICON", "GROUP_COLOR",
    "_line", "_progress_bar", "_spinner",
    "print_start", "print_done", "print_fail", "print_warn", "print_skip", "print_info",
    "print_summary", "ColorLogger",
    "add_common_args", "apply_common_args",
    "banner", "section",
]