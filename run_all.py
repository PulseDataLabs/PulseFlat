"""
run_all.py
----------
Orquestrador: executa scrapers em sequência e imprime resumo.

Uso:
    python run_all.py                     # todos
    python run_all.py anbima              # grupo ANBIMA
    python run_all.py b3                  # grupo B3
    python run_all.py anbima_indicadores  # scraper específico
"""

import importlib
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

# Suprime warning de incompatibilidade de versões do requests/urllib3
warnings.filterwarnings("ignore", category=Warning, module="requests")

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns
from rich.align import Align
from rich.logging import RichHandler
from rich import box
import logging

console = Console(highlight=False)

# ── Logging via Rich ──────────────────────────────────────────────────────────
# Usa o mesmo console do rich para que logs não quebrem o Progress.
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%H:%M:%S]",
    handlers=[RichHandler(console=console, show_path=False, markup=False)],
    force=True,
)
# Silencia loggers barulhentos de libs externas
for _noisy in ("urllib3", "requests", "charset_normalizer", "selenium", "httpx"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)

log = logging.getLogger("run_all")

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from utils import get_logger as _get_logger  # noqa: F401
except ImportError:
    pass

# ── Paleta de cores ───────────────────────────────────────────────────────────
C_PRIMARY   = "cyan"
C_ACCENT    = "bright_cyan"
C_OK        = "bright_green"
C_ERR       = "bright_red"
C_WARN      = "yellow"
C_DIM       = "grey50"
C_TITLE     = "bold white"
C_HEADER_BG = "#0d1b2a"
C_ERR_BG    = "#1f0000"

