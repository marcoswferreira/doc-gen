"""
Orquestrador central de geração da suíte de documentação Markdown.
Coordena a criação de todos os artefatos técnicos, suportando modo multi-arquivos ou consolidado (--single-file).
Integra os geradores determinísticos baseados em AST com o motor de síntese de IA.
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
from docgen.generators.api_reference_generator import (
    generate_api_reference_markdown,
)
from docgen.generators.static_site_generator import build_static_html_viewer


def generate_directory_tree(files: List[str], max_depth: int = 3) -> str:
    """Gera uma árvore visual de diretórios em texto/ASCII."""
    tree_lines = ["```", "."]
    dir_set = set()

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

    def _build_ai_pending_placeholder(self, title: str, doc_type: str) -> str:
        """Gera um aviso claro quando a documentação cognitiva é requisitada sem motor de IA ativo."""
        pname = self.project.project_name
        return f"""# {title}: {pname}

> [!NOTE]
> 🧠 **Síntese de IA Pendente**: No DocGen, documentos de arquitetura cognitiva e semântica de domínio ({doc_type}) são gerados exclusivamente pelo motor de Inteligência Artificial para garantir rigor conceitual e evitar templates genéricos.

## Como gerar este documento com IA

Execute o DocGen habilitando um provedor de IA suportado:

### 1. Google Gemini (Recomendado na Nuvem)
```bash
export GEMINI_API_KEY="sua_chave_aqui"
docgen generate . --ai --provider gemini
```

### 2. Ollama Local (100% Offline e Privado)
```bash
ollama run deepseek-r1
docgen generate . --ai --provider ollama --model deepseek-r1
```

### 3. OpenAI ou Anthropic Claude
```bash
export OPENAI_API_KEY="sk-..."
docgen generate . --ai --provider openai

export ANTHROPIC_API_KEY="sk-ant-..."
docgen generate . --ai --provider anthropic
```
"""

    def _build_c4(self) -> str:
        """Sintetiza o Modelo C4 via IA ou exibe aviso pedagógico."""
        if self.ai_architect:
            try:
                return self.ai_architect.synthesize_c4()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para C4 Model: {e}.")
        return self._build_ai_pending_placeholder(
            title="Modelo C4 (Contexto, Containers, Componentes e Código)",
            doc_type="C4 Model",
        )

    def _build_hld(self) -> str:
        """Sintetiza o High-Level Design via IA ou exibe aviso pedagógico."""
        if self.ai_architect:
            try:
                return self.ai_architect.synthesize_hld()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para HLD: {e}.")
        return self._build_ai_pending_placeholder(
            title="High-Level Design (HLD)",
            doc_type="HLD",
        )

    def _build_das(self) -> str:
        """Sintetiza o Documento de Arquitetura de Software (DAS) via IA ou exibe aviso pedagógico."""
        if self.ai_architect:
            try:
                return self.ai_architect.synthesize_das()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para DAS: {e}.")
        return self._build_ai_pending_placeholder(
            title="Documento de Arquitetura de Software (DAS / Arc42)",
            doc_type="DAS",
        )

    def _build_ubiquitous_language(self) -> str:
        """Sintetiza a Linguagem Ubíqua (DDD) via IA ou exibe aviso pedagógico."""
        if self.ai_architect:
            try:
                return self.ai_architect.synthesize_ubiquitous_language()
            except Exception as e:
                print_warning(f"Falha na síntese de IA para Linguagem Ubíqua: {e}.")
        return self._build_ai_pending_placeholder(
            title="Linguagem Ubíqua e Glossário DDD",
            doc_type="Linguagem Ubíqua",
        )

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

        # 2. ARCHITECTURE.md (Diagramas Mermaid via AST)
        arch_content = self._build_architecture()
        p = self.output_path / "ARCHITECTURE.md"
        p.write_text(arch_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["ARCHITECTURE.md"] = arch_content

        # 3. C4_MODEL.md (Sintetizado com IA)
        c4_content = self._build_c4()
        p = self.output_path / "C4_MODEL.md"
        p.write_text(c4_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["C4_MODEL.md"] = c4_content

        # 4. HLD.md (Sintetizado com IA)
        hld_content = self._build_hld()
        p = self.output_path / "HLD.md"
        p.write_text(hld_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["HLD.md"] = hld_content

        # 5. DAS.md (Sintetizado com IA)
        das_content = self._build_das()
        p = self.output_path / "DAS.md"
        p.write_text(das_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["DAS.md"] = das_content

        # 6. UBIQUITOUS_LANGUAGE.md (Sintetizado com IA)
        ubiq_content = self._build_ubiquitous_language()
        p = self.output_path / "UBIQUITOUS_LANGUAGE.md"
        p.write_text(ubiq_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["UBIQUITOUS_LANGUAGE.md"] = ubiq_content

        # 7. API_REFERENCE.md (Extraído via AST)
        api_content = generate_api_reference_markdown(self.project, self.lang)
        p = self.output_path / "API_REFERENCE.md"
        p.write_text(api_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["API_REFERENCE.md"] = api_content

        # 8. DEPENDENCIES.md (Grafo de importações via AST)
        deps_content = self._build_dependencies()
        p = self.output_path / "DEPENDENCIES.md"
        p.write_text(deps_content, encoding="utf-8")
        created_files.append(str(p))
        doc_contents["DEPENDENCIES.md"] = deps_content

        # 9. METRICS.md (Métricas determinísticas de SLOC)
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
        md.append(f"> Documentação gerada pelo **DocGen**. Repositório analisado com **{m.total_files} arquivos** e **{m.total_code_lines:,} linhas de código**.")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Sumário de Navegação da Documentação")
        md.append("")
        md.append("| Documento | Escopo e Conteúdo |")
        md.append("|---|---|")
        md.append("| 🏛️ **[Modelo C4 (C4_MODEL.md)](./C4_MODEL.md)** | Visão em 4 níveis: Contexto, Containers, Componentes e Código sintetizados via IA. |")
        md.append("| 📐 **[High-Level Design (HLD.md)](./HLD.md)** | Arquitetura macro, estilo arquitetural, fronteiras e RNFs sintetizados via IA. |")
        md.append("| 📋 **[Documento de Arquitetura (DAS.md)](./DAS.md)** | Visão 4+1 e Arc42: lógica, processos, física e riscos sintetizados via IA. |")
        md.append("| 💡 **[Linguagem Ubíqua (UBIQUITOUS_LANGUAGE.md)](./UBIQUITOUS_LANGUAGE.md)** | Glossário DDD com entidades, value objects e serviços sintetizados via IA. |")
        md.append("| 🗺️ **[Arquitetura e Fluxo (ARCHITECTURE.md)](./ARCHITECTURE.md)** | Diagrama Mermaid de componentes e fluxo de dados extraídos via AST. |")
        md.append("| 📖 **[Referência de API (API_REFERENCE.md)](./API_REFERENCE.md)** | Classes, métodos, parâmetros, retornos, docstrings e tipos via AST. |")
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
            self._build_c4(),
            "---",
            self._build_hld(),
            "---",
            self._build_das(),
            "---",
            self._build_ubiquitous_language(),
            "---",
            generate_api_reference_markdown(self.project, self.lang),
            "---",
            self._build_dependencies(),
            "---",
            self._build_metrics(),
        ]
        return "\n\n".join(parts)
