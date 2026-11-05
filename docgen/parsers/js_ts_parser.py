"""
Parser para JavaScript e TypeScript (incluindo TSX/JSX).
Extrai classes, interfaces, tipos, funções, imports, exports, JSDoc e rotas Express/Next.js.
"""

import re
from pathlib import Path
from typing import List, Optional

from docgen.models import (
    FileInfo,
    SymbolInfo,
    SymbolType,
    ParameterInfo,
    ImportInfo,
)
from docgen.parsers.base import BaseParser


class JsTsParser(BaseParser):
    """Parser estrutural e regex para JavaScript e TypeScript."""

    def can_parse(self, file_info: FileInfo) -> bool:
        return file_info.language in (
            "JavaScript",
            "JavaScript (React)",
            "TypeScript",
            "TypeScript (React)",
        ) or file_info.path.endswith((".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"))

    def parse(self, file_info: FileInfo) -> FileInfo:
        try:
            content = Path(file_info.absolute_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return file_info

        lines = content.splitlines()

        # 1. Extração de Imports
        self._extract_imports(content, file_info)

        # 2. Extração de Comentários JSDoc associados a linhas
        jsdoc_blocks = self._extract_jsdocs(content)

        # 3. Análise linha a linha / estrutural
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                continue

            # JSDoc precedente se existir
            docstring = jsdoc_blocks.get(line_no, "")

            # A. Classes
            class_match = re.search(
                r'^(?:export\s+)?(?:default\s+)?class\s+([A-Za-z0-9_$]+)(?:\s+extends\s+([A-Za-z0-9_$.]+))?(?:\s+implements\s+([^{]+))?',
                stripped,
            )
            if class_match:
                cls_name = class_match.group(1)
                base_cls = [b.strip() for b in class_match.group(2).split(",")] if class_match.group(2) else []
                if class_match.group(3):
                    base_cls.extend([b.strip() for b in class_match.group(3).split(",")])

                file_info.symbols.append(
                    SymbolInfo(
                        name=cls_name,
                        symbol_type=SymbolType.CLASS,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        base_classes=base_cls,
                        is_exported="export" in stripped,
                    )
                )
                continue

            # B. Interfaces TypeScript
            if "interface " in stripped:
                if_match = re.search(
                    r'^(?:export\s+)?interface\s+([A-Za-z0-9_$]+)(?:\s+extends\s+([^{]+))?',
                    stripped,
                )
                if if_match:
                    name = if_match.group(1)
                    bases = [b.strip() for b in if_match.group(2).split(",")] if if_match.group(2) else []
                    file_info.symbols.append(
                        SymbolInfo(
                            name=name,
                            symbol_type=SymbolType.INTERFACE,
                            line_start=line_no,
                            line_end=line_no,
                            docstring=docstring,
                            base_classes=bases,
                            is_exported="export" in stripped,
                        )
                    )
                    continue

            # C. Type Aliases TypeScript
            if "type " in stripped and "=" in stripped:
                type_match = re.search(r'^(?:export\s+)?type\s+([A-Za-z0-9_$]+)', stripped)
                if type_match:
                    name = type_match.group(1)
                    file_info.symbols.append(
                        SymbolInfo(
                            name=name,
                            symbol_type=SymbolType.TYPE_ALIAS,
                            line_start=line_no,
                            line_end=line_no,
                            docstring=docstring,
                            is_exported="export" in stripped,
                        )
                    )
                    continue

            # D. Funções nomeadas padrão: [export] [async] function name(...)
            fn_match = re.search(
                r'^(?:export\s+)?(?:default\s+)?(async\s+)?function\s+([A-Za-z0-9_$]+)\s*\(([^)]*)\)(?:\s*:\s*([^{]+))?',
                stripped,
            )
            if fn_match:
                is_async = bool(fn_match.group(1))
                name = fn_match.group(2)
                raw_params = fn_match.group(3)
                ret_type = fn_match.group(4).strip() if fn_match.group(4) else ""

                # Next.js Route Handlers (GET, POST, PUT, DELETE, PATCH)
                if name in ("GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS") and "export" in stripped:
                    file_info.symbols.append(
                        SymbolInfo(
                            name=f"{name} Handler",
                            symbol_type=SymbolType.ROUTE,
                            line_start=line_no,
                            line_end=line_no,
                            docstring=docstring,
                            route_method=name,
                            route_path=f"/{file_info.path.replace('app/', '').replace('/route.ts', '').replace('/route.js', '')}",
                            is_async=is_async,
                        )
                    )
                    continue

                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.FUNCTION,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        parameters=self._parse_ts_params(raw_params),
                        return_type=ret_type,
                        is_async=is_async,
                        is_exported="export" in stripped,
                    )
                )
                continue

            # E. Arrow Functions: [export] const name = [async] (...) =>
            arrow_match = re.search(
                r'^(?:export\s+)?(?:const|let|var)\s+([A-Za-z0-9_$]+)\s*=\s*(async\s+)?(?:\(([^)]*)\)|([A-Za-z0-9_$]+))\s*(?::\s*([A-Za-z0-9_$<>, ]+))?\s*=>',
                stripped,
            )
            if arrow_match:
                name = arrow_match.group(1)
                is_async = bool(arrow_match.group(2))
                raw_params = arrow_match.group(3) or arrow_match.group(4) or ""
                ret_type = arrow_match.group(5).strip() if arrow_match.group(5) else ""

                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.FUNCTION,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        parameters=self._parse_ts_params(raw_params),
                        return_type=ret_type,
                        is_async=is_async,
                        is_exported="export" in stripped,
                    )
                )
                continue

            # F. Express / Fastify Routes: (app|router).(get|post|put|delete)('/path', ...)
            route_match = re.search(
                r'(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
                stripped,
                re.IGNORECASE,
            )
            if route_match:
                method = route_match.group(1).upper()
                route_path = route_match.group(2)
                file_info.symbols.append(
                    SymbolInfo(
                        name=f"{method} {route_path}",
                        symbol_type=SymbolType.ROUTE,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        route_method=method,
                        route_path=route_path,
                    )
                )

        return file_info

    def _extract_imports(self, content: str, file_info: FileInfo) -> None:
        """Extrai declarações import e require."""
        # ES6 imports: import { X, Y } from 'mod' ou import X from 'mod'
        es6_pattern = re.compile(
            r'import\s+(?:(?:\*\s+as\s+[A-Za-z0-9_$]+|[A-Za-z0-9_$,\s{}]+)\s+from\s+)?[\'"]([^\'"]+)[\'"]'
        )
        for match in es6_pattern.finditer(content):
            mod_path = match.group(1)
            is_internal = mod_path.startswith(("./", "../", "@/"))
            file_info.imports.append(
                ImportInfo(
                    module=mod_path,
                    is_internal=is_internal,
                    raw=match.group(0),
                )
            )

        # CommonJS require: const x = require('mod')
        cjs_pattern = re.compile(r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)')
        for match in cjs_pattern.finditer(content):
            mod_path = match.group(1)
            is_internal = mod_path.startswith(("./", "../", "@/"))
            file_info.imports.append(
                ImportInfo(
                    module=mod_path,
                    is_internal=is_internal,
                    raw=match.group(0),
                )
            )

    def _extract_jsdocs(self, content: str) -> dict[int, str]:
        """Associa blocos de comentário JSDoc à linha subsequente de código."""
        docs: dict[int, str] = {}
        pattern = re.compile(r'/\*\*(.*?)\*/', re.DOTALL)
        lines = content.splitlines()

        for match in pattern.finditer(content):
            # Encontra em qual linha o JSDoc termina
            end_pos = match.end()
            line_no = content[:end_pos].count("\n") + 1

            raw_doc = match.group(1)
            cleaned_doc = []
            for dline in raw_doc.splitlines():
                dstripped = dline.strip().lstrip("*").strip()
                if dstripped:
                    cleaned_doc.append(dstripped)
            full_doc = "\n".join(cleaned_doc)

            # Procura a primeira linha não-vazia seguinte
            target_line = line_no + 1
            while target_line <= len(lines):
                if lines[target_line - 1].strip():
                    docs[target_line] = full_doc
                    break
                target_line += 1

        return docs

    def _parse_ts_params(self, raw: str) -> List[ParameterInfo]:
        """Faz o parse de parâmetros tipados de TypeScript/JavaScript."""
        if not raw or not raw.strip():
            return []

        params: List[ParameterInfo] = []
        # Divide por vírgula preservando tipos complexos
        parts = raw.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Exemplo: name: string = "default"
            param_name = part
            param_type = ""
            param_default = ""

            if "=" in part:
                left, right = part.split("=", 1)
                part = left.strip()
                param_default = right.strip()

            if ":" in part:
                name_part, type_part = part.split(":", 1)
                param_name = name_part.strip().rstrip("?")
                param_type = type_part.strip()
            else:
                param_name = part.strip()

            params.append(
                ParameterInfo(
                    name=param_name,
                    type_annotation=param_type,
                    default_value=param_default,
                )
            )

        return params
