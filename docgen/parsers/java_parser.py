"""
Parser para Java, C# e Kotlin.
Extrai classes, interfaces, records, métodos, anotações e comentários Javadoc.
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


class JavaParser(BaseParser):
    """Parser para linguagens orientadas a objetos baseadas em classes (Java, C#, Kotlin)."""

    def can_parse(self, file_info: FileInfo) -> bool:
        return file_info.language in ("Java", "C#", "Kotlin") or file_info.path.endswith(
            (".java", ".cs", ".kt")
        )

    def parse(self, file_info: FileInfo) -> FileInfo:
        try:
            content = Path(file_info.absolute_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return file_info

        lines = content.splitlines()

        # 1. Imports
        for match in re.finditer(r'(?:import|using)\s+([^;]+);', content):
            mod_path = match.group(1).strip()
            file_info.imports.append(
                ImportInfo(
                    module=mod_path,
                    is_internal=not mod_path.startswith(("java.", "javax.", "System.", "org.springframework")),
                    raw=match.group(0),
                )
            )

        # 2. Símbolos
        last_comments = []
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()

            if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
                last_comments.append(stripped.lstrip("/* ").rstrip("*/").strip())
                continue

            if not stripped:
                last_comments = []
                continue

            docstring = "\n".join(c for c in last_comments if c)
            last_comments = []

            # Classes e Records
            class_match = re.search(
                r'^(?:public|protected|private)?\s*(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(?:class|record)\s+([A-Za-z0-9_]+)(?:\s+extends\s+([A-Za-z0-9_.]+))?(?:\s+implements\s+([^{]+))?',
                stripped,
            )
            if class_match:
                name = class_match.group(1)
                bases = []
                if class_match.group(2):
                    bases.append(class_match.group(2).strip())
                if class_match.group(3):
                    bases.extend([b.strip() for b in class_match.group(3).split(",")])

                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.CLASS,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        base_classes=bases,
                        is_exported="public" in stripped,
                    )
                )
                continue

            # Interfaces
            if_match = re.search(
                r'^(?:public|protected|private)?\s*interface\s+([A-Za-z0-9_]+)',
                stripped,
            )
            if if_match:
                name = if_match.group(1)
                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.INTERFACE,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        is_exported="public" in stripped,
                    )
                )
                continue

            # Métodos
            method_match = re.search(
                r'^(?:public|protected|private)?\s*(?:static\s+)?(?:final\s+)?([A-Za-z0-9_<>[\]]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)(?:\s*throws\s+[^{;]+)?',
                stripped,
            )
            if method_match:
                ret_type = method_match.group(1)
                name = method_match.group(2)
                raw_params = method_match.group(3)

                # Ignora palavras reservadas como 'if', 'for', 'while', 'switch'
                if name in ("if", "for", "while", "switch", "catch"):
                    continue

                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.METHOD,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        parameters=self._parse_params(raw_params),
                        return_type=ret_type,
                        is_exported="public" in stripped,
                    )
                )

        return file_info

    def _parse_params(self, raw: str) -> list[ParameterInfo]:
        if not raw or not raw.strip():
            return []
        params = []
        for p in raw.split(","):
            p = p.strip()
            if not p:
                continue
            parts = p.split()
            if len(parts) >= 2:
                ptype = parts[-2]
                name = parts[-1]
                params.append(ParameterInfo(name=name, type_annotation=ptype))
            else:
                params.append(ParameterInfo(name=p))
        return params
