# Arquitetura e Fluxo de Dados: doc-gen

## Diagrama de Componentes e Módulos
```mermaid
flowchart TB
    subgraph sub_root["Módulo: root"]
        pyproject_toml["pyproject.toml<br/>(TOML, 0 símbolos)"]
        setup_py["setup.py<br/>(Python, 0 símbolos)"]
    end
    subgraph sub_docgen["Módulo: docgen"]
        docgen_scanner_py["scanner.py<br/>(Python, 4 símbolos)"]
        docgen___main___py["__main__.py<br/>(Python, 0 símbolos)"]
        docgen_cli_py["cli.py<br/>(Python, 5 símbolos)"]
        docgen_models_py["models.py<br/>(Python, 9 símbolos)"]
        docgen_config_py["config.py<br/>(Python, 1 símbolos)"]
        docgen_server_py["server.py<br/>(Python, 3 símbolos)"]
        docgen_ui_py["ui.py<br/>(Python, 8 símbolos)"]
        docgen___init___py["__init__.py<br/>(Python, 0 símbolos)"]
        sub_docgen_more["... +20 arquivos"]
    end
    tests_test_cli_py --> docgen_cli_py
    tests_test_python_parser_py --> docgen_models_py
    tests_test_python_parser_py --> docgen_parsers_python_parser_py
    tests_test_js_parser_py --> docgen_models_py
    tests_test_js_parser_py --> docgen_parsers_js_ts_parser_py
    tests_test_ai_py --> docgen_models_py
    tests_test_ai_py --> docgen_ai_provider_py
    tests_test_ai_py --> docgen_ai_context_builder_py
    tests_test_ai_py --> docgen_ai_architect_py
    tests_test_ai_py --> docgen_generators_doc_suite_py
    tests_test_generators_py --> docgen_models_py
    tests_test_generators_py --> docgen_generators_c4_generator_py
    tests_test_generators_py --> docgen_generators_architecture_generator_py
    tests_test_generators_py --> docgen_generators_ubiquitous_language_generator_py
    tests_test_generators_py --> docgen_generators_doc_suite_py
    tests_test_scanner_py --> docgen_scanner_py
    tests_test_scanner_py --> docgen_models_py
    docgen_scanner_py --> docgen_config_py
    docgen_scanner_py --> docgen_models_py
    docgen___main___py --> docgen_cli_py
    docgen_cli_py --> docgen_scanner_py
    docgen_cli_py --> docgen___main___py
    docgen_cli_py --> docgen_models_py
    docgen_cli_py --> docgen_config_py
    docgen_cli_py --> docgen_server_py
    docgen_server_py --> docgen_ui_py
    docgen_generators_c4_generator_py --> docgen_models_py
    docgen_generators_c4_generator_py --> docgen_config_py
    docgen_generators_c4_generator_py --> docgen_generators_mermaid_py
    docgen_generators_ubiquitous_language_generator_py --> docgen_models_py
    docgen_generators_ubiquitous_language_generator_py --> docgen_generators_mermaid_py
    docgen_generators_api_reference_generator_py --> docgen_models_py
    docgen_generators_doc_suite_py --> docgen_models_py
    docgen_generators_doc_suite_py --> docgen_ai_provider_py
    docgen_generators_doc_suite_py --> docgen_ai_architect_py
    docgen_generators_doc_suite_py --> docgen_ui_py
    docgen_generators_doc_suite_py --> docgen_generators_mermaid_py
    docgen_generators_mermaid_py --> docgen_models_py
    docgen_generators_architecture_generator_py --> docgen_models_py
    docgen_generators_architecture_generator_py --> docgen_config_py
    docgen_parsers_base_py --> docgen_models_py
    docgen_parsers_js_ts_parser_py --> docgen_models_py
    docgen_parsers_js_ts_parser_py --> docgen_parsers_base_py
    docgen_parsers_go_parser_py --> docgen_models_py
    docgen_parsers_go_parser_py --> docgen_parsers_base_py
    docgen_parsers_rust_parser_py --> docgen_models_py
    docgen_parsers_rust_parser_py --> docgen_parsers_base_py
    docgen_parsers_java_parser_py --> docgen_models_py
    docgen_parsers_java_parser_py --> docgen_parsers_base_py
    docgen_parsers_generic_parser_py --> docgen_models_py
    docgen_parsers_generic_parser_py --> docgen_parsers_base_py
    docgen_parsers_python_parser_py --> docgen_models_py
    docgen_parsers_python_parser_py --> docgen_parsers_base_py
    docgen_parsers___init___py --> docgen_models_py
    docgen_parsers___init___py --> docgen_parsers_base_py
    docgen_parsers___init___py --> docgen_parsers_python_parser_py
    docgen_parsers___init___py --> docgen_parsers_js_ts_parser_py
    docgen_parsers___init___py --> docgen_parsers_go_parser_py
    docgen_ai_context_builder_py --> docgen_models_py
    docgen_ai_architect_py --> docgen_models_py
    docgen_ai_architect_py --> docgen_ai_provider_py
    docgen_ai_architect_py --> docgen_ai_context_builder_py
    docgen_ai_architect_py --> docgen_ai_prompts_py
    docgen_ai_architect_py --> docgen_ui_py
    docgen_ai___init___py --> docgen_ai_provider_py
    docgen_ai___init___py --> docgen_ai_architect_py
```

