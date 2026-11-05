"""
Testes unitários para o scanner de repositório e o gerenciador de ignores.
"""

import unittest
import tempfile
from pathlib import Path

from docgen.scanner import IgnoreMatcher, detect_language, count_file_lines, RepositoryScanner
from docgen.models import FileInfo


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ignore_matcher(self):
        # Cria arquivo .gitignore
        (self.root / ".gitignore").write_text("*.log\nsecret_dir/\n", encoding="utf-8")

        matcher = IgnoreMatcher(self.root)
        
        # Deve ignorar pastas default
        self.assertTrue(matcher.is_ignored(self.root / "node_modules" / "foo.js"))
        self.assertTrue(matcher.is_ignored(self.root / ".git" / "config"))
        self.assertTrue(matcher.is_ignored(self.root / "__pycache__" / "file.pyc"))

        # Deve ignorar regras do .gitignore
        self.assertTrue(matcher.is_ignored(self.root / "app.log"))
        self.assertTrue(matcher.is_ignored(self.root / "secret_dir" / "file.txt"))

        # Não deve ignorar arquivos válidos
        self.assertFalse(matcher.is_ignored(self.root / "main.py"))
        self.assertFalse(matcher.is_ignored(self.root / "src" / "index.ts"))

    def test_detect_language(self):
        self.assertEqual(detect_language(Path("main.py")), "Python")
        self.assertEqual(detect_language(Path("app.tsx")), "TypeScript (React)")
        self.assertEqual(detect_language(Path("server.go")), "Go")
        self.assertEqual(detect_language(Path("main.rs")), "Rust")
        self.assertEqual(detect_language(Path("Dockerfile")), "Docker")
        self.assertEqual(detect_language(Path("config.json")), "JSON")

    def test_count_file_lines(self):
        py_file = self.root / "sample.py"
        py_file.write_text(
            "# Comentario\n\ndef hello():\n    # Outro comentario\n    return 'world'\n",
            encoding="utf-8",
        )

        total, code, comment, blank = count_file_lines(py_file, "Python")
        self.assertEqual(total, 5)
        self.assertEqual(comment, 2)
        self.assertEqual(blank, 1)
        self.assertEqual(code, 2)

    def test_repository_scanner_and_metrics(self):
        (self.root / "src").mkdir()
        (self.root / "src" / "app.py").write_text("print('hello')", encoding="utf-8")
        (self.root / "src" / "index.js").write_text("console.log('hi');", encoding="utf-8")

        scanner = RepositoryScanner(str(self.root))
        files = scanner.scan()
        self.assertEqual(len(files), 2)

        metrics = scanner.calculate_metrics(files)
        self.assertEqual(metrics.total_files, 2)
        self.assertIn("Python", metrics.language_distribution)
        self.assertIn("JavaScript", metrics.language_distribution)


if __name__ == "__main__":
    unittest.main()
