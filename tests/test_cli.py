"""
Testes unitários para os comandos da CLI do DocGen.
"""

import unittest
import tempfile
from pathlib import Path
from docgen.cli import main


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        # Cria uma estrutura de teste
        (self.root / "app").mkdir()
        (self.root / "app" / "main.py").write_text(
            '"""Modulo principal"""\n\ndef run():\n    return 42\n',
            encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cli_stats(self):
        code = main(["stats", str(self.root)])
        self.assertEqual(code, 0)

    def test_cli_generate_multi(self):
        out_dir = self.root / "docs_out"
        code = main(["generate", str(self.root), "-o", str(out_dir)])
        self.assertEqual(code, 0)
        self.assertTrue((out_dir / "INDEX.md").is_file())
        self.assertTrue((out_dir / "C4_MODEL.md").is_file())
        self.assertTrue((out_dir / "HLD.md").is_file())
        self.assertTrue((out_dir / "LLD.md").is_file())
        self.assertTrue((out_dir / "DAS.md").is_file())
        self.assertTrue((out_dir / "UBIQUITOUS_LANGUAGE.md").is_file())
        self.assertTrue((out_dir / "ADRS.md").is_file())

    def test_cli_generate_single_file(self):
        single_doc = self.root / "SINGLE_DOC.md"
        code = main(["generate", str(self.root), "-s", "-o", str(single_doc)])
        self.assertEqual(code, 0)
        self.assertTrue(single_doc.is_file())
        content = single_doc.read_text(encoding="utf-8")
        self.assertIn("Modelo C4", content)
        self.assertIn("Linguagem Ubíqua", content)


if __name__ == "__main__":
    unittest.main()
