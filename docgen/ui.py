"""
Terminal UI com cores ANSI, tabelas formatadas e indicadores visuais elegantes sem dependências externas.
"""

import sys
from typing import List, Dict, Any, Tuple


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"


def print_banner():
    """Exibe o cabeçalho estilizado do DocGen."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║   ██████╗  ██████╗  ██████╗ ██████╗ ███████╗███╗   ██╗        ║
║   ██╔══██╗██╔═══██╗██╔════╝██╔════╝ ██╔════╝████╗  ██║        ║
║   ██║  ██║██║   ██║██║     ██║  ███╗█████╗  ██╔██╗ ██║        ║
║   ██║  ██║██║   ██║██║     ██║   ██║██╔══╝  ██║╚██╗██║        ║
║   ██████╔╝╚██████╔╝╚██████╗╚██████╔╝███████╗██║ ╚████║        ║
║   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝        ║
║   {Colors.YELLOW}Gerador Automático de Documentação Técnica & Arquitetura{Colors.CYAN}    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_step(title: str, status: str = "...", end: str = "\n"):
    """Imprime uma etapa do processo."""
    print(f" {Colors.CYAN}▶{Colors.RESET} {Colors.BOLD}{title}{Colors.RESET} {Colors.DIM}{status}{Colors.RESET}", end=end, flush=True)


def print_success(title: str):
    """Imprime confirmação de sucesso."""
    print(f" {Colors.GREEN}✔{Colors.RESET} {title}")


def print_info(message: str):
    """Imprime mensagem informativa."""
    print(f" {Colors.BLUE}ℹ{Colors.RESET} {message}")


def print_warning(message: str):
    """Imprime aviso."""
    print(f" {Colors.YELLOW}⚠{Colors.RESET} {message}")


def print_error(message: str):
    """Imprime erro."""
    print(f" {Colors.RED}✖{Colors.RESET} {Colors.BOLD}{message}{Colors.RESET}")


def print_table(headers: List[str], rows: List[List[Any]], title: str = ""):
    """Renderiza uma tabela formatada com bordas Unicode no terminal."""
    if not rows:
        return

    # Converte tudo para string
    str_rows = [[str(cell) for cell in row] for row in rows]
    col_widths = [len(h) for h in headers]

    for row in str_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(cell))

    # Largura total
    total_w = sum(col_widths) + (3 * len(col_widths)) + 1

    if title:
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}  {title}{Colors.RESET}")

    # Top border
    top = "  ┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    print(f"{Colors.DIM}{top}{Colors.RESET}")

    # Header
    header_str = "  │"
    for h, w in zip(headers, col_widths):
        header_str += f" {Colors.BOLD}{h.ljust(w)}{Colors.RESET}{Colors.DIM} │"
    print(f"{header_str}{Colors.RESET}")

    # Header separator
    sep = "  ├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    print(f"{Colors.DIM}{sep}{Colors.RESET}")

    # Rows
    for row in str_rows:
        row_str = "  │"
        for cell, w in zip(row, col_widths):
            row_str += f" {cell.ljust(w)} │"
        print(f"{Colors.DIM}{row_str}{Colors.RESET}")

    # Bottom border
    bot = "  └" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
    print(f"{Colors.DIM}{bot}{Colors.RESET}\n")