# ── Banner ASCII ──────────────────────────────────────────────────────────────
BANNER = r"""
 ██████╗ ██╗   ██╗███╗   ██╗    █████╗ ██╗     ██╗
 ██╔══██╗██║   ██║████╗  ██║   ██╔══██╗██║     ██║
 ██████╔╝██║   ██║██╔██╗ ██║   ███████║██║     ██║
 ██╔══██╗██║   ██║██║╚██╗██║   ██╔══██║██║     ██║
 ██║  ██║╚██████╔╝██║ ╚████║   ██║  ██║███████╗███████╗
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝  ╚═╝╚══════╝╚══════╝
"""
SCRAPERS = [
    {
        "id": "anbima_indicadores",
        "modulo": "scrapers.anbima_indicadores",
        "descricao": "ANBIMA — Indicadores (SELIC, DI, IGP-M, IPCA, Câmbio, TR, FDS)",
        "grupo": "anbima",
    },
    {
        "id": "anbima_projecoes",
        "modulo": "scrapers.anbima_projecoes",
        "descricao": "ANBIMA — Projeções IPCA e IGP-M",
        "grupo": "anbima",
    },
    {
        "id": "anbima_titulos_publicos",
        "modulo": "scrapers.anbima_titulos_publicos",
        "descricao": "ANBIMA — Títulos Públicos (preços e taxas indicativas)",
        "grupo": "anbima",
    },
    {
        "id": "anbima_debentures",
        "modulo": "scrapers.anbima_debentures",
        "descricao": "ANBIMA — Debêntures (preços e taxas indicativas)",
        "grupo": "anbima",
    },
    {
        "id": "anbima_ima",
        "modulo": "scrapers.anbima_ima",
        "descricao": "ANBIMA — Índices IMA/IDA (mark-to-market diário)",
        "grupo": "anbima",
    },
    {
        "id": "anbima_550",
        "modulo": "scrapers.anbima_550",
        "descricao": "ANBIMA — Resolução 550 (renda fixa: preço, retorno, custódia)",
        "grupo": "anbima",
    },
    {
        "id": "bcb_ptax",
        "modulo": "scrapers.bcb_ptax",
        "descricao": "BCB — PTAX (cotação USD/BRL compra e venda)",
        "grupo": "bcb",
    },
    {
        "id": "bcb_sgs",
        "modulo": "scrapers.bcb_sgs",
        "descricao": "BCB — SGS (SELIC, CDI, IPCA, IGP-M, Dólar — séries temporais)",
        "grupo": "bcb",
    },
    {
        "id": "ibge_sidra",
        "modulo": "scrapers.ibge_sidra",
        "descricao": "IBGE — SIDRA (metadados IPCA, IPCA-15, INPC, IPC-Br)",
        "grupo": "ibge",
    },
    {
        "id": "b3_fiis",
        "modulo": "scrapers.b3_fiis",
        "descricao": "B3 — FIIs Listados",
        "grupo": "b3",
    },
    {
        "id": "b3_etfs",
        "modulo": "scrapers.b3_etfs",
        "descricao": "B3 — ETFs Listados (RV + RF)",
        "grupo": "b3",
    },
    {
        "id": "b3_carteiras",
        "modulo": "scrapers.b3_carteiras",
        "descricao": "B3 — Carteiras Teóricas (22 índices)",
        "grupo": "b3",
    },
    {
        "id": "b3_futuros_ajustes",
        "modulo": "scrapers.b3_futuros_ajustes",
        "descricao": "B3 — Futuros (ajustes de fechamento do pregão BM&F)",
        "grupo": "b3",
    },
    {
        "id": "b3_bmf_taxas_juros",
        "modulo": "scrapers.b3_bmf_taxas_juros",
        "descricao": "B3 — BM&F Taxas de Juros de Referência (DI, SELIC, Dólar, IPCA…)",
        "grupo": "b3",
    },
    {
        "id": "b3_indicadores_financeiros",
        "modulo": "scrapers.b3_indicadores_financeiros",
        "descricao": "B3 — Indicadores Financeiros (SELIC, CDI, IPCA, IGP-M, câmbio)",
        "grupo": "b3",
    },
    {
        "id": "b3_bdi_di_over",
        "modulo": "scrapers.b3_bdi_di_over",
        "descricao": "B3 — BDI DI Over (taxa overnight, volume, fator diário)",
        "grupo": "b3",
    },
    # {
    #    "id": "b3_bdi_trades_acoes",
    #    "modulo": "scrapers.b3_bdi_trades_acoes",
    #    "descricao": "B3 — BDI Trades Consolidados de Ações (OHLC, volume, oscilação)",
    #    "grupo": "b3",
    # },
    # {
    #     "id": "b3_boletim_diario",
    #     "modulo": "scrapers.b3_boletim_diario",
    #     "descricao": "B3 — Boletim Diário (arquivos para download)",
    #     "grupo": "b3"
    # },
    # {
    #    "id": "cvm_fundos_cadastro",
    #    "modulo": "scrapers.cvm_fundos_cadastro",
    #    "descricao": "CVM — Cadastro de Fundos (cad_fi.csv)",
    #    "grupo": "cvm",
    # },
    # {
    #    "id": "cvm_fundos_informe_diario",
    #    "modulo": "scrapers.cvm_fundos_informe_diario",
    #    "descricao": "CVM — Informe Diário de Fundos (cota, PL, captação, resgates)",
    #    "grupo": "cvm",
    # },
    {
        "id": "captura_downloads_migrados",
        "modulo": "scrapers.captura_downloads_migrados",
        "descricao": "Migração captura_downloads — conjuntos requests em CSV",
        "grupo": "migrados",
    },
    # {
    #     "id": "brasa_migrados",
    #     "modulo": "scrapers.brasa_migrados",
    #     "descricao": "Migração brasa — conjuntos requests em CSV",
    #     "grupo": "migrados"
    # },
]


# ── Helpers visuais ───────────────────────────────────────────────────────────

def _grupo_cor(grupo: str) -> str:
    return {
        "anbima":   "bright_yellow",
        "b3":       "bright_blue",
        "migrados": "bright_magenta",
    }.get(grupo, "white")


def _grupo_icone(grupo: str) -> str:
    return {
        "anbima":   "◈",
        "b3":       "◉",
        "migrados": "◆",
    }.get(grupo, "●")


