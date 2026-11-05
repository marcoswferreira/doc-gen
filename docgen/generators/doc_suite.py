"""
Orquestrador central de geração da suíte de documentação Markdown.
Coordena a criação de todos os artefatos técnicos, suportando modo multi-arquivos ou consolidado (--single-file).
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from docgen.models import ProjectData
from docgen.ai.provider import LLMProvider
from docgen.ai.architect import AIArchitect
from docgen.ui import print_info, print_warning
from docgen.generators.mermaid import (
    generate_architecture_diagram,
    generate_class_diagram,
    generate_dependency_graph,
)
from docgen.generators.c4_generator import generate_c4_documentation
from docgen.generators.architecture_generator import (
    generate_hld,
    generate_das,
)
from docgen.generators.ubiquitous_language_generator import (
    generate_ubiquitous_language_markdown,
)
from docgen.generators.api_reference_generator import (
    generate_api_reference_markdown,
)
from docgen.generators.static_site_generator import build_static_html_viewer


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

    def __init__(
        self,
        project_data: ProjectData,
        output_dir: str = "docs",
        lang: str = "pt",
        ai_provider: Optional[LLMProvider] = None,
    ):
        self.project = project_data
        self.output_path = Path(output_dir).resolve()
        self.lang = lang
        self.ai_provider = ai_provider
        self.ai_architect = AIArchitect(project_data, ai_provider, lang=lang) if ai_provider else None

    def generate_all(self, single_file: bool = False, single_file_name: str = "DOCUMENTATION.md") -> List[str]:
        """Gera todos os arquivos e retorna a lista de caminhos gravados."""
        created_files = []

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
        doc_contents: Dict[str, str] = {}

        # 1. INDEX.md
        index_content = self._build_index()
        p = self.output_path / "INDEX.md"
        p.write_text(index_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["INDEX.md"] = index_content

        # 2. ARCHITECTURE.md
        arch_content = self._build_architecture()
        p = self.output_path / "ARCHITECTURE.md"
        p.write_text(arch_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["ARCHITECTURE.md"] = arch_content

        # 3. C4_MODEL.md (Sintetizado com IA ou Heurístico)
        if self.ai_architect:
            try:
                c4_content = self.ai_architect.synthesize_c4()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para C4 Model: {e}. Usando fallback determinístico.")
                c4_content = generate_c4_documentation(self.project, self.lang)
        else:
            c4_content = generate_c4_documentation(self.project, self.lang)
        p = self.output_path / "C4_MODEL.md"
        p.write_text(c4_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["C4_MODEL.md"] = c4_content

        # 4. HLD.md (Sintetizado com IA ou Heurístico)
        if self.ai_architect:
            try:
                hld_content = self.ai_architect.synthesize_hld()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para HLD: {e}. Usando fallback determinístico.")
                hld_content = generate_hld(self.project, self.lang)
        else:
            hld_content = generate_hld(self.project, self.lang)
        p = self.output_path / "HLD.md"
        p.write_text(hld_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["HLD.md"] = hld_content

        # 5. DAS.md (Sintetizado com IA ou Heurístico)
        if self.ai_architect:
            try:
                das_content = self.ai_architect.synthesize_das()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para DAS: {e}. Usando fallback determinístico.")
                das_content = generate_das(self.project, self.lang)
        else:
            das_content = generate_das(self.project, self.lang)
        p = self.output_path / "DAS.md"
        p.write_text(das_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["DAS.md"] = das_content

        # 6. UBIQUITOUS_LANGUAGE.md (Sintetizado com IA ou Heurístico)
        if self.ai_architect:
            try:
                ubiq_content = self.ai_architect.synthesize_ubiquitous_language()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para Linguagem Ubíqua: {e}. Usando fallback determinístico.")
                ubiq_content = generate_ubiquitous_language_markdown(self.project, self.lang)
        else:
            ubiq_content = generate_ubiquitous_language_markdown(self.project, self.lang)
        p = self.output_path / "UBIQUITOUS_LANGUAGE.md"
        p.write_text(ubiq_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["UBIQUITOUS_LANGUAGE.md"] = ubiq_content

        # 7. API_REFERENCE.md
        api_content = generate_api_reference_markdown(self.project, self.lang)
        p = self.output_path / "API_REFERENCE.md"
        p.write_text(api_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["API_REFERENCE.md"] = api_content

        # 8. DEPENDENCIES.md
        deps_content = self._build_dependencies()
        p = self.output_path / "DEPENDENCIES.md"
        p.write_text(deps_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["DEPENDENCIES.md"] = deps_content

        # 9. METRICS.md
        metrics_content = self._build_metrics()
        p = self.output_path / "METRICS.md"
        p.write_text(metrics_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["METRICS.md"] = metrics_content

        # 10. index.html para GitHub Pages e Navegação Estática
        html_content = build_static_html_viewer(self.project.project_name, doc_contents)
        html_path = self.output_path / "index.html"
        html_path.write_text(html_content, encoding="utf-8")
        created_files.append(str(html_path))

        # 11. .nojekyll para GitHub Pages não filtrar arquivos
        nojekyll_path = self.output_path / ".nojekyll"
        nojekyll_path.write_text("", encoding="utf-8")

        return created_files

    def _build_index(self) -> str:
        pname = self.project.project_name
        m = self.project.metrics
        file_paths = [f.path for f in self.project.files]

        md = []
        md.append(f"# Documentação Técnica: {pname}")
        md.append("")
        if self.ai_provider:
            md.append("> [!IMPORTANT]")
            md.append(f"> 🧠 **Engenharia de IA Ativa:** Documentação analisada e sintetizada pelo motor de Inteligência Artificial **{self.ai_provider.name}** (`{self.ai_provider.model_name}`).")
            md.append("")
        md.append("> [!TIP]")
        md.append(f"> Documentação gerada pelo **DocGen**. Repositório analisado com **{m.total_files} arquivos**, **{m.total_code_lines:,} linhas de código** e **{len(self.project.ubiquitous_terms)} termos conceituais**.")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Sumário de Navegação da Documentação")
        md.append("")
        md.append("| Documento | Escopo e Conteúdo |")
        md.append("|---|---|")
        md.append("| 🏛️ **[Modelo C4 (C4_MODEL.md)](./C4_MODEL.md)** | Visão em 4 níveis: Contexto, Containers, Componentes e Código sintetizados via IA. |")
        md.append("| 📐 **[High-Level Design (HLD.md)](./HLD.md)** | Arquitetura macro, estilo arquitetural, fronteiras e RNFs. |")
        md.append("| 📋 **[Documento de Arquitetura (DAS.md)](./DAS.md)** | Visão 4+1 e Arc42: lógica, processos, física e riscos. |")
        md.append("| 💡 **[Linguagem Ubíqua (UBIQUITOUS_LANGUAGE.md)](./UBIQUITOUS_LANGUAGE.md)** | Glossário DDD com entidades, value objects, serviços e mapa conceitual. |")
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
            generate_das(self.project, self.lang),
            "---",
            generate_ubiquitous_language_markdown(self.project, self.lang),
            "---",
            generate_api_reference_markdown(self.project, self.lang),
            "---",
            self._build_dependencies(),
            "---",
            self._build_metrics(),
        ]
        return "\n\n".join(parts)
