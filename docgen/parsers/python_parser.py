"""
Parser de código Python utilizando o módulo AST nativo.
Extrai classes, herança, métodos, funções, decoradores, anotações de tipo e imports.
"""

import ast
from pathlib import Path
from typing import List, Optional, Any

from docgen.models import (
    FileInfo,
    SymbolInfo,
    SymbolType,
    ParameterInfo,
    ImportInfo,
)
from docgen.parsers.base import BaseParser


def _format_annotation(node: Optional[ast.AST]) -> str:
    """Converte um nó AST de anotação de tipo em string legível."""
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return ""


def _format_decorator(node: ast.AST) -> str:
    """Converte um nó AST de decorador em string."""
    try:
        return f"@{ast.unparse(node)}"
    except Exception:
        return "@decorator"


class PythonParser(BaseParser):
    """Parser para arquivos Python usando AST."""

    def can_parse(self, file_info: FileInfo) -> bool:
        return file_info.language == "Python" or file_info.path.endswith((".py", ".pyw"))

    def parse(self, file_info: FileInfo) -> FileInfo:
        try:
            content = Path(file_info.absolute_path).read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(content, filename=file_info.path)
        except Exception:
            # Fallback se o arquivo tiver erro de sintaxe
            return file_info

        # Docstring do módulo
        file_info.module_docstring = ast.get_docstring(tree) or ""

        # Itera sobre os nós de nível superior
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self._extract_import(node, file_info)
            elif isinstance(node, ast.ClassDef):
                sym = self._extract_class(node)
                file_info.symbols.append(sym)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                sym = self._extract_function(node, is_method=False)
                file_info.symbols.append(sym)
            elif isinstance(node, ast.Assign):
                # Constantes de nível de módulo (ex: ALL_CAPS = ...)
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        file_info.symbols.append(
                            SymbolInfo(
                                name=target.id,
                                symbol_type=SymbolType.CONSTANT,
                                line_start=node.lineno,
                                line_end=node.end_lineno or node.lineno,
                                docstring="",
                            )
                        )

        return file_info

    def _extract_import(self, node: ast.AST, file_info: FileInfo) -> None:
        if isinstance(node, ast.Import):
            for alias in node.names:
                file_info.imports.append(
                    ImportInfo(
                        module=alias.name,
                        symbols=[alias.asname or alias.name],
                        is_internal=not alias.name.startswith(
                            ("os", "sys", "re", "json", "ast", "math", "typing", "collections", "datetime")
                        ),
                        raw=f"import {alias.name}",
                    )
                )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            syms = [alias.name for alias in node.names]
            # Se for relativo (node.level > 0), é interno
            is_internal = node.level > 0 or not mod.startswith(
                ("os", "sys", "re", "json", "ast", "math", "typing", "collections", "datetime")
            )
            file_info.imports.append(
                ImportInfo(
                    module=mod,
                    symbols=syms,
                    is_internal=is_internal,
                    raw=f"from {'.' * node.level}{mod} import {', '.join(syms)}",
                )
            )

    def _extract_class(self, node: ast.ClassDef) -> SymbolInfo:
        base_classes = [_format_annotation(b) for b in node.bases]
        decorators = [_format_decorator(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node) or ""

        methods: List[SymbolInfo] = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(self._extract_function(item, is_method=True))

        return SymbolInfo(
            name=node.name,
            symbol_type=SymbolType.CLASS,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            decorators=decorators,
            base_classes=base_classes,
            children=methods,
        )

    def _extract_function(
        self, node: Any, is_method: bool = False
    ) -> SymbolInfo:
        decorators = [_format_decorator(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node) or ""
        return_type = _format_annotation(node.returns)
        is_async = isinstance(node, ast.AsyncFunctionDef)

        # Parâmetros
        params: List[ParameterInfo] = []
        args_obj = node.args

        # Positional / Standard args
        total_args = len(args_obj.args)
        num_defaults = len(args_obj.defaults)
        default_offset = total_args - num_defaults

        for i, arg in enumerate(args_obj.args):
            # Em métodos, 'self' ou 'cls' não precisam de anotação
            if is_method and i == 0 and arg.arg in ("self", "cls"):
                continue

            param_name = arg.arg
            param_type = _format_annotation(arg.annotation)
            param_default = ""

            if i >= default_offset:
                def_node = args_obj.defaults[i - default_offset]
                try:
                    param_default = ast.unparse(def_node)
                except Exception:
                    param_default = "..."

            params.append(
                ParameterInfo(
                    name=param_name,
                    type_annotation=param_type,
                    default_value=param_default,
                )
            )

        # Detecta rotas em decoradores (ex: @app.get("/users"), @router.post("/items"))
        route_method = ""
        route_path = ""
        for dec in decorators:
            dec_lower = dec.lower()
            for verb in ["get", "post", "put", "delete", "patch", "options", "head"]:
                if f".{verb}(" in dec_lower:
                    route_method = verb.upper()
                    # Tenta extrair o path da string do decorador
                    import re
                    match = re.search(r'[\'"]([^\'"]+)[\'"]', dec)
                    if match:
                        route_path = match.group(1)
                    break

        sym_type = SymbolType.METHOD if is_method else (
            SymbolType.ROUTE if route_method else SymbolType.FUNCTION
        )

        return SymbolInfo(
            name=node.name,
            symbol_type=sym_type,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            parameters=params,
            return_type=return_type,
            decorators=decorators,
            is_async=is_async,
            route_method=route_method,
            route_path=route_path,
        )