---

## Diagrama de Classes e Entidades
```mermaid
classDiagram
    class IgnoreMatcher {
        +init()
        -load_file()
        +is_ignored() bool
    }
    class RepositoryScanner {
        +init()
        +scan() List
        +calculate_metrics() ProjectMetrics
        +detect_manifests() Tuple
    }
    class SymbolType {
    }
    class ParameterInfo {
        +formatted() str
    }
    class SymbolInfo {
        +signature() str
    }
    class ImportInfo {
    }
    class FileInfo {
    }
    class ModuleGroup {
    }
    class ProjectMetrics {
    }
    class UbiquitousTerm {
    }
    class ProjectData {
    }
    class DocViewerHandler {
        +do_GET()
    }
    class Colors {
    }
    class DocSuiteGenerator {
        +init()
        +generate_all() List
        -build_index() str
        -build_architecture() str
        -build_dependencies() str
        -build_metrics() str
    }
    class BaseParser {
        +can_parse() bool
        +parse() FileInfo
    }
    class JsTsParser {
        +can_parse() bool
        +parse() FileInfo
        -extract_imports()
        -extract_jsdocs() dict
        -parse_ts_params() List
    }
    class GoParser {
        +can_parse() bool
        +parse() FileInfo
        -extract_imports()
        -parse_go_params() list
    }
    class RustParser {
        +can_parse() bool
        +parse() FileInfo
        -parse_rust_params() list
    }
    class JavaParser {
        +can_parse() bool
        +parse() FileInfo
        -parse_params() list
    }
    class GenericParser {
        +can_parse() bool
        +parse() FileInfo
    }
    class PythonParser {
        +can_parse() bool
        +parse() FileInfo
        -extract_import()
        -extract_class() SymbolInfo
        -extract_function() SymbolInfo
    }
    class ParserRegistry {
        +init()
        +parse_file() FileInfo
        +parse_all() List
    }
    class CodebaseContextBuilder {
        +init()
        +build_context() str
    }
    class LLMProvider {
        +generate() str
        +name() str
        +model_name() str
    }
    class GeminiProvider {
        +init()
        +name() str
        +model_name() str
        +generate() str
    }
    BaseParser <|-- JsTsParser
    BaseParser <|-- GoParser
    BaseParser <|-- RustParser
    BaseParser <|-- JavaParser
    BaseParser <|-- GenericParser
    BaseParser <|-- PythonParser
    LLMProvider <|-- GeminiProvider
```
