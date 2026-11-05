"""
Testes unitários para todos os geradores de documentação técnica e arquitetural:
- C4 Model
- HLD / LLD / DAS
- ADRs
- Linguagem Ubíqua (DDD)
- DocSuiteGenerator (Multi e Single-file)
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
from docgen.generators.c4_generator import generate_c4_documentation
from docgen.generators.architecture_generator import generate_hld, generate_lld, generate_das
from docgen.generators.adr_generator import synthesize_project_adrs, generate_adrs_index_markdown
from docgen.generators.ubiquitous_language_generator import extract_ubiquitous_terms, generate_ubiquitous_language_markdown
from docgen.generators.doc_suite import DocSuiteGenerator


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

    def test_c4_model_generation(self):
        c4_md = generate_c4_documentation(self.project_data)
        self.assertIn("# Modelo C4: OrderSystem", c4_md)
        self.assertIn("Nível 1: Diagrama de Contexto", c4_md)
        self.assertIn("Nível 2: Diagrama de Containers", c4_md)
        self.assertIn("Nível 3: Diagrama de Componentes", c4_md)
        self.assertIn("Nível 4: Diagrama de Código", c4_md)
        self.assertIn("```mermaid", c4_md)

    def test_hld_lld_das_generation(self):
        hld_md = generate_hld(self.project_data)
        self.assertIn("# High-Level Design (HLD): OrderSystem", hld_md)
        self.assertIn("Requisitos Não-Funcionais", hld_md)

        lld_md = generate_lld(self.project_data)
        self.assertIn("# Low-Level Design (LLD): OrderSystem", lld_md)
        self.assertIn("sequenceDiagram", lld_md)

        das_md = generate_das(self.project_data)
        self.assertIn("# Documento de Arquitetura de Software (DAS): OrderSystem", das_md)
        self.assertIn("Visão Lógica (Logical View)", das_md)
        self.assertIn("Visão de Implantação", das_md)

    def test_adr_generation(self):
        adrs = synthesize_project_adrs(self.project_data)
        self.assertGreaterEqual(len(adrs), 4)

        index_md = generate_adrs_index_markdown(adrs, "OrderSystem")
        self.assertIn("# Registro de Decisões Arquiteturais (ADRs): OrderSystem", index_md)
        self.assertIn("ADR-001", index_md)

    def test_ubiquitous_language_generation(self):
        terms = extract_ubiquitous_terms(self.project_data)
        term_names = [t.term for t in terms]
        self.assertIn("OrderService", term_names)
        self.assertIn("Order", term_names)

        ubiq_md = generate_ubiquitous_language_markdown(self.project_data)
        self.assertIn("# Linguagem Ubíqua (Glossário DDD): OrderSystem", ubiq_md)
        self.assertIn("Mapa Conceitual do Domínio", ubiq_md)
        self.assertIn("Glossário de Termos do Negócio", ubiq_md)

    def test_doc_suite_generator_multi_file(self):
        suite = DocSuiteGenerator(self.project_data, output_dir=str(self.output_dir))
        files = suite.generate_all(single_file=False)

        expected_files = [
            "INDEX.md",
            "ARCHITECTURE.md",
            "C4_MODEL.md",
            "HLD.md",
            "LLD.md",
            "DAS.md",
            "UBIQUITOUS_LANGUAGE.md",
            "ADRS.md",
            "API_REFERENCE.md",
            "DEPENDENCIES.md",
            "METRICS.md",
        ]

        for ef in expected_files:
            file_path = self.output_dir / ef
            self.assertTrue(file_path.is_file(), f"Arquivo esperado não encontrado: {ef}")

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