def _imprimir_banner():
    console.print()
    linhas = BANNER.strip("\n").splitlines()
    largura_banner = max(len(l) for l in linhas)
    largura_console = console.width or 80
    pad = max(0, (largura_console - largura_banner) // 2)
    espacos = " " * pad

    for linha in linhas:
        console.print(f"{espacos}[bold {C_ACCENT}]{linha}[/]")
    console.print()

    ts = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    meta = Text.assemble(
        ("  Orquestrador de Scrapers  ", f"bold {C_DIM}"),
        ("│", C_DIM),
        (f"  {ts}  ", C_DIM),
    )
    console.print(Align.center(meta))
    console.print()
    console.print(Rule(style=C_DIM))
    console.print()


def _imprimir_plano(selecionados: list, filtro: str | None):
    grupos = {}
    for s in selecionados:
        grupos.setdefault(s["grupo"], []).append(s)

    paineis = []
    for grupo, items in grupos.items():
        cor = _grupo_cor(grupo)
        icone = _grupo_icone(grupo)
        linhas = Text()
        for i, s in enumerate(items):
            prefix = "└─" if i == len(items) - 1 else "├─"
            linhas.append(f"  {prefix} ", style=C_DIM)
            linhas.append(s["id"], style=f"bold {C_ACCENT}")
            linhas.append("\n")
        paineis.append(
            Panel(
                linhas,
                title=f"[bold {cor}]{icone}  {grupo.upper()}[/]",
                border_style=cor,
                padding=(0, 1),
                expand=True,
            )
        )

    titulo_filtro = f"  [dim]filtro:[/] [italic {C_WARN}]{filtro}[/]" if filtro else ""
    console.print(
        Panel(
            f"[bold {C_TITLE}]🕷  {len(selecionados)} scraper(s) agendado(s)[/]{titulo_filtro}",
            border_style=C_PRIMARY,
            expand=False,
            padding=(0, 2),
        )
    )
    console.print()

    if len(paineis) == 1:
        console.print(paineis[0])
    else:
        console.print(Columns(paineis, equal=True, expand=True))

    console.print()
    console.print(Rule(style=C_DIM))
    console.print()


# ── Execução ──────────────────────────────────────────────────────────────────

def executar(scraper: dict) -> tuple[bool, float]:
    inicio = time.time()
    try:
        mod = importlib.import_module(scraper["modulo"])
        mod.main()
        return True, time.time() - inicio
    except SystemExit as e:
        return (e.code in (0, None)), time.time() - inicio
    except Exception as e:
        log.error(f"[{scraper['id']}] Erro inesperado: {e}", exc_info=True)
        return False, time.time() - inicio


def _imprimir_resultados(resultados: list):
    console.print()
    console.print(Rule(f"[bold {C_PRIMARY}] Resumo da Execução [/]", style=C_PRIMARY))
    console.print()

    table = Table(
        box=box.SIMPLE_HEAD,
        border_style=C_PRIMARY,
        header_style=f"bold white on {C_HEADER_BG}",
        show_lines=True,
        expand=False,
        padding=(0, 1),
    )

    table.add_column("",          width=3,  justify="center", no_wrap=True)
    table.add_column("Grupo",     width=12, justify="left",   no_wrap=True)
    table.add_column("ID",        width=32, style=f"bold {C_ACCENT}", no_wrap=True)
    table.add_column("Descrição",           style="white",    no_wrap=True)
    table.add_column("Tempo",     width=7,  justify="right",  style=C_DIM)

    id_grupo = {s["id"]: s["grupo"] for s in SCRAPERS}

    n_ok = n_err = 0
    tempo_total = 0.0

    for id_, desc, ok, dur in resultados:
        tempo_total += dur
        grupo = id_grupo.get(id_, "—")
        cor_grupo = _grupo_cor(grupo)
        icone_grupo = _grupo_icone(grupo)

        if ok:
            n_ok += 1
            icon      = f"[bold {C_OK}]✔[/]"
            row_style = ""
        else:
            n_err += 1
            icon      = f"[bold {C_ERR}]✘[/]"
            row_style = f"on {C_ERR_BG}"

        table.add_row(
            icon,
            f"[{cor_grupo}]{icone_grupo} {grupo}[/]",
            id_,
            desc,
            f"{dur:.1f}s",
            style=row_style,
        )

    console.print(Align.center(table))
    console.print()

    # ── Barra de progresso final (visual) ────────────────────────────────────
    pct = n_ok / len(resultados) if resultados else 0
    barra_len = 40
    preenchido = int(barra_len * pct)

    conteudo = Text()
    conteudo.append("\n  ")
    conteudo.append(f"✔ {n_ok} ok", style=f"bold {C_OK}")
    conteudo.append("   │   ", style=C_DIM)
    if n_err:
        conteudo.append(f"✘ {n_err} erro(s)", style=f"bold {C_ERR}")
    else:
        conteudo.append(f"✘ {n_err} erros", style=C_DIM)
    conteudo.append("   │   ", style=C_DIM)
    conteudo.append(f"⏱  {tempo_total:.1f}s total", style=C_DIM)
    conteudo.append("\n\n  ")
    conteudo.append("█" * preenchido, style=f"bold {C_OK}")
    conteudo.append("░" * (barra_len - preenchido), style=C_DIM)
    conteudo.append("\n")

    console.print(
        Panel(
            conteudo,
            border_style=C_OK if not n_err else C_ERR,
            expand=False,
            padding=(0, 2),
        )
    )
    console.print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None

    selecionados = [
        s for s in SCRAPERS
        if filtro is None or filtro == s["id"] or filtro == s["grupo"]
    ]

    _imprimir_banner()

    if not selecionados:
        validos = sorted(
            [s["id"] for s in SCRAPERS] + list({s["grupo"] for s in SCRAPERS})
        )
        console.print(
            Panel(
                Text.assemble(
                    ("✘  Filtro inválido: ", f"bold {C_ERR}"),
                    (f"'{filtro}'\n\n", f"bold {C_WARN}"),
                    ("Opções válidas:\n  ", C_DIM),
                    ("  ".join(validos), C_ACCENT),
                ),
                border_style=C_ERR,
                expand=False,
                padding=(1, 2),
            )
        )
        sys.exit(1)

    _imprimir_plano(selecionados, filtro)

    # ── Execução com barra de progresso ──────────────────────────────────────
    resultados = []

    with Progress(
        SpinnerColumn(spinner_name="dots12", style=C_ACCENT),
        TextColumn("[bold]{task.description}"),
        BarColumn(
            bar_width=20,
            style=C_DIM,
            complete_style=C_OK,
            finished_style=C_OK,
        ),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,   # mantém o bloco de progresso na tela ao finalizar
        expand=False,
    ) as progress:

        total_task = progress.add_task(
            f"[bold {C_PRIMARY}]Total[/]",
            total=len(selecionados),
        )

        for s in selecionados:
            cor_grupo = _grupo_cor(s["grupo"])
            icone     = _grupo_icone(s["grupo"])

            # Task individual: começa visível, some ao concluir
            task_id = progress.add_task(
                f"[{cor_grupo}]{icone}[/]  [{C_DIM}]{s['id']}[/]"
                f"  [{C_DIM}]{s['descricao']}[/]",
                total=1,
                visible=True,
            )

            ok, dur = executar(s)
            resultados.append((s["id"], s["descricao"], ok, dur))

            status_style = C_OK if ok else C_ERR
            status_icon  = "✔" if ok else "✘"

            # Atualiza descrição final e esconde a task individual
            progress.update(
                task_id,
                description=(
                    f"[bold {status_style}]{status_icon}[/]  "
                    f"[{cor_grupo}]{icone}[/]  [bold {C_ACCENT}]{s['id']}[/]"
                    f"  [{C_DIM}]{dur:.1f}s[/]"
                ),
                completed=1,
                visible=False,   # ← some da área de progresso ao terminar
            )
            progress.advance(total_task)

            # Imprime linha de status fora do progress (limpa, sem quebrar)
            console.log(
                f"[bold {status_style}]{status_icon}[/]  "
                f"[{cor_grupo}]{icone} {s['grupo']}[/]  "
                f"[bold {C_ACCENT}]{s['id']}[/]  "
                f"[{C_DIM}]{dur:.1f}s[/]"
            )

            time.sleep(0.3)

    _imprimir_resultados(resultados)

    n_err = sum(1 for _, _, ok, _ in resultados if not ok)
    if n_err:
        sys.exit(1)


if __name__ == "__main__":
    main()
