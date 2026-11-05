"""
Testes unitários para os geradores e orquestrador de documentação:
- DocSuiteGenerator (Multi e Single-file)
- Referência de API (AST)
- Diagramas Mermaid (Arquitetura, Dependências e Classes)
- Síntese com MockProvider de IA
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
from docgen.generators.doc_suite import DocSuiteGenerator
from docgen.generators.api_reference_generator import generate_api_reference_markdown
from docgen.generators.mermaid import (
    generate_architecture_diagram,
    generate_class_diagram,
    generate_dependency_graph,
)
from docgen.ai.provider import MockProvider


class TestGenerators(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name) / "docs"

        # Cria um modelo de projeto simulado
        file1 = FileInfo(
            path="core/order_service.py",
            absolute_path="/tmp/order_service.py",
            language="Python",
            lines_total=100,
            lines_code=75,
            lines_comment=15,
            lines_blank=10,
            symbols=[
                SymbolInfo(
                    name="OrderService",
                    symbol_type=SymbolType.CLASS,
                    docstring="Serviço de gerenciamento de pedidos.",
                    children=[
                        SymbolInfo(
                            name="create_order",
                            symbol_type=SymbolType.METHOD,
                            docstring="Cria um novo pedido.",
                            parameters=[
                                ParameterInfo(name="customer_id", type_annotation="str"),
                                ParameterInfo(name="amount", type_annotation="float"),
                            ],
                            return_type="Order",
                        )
                    ]
                )
            ]
        )

        file2 = FileInfo(
            path="models/order.py",
            absolute_path="/tmp/order.py",
            language="Python",
            lines_total=50,
            lines_code=40,
            lines_comment=5,
            lines_blank=5,
            symbols=[
                SymbolInfo(
                    name="Order",
                    symbol_type=SymbolType.CLASS,
                    docstring="Entidade que representa um pedido.",
                )
            ]
        )

        metrics = ProjectMetrics(
            total_files=2,
            total_lines=150,
            total_code_lines=115,
            total_comment_lines=20,
            total_blank_lines=15,
            language_distribution={"Python": {"files": 2, "code_lines": 115, "total_lines": 150, "percentage": 100.0}},
            docstring_ratio=17.4,
        )

        self.project_data = ProjectData(
            root_path=self.temp_dir.name,
            project_name="OrderSystem",
            files=[file1, file2],
            metrics=metrics,
            internal_dependencies={"core/order_service.py": ["models/order.py"]},
            external_dependencies=["pydantic", "fastapi"],
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_api_reference_and_mermaid_generators(self):
        # 1. API Reference via AST
        api_md = generate_api_reference_markdown(self.project_data)
        self.assertIn("# Referência de API", api_md)
        self.assertIn("OrderService", api_md)
        self.assertIn("create_order", api_md)

        # 2. Diagramas Mermaid determinísticos
        arch_diagram = generate_architecture_diagram(self.project_data)
        self.assertIn("flowchart TB", arch_diagram)

        dep_graph = generate_dependency_graph(self.project_data.internal_dependencies)
        self.assertIn("graph LR", dep_graph)
        self.assertIn("order_service", dep_graph)

        class_diag = generate_class_diagram(self.project_data.files)
        self.assertIn("classDiagram", class_diag)
        self.assertIn("class OrderService", class_diag)

    def test_doc_suite_generator_with_ai(self):
        mock_ai = MockProvider(model="mock-architect")
        suite = DocSuiteGenerator(self.project_data, output_dir=str(self.output_dir), ai_provider=mock_ai)
        files = suite.generate_all(single_file=False)

        expected_files = [
            "INDEX.md",
            "ARCHITECTURE.md",
            "C4_MODEL.md",
            "HLD.md",
            "DAS.md",
            "UBIQUITOUS_LANGUAGE.md",
            "API_REFERENCE.md",
            "DEPENDENCIES.md",
            "METRICS.md",
            "index.html",
        ]

        for ef in expected_files:
            file_path = self.output_dir / ef
            self.assertTrue(file_path.is_file(), f"Arquivo esperado não encontrado: {ef}")

        # Verifica se o C4 gerado com IA contém a resposta sintetizada
        c4_text = (self.output_dir / "C4_MODEL.md").read_text(encoding="utf-8")
        self.assertIn("Mock AI Provider", c4_text)

    def test_doc_suite_generator_without_ai(self):
        suite = DocSuiteGenerator(self.project_data, output_dir=str(self.output_dir))
        files = suite.generate_all(single_file=False)

        c4_text = (self.output_dir / "C4_MODEL.md").read_text(encoding="utf-8")
        self.assertIn("Síntese de IA Pendente", c4_text)
        self.assertIn("export GEMINI_API_KEY", c4_text)

    def test_doc_suite_generator_single_file(self):
        single_path = self.output_dir / "DOCUMENTATION.md"
        suite = DocSuiteGenerator(self.project_data, output_dir=str(self.output_dir))
        files = suite.generate_all(single_file=True, single_file_name="DOCUMENTATION.md")

        self.assertEqual(len(files), 1)
        self.assertTrue(single_path.is_file())
        content = single_path.read_text(encoding="utf-8")
        self.assertIn("Modelo C4", content)
        self.assertIn("High-Level Design", content)
        self.assertIn("Linguagem Ubíqua", content)


if __name__ == "__main__":
    unittest.main()
