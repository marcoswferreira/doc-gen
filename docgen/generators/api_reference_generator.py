"""
Gerador de referência de API e catálogo detalhado de classes, métodos e funções.
"""

from typing import List
from pathlib import Path
from docgen.models import ProjectData, FileInfo, SymbolInfo, SymbolType


def generate_api_reference_markdown(project: ProjectData, lang: str = "pt") -> str:
    """Gera o documento API_REFERENCE.md."""
    pname = project.project_name

    md = []
    md.append(f"# Referência de API e Símbolos: {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> Esta seção fornece a documentação técnica detalhada das interfaces, classes, métodos, funções e rotas expostas pelo código-fonte.")
    md.append("")
    md.append("---")
    md.append("")

    # Sumário de Módulos
    md.append("## Módulos Documentados")
    md.append("")
    md.append("| Módulo / Arquivo | Linguagem | Símbolos | SLOC |")
    md.append("|---|---|---|---|")

    # Filtra apenas arquivos com símbolos ou código relevante
    doc_files = [f for f in project.files if f.symbols or f.lines_code > 0]
    for f in doc_files:
        anchor = f.path.lower().replace("/", "-").replace(".", "-")
        md.append(f"| [{f.path}](#{anchor}) | {f.language} | {len(f.symbols)} | {f.lines_code} |")

    md.append("")
    md.append("---")
    md.append("")

    # Detalhe por Arquivo
    for f in doc_files:
        anchor = f.path.lower().replace("/", "-").replace(".", "-")
        md.append(f"<a id='{anchor}'></a>")
        md.append(f"## Arquivo: `{f.path}`")
        md.append(f"**Linguagem:** {f.language} | **Linhas de Código:** {f.lines_code} | **Comentários:** {f.lines_comment}")
        md.append("")

        if f.module_docstring:
            md.append("### Descrição do Módulo")
            md.append(f"> {f.module_docstring.strip()}")
            md.append("")

        if not f.symbols:
            md.append("*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*")
            md.append("")
            md.append("---")
            md.append("")
            continue

        for s in f.symbols:
            md.append(f"### `{s.symbol_type.value}` {s.name}")
            if s.decorators:
                md.append("```python")
                for d in s.decorators:
                    md.append(d)
                md.append(s.signature())
                md.append("```")
            else:
                lang_code = "python" if f.language == "Python" else ("typescript" if "TypeScript" in f.language else "javascript")
                md.append(f"```{lang_code}")
                md.append(s.signature())
                md.append("```")

            if s.docstring:
                md.append("")
                md.append(s.docstring.strip())

            # Tabela de parâmetros
            if s.parameters:
                md.append("")
                md.append("#### Parâmetros")
                md.append("| Nome | Tipo | Default |")
                md.append("|---|---|---|")
                for p in s.parameters:
                    t = f"`{p.type_annotation}`" if p.type_annotation else "*any*"
                    d = f"`{p.default_value}`" if p.default_value else "-"
                    md.append(f"| `{p.name}` | {t} | {d} |")

            # Métodos internos de classes
            if s.children:
                md.append("")
                md.append("#### Métodos da Classe")
                for m in s.children:
                    md.append(f"- **`{m.name}`**`({', '.join(p.name for p in m.parameters)})`" + (f" -> `{m.return_type}`" if m.return_type else ""))
                    if m.docstring:
                        md.append(f"  - *{m.docstring.strip().splitlines()[0]}*")

            md.append("")

        md.append("---")
        md.append("")

    return "\n".join(md)

