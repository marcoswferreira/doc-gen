"""
Registro e orquestração de parsers de código.
"""

from typing import List
from docgen.models import FileInfo
from docgen.parsers.base import BaseParser
from docgen.parsers.python_parser import PythonParser
from docgen.parsers.js_ts_parser import JsTsParser
from docgen.parsers.go_parser import GoParser
from docgen.parsers.rust_parser import RustParser
from docgen.parsers.java_parser import JavaParser
from docgen.parsers.generic_parser import GenericParser


class ParserRegistry:
    """Gerencia a lista de parsers disponíveis e aplica o mais adequado a cada arquivo."""

    def __init__(self):
        self.parsers: List[BaseParser] = [
            PythonParser(),
            JsTsParser(),
            GoParser(),
            RustParser(),
            JavaParser(),
            GenericParser(),  # Fallback final
        ]

    def parse_file(self, file_info: FileInfo) -> FileInfo:
        """Aplica o primeiro parser que aceitar o arquivo."""
        for parser in self.parsers:
            if parser.can_parse(file_info):
                return parser.parse(file_info)
        return file_info

    def parse_all(self, files: List[FileInfo]) -> List[FileInfo]:
        """Processa todos os arquivos da lista."""
        parsed = []
        for f in files:
            parsed.append(self.parse_file(f))
        return parsed
