"""
Classe base para parsers de linguagem do DocGen.
"""

from abc import ABC, abstractmethod
from docgen.models import FileInfo


class BaseParser(ABC):
    """Contrato base para analisadores de código fonte."""

    @abstractmethod
    def can_parse(self, file_info: FileInfo) -> bool:
        """Retorna True se o parser suporta o arquivo informado."""
        pass

    @abstractmethod
    def parse(self, file_info: FileInfo) -> FileInfo:
        """
        Executa a análise sintática e semântica do arquivo,
        preenchendo símbolos, imports, exports e docstring do módulo.
        """
        pass
