"""
Ponto de entrada da CLI do DocGen.
Orquestra a varredura, análise sintática, extração de conceitos e escrita dos Markdowns.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List, Dict

from docgen import __version__
from docgen.models import ProjectData, FileInfo
from docgen.scanner import RepositoryScanner
from docgen.parsers import ParserRegistry
from docgen.generators.doc_suite import DocSuiteGenerator
from docgen.server import start_doc_server
from docgen.ai.provider import get_ai_provider
from docgen.ui import (
    Colors,
    print_banner,
    print_step,
    print_success,
    print_info,
    print_warning,
    print_error,
    print_table,
)


def resolve_internal_dependencies(files: List[FileInfo]) -> Dict[str, List[str]]:
    """Mapeia os imports internos entre arquivos do projeto."""
    file_map = {Path(f.path).stem: f.path for f in files}
    full_path_map = {f.path: f.path for f in files}
    deps: Dict[str, List[str]] = {}

    for f in files:
        deps[f.path] = []
        for imp in f.imports:
            if not imp.is_internal:
                continue
            
            # Tenta casar com o nome do módulo
            mod_cleaned = imp.module.replace(".", "/").strip("/")
            mod_stem = Path(mod_cleaned).stem

            # Busca por correspondência exata de caminho ou stem
            for p in files:
                if p.path.startswith(mod_cleaned) or Path(p.path).stem == mod_stem:
                    if p.path != f.path and p.path not in deps[f.path]:
                        deps[f.path].append(p.path)

    return deps


def run_generate(args: argparse.Namespace) -> int:
    """Executa a análise do repositório e a geração completa da documentação."""
    repo_path = Path(args.repo or ".").resolve()
    if not repo_path.is_dir():
        print_error(f"Diretório não encontrado: {repo_path}")
        return 1

    project_name = args.title or repo_path.name
    output_dir = args.output or ("DOCUMENTATION.md" if args.single_file else "docs")

    print_banner()
    print_step(f"Iniciando análise do repositório: {Colors.BOLD}{project_name}{Colors.RESET}")
    print_info(f"Caminho alvo: {repo_path}")

    # 1. Scanner & Descoberta
    custom_ignores = args.ignore.split(",") if args.ignore else []
    scanner = RepositoryScanner(str(repo_path), custom_ignores)
    
    print_step("Varrendo arquivos e aplicando regras de exclusão...")
    discovered_files = scanner.scan()
    manifests, external_deps = scanner.detect_manifests()

    if not discovered_files:
        print_warning("Nenhum arquivo de código elegível para documentação foi encontrado.")
        return 0

    print_success(f"{len(discovered_files)} arquivos descobertos com sucesso.")

    # 2. Parsers & Análise Sintática
    print_step("Executando análise sintática e extração de símbolos (AST)...")
    registry = ParserRegistry()
    parsed_files = registry.parse_all(discovered_files)

    # 3. Métricas e Grafo
    metrics = scanner.calculate_metrics(parsed_files)
    internal_deps = resolve_internal_dependencies(parsed_files)

    project_data = ProjectData(
        root_path=str(repo_path),
        project_name=project_name,
        files=parsed_files,
        metrics=metrics,
        manifests=manifests,
        external_dependencies=external_deps,
        internal_dependencies=internal_deps,
    )

    # 4. Exibe Resumo em Tabela no Terminal
    table_rows = []
    for lang, data in list(metrics.language_distribution.items())[:6]:
        table_rows.append([lang, data["files"], f"{data['code_lines']:,}", f"{data.get('percentage', 0)}%"])

    print_table(
        headers=["Linguagem", "Arquivos", "SLOC", "% Código"],
        rows=table_rows,
        title="DISTRIBUIÇÃO DE LINGUAGENS NO REPOSITÓRIO",
    )

    # 6. Configuração e Inicialização do Motor de IA
    ai_provider = None
    force_ai = getattr(args, "ai", False) or getattr(args, "provider", None) is not None
    
    try:
        ai_provider = get_ai_provider(
            provider_name=getattr(args, "provider", None),
            model=getattr(args, "model", None),
            api_key=getattr(args, "api_key", None),
            ollama_url=getattr(args, "ollama_url", None),
        )
    except Exception as e:
        if force_ai:
            print_error(f"Erro ao inicializar provedor de IA: {e}")
            return 1
        else:
            print_warning(f"Provedor de IA não inicializado: {e}")

    if ai_provider:
        print_info(f"🧠 {Colors.BOLD}Motor de IA Ativo:{Colors.RESET} {ai_provider.name} ({ai_provider.model_name})")
    elif force_ai:
        print_error("Modo de IA solicitado, mas nenhum provedor ou chave foi configurado.")
        print_info("Defina GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY ou execute 'ollama serve' para modelos locais.")
        return 1

    # 7. Geração de Documentos
    print_step(f"Gerando suíte de documentação em Markdown: {output_dir}...")
    suite = DocSuiteGenerator(project_data, output_dir=output_dir, lang=args.lang, ai_provider=ai_provider)
    created_files = suite.generate_all(
        single_file=args.single_file,
        single_file_name=output_dir if output_dir.endswith(".md") else "DOCUMENTATION.md"
    )

    print_success(f"{len(created_files)} documento(s) gerado(s) com sucesso:")
    for cf in created_files:
        print(f"   {Colors.CYAN}•{Colors.RESET} {Path(cf).relative_to(repo_path) if cf.startswith(str(repo_path)) else cf}")

    # 7. Servidor Opcional
    if args.serve:
        start_doc_server(output_dir, port=args.port or 8080)

    print(f"\n{Colors.GREEN}{Colors.BOLD}✔ Concluído com sucesso!{Colors.RESET}\n")
    return 0


def run_stats(args: argparse.Namespace) -> int:
    """Apenas analisa e exibe métricas no terminal."""
    repo_path = Path(args.repo or ".").resolve()
    print_banner()
    print_step(f"Coletando estatísticas de: {repo_path.name}")

    scanner = RepositoryScanner(str(repo_path))
    files = scanner.scan()
    registry = ParserRegistry()
    parsed_files = registry.parse_all(files)
    metrics = scanner.calculate_metrics(parsed_files)

    table_rows = []
    for lang, data in metrics.language_distribution.items():
        table_rows.append([lang, data["files"], f"{data['code_lines']:,}", f"{data['comment_lines']:,}", f"{data.get('percentage', 0)}%"])

    print_table(
        headers=["Linguagem", "Arquivos", "SLOC", "Comentários", "% Código"],
        rows=table_rows,
        title="MÉTRICAS DETALHADAS DE CÓDIGO",
    )

    print(f" {Colors.BOLD}Total de Arquivos:{Colors.RESET} {metrics.total_files}")
    print(f" {Colors.BOLD}Linhas de Código Efetivo:{Colors.RESET} {metrics.total_code_lines:,}")
    print(f" {Colors.BOLD}Linhas de Comentários:{Colors.RESET} {metrics.total_comment_lines:,}")
    print(f" {Colors.BOLD}Taxa de Documentação:{Colors.RESET} {metrics.docstring_ratio}%\n")
    return 0


def run_init(args: argparse.Namespace) -> int:
    """Inicializa arquivos de configuração padrão."""
    repo_path = Path(".").resolve()
    docgen_json = repo_path / ".docgen.json"
    docgen_ignore = repo_path / ".docgenignore"

    if not docgen_json.exists():
        docgen_json.write_text('{\n  "title": "",\n  "output": "docs",\n  "lang": "pt",\n  "singleFile": false\n}\n', encoding="utf-8")
        print_success("Criado arquivo de configuração: .docgen.json")

    if not docgen_ignore.exists():
        docgen_ignore.write_text("# Arquivos e pastas a serem ignorados pelo DocGen\ntests/fixtures/\n*.log\n", encoding="utf-8")
        print_success("Criado arquivo de regras: .docgenignore")

    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="docgen",
        description="DocGen - Gerador Automático de Documentação Técnica e Arquitetura",
    )
    parser.add_argument("--version", action="version", version=f"docgen {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando 'generate' (ou default)
    gen_parser = subparsers.add_parser("generate", help="Gera a documentação completa")
    gen_parser.add_argument("repo", nargs="?", default=".", help="Diretório raiz do repositório a ser analisado")
    gen_parser.add_argument("-o", "--output", help="Diretório de saída para os arquivos gerados (default: docs/)")
    gen_parser.add_argument("-s", "--single-file", action="store_true", help="Gera um único arquivo DOCUMENTATION.md consolidado")
    gen_parser.add_argument("--lang", default="pt", choices=["pt", "en"], help="Idioma da documentação (default: pt)")
    gen_parser.add_argument("--title", help="Nome personalizado do projeto")
    gen_parser.add_argument("--ignore", help="Padrões extras para ignorar separados por vírgula")
    gen_parser.add_argument("--serve", action="store_true", help="Inicia o servidor de visualização local após gerar")
    gen_parser.add_argument("--port", type=int, default=8080, help="Porta do servidor local")
    # Flags de Inteligência Artificial
    gen_parser.add_argument("--ai", action="store_true", help="Ativa a síntese arquitetural profunda via Inteligência Artificial (LLM)")
    gen_parser.add_argument("--provider", choices=["gemini", "openai", "anthropic", "ollama", "mock"], help="Provedor de IA desejado")
    gen_parser.add_argument("--model", help="Nome do modelo de IA (ex: gemini-2.5-flash, gpt-4o-mini, deepseek-r1)")
    gen_parser.add_argument("--api-key", help="Chave de API do provedor (ou configurada via variáveis de ambiente)")
    gen_parser.add_argument("--ollama-url", default="http://localhost:11434", help="URL do servidor Ollama local (default: http://localhost:11434)")

    # Comando 'stats'
    stats_parser = subparsers.add_parser("stats", help="Exibe estatísticas de código no terminal")
    stats_parser.add_argument("repo", nargs="?", default=".", help="Diretório raiz do repositório")

    # Comando 'serve'
    serve_parser = subparsers.add_parser("serve", help="Inicia o servidor local de visualização de docs")
    serve_parser.add_argument("docs", nargs="?", default="docs", help="Caminho da pasta de documentos gerada")
    serve_parser.add_argument("-p", "--port", type=int, default=8080, help="Porta HTTP (default: 8080)")

    # Comando 'init'
    subparsers.add_parser("init", help="Cria arquivos de configuração inicial (.docgen.json e .docgenignore)")

    # Se nenhum argumento for passado ou o primeiro não for subcomando conhecido, assume generate
    if not argv or argv[0] not in ("generate", "stats", "serve", "init", "-h", "--help", "--version"):
        argv = ["generate"] + argv

    args = parser.parse_args(argv)

    if args.command == "generate":
        return run_generate(args)
    elif args.command == "stats":
        return run_stats(args)
    elif args.command == "serve":
        start_doc_server(args.docs, port=args.port)
        return 0
    elif args.command == "init":
        return run_init(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())

