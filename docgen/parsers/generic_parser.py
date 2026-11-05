"""
Parser genérico para arquivos de configuração, scripts shell, SQL, Dockerfile, etc.
Extrai comentários de cabeçalho, instruções principais e variáveis.
"""

from pathlib import Path
from docgen.models import FileInfo, SymbolInfo, SymbolType
from docgen.parsers.base import BaseParser


class GenericParser(BaseParser):
    """Parser de fallback para qualquer arquivo de código ou configuração."""

    def can_parse(self, file_info: FileInfo) -> bool:
        return True  # Fallback geral

    def parse(self, file_info: FileInfo) -> FileInfo:
        try:
            content = Path(file_info.absolute_path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return file_info

        lines = content.splitlines()
        header_comments = []

        # Extrai comentários de cabeçalho (descrição do arquivo)
        for line in lines[:20]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("#", "//", "/*", "*", "--")):
                cleaned = stripped.lstrip("#/*- ").rstrip("*/")
                if cleaned and not cleaned.startswith("!/"):  # ignora shebang
                    header_comments.append(cleaned)
            else:
                break

        if header_comments:
            file_info.module_docstring = "\n".join(header_comments)

        # Extração de instruções para Dockerfile
        if file_info.language == "Docker":
            for line_no, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith(("FROM", "RUN", "CMD", "ENTRYPOINT", "EXPOSE", "ENV")):
                    parts = stripped.split(maxsplit=1)
                    instruction = parts[0]
                    value = parts[1] if len(parts) > 1 else ""
                    file_info.symbols.append(
                        SymbolInfo(
                            name=f"{instruction} {value}",
                            symbol_type=SymbolType.CONSTANT,
                            line_start=line_no,
                            line_end=line_no,
                            docstring="",
                        )
                    )

        return file_info
