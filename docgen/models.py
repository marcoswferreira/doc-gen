"""
Modelos de dados (dataclasses) para o DocGen.
Representa símbolos, arquivos, módulos, métricas, diagramas e termos de domínio.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class SymbolType(str, Enum):
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    INTERFACE = "interface"
    TYPE_ALIAS = "type"
    STRUCT = "struct"
    ENUM = "enum"
    TRAIT = "trait"
    ROUTE = "route"
    CONSTANT = "constant"
    MODULE = "module"


@dataclass
class ParameterInfo:
    name: str
    type_annotation: str = ""
    default_value: str = ""

    def formatted(self) -> str:
        s = self.name
        if self.type_annotation:
            s += f": {self.type_annotation}"
        if self.default_value:
            s += f" = {self.default_value}"
        return s


@dataclass
class SymbolInfo:
    name: str
    symbol_type: SymbolType
    line_start: int = 1
    line_end: int = 1
    docstring: str = ""
    parameters: List[ParameterInfo] = field(default_factory=list)
    return_type: str = ""
    decorators: List[str] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    is_async: bool = False
    is_exported: bool = True
    route_method: str = ""  # ex: GET, POST, PUT, DELETE
    route_path: str = ""    # ex: /api/v1/users
    children: List["SymbolInfo"] = field(default_factory=list)  # métodos de uma classe, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)

    def signature(self) -> str:
        """Retorna uma assinatura formatada e legível."""
        prefix = ""
        if self.is_async:
            prefix = "async "
        if self.symbol_type == SymbolType.CLASS:
            bases = f"({', '.join(self.base_classes)})" if self.base_classes else ""
            return f"class {self.name}{bases}"
        if self.symbol_type == SymbolType.INTERFACE:
            return f"interface {self.name}"
        if self.symbol_type == SymbolType.STRUCT:
            return f"struct {self.name}"
        if self.symbol_type == SymbolType.ROUTE:
            return f"[{self.route_method or 'ROUTE'}] {self.route_path or self.name}"
        
        # Funções e Métodos
        params_str = ", ".join(p.formatted() for p in self.parameters)
        ret = f" -> {self.return_type}" if self.return_type else ""
        return f"{prefix}{self.name}({params_str}){ret}"


@dataclass
class ImportInfo:
    module: str
    symbols: List[str] = field(default_factory=list)
    is_internal: bool = False
    raw: str = ""


@dataclass
class FileInfo:
    path: str               # Caminho relativo, ex: "docgen/models.py"
    absolute_path: str      # Caminho absoluto
    language: str           # ex: "Python", "TypeScript"
    lines_total: int = 0
    lines_code: int = 0
    lines_comment: int = 0
    lines_blank: int = 0
    file_size_bytes: int = 0
    module_docstring: str = ""
    symbols: List[SymbolInfo] = field(default_factory=list)
    imports: List[ImportInfo] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)


@dataclass
class ModuleGroup:
    name: str               # ex: "docgen/parsers"
    path: str
    files: List[FileInfo] = field(default_factory=list)
    description: str = ""


@dataclass
class ProjectMetrics:
    total_files: int = 0
    total_lines: int = 0
    total_code_lines: int = 0
    total_comment_lines: int = 0
    total_blank_lines: int = 0
    language_distribution: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    symbol_counts: Dict[str, int] = field(default_factory=dict)
    docstring_ratio: float = 0.0


@dataclass
class UbiquitousTerm:
    term: str
    category: str           # "Entidade", "Value Object", "Serviço", "Operação", "Evento", "Enum"
    definition: str
    source_files: List[str] = field(default_factory=list)
    related_terms: List[str] = field(default_factory=list)


@dataclass
class ProjectData:
    root_path: str
    project_name: str
    files: List[FileInfo] = field(default_factory=list)
    modules: Dict[str, ModuleGroup] = field(default_factory=dict)
    metrics: ProjectMetrics = field(default_factory=ProjectMetrics)
    manifests: Dict[str, str] = field(default_factory=dict)
    external_dependencies: List[str] = field(default_factory=list)
    internal_dependencies: Dict[str, List[str]] = field(default_factory=dict)
    detected_frameworks: List[str] = field(default_factory=list)
    detected_arch_patterns: List[str] = field(default_factory=list)
    ubiquitous_terms: List[UbiquitousTerm] = field(default_factory=list)

