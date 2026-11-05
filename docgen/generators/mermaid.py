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

    # Identifica pastas de primeiro nível como camadas/módulos, focando em arquivos de código
    modules: Dict[str, List[FileInfo]] = {}
    for f in project.files:
        # Ignora arquivos de documentação pura ou pastas ocultas/testes no diagrama principal
        if f.language in ("Markdown", "Other", "Text") and not f.symbols:
            continue
        parts = Path(f.path).parts
        if parts[0] in (".github", "tests"):
            continue
        mod = parts[0] if len(parts) > 1 else "root"
        if mod not in modules:
            modules[mod] = []
        modules[mod].append(f)

    # Cria subgrafos por módulo
    for mod_name, files in modules.items():
        mod_id = f"sub_{sanitize_id(mod_name)}"
        lines.append(f'    subgraph {mod_id}["Módulo: {mod_name}"]')
        for f in files[:8]:  # Limita para manter o diagrama limpo e legível
            fid = sanitize_id(f.path)
            sym_count = len(f.symbols)
            label = f"{Path(f.path).name}<br/>({f.language}, {sym_count} símbolos)"
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


IGNORED_BASE_CLASSES = {
    "str", "int", "float", "bool", "dict", "list", "set", "tuple",
    "object", "any", "enum", "type", "abc", "unittest", "testcase",
    "unittest_testcase", "baseexception", "exception", "basehttprequesthandler",
}


def is_test_file(path: str) -> bool:
    """Verifica se o arquivo é um arquivo de teste."""
    p = path.lower()
    return "test" in p or p.startswith("tests/") or p.startswith("test_")


def sanitize_method_for_mermaid(method) -> str:
    """Sanitiza o nome e retorno do método para sintaxe estrita do Mermaid classDiagram."""
    name = method.name
    if name.startswith("__") and name.endswith("__"):
        if "init" in name:
            clean_name = "init"
            visibility = "+"
        else:
            return ""
    elif name.startswith("_"):
        clean_name = name.lstrip("_")
        visibility = "-"
    else:
        clean_name = name
        visibility = "+"

    clean_name = "".join(c for c in clean_name if c.isalnum() or c == "_")
    if not clean_name:
        return ""

    ret = ""
    if method.return_type:
        raw_ret = method.return_type.split("[")[0].split("(")[0].strip()
        clean_ret = "".join(c for c in raw_ret if c.isalnum())
        if clean_ret and clean_ret.lower() not in ("none", "void", "object"):
            ret = f" {clean_ret}"

    return f"        {visibility}{clean_name}(){ret}"


def generate_class_diagram(files: List[FileInfo]) -> str:
    """Gera um diagrama de classes Mermaid válido para entidades e classes de domínio."""
    domain_classes = []
    # Prioriza arquivos de domínio (fora da pasta de testes)
    for f in files:
        if is_test_file(f.path):
            continue
        for s in f.symbols:
            if s.symbol_type == SymbolType.CLASS:
                domain_classes.append((f, s))

    if not domain_classes:
        for f in files:
            for s in f.symbols:
                if s.symbol_type == SymbolType.CLASS:
                    domain_classes.append((f, s))

    if not domain_classes:
        return ""

    lines = ["```mermaid", "classDiagram"]
    known_classes: Set[str] = set()

    for f, cls in domain_classes[:25]:
        cls_id = sanitize_id(cls.name)
        if not cls_id or cls_id.lower() in IGNORED_BASE_CLASSES:
            continue

        known_classes.add(cls_id)
        lines.append(f"    class {cls_id} {{")
        for m in cls.children[:6]:
            m_str = sanitize_method_for_mermaid(m)
            if m_str:
                lines.append(m_str)
        lines.append("    }")

    # Relações de herança válidas (apenas entre classes conhecidas no diagrama)
    for f, cls in domain_classes[:25]:
        cls_id = sanitize_id(cls.name)
        if cls_id not in known_classes:
            continue
        for base in cls.base_classes:
            base_id = sanitize_id(base)
            if not base_id or base_id.lower() in IGNORED_BASE_CLASSES or base_id not in known_classes:
                continue
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

