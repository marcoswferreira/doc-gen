"""
Parser para a linguagem Go.
Extrai pacotes, structs, interfaces, funções, métodos (com receivers) e imports.
"""

import re
from pathlib import Path
from docgen.models import (
    FileInfo,
    SymbolInfo,
    SymbolType,
    ParameterInfo,
    ImportInfo,
)
from docgen.parsers.base import BaseParser


class GoParser(BaseParser):
    """Parser estrutural para código Go."""

    def can_parse(self, file_info: FileInfo) -> bool:
        return file_info.language == "Go" or file_info.path.endswith(".go")

    def parse(self, file_info: FileInfo) -> FileInfo:
        try:
            content = Path(file_info.absolute_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return file_info

        lines = content.splitlines()

        # 1. Imports
        self._extract_imports(content, file_info)

        # 2. Símbolos (struct, interface, func)
        last_comments = []
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()

            if stripped.startswith("//"):
                last_comments.append(stripped.lstrip("/").strip())
                continue

            if not stripped:
                last_comments = []
                continue

            docstring = "\n".join(last_comments)
            last_comments = []

            # A. Structs
            struct_match = re.search(r'^type\s+([A-Za-z0-9_]+)\s+struct\b', stripped)
            if struct_match:
                name = struct_match.group(1)
                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.STRUCT,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        is_exported=name[0].isupper(),
                    )
                )
                continue

            # B. Interfaces
            if_match = re.search(r'^type\s+([A-Za-z0-9_]+)\s+interface\b', stripped)
            if if_match:
                name = if_match.group(1)
                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.INTERFACE,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        is_exported=name[0].isupper(),
                    )
                )
                continue

            # C. Métodos: func (r *Receiver) MethodName(...) ...
            method_match = re.search(
                r'^func\s*\(([^)]+)\)\s*([A-Za-z0-9_]+)\s*\(([^)]*)\)(?:\s*([^{]+))?',
                stripped,
            )
            if method_match:
                receiver = method_match.group(1).strip()
                name = method_match.group(2)
                raw_params = method_match.group(3)
                ret_type = method_match.group(4).strip() if method_match.group(4) else ""

                file_info.symbols.append(
                    SymbolInfo(
                        name=f"({receiver}) {name}",
                        symbol_type=SymbolType.METHOD,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        parameters=self._parse_go_params(raw_params),
                        return_type=ret_type,
                        is_exported=name[0].isupper(),
                    )
                )
                continue

            # D. Funções normais: func FunctionName(...) ...
            func_match = re.search(
                r'^func\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)(?:\s*([^{]+))?',
                stripped,
            )
            if func_match:
                name = func_match.group(1)
                raw_params = func_match.group(2)
                ret_type = func_match.group(3).strip() if func_match.group(3) else ""

                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.FUNCTION,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        parameters=self._parse_go_params(raw_params),
                        return_type=ret_type,
                        is_exported=name[0].isupper(),
                    )
                )

        return file_info

    def _extract_imports(self, content: str, file_info: FileInfo) -> None:
        single_imports = re.findall(r'import\s+[\'"]([^\'"]+)[\'"]', content)
        for imp in single_imports:
            file_info.imports.append(
                ImportInfo(module=imp, is_internal=imp.startswith((".", "/")), raw=f'import "{imp}"')
            )

        block_match = re.search(r'import\s*\(([^)]+)\)', content)
        if block_match:
            for line in block_match.group(1).splitlines():
                line = line.strip().strip('"')
                if line:
                    file_info.imports.append(
                        ImportInfo(
                            module=line,
                            is_internal=line.startswith((".", "/")),
                            raw=f'"{line}"',
                        )
                    )

    def _parse_go_params(self, raw: str) -> list[ParameterInfo]:
        if not raw or not raw.strip():
            return []
        params = []
        for p in raw.split(","):
            p = p.strip()
            if not p:
                continue
            parts = p.split()
            if len(parts) >= 2:
                name = parts[0]
                ptype = " ".join(parts[1:])
                params.append(ParameterInfo(name=name, type_annotation=ptype))
            else:
                params.append(ParameterInfo(name=p))
        return params

