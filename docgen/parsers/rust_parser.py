"""
Parser para a linguagem Rust.
Extrai structs, enums, traits, blocos impl, funções e comentários rustdoc (///).
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


class RustParser(BaseParser):
    """Parser estrutural para código Rust."""

    def can_parse(self, file_info: FileInfo) -> bool:
        return file_info.language == "Rust" or file_info.path.endswith(".rs")

    def parse(self, file_info: FileInfo) -> FileInfo:
        try:
            content = Path(file_info.absolute_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return file_info

        lines = content.splitlines()

        # 1. Imports (use crate::...;)
        for match in re.finditer(r'use\s+([^;]+);', content):
            mod_path = match.group(1).strip()
            file_info.imports.append(
                ImportInfo(
                    module=mod_path,
                    is_internal=mod_path.startswith(("crate", "super", "self")),
                    raw=match.group(0),
                )
            )

        # 2. Símbolos
        last_doc_comments = []
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()

            if stripped.startswith("///"):
                last_doc_comments.append(stripped.lstrip("/").strip())
                continue

            if not stripped:
                last_doc_comments = []
                continue

            docstring = "\n".join(last_doc_comments)
            last_doc_comments = []

            # A. Structs
            struct_match = re.search(r'^(?:pub\s+)?struct\s+([A-Za-z0-9_]+)', stripped)
            if struct_match:
                name = struct_match.group(1)
                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.STRUCT,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        is_exported="pub " in stripped,
                    )
                )
                continue

            # B. Enums
            enum_match = re.search(r'^(?:pub\s+)?enum\s+([A-Za-z0-9_]+)', stripped)
            if enum_match:
                name = enum_match.group(1)
                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.ENUM,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        is_exported="pub " in stripped,
                    )
                )
                continue

            # C. Traits
            trait_match = re.search(r'^(?:pub\s+)?trait\s+([A-Za-z0-9_]+)', stripped)
            if trait_match:
                name = trait_match.group(1)
                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.TRAIT,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        is_exported="pub " in stripped,
                    )
                )
                continue

            # D. Funções (pub fn / fn)
            fn_match = re.search(
                r'^(?:pub\s+)?(?:async\s+)?fn\s+([A-Za-z0-9_]+)\s*(?:<[^>]+>)?\s*\(([^)]*)\)(?:\s*->\s*([^{;]+))?',
                stripped,
            )
            if fn_match:
                name = fn_match.group(1)
                raw_params = fn_match.group(2)
                ret_type = fn_match.group(3).strip() if fn_match.group(3) else ""

                file_info.symbols.append(
                    SymbolInfo(
                        name=name,
                        symbol_type=SymbolType.FUNCTION,
                        line_start=line_no,
                        line_end=line_no,
                        docstring=docstring,
                        parameters=self._parse_rust_params(raw_params),
                        return_type=ret_type,
                        is_async="async " in stripped,
                        is_exported="pub " in stripped,
                    )
                )

        return file_info

    def _parse_rust_params(self, raw: str) -> list[ParameterInfo]:
        if not raw or not raw.strip():
            return []
        params = []
        for p in raw.split(","):
            p = p.strip()
            if not p:
                continue
            if ":" in p:
                pname, ptype = p.split(":", 1)
                params.append(ParameterInfo(name=pname.strip(), type_annotation=ptype.strip()))
            else:
                params.append(ParameterInfo(name=p))
        return params

