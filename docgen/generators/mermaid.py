"""
Gerador de diagramas Mermaid para arquitetura, componentes, dependências e classes.
"""

from typing import List, Dict, Set
from pathlib import Path
from docgen.models import FileInfo, SymbolType, ProjectData


def sanitize_id(text: str) -> str:
    """Sanitiza strings para identificadores válidos em nós Mermaid."""
    return "".join(c if c.isalnum() else "_" for c in text).strip("_")


def generate_architecture_diagram(project: ProjectData) -> str:
    """Gera um diagrama de arquitetura em alto nível agrupando módulos em subgraphs."""
    lines = ["```mermaid", "flowchart TB"]

    # Identifica pastas de primeiro nível como camadas/módulos
    modules: Dict[str, List[FileInfo]] = {}
    for f in project.files:
        parts = Path(f.path).parts
        mod = parts[0] if len(parts) > 1 else "root"
        if mod not in modules:
            modules[mod] = []
        modules[mod].append(f)

    # Cria subgrafos por módulo
    for mod_name, files in modules.items():
        mod_id = f"sub_{sanitize_id(mod_name)}"
        lines.append(f'    subgraph {mod_id}["Módulo: {mod_name}"]')
        for f in files[:8]:  # Limita para não sobrecarregar o diagrama
            fid = sanitize_id(f.path)
            sym_count = len(f.symbols)
            label = f"{Path(f.path).name}\\n({f.language}, {sym_count} símbolos)"
            lines.append(f'        {fid}["{label}"]')
        if len(files) > 8:
            more_id = f"{mod_id}_more"
            lines.append(f'        {more_id}["... +{len(files) - 8} arquivos"]')
        lines.append("    end")

    # Adiciona arestas de dependências internas
    added_edges: Set[str] = set()
    for src_file, targets in project.internal_dependencies.items():
        src_id = sanitize_id(src_file)
        for tgt in targets[:5]:
            tgt_id = sanitize_id(tgt)
            edge = f"{src_id} --> {tgt_id}"
            if edge not in added_edges and src_id != tgt_id:
                lines.append(f"    {edge}")
                added_edges.add(edge)

    lines.append("```")
    return "\n".join(lines)


def generate_class_diagram(files: List[FileInfo]) -> str:
    """Gera um diagrama de classes Mermaid para entidades e classes detectadas."""
    classes = []
    for f in files:
        for s in f.symbols:
            if s.symbol_type == SymbolType.CLASS:
                classes.append((f, s))

    if not classes:
        return ""

    lines = ["```mermaid", "classDiagram"]
    for f, cls in classes[:25]:  # Limita a 25 classes principais
        cls_id = sanitize_id(cls.name)
        lines.append(f"    class {cls_id} {{")
        # Métodos da classe
        for m in cls.children[:6]:
            ret = f": {m.return_type}" if m.return_type else ""
            lines.append(f"        +{m.name}(){ret}")
        lines.append("    }")

        # Herança
        for base in cls.base_classes:
            base_id = sanitize_id(base)
            lines.append(f"    {base_id} <|-- {cls_id}")

    lines.append("```")
    return "\n".join(lines)


def generate_dependency_graph(internal_deps: Dict[str, List[str]]) -> str:
    """Gera o grafo de dependências internas entre módulos do projeto."""
    lines = ["```mermaid", "graph LR"]
    edges: Set[str] = set()

    for src, targets in internal_deps.items():
        src_id = sanitize_id(src)
        src_name = Path(src).name
        for tgt in targets:
            tgt_id = sanitize_id(tgt)
            tgt_name = Path(tgt).name
            edge = f'    {src_id}["{src_name}"] --> {tgt_id}["{tgt_name}"]'
            if edge not in edges and src_id != tgt_id:
                lines.append(edge)
                edges.add(edge)

    if len(lines) == 2:
        lines.append('    info["Sem dependências circulares ou mapeadas"]')

    lines.append("```")
    return "\n".join(lines)
