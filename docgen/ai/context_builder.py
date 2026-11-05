"""
Construtor de contexto semântico do repositório para o modelo de IA.
Extrai metadados, árvore de módulos, contratos do AST e trechos essenciais de código.
"""

from pathlib import Path
from typing import List, Dict, Any
from docgen.models import ProjectData, FileInfo, SymbolType


class CodebaseContextBuilder:
    """Monta o contexto técnico completo do repositório para ingestão por LLMs."""

    def __init__(self, project_data: ProjectData, max_char_budget: int = 120_000):
        self.project = project_data
        self.max_char_budget = max_char_budget

    def build_context(self) -> str:
        """Produz uma representação densa e estruturada do repositório."""
        sections = []

        # 1. Metadados do Projeto
        m = self.project.metrics
        lang_dist = ", ".join(
            f"{k} ({v.get('percentage', 0)}%)"
            for k, v in m.language_distribution.items()
        )
        meta_lines = [
            f"# REPOSITÓRIO: {self.project.project_name}",
            f"- Total de Arquivos: {m.total_files}",
            f"- Linhas de Código (SLOC): {m.total_code_lines:,}",
            f"- Distribuição de Linguagens: {lang_dist}",
        ]
        if self.project.manifests:
            meta_lines.append(f"- Manifestos Detectados: {', '.join(self.project.manifests.keys())}")
        if self.project.external_dependencies:
            meta_lines.append(f"- Principais Dependências Externas: {', '.join(self.project.external_dependencies[:25])}")

        sections.append("\n".join(meta_lines))

        # 2. Árvore e Mapeamento de Arquivos
        tree_lines = ["\n## ARQUITETURA DE ARQUIVOS E MÓDULOS:"]
        for f in self.project.files:
            sym_summary = f"{len(f.symbols)} símbolos" if f.symbols else "0 símbolos"
            tree_lines.append(f"- `{f.path}` ({f.language}, {f.lines_code} linhas, {sym_summary})")
            if f.module_docstring:
                tree_lines.append(f"  Doc: {f.module_docstring.strip().splitlines()[0]}")
        sections.append("\n".join(tree_lines))

        # 3. Contratos e Símbolos Extraídos via AST
        symbol_lines = ["\n## CONTRATOS, CLASSES E INTERFACES (VIA AST):"]
        for f in self.project.files:
            if not f.symbols:
                continue
            symbol_lines.append(f"\n### Arquivo: `{f.path}`")
            for s in f.symbols:
                symbol_lines.append(f"- {s.symbol_type.value} `{s.signature()}`")
                if s.docstring:
                    symbol_lines.append(f"  Descrição: {s.docstring.strip().splitlines()[0]}")
                for child in s.children:
                    symbol_lines.append(f"    * {child.symbol_type.value} `{child.signature()}`")
        sections.append("\n".join(symbol_lines))

        # 4. Grafo de Dependências Internas
        dep_lines = ["\n## GRAFO DE IMPORTAÇÕES INTERNAS:"]
        for src, tgts in self.project.internal_dependencies.items():
            if tgts:
                dep_lines.append(f"- `{src}` importa: {', '.join(f'`{t}`' for t in tgts)}")
        sections.append("\n".join(dep_lines))

        # 5. Código Fonte Chave (Pontos de Entrada e Modelos)
        code_lines = ["\n## CÓDIGO FONTE DOS PRINCIPAIS COMPONENTES:"]
        current_chars = sum(len(s) for s in sections)

        # Prioriza arquivos chave (core, models, cli, main, engine)
        priority_keywords = ("model", "core", "cli", "main", "app", "service", "engine", "parser", "schema", "config")
        sorted_files = sorted(
            self.project.files,
            key=lambda f: any(k in f.path.lower() for k in priority_keywords),
            reverse=True
        )

        for f in sorted_files:
            # Ignora arquivos de teste ou documentação na leitura de código bruto
            if "test" in f.path.lower() or f.language in ("Markdown", "Other", "Text"):
                continue

            try:
                content = Path(f.absolute_path).read_text(encoding="utf-8", errors="ignore")
                # Limita tamanho do arquivo a 150 linhas para não esgotar a janela
                lines = content.splitlines()[:150]
                truncated_content = "\n".join(lines)
                block = f"\n\n### Arquivo: `{f.path}`\n```{f.language.lower()}\n{truncated_content}\n```"

                if current_chars + len(block) > self.max_char_budget:
                    code_lines.append("\n... (demais arquivos omitidos pelo limite de contexto do modelo)")
                    break

                code_lines.append(block)
                current_chars += len(block)
            except Exception:
                continue

        sections.append("\n".join(code_lines))
        return "\n\n".join(sections)

