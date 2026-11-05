"""
Testes unitários para o analisador de código Python via AST.
"""

import unittest
import tempfile
from pathlib import Path

from docgen.models import FileInfo, SymbolType
from docgen.parsers.python_parser import PythonParser


class TestPythonParser(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.parser = PythonParser()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_classes_and_methods(self):
        code = '''"""Modulo de teste"""
from typing import Optional

class Animal:
    """Classe base animal"""
    pass

class Dog(Animal):
    """Classe cachorro"""
    def __init__(self, name: str, age: int = 1):
        self.name = name
        self.age = age

    async def bark(self, volume: int = 10) -> str:
        """Emite latido"""
        return "Woof!"
'''
        file_path = self.root / "models.py"
        file_path.write_text(code, encoding="utf-8")

        f_info = FileInfo(
            path="models.py",
            absolute_path=str(file_path),
            language="Python",
        )

        parsed = self.parser.parse(f_info)

        self.assertEqual(parsed.module_docstring, "Modulo de teste")
        self.assertEqual(len(parsed.symbols), 2)  # Animal e Dog

        dog_cls = parsed.symbols[1]
        self.assertEqual(dog_cls.name, "Dog")
        self.assertEqual(dog_cls.base_classes, ["Animal"])
        self.assertEqual(len(dog_cls.children), 2)  # __init__ e bark

        bark_method = dog_cls.children[1]
        self.assertEqual(bark_method.name, "bark")
        self.assertTrue(bark_method.is_async)
        self.assertEqual(bark_method.return_type, "str")
        self.assertEqual(len(bark_method.parameters), 1)
        self.assertEqual(bark_method.parameters[0].name, "volume")
        self.assertEqual(bark_method.parameters[0].default_value, "10")

    def test_parse_routes(self):
        code = '''
@app.get("/api/v1/users")
def get_users():
    """Retorna lista de usuarios"""
    return []
'''
        file_path = self.root / "routes.py"
        file_path.write_text(code, encoding="utf-8")

        f_info = FileInfo(
            path="routes.py",
            absolute_path=str(file_path),
            language="Python",
        )

        parsed = self.parser.parse(f_info)
        self.assertEqual(len(parsed.symbols), 1)
        route = parsed.symbols[0]
        self.assertEqual(route.symbol_type, SymbolType.ROUTE)
        self.assertEqual(route.route_method, "GET")
        self.assertEqual(route.route_path, "/api/v1/users")


if __name__ == "__main__":
    unittest.main()
