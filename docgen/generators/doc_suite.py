"""
Orquestrador central de geração da suíte de documentação Markdown.
Coordena a criação de todos os artefatos técnicos, suportando modo multi-arquivos ou consolidado (--single-file).
"""

import os
from pathlib import Path
from typing import Dict, List

from docgen.models import ProjectData
from docgen.generators.mermaid import (
    generate_architecture_diagram,
    generate_class_diagram,
    generate_dependency_graph,
)
from docgen.generators.c4_generator import generate_c4_documentation
from docgen.generators.architecture_generator import (
    generate_hld,
    generate_lld,
    generate_das,
)
from docgen.generators.adr_generator import (
    synthesize_project_adrs,
    generate_adrs_index_markdown,
    generate_adr_template,
)
from docgen.generators.ubiquitous_language_generator import (
    generate_ubiquitous_language_markdown,
)
from docgen.generators.api_reference_generator import (
    generate_api_reference_markdown,
)


def generate_directory_tree(files: List[str], max_depth: int = 3) -> str:
    """Gera uma árvore visual de diretórios em texto/ASCII."""
    tree_lines = ["```", "."]
    dir_set = set()

    # Agrupa por estrutura de diretórios
    for f in sorted(files):
        parts = Path(f).parts
        for i in range(1, min(len(parts) + 1, max_depth + 1)):
            dir_set.add(parts[:i])

    sorted_paths = sorted(list(dir_set), key=lambda p: (len(p), p))
    for p in sorted_paths:
        indent = "  " * (len(p) - 1)
        prefix = "├── " if len(p) > 1 else ""
        tree_lines.append(f"{indent}{prefix}{p[-1]}")

    tree_lines.append("```")
    return "\n".join(tree_lines)


