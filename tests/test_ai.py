"""
Testes unitários para o subsistema de Engenharia de IA do DocGen.
Valida o construtor de contexto, os provedores de LLM e o AIArchitect.
"""

import unittest
import tempfile
from pathlib import Path

from docgen.models import (
    ProjectData,
    FileInfo,
    SymbolInfo,
    SymbolType,
    ParameterInfo,
    ProjectMetrics,
)
from docgen.ai.provider import MockProvider, get_ai_provider
from docgen.ai.context_builder import CodebaseContextBuilder
from docgen.ai.architect import AIArchitect
from docgen.generators.doc_suite import DocSuiteGenerator
from docgen.cli import main


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        # Arquivo de modelo de domínio
        models_py = self.root / "models.py"
        models_py.write_text(
            '"""Modulo de dados"""\nclass User:\n    """Entidade de usuario"""\n    def __init__(self, name: str):\n        self.name = name\n',
            encoding="utf-8"
        )

        f_info = FileInfo(
            path="models.py",
            absolute_path=str(models_py),
            language="Python",
            lines_total=6,
            lines_code=5,
            lines_comment=1,
            lines_blank=0,
            symbols=[
                SymbolInfo(
                    name="User",
                    symbol_type=SymbolType.CLASS,
                    docstring="Entidade de usuario",
                )
            ]
        )

        self.project_data = ProjectData(
            root_path=str(self.root),
            project_name="TestAIApp",
            files=[f_info],
            metrics=ProjectMetrics(total_files=1, total_code_lines=5, total_lines=6),
            external_dependencies=["fastapi", "sqlalchemy"],
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_context_builder(self):
        builder = CodebaseContextBuilder(self.project_data)
        context = builder.build_context()

        self.assertIn("REPOSITÓRIO: TestAIApp", context)
        self.assertIn("models.py", context)
        self.assertIn("fastapi", context)
        self.assertIn("User", context)

    def test_ai_architect_synthesis(self):
        provider = MockProvider(model="mock-architect-v1")
        architect = AIArchitect(self.project_data, provider, lang="pt")

        c4_doc = architect.synthesize_c4()
        self.assertTrue(len(c4_doc) > 0)

        hld_doc = architect.synthesize_hld()
        self.assertTrue(len(hld_doc) > 0)

        das_doc = architect.synthesize_das()
        self.assertTrue(len(das_doc) > 0)

        ubiq_doc = architect.synthesize_ubiquitous_language()
        self.assertTrue(len(ubiq_doc) > 0)

    def test_doc_suite_with_ai_provider(self):
        provider = MockProvider()
        out_dir = self.root / "docs_ai"
        suite = DocSuiteGenerator(self.project_data, output_dir=str(out_dir), lang="pt", ai_provider=provider)
        created = suite.generate_all(single_file=False)

        self.assertIn(str(out_dir / "C4_MODEL.md"), created)
        self.assertIn(str(out_dir / "INDEX.md"), created)

        index_text = (out_dir / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("Engenharia de IA Ativa", index_text)

    def test_cli_ai_flags(self):
        out_dir = self.root / "docs_cli_ai"
        code = main(["generate", str(self.root), "-o", str(out_dir), "--ai", "--provider", "mock"])
        self.assertEqual(code, 0)
        self.assertTrue((out_dir / "C4_MODEL.md").is_file())


if __name__ == "__main__":
    unittest.main()