class DocSuiteGenerator:
    """Orquestra a escrita dos documentos Markdown."""

    def __init__(self, project_data: ProjectData, output_dir: str = "docs", lang: str = "pt"):
        self.project = project_data
        self.output_path = Path(output_dir).resolve()
        self.lang = lang

    def generate_all(self, single_file: bool = False, single_file_name: str = "DOCUMENTATION.md") -> List[str]:
        """Gera todos os arquivos e retorna a lista de caminhos gravados."""
        created_files = []

        # Certifica que os ADRs foram sintetizados/lidos
        self.project.adrs = synthesize_project_adrs(self.project)

        if single_file:
            if self.output_path.suffix.lower() == ".md":
                single_path = self.output_path
                single_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                self.output_path.mkdir(parents=True, exist_ok=True)
                single_path = self.output_path / single_file_name

            content = self._build_consolidated_documentation()
            single_path.write_text(content, encoding="utf-8")
            return [str(single_path)]

        self.output_path.mkdir(parents=True, exist_ok=True)

        # 1. INDEX.md
        index_content = self._build_index()
        p = self.output_path / "INDEX.md"
        p.write_text(index_content, encoding="utf-8")
        created_files.append(str(p))

        # 2. ARCHITECTURE.md
        arch_content = self._build_architecture()
        p = self.output_path / "ARCHITECTURE.md"
        p.write_text(arch_content, encoding="utf-8")
        created_files.append(str(p))

        # 3. C4_MODEL.md
        c4_content = generate_c4_documentation(self.project, self.lang)
        p = self.output_path / "C4_MODEL.md"
        p.write_text(c4_content, encoding="utf-8")
        created_files.append(str(p))

        # 4. HLD.md
        hld_content = generate_hld(self.project, self.lang)
        p = self.output_path / "HLD.md"
        p.write_text(hld_content, encoding="utf-8")
        created_files.append(str(p))

        # 5. LLD.md
        lld_content = generate_lld(self.project, self.lang)
        p = self.output_path / "LLD.md"
        p.write_text(lld_content, encoding="utf-8")
        created_files.append(str(p))

        # 6. DAS.md
        das_content = generate_das(self.project, self.lang)
        p = self.output_path / "DAS.md"
        p.write_text(das_content, encoding="utf-8")
        created_files.append(str(p))

        # 7. UBIQUITOUS_LANGUAGE.md
        ubiq_content = generate_ubiquitous_language_markdown(self.project, self.lang)
        p = self.output_path / "UBIQUITOUS_LANGUAGE.md"
        p.write_text(ubiq_content, encoding="utf-8")
        created_files.append(str(p))

        # 8. ADRs
        adrs_dir = self.output_path / "adrs"
        adrs_dir.mkdir(exist_ok=True)
        # Template
        template_path = adrs_dir / "ADR_TEMPLATE.md"
        template_path.write_text(generate_adr_template(), encoding="utf-8")
        # ADRs individuais
        for adr in self.project.adrs:
            slug = adr.title.lower().replace(" ", "-").replace(":", "").replace("/", "-")
            adr_file = adrs_dir / f"ADR-{adr.number:03d}-{slug}.md"
            adr_md = f"# ADR-{adr.number:03d}: {adr.title}\n\n## Status\n`{adr.status}`\n\n## Contexto\n{adr.context}\n\n## Decisão\n{adr.decision}\n\n## Consequências\n{adr.consequences}\n\n## Data\n{adr.date}\n"
            adr_file.write_text(adr_md, encoding="utf-8")
        
        adrs_index = generate_adrs_index_markdown(self.project.adrs, self.project.project_name)
        p = self.output_path / "ADRS.md"
        p.write_text(adrs_index, encoding="utf-8")
        created_files.append(str(p))

        # 9. API_REFERENCE.md
        api_content = generate_api_reference_markdown(self.project, self.lang)
        p = self.output_path / "API_REFERENCE.md"
        p.write_text(api_content, encoding="utf-8")
        created_files.append(str(p))

        # 10. DEPENDENCIES.md
        deps_content = self._build_dependencies()
        p = self.output_path / "DEPENDENCIES.md"
        p.write_text(deps_content, encoding="utf-8")
        created_files.append(str(p))

        # 11. METRICS.md
        metrics_content = self._build_metrics()
        p = self.output_path / "METRICS.md"
        p.write_text(metrics_content, encoding="utf-8")
        created_files.append(str(p))

        return created_files

    def _build_index(self) -> str:
        pname = self.project.project_name
        m = self.project.metrics
        file_paths = [f.path for f in self.project.files]

        md = []
        md.append(f"# Documentação Técnica: {pname}")
        md.append("")
        md.append("> [!TIP]")
        md.append(f"> Documentação gerada automaticamente pelo **DocGen**. Repositório analisado com **{m.total_files} arquivos**, **{m.total_code_lines:,} linhas de código** e **{len(self.project.ubiquitous_terms)} termos conceituais**.")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Sumário de Navegação da Documentação")
        md.append("")
        md.append("| Documento | Escopo e Conteúdo |")
        md.append("|---|---|")
        md.append("| 🏛️ **[Modelo C4 (C4_MODEL.md)](./C4_MODEL.md)** | Visão em 4 níveis: Contexto, Containers, Componentes e Código. |")
        md.append("| 📐 **[High-Level Design (HLD.md)](./HLD.md)** | Arquitetura macro, estilo arquitetural, fronteiras e RNFs. |")
        md.append("| ⚙️ **[Low-Level Design (LLD.md)](./LLD.md)** | Padrões de projeto, estruturas de dados e diagrama de sequência. |")
        md.append("| 📋 **[Documento de Arquitetura (DAS.md)](./DAS.md)** | Visão 4+1 e Arc42: lógica, processos, física e riscos. |")
        md.append("| 💡 **[Linguagem Ubíqua (UBIQUITOUS_LANGUAGE.md)](./UBIQUITOUS_LANGUAGE.md)** | Glossário DDD com entidades, value objects, serviços e mapa conceitual. |")
        md.append("| ⚖️ **[Decisões de Arquitetura (ADRS.md)](./ADRS.md)** | Registro formal de ADRs (Architecture Decision Records) e template. |")
        md.append("| 🗺️ **[Arquitetura e Fluxo (ARCHITECTURE.md)](./ARCHITECTURE.md)** | Diagrama Mermaid de componentes e fluxo de dados. |")
        md.append("| 📖 **[Referência de API (API_REFERENCE.md)](./API_REFERENCE.md)** | Classes, métodos, parâmetros, retornos, docstrings e tipos. |")
        md.append("| 📦 **[Dependências (DEPENDENCIES.md)](./DEPENDENCIES.md)** | Pacotes externos e grafo de importações internas. |")
        md.append("| 📊 **[Métricas do Projeto (METRICS.md)](./METRICS.md)** | SLOC, comentários, taxa de documentação e linguagens. |")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Estrutura de Diretórios")
        md.append(generate_directory_tree(file_paths, max_depth=3))
        md.append("")

        return "\n".join(md)

    def _build_architecture(self) -> str:
        pname = self.project.project_name
        md = []
        md.append(f"# Arquitetura e Fluxo de Dados: {pname}")
        md.append("")
        md.append("## Diagrama de Componentes e Módulos")
        md.append(generate_architecture_diagram(self.project))
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Diagrama de Classes e Entidades")
        class_diag = generate_class_diagram(self.project.files)
        if class_diag:
            md.append(class_diag)
        else:
            md.append("*Nenhum grafo de classes complexo identificado.*")
        md.append("")
        return "\n".join(md)

    def _build_dependencies(self) -> str:
        pname = self.project.project_name
        md = []
        md.append(f"# Dependências do Projeto: {pname}")
        md.append("")
        md.append("## Grafo de Dependências Internas")
        md.append(generate_dependency_graph(self.project.internal_dependencies))
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Dependências Externas Registradas")
        if self.project.external_dependencies:
            md.append("| Pacote / Dependência |")
            md.append("|---|")
            for dep in self.project.external_dependencies:
                md.append(f"| `{dep}` |")
        else:
            md.append("*Nenhuma dependência externa registrada em arquivos de manifesto.*")
        md.append("")
        return "\n".join(md)

    def _build_metrics(self) -> str:
        pname = self.project.project_name
        m = self.project.metrics
        md = []
        md.append(f"# Métricas de Código e Estatísticas: {pname}")
        md.append("")
        md.append("## Resumo Geral")
        md.append(f"- **Arquivos Totais Analisados:** {m.total_files}")
        md.append(f"- **Linhas Totais:** {m.total_lines:,}")
        md.append(f"- **Linhas de Código Efetivo (SLOC):** {m.total_code_lines:,}")
        md.append(f"- **Linhas de Comentários:** {m.total_comment_lines:,}")
        md.append(f"- **Linhas em Branco:** {m.total_blank_lines:,}")
        md.append(f"- **Taxa de Documentação / Comentários:** {m.docstring_ratio}%")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Distribuição por Linguagem")
        md.append("")
        md.append("| Linguagem | Arquivos | Linhas de Código | Total Linhas | % Código |")
        md.append("|---|---|---|---|---|")
        for lang, data in m.language_distribution.items():
            md.append(f"| **{lang}** | {data['files']} | {data['code_lines']:,} | {data['total_lines']:,} | {data.get('percentage', 0)}% |")
        md.append("")
        return "\n".join(md)

    def _build_consolidated_documentation(self) -> str:
        """Gera um único arquivo DOCUMENTATION.md contendo todas as seções."""
        parts = [
            self._build_index(),
            "---",
            self._build_architecture(),
            "---",
            generate_c4_documentation(self.project, self.lang),
            "---",
            generate_hld(self.project, self.lang),
            "---",
            generate_lld(self.project, self.lang),
            "---",
            generate_das(self.project, self.lang),
            "---",
            generate_ubiquitous_language_markdown(self.project, self.lang),
            "---",
            generate_adrs_index_markdown(self.project.adrs, self.project.project_name),
            "---",
            generate_api_reference_markdown(self.project, self.lang),
            "---",
            self._build_dependencies(),
            "---",
            self._build_metrics(),
        ]
        return "\n\n".join(parts)
