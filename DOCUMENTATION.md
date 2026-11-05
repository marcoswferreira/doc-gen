# Documentação Técnica: doc-gen

> [!TIP]
> Documentação gerada pelo **DocGen**. Repositório analisado com **42 arquivos**, **2,039 linhas de código** e **73 termos conceituais**.

---

## Sumário de Navegação da Documentação

| Documento | Escopo e Conteúdo |
|---|---|
| 🏛️ **[Modelo C4 (C4_MODEL.md)](./C4_MODEL.md)** | Visão em 4 níveis: Contexto, Containers, Componentes e Código sintetizados via IA. |
| 📐 **[High-Level Design (HLD.md)](./HLD.md)** | Arquitetura macro, estilo arquitetural, fronteiras e RNFs. |
| 📋 **[Documento de Arquitetura (DAS.md)](./DAS.md)** | Visão 4+1 e Arc42: lógica, processos, física e riscos. |
| 💡 **[Linguagem Ubíqua (UBIQUITOUS_LANGUAGE.md)](./UBIQUITOUS_LANGUAGE.md)** | Glossário DDD com entidades, value objects, serviços e mapa conceitual. |
| 🗺️ **[Arquitetura e Fluxo (ARCHITECTURE.md)](./ARCHITECTURE.md)** | Diagrama Mermaid de componentes e fluxo de dados. |
| 📖 **[Referência de API (API_REFERENCE.md)](./API_REFERENCE.md)** | Classes, métodos, parâmetros, retornos, docstrings e tipos. |
| 📦 **[Dependências (DEPENDENCIES.md)](./DEPENDENCIES.md)** | Pacotes externos e grafo de importações internas. |
| 📊 **[Métricas do Projeto (METRICS.md)](./METRICS.md)** | SLOC, comentários, taxa de documentação e linguagens. |

---

## Estrutura de Diretórios
```
.
.github
.gitignore
DOCUMENTATION.md
README.md
README.pt-BR.md
docgen
pyproject.toml
setup.py
tests
  ├── workflows
  ├── __init__.py
  ├── __main__.py
  ├── ai
  ├── cli.py
  ├── config.py
  ├── generators
  ├── models.py
  ├── parsers
  ├── scanner.py
  ├── server.py
  ├── ui.py
  ├── test_ai.py
  ├── test_cli.py
  ├── test_generators.py
  ├── test_js_parser.py
  ├── test_python_parser.py
  ├── test_scanner.py
    ├── ci.yml
    ├── deploy-docs.yml
    ├── __init__.py
    ├── architect.py
    ├── context_builder.py
    ├── prompts.py
    ├── provider.py
    ├── api_reference_generator.py
    ├── architecture_generator.py
    ├── c4_generator.py
    ├── doc_suite.py
    ├── mermaid.py
    ├── static_site_generator.py
    ├── ubiquitous_language_generator.py
    ├── __init__.py
    ├── base.py
    ├── generic_parser.py
    ├── go_parser.py
    ├── java_parser.py
    ├── js_ts_parser.py
    ├── python_parser.py
    ├── rust_parser.py
```


---

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


---

# Modelo C4: doc-gen

> [!NOTE]
> O **Modelo C4** (Context, Containers, Components, Code) fornece uma maneira hierárquica e padronizada de mapear e comunicar a arquitetura de software em diferentes níveis de abstração.

---

## Nível 1: Diagrama de Contexto do Sistema (System Context)

O diagrama de contexto estabelece as fronteiras do sistema, destacando os usuários (atores humanos) e as interações com sistemas e plataformas externas.

```mermaid
flowchart TB
    user["👤 Usuário / Desenvolvedor<br/>[Pessoa]<br/>Executa e interage com o sistema"]
    sys["🏢 doc-gen<br/>[Ferramenta de Linha de Comando (CLI)]<br/>Sistema principal"]
    fs["📁 Sistema de Arquivos / Repositório<br/>[Sistema Externo]<br/>Armazena código-fonte e saídas"]
    user -->|Interage / Executa| sys
    sys -->|Lê e Grava dados| fs
```

### Atores e Fronteiras
- **Usuário / Desenvolvedor**: Opera o sistema doc-gen para realizar tarefas e consultar informações.
- **doc-gen**: O software sob análise, responsável pela lógica principal, orquestração e fluxos.
- **Sistema de Arquivos / Repositório**: Provedor de entrada (código, configurações) e destino de artefatos gerados.

---

## Nível 2: Diagrama de Containers (Containers)

Containers representam as unidades executáveis ou de armazenamento independentes que compõem a solução (aplicações, bancos de dados, serviços, file systems).

```mermaid
flowchart LR
    subgraph boundary["Fronteira do Sistema: doc-gen"]
        cli["💻 Interface CLI<br/>[Python]<br/>Interface de terminal e parser de comandos"]
        core["⚙️ Motor de Processamento<br/>[Python]<br/>Lógica de negócio e transformações"]
        server["🌐 Servidor Web Local<br/>[HTTP / HTML]<br/>Visualização interativa"]
        cli -->|Invoca| core
        cli -.->|Inicializa| server
    end
    disk["💾 Disco Local / Repositório<br/>[File System]<br/>Arquivos de entrada e documentação gerada"]
    core -->|Varre e Escreve| disk
    server -->|Lê documentos de| disk
```

### Descrição dos Containers
| Container | Tecnologia | Responsabilidade |
|---|---|---|
| **Interface CLI** | Python / CLI | Receber argumentos do usuário, configurar modos de execução e exibir status formatado. |
| **Motor de Processamento** | Python | Analisar estruturas, parsear ASTs, compilar grafos e gerar relatórios. |
| **Servidor Web Local** | HTTP / HTML5 / JS | Servir e renderizar os documentos Markdown e diagramas interativos localmente. |
| **Disco / Storage** | File System Local | Armazenar fontes, configurações e saídas de documentação. |

---

## Nível 3: Diagrama de Componentes (Components)

Exibe a decomposição interna dos módulos de software que formam o container principal e como eles colaboram entre si.

```mermaid
flowchart TD
    subgraph core_container["Container: doc-gen Core"]
        scanner["Scanner & Ignore Matcher<br/>[Varredura de arquivos]"]
        parser_reg["Parser Registry<br/>[Fábrica de analisadores]"]
        ast_parsers["Parsers de Linguagem<br/>[Python, JS/TS, Go, Rust, Java]"]
        model_store["Data Models<br/>[FileInfo, SymbolInfo, ProjectData]"]
        generators["Geradores de Documentação<br/>[C4, HLD/LLD, DAS, ADR, API, Mermaid]"]
        ui_engine["UI & Formatter Engine<br/>[Saída em terminal e Markdown]"]
        scanner -->|Lista de arquivos| parser_reg
        parser_reg -->|Delega para| ast_parsers
        ast_parsers -->|Popula| model_store
        model_store -->|Alimenta| generators
        generators -->|Exporta| ui_engine
    end
```

### Catálogo de Componentes Chave
- **Scanner & Ignore Matcher**: Responsável por navegar recursivamente pelos diretórios, respeitando regras do `.gitignore` e contabilizando linhas de código.
- **Parser Registry & Analyzers**: Fábrica polimórfica que seleciona o parser adequado para cada linguagem e extrai símbolos, classes, métodos e tipos.
- **Data Models**: Dataclasses imutáveis que garantem integridade estrutural em toda a pipeline.
- **Generators Suite**: Conjunto de especialistas em formatar saídas técnicas (C4, HLD, LLD, DAS, ADRs, Glossário DDD e API).

---

## Nível 4: Diagrama de Código (Code / Class Diagram)

Mapeamento das principais classes, interfaces e tipos estruturais que implementam as regras de domínio.

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

---

# High-Level Design (HLD): doc-gen

> [!NOTE]
> O **High-Level Design (HLD)** documenta a arquitetura macro, o estilo arquitetural, as fronteiras do sistema e os requisitos não-funcionais que orientam a engenharia da solução.

---

## 1. Visão Geral da Solução
O projeto **doc-gen** foi projetado como uma solução modular desenvolvida principalmente em **Python**, totalizando aproximadamente **2,039 linhas de código** distribuídas em **42 arquivos**.

### Objetivos Principais
- Fornecer processamento confiável, previsível e desacoplado.
- Permitir fácil extensão para novas linguagens e formatos sem quebrar contratos existentes.
- Garantir portabilidade multiplataforma sem necessidade de dependências pesadas de terceiros.

## 2. Estilo Arquitetural
A solução adota uma **Arquitetura em Camadas (Layered Architecture)** combinada com o padrão **Pipeline / Filter**, onde o fluxo de dados passa por etapas sequenciais bem definidas:

```mermaid
flowchart LR
    A[Input: Repositório] --> B[Camada de Descoberta / Scanner]
    B --> C[Camada de Análise / Parsers]
    C --> D[Camada de Modelo / Grafo de Dados]
    D --> E[Camada de Geração / Renderers]
    E --> F[Output: Markdown / Web]
```

### Benefícios do Estilo Adotado
- **Separação de Responsabilidades (SoC)**: O módulo de varredura não sabe como gerar Markdown; o gerador não sabe como o AST foi extraído.
- **Testabilidade Isolada**: Cada camada pode ser testada unitariamente com fixtures e dados mockados.
- **Extensibilidade**: Novos parsers e novos geradores podem ser adicionados plugando-se nas fábricas correspondentes.

## 3. Requisitos Não-Funcionais (RNFs)
| Categoria | Requisito | Estratégia de Implementação |
|---|---|---|
| **Portabilidade** | Executar em Linux, macOS e Windows sem compilação nativa externa | Uso de módulos padrão (`pathlib`, `os`, `sys`, `ast`) compatíveis entre SOs. |
| **Performance** | Analisar repositórios em tempo inferior a poucos segundos | Otimização de varredura de diretórios com poda rápida via `.gitignore` e regex pré-compiladas. |
| **Autonomia** | Funcionamento 100% offline (Zero dependência de rede obrigatória) | Motor sintático nativo que dispensa conexões remotas ou APIs externas para gerar a documentação completa. |
| **Manutenibilidade** | Código limpo, tipado e com alta taxa de documentação | Dataclasses estritas, contratos abstratos (`BaseParser`) e modularização em submódulos. |

## 4. Integrações e Fronteiras Externas
- **Sistema Operacional & File System**: Acesso a diretórios locais com permissão de leitura/escrita.
- **Bibliotecas Externas**: Autossuficiente utilizando exclusivamente a runtime padrão.

---

# Documento de Arquitetura de Software (DAS): doc-gen

> [!NOTE]
> Este **Documento de Arquitetura de Software (DAS)** foi estruturado com base nas melhores práticas do padrão **Arc42** e do **Modelo 4+1 Visões de Philippe Kruchten**, registrando decisões, restrições, visões de processo e de implantação.

---

## 1. Introdução e Metas Arquiteturais
O objetivo do software **doc-gen** é fornecer análise estática e geração estruturada de documentação técnica para bases de código heterogêneas.

### Metas de Qualidade Prioritárias
1. **Alta Acurácia**: Extração fidedigna de tipos, classes, funções e comentários de documentação.
2. **Velocidade de Execução**: Varredura ágil mesmo em repositórios de grande porte.
3. **Legibilidade e Riqueza Visual**: Geração de Markdown estruturado com suporte nativo a diagramas Mermaid.

## 2. Restrições e Premissas Arquiteturais
- **Runtime Principal**: Python.
- **Independência de Ambiente**: Compatibilidade direta com ambientes isolados (containers, sandboxes e pipelines de CI/CD).
- **Respeito a Políticas de Código**: Conformidade total com regras de exclusão (`.gitignore`, `.docgenignore`).

## 3. Visão Lógica (Logical View)
Mapeia a organização modular do software e como as responsabilidades são divididas entre os subsistemas:

```mermaid
graph TD
    subgraph Presentation_Layer["Camada de Apresentação e CLI"]
        CLI["CLI Controller / Terminal UI"]
        Web["Built-in HTTP Server"]
    end
    subgraph Core_Layer["Camada de Negócio e Processamento"]
        Scanner["Repository Scanner"]
        Parsers["AST & Structural Parsers"]
        Analyzers["Metrics & Graph Analyzer"]
    end
    subgraph Generation_Layer["Camada de Geração de Documentos"]
        C4["C4 Model Generator"]
        HLD_LLD["HLD & LLD Generator"]
        DAS_Gen["DAS & ADR Generator"]
        API_Gen["API Reference & Ubiquitous Language"]
    end
    CLI --> Scanner
    CLI --> Parsers
    Parsers --> Analyzers
    Analyzers --> Generation_Layer
    Web -.-> Generation_Layer
```

## 4. Visão de Processo (Process View)
- **Ciclo de Vida Síncrono e Determinístico**: Cada execução do pipeline opera em batch síncrono, garantindo idempotência (a mesma base de código gera o mesmo conjunto de documentações).
- **Uso de Memória**: O modelo `ProjectData` é retido em memória apenas durante o ciclo de execução e liberado após a escrita em disco.

## 5. Visão de Implantação e Execução (Deployment View)
O sistema pode ser distribuído e executado das seguintes maneiras:
1. **Executável Local**: Via CLI empacotada (`docgen`).
2. **Pipeline de CI/CD**: Executado em GitHub Actions, GitLab CI ou Jenkins para atualizar os documentos a cada pull request ou push.
3. **Container Docker**: Executável dentro de imagens base mínimas.

## 6. Riscos Arquiteturais e Mitigações
| Risco Identificado | Impacto | Estratégia de Mitigação |
|---|---|---|
| Arquivos com sintaxe inválida no repositório | Falha durante o parseamento | Parsers implementados com blocos `try/except` resilientes e fallback para `GenericParser`. |
| Repositórios gigantescos com milhões de linhas | Lentidão ou estouro de memória | Limitação de tamanho individual de arquivo (5MB) e poda de diretórios ignorados antes do parse. |
| Falta de tipagem estática no código analisado | Documentação com tipos vazios | Detecção heurística de valores default e docstrings para enriquecer assinaturas. |

---

# Linguagem Ubíqua (Glossário DDD): doc-gen

> [!NOTE]
> No **Domain-Driven Design (DDD)**, a **Linguagem Ubíqua** (Ubiquitous Language) é o vocabulário compartilhado e rigoroso utilizado tanto por especialistas de negócio quanto pela equipe técnica para eliminar ambiguidades no software.

---

## 1. Mapa Conceitual do Domínio
Relação visual dos termos mais representativos identificados na base de código:

```mermaid
graph TD
    C4_PROMPT["<b>C4_PROMPT</b><br/><i>(Entidade)</i>"]
    DAS_PROMPT["<b>DAS_PROMPT</b><br/><i>(Entidade)</i>"]
    HLD_PROMPT["<b>HLD_PROMPT</b><br/><i>(Entidade)</i>"]
    HTML_TEMPLATE["<b>HTML_TEMPLATE</b><br/><i>(Entidade)</i>"]
    IGNORED_BASE_CLASSES["<b>IGNORED_BASE_CLASSES</b><br/><i>(Entidade)</i>"]
    SYSTEM_ARCHITECT_PROMPT["<b>SYSTEM_ARCHITECT_PROMPT</b><br/><i>(Entidade)</i>"]
    UBIQUITOUS_LANGUAGE_PROMPT["<b>UBIQUITOUS_LANGUAGE_PROMPT</b><br/><i>(Entidade)</i>"]
    build_static_html_viewer["<b>build_static_html_viewer</b><br/><i>(Entidade)</i>"]
    count_file_lines["<b>count_file_lines</b><br/><i>(Entidade)</i>"]
    detect_language["<b>detect_language</b><br/><i>(Entidade)</i>"]
    extract_ubiquitous_terms["<b>extract_ubiquitous_terms</b><br/><i>(Entidade)</i>"]
    generate_api_reference_markdown["<b>generate_api_reference_markdown</b><br/><i>(Entidade)</i>"]
    C4_PROMPT -.->|Relacionado| DAS_PROMPT
    C4_PROMPT -.->|Relacionado| HLD_PROMPT
    C4_PROMPT -.->|Relacionado| SYSTEM_ARCHITECT_PROMPT
    C4_PROMPT -.->|Relacionado| UBIQUITOUS_LANGUAGE_PROMPT
    DAS_PROMPT -.->|Relacionado| HLD_PROMPT
    DAS_PROMPT -.->|Relacionado| SYSTEM_ARCHITECT_PROMPT
    DAS_PROMPT -.->|Relacionado| UBIQUITOUS_LANGUAGE_PROMPT
    HLD_PROMPT -.->|Relacionado| SYSTEM_ARCHITECT_PROMPT
    HLD_PROMPT -.->|Relacionado| UBIQUITOUS_LANGUAGE_PROMPT
    SYSTEM_ARCHITECT_PROMPT -.->|Relacionado| UBIQUITOUS_LANGUAGE_PROMPT
    count_file_lines -.->|Relacionado| detect_language
```

## 2. Glossário de Termos do Negócio

| Termo / Conceito | Categoria DDD | Definição / Papel no Sistema | Ocorrências |
|---|---|---|---|
| **C4_PROMPT** | `Entidade` | Elemento estrutural do domínio do sistema. | `prompts.py` |
| **DAS_PROMPT** | `Entidade` | Elemento estrutural do domínio do sistema. | `prompts.py` |
| **HLD_PROMPT** | `Entidade` | Elemento estrutural do domínio do sistema. | `prompts.py` |
| **HTML_TEMPLATE** | `Entidade` | Elemento estrutural do domínio do sistema. | `server.py` |
| **IGNORED_BASE_CLASSES** | `Entidade` | Elemento estrutural do domínio do sistema. | `mermaid.py` |
| **SYSTEM_ARCHITECT_PROMPT** | `Entidade` | Elemento estrutural do domínio do sistema. | `prompts.py` |
| **UBIQUITOUS_LANGUAGE_PROMPT** | `Entidade` | Elemento estrutural do domínio do sistema. | `prompts.py` |
| **build_static_html_viewer** | `Entidade` | Gera um index.html autossuficiente contendo todos os Markdowns embutidos. | `static_site_generator.py` |
| **count_file_lines** | `Entidade` | Analisa as linhas de um arquivo e retorna:. | `scanner.py` |
| **detect_language** | `Entidade` | Identifica a linguagem pelo nome ou extensão do arquivo. | `scanner.py` |
| **extract_ubiquitous_terms** | `Entidade` | Analisa as definições de classes, tipos e enums para compor a Linguagem Ubíqua. | `ubiquitous_language_generator.py` |
| **generate_api_reference_markdown** | `Entidade` | Gera o documento API_REFERENCE.md. | `api_reference_generator.py` |
| **generate_architecture_diagram** | `Entidade` | Gera um diagrama de arquitetura em alto nível agrupando módulos em subgraphs. | `mermaid.py` |
| **generate_c4_documentation** | `Entidade` | Gera o documento completo C4_MODEL.md. | `c4_generator.py` |
| **generate_class_diagram** | `Entidade` | Gera um diagrama de classes Mermaid válido para entidades e classes de domínio. | `mermaid.py` |
| **generate_das** | `Entidade` | Gera o Documento de Arquitetura de Software (DAS.md) no padrão Arc42 / 4+1 Views. | `architecture_generator.py` |
| **generate_dependency_graph** | `Entidade` | Gera o grafo de dependências internas entre módulos do projeto. | `mermaid.py` |
| **generate_directory_tree** | `Entidade` | Gera uma árvore visual de diretórios em texto/ASCII. | `doc_suite.py` |
| **generate_hld** | `Entidade` | Gera o documento High-Level Design (HLD.md). | `architecture_generator.py` |
| **generate_ubiquitous_language_markdown** | `Entidade` | Gera o documento UBIQUITOUS_LANGUAGE.md. | `ubiquitous_language_generator.py` |
| **get_ai_provider** | `Entidade` | Fábrica inteligente de provedores de IA. | `provider.py` |
| **get_primary_programming_language** | `Entidade` | Retorna a linguagem de programação principal, desconsiderando arquivos de doc/config. | `config.py` |
| **is_test_file** | `Entidade` | Verifica se o arquivo é um arquivo de teste. | `mermaid.py` |
| **print_banner** | `Entidade` | Exibe o cabeçalho estilizado do DocGen. | `ui.py` |
| **print_error** | `Entidade` | Imprime erro. | `ui.py` |
| **print_info** | `Entidade` | Imprime mensagem informativa. | `ui.py` |
| **print_step** | `Entidade` | Imprime uma etapa do processo. | `ui.py` |
| **print_success** | `Entidade` | Imprime confirmação de sucesso. | `ui.py` |
| **print_table** | `Entidade` | Renderiza uma tabela formatada com bordas Unicode no terminal. | `ui.py` |
| **print_warning** | `Entidade` | Imprime aviso. | `ui.py` |
| **resolve_internal_dependencies** | `Entidade` | Mapeia os imports internos entre arquivos do projeto. | `cli.py` |
| **run_generate** | `Entidade` | Executa a análise do repositório e a geração completa da documentação. | `cli.py` |
| **run_init** | `Entidade` | Inicializa arquivos de configuração padrão. | `cli.py` |
| **run_stats** | `Entidade` | Apenas analisa e exibe métricas no terminal. | `cli.py` |
| **sanitize_id** | `Entidade` | Sanitiza strings para identificadores válidos em nós Mermaid. | `mermaid.py` |
| **sanitize_method_for_mermaid** | `Entidade` | Sanitiza o nome e retorno do método para sintaxe estrita do Mermaid classDiagram. | `mermaid.py` |
| **start_doc_server** | `Entidade` | Inicia o servidor de visualização local. | `server.py` |
| **AIArchitect** | `Entidade de Domínio` | Agente de arquitetura de software alimentado por IA Generativa. | `architect.py` |
| **AnthropicProvider** | `Entidade de Domínio` | Integração com Anthropic Claude via REST nativo. | `provider.py` |
| **BaseParser** | `Entidade de Domínio` | Contrato base para analisadores de código fonte. | `base.py` |
| **CodebaseContextBuilder** | `Entidade de Domínio` | Monta o contexto técnico completo do repositório para ingestão por LLMs. | `context_builder.py` |
| **Colors** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em Colors. | `ui.py` |
| **GeminiProvider** | `Entidade de Domínio` | Integração com Google Gemini API via REST nativo. | `provider.py` |
| **GenericParser** | `Entidade de Domínio` | Parser de fallback para qualquer arquivo de código ou configuração. | `generic_parser.py` |
| **GoParser** | `Entidade de Domínio` | Parser estrutural para código Go. | `go_parser.py` |
| **IgnoreMatcher** | `Entidade de Domínio` | Implementa correspondência de padrões estilo .gitignore. | `scanner.py` |
| **JavaParser** | `Entidade de Domínio` | Parser para linguagens orientadas a objetos baseadas em classes (Java, C#, Kotlin). | `java_parser.py` |
| **JsTsParser** | `Entidade de Domínio` | Parser estrutural e regex para JavaScript e TypeScript. | `js_ts_parser.py` |
| **LLMProvider** | `Entidade de Domínio` | Interface abstrata para provedores de inteligência artificial generativa. | `provider.py` |
| **MockProvider** | `Entidade de Domínio` | Provedor mock utilizado para testes unitários ou modo determinístico. | `provider.py` |
| **ModuleGroup** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em ModuleGroup. | `models.py` |
| **OllamaProvider** | `Entidade de Domínio` | Integração com LLM local via Ollama (DeepSeek-R1, Llama 3, Qwen, etc.). | `provider.py` |
| **OpenAIProvider** | `Entidade de Domínio` | Integração com OpenAI (GPT-4o, GPT-4o-mini) via REST nativo. | `provider.py` |
| **PythonParser** | `Entidade de Domínio` | Parser para arquivos Python usando AST. | `python_parser.py` |
| **RustParser** | `Entidade de Domínio` | Parser estrutural para código Rust. | `rust_parser.py` |
| **SymbolType** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em SymbolType. | `models.py` |
| **TestCLI** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em TestCLI. | `test_cli.py` |
| **TestJsTsParser** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em TestJsTsParser. | `test_js_parser.py` |
| **TestPythonParser** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em TestPythonParser. | `test_python_parser.py` |
| **UbiquitousTerm** | `Entidade de Domínio` | Entidade central com ciclo de vida e estado gerenciado em UbiquitousTerm. | `models.py` |
| **FileInfo** | `Objeto de Valor (Value Object)` | Representação imutável com propriedades e métricas de FileInfo. | `models.py` |
| **ImportInfo** | `Objeto de Valor (Value Object)` | Representação imutável com propriedades e métricas de ImportInfo. | `models.py` |
| **ParameterInfo** | `Objeto de Valor (Value Object)` | Representação imutável com propriedades e métricas de ParameterInfo. | `models.py` |
| **ProjectData** | `Objeto de Valor (Value Object)` | Representação imutável com propriedades e métricas de ProjectData. | `models.py` |
| **ProjectMetrics** | `Objeto de Valor (Value Object)` | Representação imutável com propriedades e métricas de ProjectMetrics. | `models.py` |
| **SymbolInfo** | `Objeto de Valor (Value Object)` | Representação imutável com propriedades e métricas de SymbolInfo. | `models.py` |
| **DocSuiteGenerator** | `Serviço de Domínio` | Orquestra a escrita dos documentos Markdown. | `doc_suite.py` |
| **DocViewerHandler** | `Serviço de Domínio` | Handler HTTP para servir a UI interativa e os arquivos Markdown. | `server.py` |
| **ParserRegistry** | `Serviço de Domínio` | Gerencia a lista de parsers disponíveis e aplica o mais adequado a cada arquivo. | `__init__.py` |
| **RepositoryScanner** | `Serviço de Domínio` | Escaneia o repositório e constrói a lista inicial de arquivos e métricas. | `scanner.py` |
| **TestAIEngine** | `Serviço de Domínio` | Serviço responsável por executar operações e orquestrações de TestAIEngine. | `test_ai.py` |
| **TestGenerators** | `Serviço de Domínio` | Serviço responsável por executar operações e orquestrações de TestGenerators. | `test_generators.py` |
| **TestScanner** | `Serviço de Domínio` | Serviço responsável por executar operações e orquestrações de TestScanner. | `test_scanner.py` |

---

### Entidade (37)
- **C4_PROMPT**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/ai/prompts.py`
- **DAS_PROMPT**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/ai/prompts.py`
- **HLD_PROMPT**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/ai/prompts.py`
- **HTML_TEMPLATE**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/server.py`
- **IGNORED_BASE_CLASSES**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **SYSTEM_ARCHITECT_PROMPT**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/ai/prompts.py`
- **UBIQUITOUS_LANGUAGE_PROMPT**: Elemento estrutural do domínio do sistema.
  - *Arquivos*: `docgen/ai/prompts.py`
- **build_static_html_viewer**: Gera um index.html autossuficiente contendo todos os Markdowns embutidos.
  - *Arquivos*: `docgen/generators/static_site_generator.py`
- **count_file_lines**: Analisa as linhas de um arquivo e retorna:.
  - *Arquivos*: `docgen/scanner.py`
- **detect_language**: Identifica a linguagem pelo nome ou extensão do arquivo.
  - *Arquivos*: `docgen/scanner.py`
- **extract_ubiquitous_terms**: Analisa as definições de classes, tipos e enums para compor a Linguagem Ubíqua.
  - *Arquivos*: `docgen/generators/ubiquitous_language_generator.py`
- **generate_api_reference_markdown**: Gera o documento API_REFERENCE.md.
  - *Arquivos*: `docgen/generators/api_reference_generator.py`
- **generate_architecture_diagram**: Gera um diagrama de arquitetura em alto nível agrupando módulos em subgraphs.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **generate_c4_documentation**: Gera o documento completo C4_MODEL.md.
  - *Arquivos*: `docgen/generators/c4_generator.py`
- **generate_class_diagram**: Gera um diagrama de classes Mermaid válido para entidades e classes de domínio.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **generate_das**: Gera o Documento de Arquitetura de Software (DAS.md) no padrão Arc42 / 4+1 Views.
  - *Arquivos*: `docgen/generators/architecture_generator.py`
- **generate_dependency_graph**: Gera o grafo de dependências internas entre módulos do projeto.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **generate_directory_tree**: Gera uma árvore visual de diretórios em texto/ASCII.
  - *Arquivos*: `docgen/generators/doc_suite.py`
- **generate_hld**: Gera o documento High-Level Design (HLD.md).
  - *Arquivos*: `docgen/generators/architecture_generator.py`
- **generate_ubiquitous_language_markdown**: Gera o documento UBIQUITOUS_LANGUAGE.md.
  - *Arquivos*: `docgen/generators/ubiquitous_language_generator.py`
- **get_ai_provider**: Fábrica inteligente de provedores de IA.
  - *Arquivos*: `docgen/ai/provider.py`
- **get_primary_programming_language**: Retorna a linguagem de programação principal, desconsiderando arquivos de doc/config.
  - *Arquivos*: `docgen/config.py`
- **is_test_file**: Verifica se o arquivo é um arquivo de teste.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **print_banner**: Exibe o cabeçalho estilizado do DocGen.
  - *Arquivos*: `docgen/ui.py`
- **print_error**: Imprime erro.
  - *Arquivos*: `docgen/ui.py`
- **print_info**: Imprime mensagem informativa.
  - *Arquivos*: `docgen/ui.py`
- **print_step**: Imprime uma etapa do processo.
  - *Arquivos*: `docgen/ui.py`
- **print_success**: Imprime confirmação de sucesso.
  - *Arquivos*: `docgen/ui.py`
- **print_table**: Renderiza uma tabela formatada com bordas Unicode no terminal.
  - *Arquivos*: `docgen/ui.py`
- **print_warning**: Imprime aviso.
  - *Arquivos*: `docgen/ui.py`
- **resolve_internal_dependencies**: Mapeia os imports internos entre arquivos do projeto.
  - *Arquivos*: `docgen/cli.py`
- **run_generate**: Executa a análise do repositório e a geração completa da documentação.
  - *Arquivos*: `docgen/cli.py`
- **run_init**: Inicializa arquivos de configuração padrão.
  - *Arquivos*: `docgen/cli.py`
- **run_stats**: Apenas analisa e exibe métricas no terminal.
  - *Arquivos*: `docgen/cli.py`
- **sanitize_id**: Sanitiza strings para identificadores válidos em nós Mermaid.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **sanitize_method_for_mermaid**: Sanitiza o nome e retorno do método para sintaxe estrita do Mermaid classDiagram.
  - *Arquivos*: `docgen/generators/mermaid.py`
- **start_doc_server**: Inicia o servidor de visualização local.
  - *Arquivos*: `docgen/server.py`

### Entidade de Domínio (23)
- **AIArchitect**: Agente de arquitetura de software alimentado por IA Generativa.
  - *Arquivos*: `docgen/ai/architect.py`
- **AnthropicProvider**: Integração com Anthropic Claude via REST nativo.
  - *Arquivos*: `docgen/ai/provider.py`
- **BaseParser**: Contrato base para analisadores de código fonte.
  - *Arquivos*: `docgen/parsers/base.py`
- **CodebaseContextBuilder**: Monta o contexto técnico completo do repositório para ingestão por LLMs.
  - *Arquivos*: `docgen/ai/context_builder.py`
- **Colors**: Entidade central com ciclo de vida e estado gerenciado em Colors.
  - *Arquivos*: `docgen/ui.py`
- **GeminiProvider**: Integração com Google Gemini API via REST nativo.
  - *Arquivos*: `docgen/ai/provider.py`
- **GenericParser**: Parser de fallback para qualquer arquivo de código ou configuração.
  - *Arquivos*: `docgen/parsers/generic_parser.py`
- **GoParser**: Parser estrutural para código Go.
  - *Arquivos*: `docgen/parsers/go_parser.py`
- **IgnoreMatcher**: Implementa correspondência de padrões estilo .gitignore.
  - *Arquivos*: `docgen/scanner.py`
- **JavaParser**: Parser para linguagens orientadas a objetos baseadas em classes (Java, C#, Kotlin).
  - *Arquivos*: `docgen/parsers/java_parser.py`
- **JsTsParser**: Parser estrutural e regex para JavaScript e TypeScript.
  - *Arquivos*: `docgen/parsers/js_ts_parser.py`
- **LLMProvider**: Interface abstrata para provedores de inteligência artificial generativa.
  - *Arquivos*: `docgen/ai/provider.py`
- **MockProvider**: Provedor mock utilizado para testes unitários ou modo determinístico.
  - *Arquivos*: `docgen/ai/provider.py`
- **ModuleGroup**: Entidade central com ciclo de vida e estado gerenciado em ModuleGroup.
  - *Arquivos*: `docgen/models.py`
- **OllamaProvider**: Integração com LLM local via Ollama (DeepSeek-R1, Llama 3, Qwen, etc.).
  - *Arquivos*: `docgen/ai/provider.py`
- **OpenAIProvider**: Integração com OpenAI (GPT-4o, GPT-4o-mini) via REST nativo.
  - *Arquivos*: `docgen/ai/provider.py`
- **PythonParser**: Parser para arquivos Python usando AST.
  - *Arquivos*: `docgen/parsers/python_parser.py`
- **RustParser**: Parser estrutural para código Rust.
  - *Arquivos*: `docgen/parsers/rust_parser.py`
- **SymbolType**: Entidade central com ciclo de vida e estado gerenciado em SymbolType.
  - *Arquivos*: `docgen/models.py`
- **TestCLI**: Entidade central com ciclo de vida e estado gerenciado em TestCLI.
  - *Arquivos*: `tests/test_cli.py`
- **TestJsTsParser**: Entidade central com ciclo de vida e estado gerenciado em TestJsTsParser.
  - *Arquivos*: `tests/test_js_parser.py`
- **TestPythonParser**: Entidade central com ciclo de vida e estado gerenciado em TestPythonParser.
  - *Arquivos*: `tests/test_python_parser.py`
- **UbiquitousTerm**: Entidade central com ciclo de vida e estado gerenciado em UbiquitousTerm.
  - *Arquivos*: `docgen/models.py`

### Objeto de Valor (Value Object) (6)
- **FileInfo**: Representação imutável com propriedades e métricas de FileInfo.
  - *Arquivos*: `docgen/models.py`
- **ImportInfo**: Representação imutável com propriedades e métricas de ImportInfo.
  - *Arquivos*: `docgen/models.py`
- **ParameterInfo**: Representação imutável com propriedades e métricas de ParameterInfo.
  - *Arquivos*: `docgen/models.py`
- **ProjectData**: Representação imutável com propriedades e métricas de ProjectData.
  - *Arquivos*: `docgen/models.py`
- **ProjectMetrics**: Representação imutável com propriedades e métricas de ProjectMetrics.
  - *Arquivos*: `docgen/models.py`
- **SymbolInfo**: Representação imutável com propriedades e métricas de SymbolInfo.
  - *Arquivos*: `docgen/models.py`

### Serviço de Domínio (7)
- **DocSuiteGenerator**: Orquestra a escrita dos documentos Markdown.
  - *Arquivos*: `docgen/generators/doc_suite.py`
- **DocViewerHandler**: Handler HTTP para servir a UI interativa e os arquivos Markdown.
  - *Arquivos*: `docgen/server.py`
- **ParserRegistry**: Gerencia a lista de parsers disponíveis e aplica o mais adequado a cada arquivo.
  - *Arquivos*: `docgen/parsers/__init__.py`
- **RepositoryScanner**: Escaneia o repositório e constrói a lista inicial de arquivos e métricas.
  - *Arquivos*: `docgen/scanner.py`
- **TestAIEngine**: Serviço responsável por executar operações e orquestrações de TestAIEngine.
  - *Arquivos*: `tests/test_ai.py`
- **TestGenerators**: Serviço responsável por executar operações e orquestrações de TestGenerators.
  - *Arquivos*: `tests/test_generators.py`
- **TestScanner**: Serviço responsável por executar operações e orquestrações de TestScanner.
  - *Arquivos*: `tests/test_scanner.py`


---

# Referência de API e Símbolos: doc-gen

> [!NOTE]
> Esta seção fornece a documentação técnica detalhada das interfaces, classes, métodos, funções e rotas expostas pelo código-fonte.

---

## Módulos Documentados

| Módulo / Arquivo | Linguagem | Símbolos | SLOC |
|---|---|---|---|
| [DOCUMENTATION.md](#documentation-md) | Markdown | 0 | 1435 |
| [pyproject.toml](#pyproject-toml) | TOML | 0 | 22 |
| [setup.py](#setup-py) | Python | 0 | 11 |
| [README.pt-BR.md](#readme-pt-br-md) | Markdown | 0 | 81 |
| [README.md](#readme-md) | Markdown | 0 | 81 |
| [.gitignore](#-gitignore) | Other | 0 | 30 |
| [.github/workflows/deploy-docs.yml](#-github-workflows-deploy-docs-yml) | YAML | 0 | 39 |
| [.github/workflows/ci.yml](#-github-workflows-ci-yml) | YAML | 0 | 46 |
| [tests/test_cli.py](#tests-test_cli-py) | Python | 1 | 0 |
| [tests/test_python_parser.py](#tests-test_python_parser-py) | Python | 1 | 0 |
| [tests/test_js_parser.py](#tests-test_js_parser-py) | Python | 1 | 12 |
| [tests/test_ai.py](#tests-test_ai-py) | Python | 1 | 0 |
| [tests/test_generators.py](#tests-test_generators-py) | Python | 1 | 0 |
| [tests/test_scanner.py](#tests-test_scanner-py) | Python | 1 | 0 |
| [docgen/scanner.py](#docgen-scanner-py) | Python | 4 | 126 |
| [docgen/cli.py](#docgen-cli-py) | Python | 5 | 0 |
| [docgen/models.py](#docgen-models-py) | Python | 9 | 0 |
| [docgen/config.py](#docgen-config-py) | Python | 1 | 0 |
| [docgen/server.py](#docgen-server-py) | Python | 3 | 0 |
| [docgen/ui.py](#docgen-ui-py) | Python | 8 | 0 |
| [docgen/generators/c4_generator.py](#docgen-generators-c4_generator-py) | Python | 1 | 0 |
| [docgen/generators/ubiquitous_language_generator.py](#docgen-generators-ubiquitous_language_generator-py) | Python | 2 | 0 |
| [docgen/generators/api_reference_generator.py](#docgen-generators-api_reference_generator-py) | Python | 1 | 0 |
| [docgen/generators/doc_suite.py](#docgen-generators-doc_suite-py) | Python | 2 | 0 |
| [docgen/generators/static_site_generator.py](#docgen-generators-static_site_generator-py) | Python | 1 | 0 |
| [docgen/generators/mermaid.py](#docgen-generators-mermaid-py) | Python | 7 | 0 |
| [docgen/generators/architecture_generator.py](#docgen-generators-architecture_generator-py) | Python | 2 | 0 |
| [docgen/parsers/base.py](#docgen-parsers-base-py) | Python | 1 | 0 |
| [docgen/parsers/js_ts_parser.py](#docgen-parsers-js_ts_parser-py) | Python | 1 | 48 |
| [docgen/parsers/go_parser.py](#docgen-parsers-go_parser-py) | Python | 1 | 0 |
| [docgen/parsers/rust_parser.py](#docgen-parsers-rust_parser-py) | Python | 1 | 0 |
| [docgen/parsers/java_parser.py](#docgen-parsers-java_parser-py) | Python | 1 | 85 |
| [docgen/parsers/generic_parser.py](#docgen-parsers-generic_parser-py) | Python | 1 | 23 |
| [docgen/parsers/python_parser.py](#docgen-parsers-python_parser-py) | Python | 3 | 0 |
| [docgen/parsers/__init__.py](#docgen-parsers-__init__-py) | Python | 1 | 0 |
| [docgen/ai/context_builder.py](#docgen-ai-context_builder-py) | Python | 1 | 0 |
| [docgen/ai/prompts.py](#docgen-ai-prompts-py) | Python | 5 | 0 |
| [docgen/ai/provider.py](#docgen-ai-provider-py) | Python | 7 | 0 |
| [docgen/ai/architect.py](#docgen-ai-architect-py) | Python | 2 | 0 |

---

<a id='documentation-md'></a>
## Arquivo: `DOCUMENTATION.md`
**Linguagem:** Markdown | **Linhas de Código:** 1435 | **Comentários:** 235

### Descrição do Módulo
> Documentação Técnica: doc-gen

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='pyproject-toml'></a>
## Arquivo: `pyproject.toml`
**Linguagem:** TOML | **Linhas de Código:** 22 | **Comentários:** 0

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='setup-py'></a>
## Arquivo: `setup.py`
**Linguagem:** Python | **Linhas de Código:** 11 | **Comentários:** 0

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='readme-pt-br-md'></a>
## Arquivo: `README.pt-BR.md`
**Linguagem:** Markdown | **Linhas de Código:** 81 | **Comentários:** 21

### Descrição do Módulo
> DocGen (CLI) ⚡🧠

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='readme-md'></a>
## Arquivo: `README.md`
**Linguagem:** Markdown | **Linhas de Código:** 81 | **Comentários:** 21

### Descrição do Módulo
> DocGen (CLI) ⚡🧠

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='-gitignore'></a>
## Arquivo: `.gitignore`
**Linguagem:** Other | **Linhas de Código:** 30 | **Comentários:** 4

### Descrição do Módulo
> Python

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='-github-workflows-deploy-docs-yml'></a>
## Arquivo: `.github/workflows/deploy-docs.yml`
**Linguagem:** YAML | **Linhas de Código:** 39 | **Comentários:** 0

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='-github-workflows-ci-yml'></a>
## Arquivo: `.github/workflows/ci.yml`
**Linguagem:** YAML | **Linhas de Código:** 46 | **Comentários:** 0

*Nenhum símbolo estruturado (funções ou classes) declarado diretamente neste arquivo.*

---

<a id='tests-test_cli-py'></a>
## Arquivo: `tests/test_cli.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 42

### Descrição do Módulo
> Testes unitários para os comandos da CLI do DocGen.

### `class` TestCLI
```python
class TestCLI(unittest.TestCase)
```

#### Métodos da Classe
- **`setUp`**`()`
- **`tearDown`**`()`
- **`test_cli_stats`**`()`
- **`test_cli_generate_multi`**`()`
- **`test_cli_generate_single_file`**`()`

---

<a id='tests-test_python_parser-py'></a>
## Arquivo: `tests/test_python_parser.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 73

### Descrição do Módulo
> Testes unitários para o analisador de código Python via AST.

### `class` TestPythonParser
```python
class TestPythonParser(unittest.TestCase)
```

#### Métodos da Classe
- **`setUp`**`()`
- **`tearDown`**`()`
- **`test_parse_classes_and_methods`**`()`
- **`test_parse_routes`**`()`

---

<a id='tests-test_js_parser-py'></a>
## Arquivo: `tests/test_js_parser.py`
**Linguagem:** Python | **Linhas de Código:** 12 | **Comentários:** 74

### Descrição do Módulo
> Testes unitários para o analisador de código JavaScript e TypeScript.

### `class` TestJsTsParser
```python
class TestJsTsParser(unittest.TestCase)
```

#### Métodos da Classe
- **`setUp`**`()`
- **`tearDown`**`()`
- **`test_parse_typescript_interfaces_and_classes`**`()`
- **`test_parse_express_routes`**`()`

---

<a id='tests-test_ai-py'></a>
## Arquivo: `tests/test_ai.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 89

### Descrição do Módulo
> Testes unitários para o subsistema de Engenharia de IA do DocGen.
Valida o construtor de contexto, os provedores de LLM e o AIArchitect.

### `class` TestAIEngine
```python
class TestAIEngine(unittest.TestCase)
```

#### Métodos da Classe
- **`setUp`**`()`
- **`tearDown`**`()`
- **`test_context_builder`**`()`
- **`test_ai_architect_synthesis`**`()`
- **`test_doc_suite_with_ai_provider`**`()`
- **`test_cli_ai_flags`**`()`

---

<a id='tests-test_generators-py'></a>
## Arquivo: `tests/test_generators.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 146

### Descrição do Módulo
> Testes unitários para todos os geradores de documentação técnica e arquitetural:
- C4 Model
- HLD / LLD / DAS
- ADRs
- Linguagem Ubíqua (DDD)
- DocSuiteGenerator (Multi e Single-file)

### `class` TestGenerators
```python
class TestGenerators(unittest.TestCase)
```

#### Métodos da Classe
- **`setUp`**`()`
- **`tearDown`**`()`
- **`test_c4_model_generation`**`()`
- **`test_hld_das_generation`**`()`
- **`test_ubiquitous_language_generation`**`()`
- **`test_doc_suite_generator_multi_file`**`()`
- **`test_doc_suite_generator_single_file`**`()`

---

<a id='tests-test_scanner-py'></a>
## Arquivo: `tests/test_scanner.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 59

### Descrição do Módulo
> Testes unitários para o scanner de repositório e o gerenciador de ignores.

### `class` TestScanner
```python
class TestScanner(unittest.TestCase)
```

#### Métodos da Classe
- **`setUp`**`()`
- **`tearDown`**`()`
- **`test_ignore_matcher`**`()`
- **`test_detect_language`**`()`
- **`test_count_file_lines`**`()`
- **`test_repository_scanner_and_metrics`**`()`

---

<a id='docgen-scanner-py'></a>
## Arquivo: `docgen/scanner.py`
**Linguagem:** Python | **Linhas de Código:** 126 | **Comentários:** 187

### Descrição do Módulo
> Scanner de repositório e analisador de arquivos.
Varre a árvore de diretórios respeitando regras do .gitignore,
calcula linhas de código (SLOC), comentários e identifica manifests.

### `class` IgnoreMatcher
```python
class IgnoreMatcher
```

Implementa correspondência de padrões estilo .gitignore.

#### Métodos da Classe
- **`__init__`**`(root_dir, custom_patterns)`
- **`_load_file`**`(filepath)` -> `None`
- **`is_ignored`**`(path)` -> `bool`
  - *Verifica se um determinado Path deve ser ignorado.*

### `function` detect_language
```python
detect_language(path: Path) -> str
```

Identifica a linguagem pelo nome ou extensão do arquivo.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `path` | `Path` | - |

### `function` count_file_lines
```python
count_file_lines(path: Path, language: str) -> Tuple[int, int, int, int]
```

Analisa as linhas de um arquivo e retorna:
(total_lines, code_lines, comment_lines, blank_lines)

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `path` | `Path` | - |
| `language` | `str` | - |

### `class` RepositoryScanner
```python
class RepositoryScanner
```

Escaneia o repositório e constrói a lista inicial de arquivos e métricas.

#### Métodos da Classe
- **`__init__`**`(root_dir, custom_ignores)`
- **`scan`**`()` -> `List[FileInfo]`
  - *Varre o repositório retornando FileInfo para todos os arquivos válidos.*
- **`calculate_metrics`**`(files)` -> `ProjectMetrics`
  - *Gera as métricas agregadas do projeto.*
- **`detect_manifests`**`()` -> `Tuple[Dict[str, str], List[str]]`
  - *Localiza manifests e extrai lista de dependências externas.*

---

<a id='docgen-cli-py'></a>
## Arquivo: `docgen/cli.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 218

### Descrição do Módulo
> Ponto de entrada da CLI do DocGen.
Orquestra a varredura, análise sintática, extração de conceitos e escrita dos Markdowns.

### `function` resolve_internal_dependencies
```python
resolve_internal_dependencies(files: List[FileInfo]) -> Dict[str, List[str]]
```

Mapeia os imports internos entre arquivos do projeto.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `files` | `List[FileInfo]` | - |

### `function` run_generate
```python
run_generate(args: argparse.Namespace) -> int
```

Executa a análise do repositório e a geração completa da documentação.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `args` | `argparse.Namespace` | - |

### `function` run_stats
```python
run_stats(args: argparse.Namespace) -> int
```

Apenas analisa e exibe métricas no terminal.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `args` | `argparse.Namespace` | - |

### `function` run_init
```python
run_init(args: argparse.Namespace) -> int
```

Inicializa arquivos de configuração padrão.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `args` | `argparse.Namespace` | - |

### `function` main
```python
main(argv = None)
```

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `argv` | *any* | `None` |

---

<a id='docgen-models-py'></a>
## Arquivo: `docgen/models.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 122

### Descrição do Módulo
> Modelos de dados (dataclasses) para o DocGen.
Representa símbolos, arquivos, módulos, métricas, diagramas e termos de domínio.

### `class` SymbolType
```python
class SymbolType(str, Enum)
```

### `class` ParameterInfo
```python
@dataclass
class ParameterInfo
```

#### Métodos da Classe
- **`formatted`**`()` -> `str`

### `class` SymbolInfo
```python
@dataclass
class SymbolInfo
```

#### Métodos da Classe
- **`signature`**`()` -> `str`
  - *Retorna uma assinatura formatada e legível.*

### `class` ImportInfo
```python
@dataclass
class ImportInfo
```

### `class` FileInfo
```python
@dataclass
class FileInfo
```

### `class` ModuleGroup
```python
@dataclass
class ModuleGroup
```

### `class` ProjectMetrics
```python
@dataclass
class ProjectMetrics
```

### `class` UbiquitousTerm
```python
@dataclass
class UbiquitousTerm
```

### `class` ProjectData
```python
@dataclass
class ProjectData
```

---

<a id='docgen-config-py'></a>
## Arquivo: `docgen/config.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 166

### Descrição do Módulo
> Configurações, constantes e mapeamentos padrão do DocGen.

### `function` get_primary_programming_language
```python
get_primary_programming_language(language_dist: Dict[str, Any]) -> str
```

Retorna a linguagem de programação principal, desconsiderando arquivos de doc/config.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `language_dist` | `Dict[str, Any]` | - |

---

<a id='docgen-server-py'></a>
## Arquivo: `docgen/server.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 278

### Descrição do Módulo
> Servidor HTTP embutido com visualizador interativo moderno de Markdown e Mermaid.
Zero dependências externas: utiliza http.server da biblioteca padrão.

### `constant` HTML_TEMPLATE
```python
HTML_TEMPLATE()
```

### `class` DocViewerHandler
```python
class DocViewerHandler(BaseHTTPRequestHandler)
```

Handler HTTP para servir a UI interativa e os arquivos Markdown.

#### Métodos da Classe
- **`do_GET`**`()`

### `function` start_doc_server
```python
start_doc_server(docs_path: str = 'docs', port: int = 8080)
```

Inicia o servidor de visualização local.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `docs_path` | `str` | `'docs'` |
| `port` | `int` | `8080` |

---

<a id='docgen-ui-py'></a>
## Arquivo: `docgen/ui.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 85

### Descrição do Módulo
> Terminal UI com cores ANSI, tabelas formatadas e indicadores visuais elegantes sem dependências externas.

### `class` Colors
```python
class Colors
```

### `function` print_banner
```python
print_banner()
```

Exibe o cabeçalho estilizado do DocGen.

### `function` print_step
```python
print_step(title: str, status: str = '...', end: str = '\n')
```

Imprime uma etapa do processo.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `title` | `str` | - |
| `status` | `str` | `'...'` |
| `end` | `str` | `'\n'` |

### `function` print_success
```python
print_success(title: str)
```

Imprime confirmação de sucesso.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `title` | `str` | - |

### `function` print_info
```python
print_info(message: str)
```

Imprime mensagem informativa.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `message` | `str` | - |

### `function` print_warning
```python
print_warning(message: str)
```

Imprime aviso.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `message` | `str` | - |

### `function` print_error
```python
print_error(message: str)
```

Imprime erro.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `message` | `str` | - |

### `function` print_table
```python
print_table(headers: List[str], rows: List[List[Any]], title: str = '')
```

Renderiza uma tabela formatada com bordas Unicode no terminal.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `headers` | `List[str]` | - |
| `rows` | `List[List[Any]]` | - |
| `title` | `str` | `''` |

---

<a id='docgen-generators-c4_generator-py'></a>
## Arquivo: `docgen/generators/c4_generator.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 140

### Descrição do Módulo
> Gerador de documentação no Modelo C4 (Contexto, Containers, Componentes e Código).
Gera diagramas Mermaid e detalhamento textual baseado na arquitetura de Simon Brown.

### `function` generate_c4_documentation
```python
generate_c4_documentation(project: ProjectData, lang: str = 'pt') -> str
```

Gera o documento completo C4_MODEL.md.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |
| `lang` | `str` | `'pt'` |

---

<a id='docgen-generators-ubiquitous_language_generator-py'></a>
## Arquivo: `docgen/generators/ubiquitous_language_generator.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 116

### Descrição do Módulo
> Gerador de Linguagem Ubíqua (Ubiquitous Language / Glossário de Domínio - DDD).
Extrai conceitos centrais do negócio, entidades, value objects, enums e operações do código.

### `function` extract_ubiquitous_terms
```python
extract_ubiquitous_terms(project: ProjectData) -> List[UbiquitousTerm]
```

Analisa as definições de classes, tipos e enums para compor a Linguagem Ubíqua.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |

### `function` generate_ubiquitous_language_markdown
```python
generate_ubiquitous_language_markdown(project: ProjectData, lang: str = 'pt') -> str
```

Gera o documento UBIQUITOUS_LANGUAGE.md.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |
| `lang` | `str` | `'pt'` |

---

<a id='docgen-generators-api_reference_generator-py'></a>
## Arquivo: `docgen/generators/api_reference_generator.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 85

### Descrição do Módulo
> Gerador de referência de API e catálogo detalhado de classes, métodos e funções.

### `function` generate_api_reference_markdown
```python
generate_api_reference_markdown(project: ProjectData, lang: str = 'pt') -> str
```

Gera o documento API_REFERENCE.md.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |
| `lang` | `str` | `'pt'` |

---

<a id='docgen-generators-doc_suite-py'></a>
## Arquivo: `docgen/generators/doc_suite.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 283

### Descrição do Módulo
> Orquestrador central de geração da suíte de documentação Markdown.
Coordena a criação de todos os artefatos técnicos, suportando modo multi-arquivos ou consolidado (--single-file).

### `function` generate_directory_tree
```python
generate_directory_tree(files: List[str], max_depth: int = 3) -> str
```

Gera uma árvore visual de diretórios em texto/ASCII.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `files` | `List[str]` | - |
| `max_depth` | `int` | `3` |

### `class` DocSuiteGenerator
```python
class DocSuiteGenerator
```

Orquestra a escrita dos documentos Markdown.

#### Métodos da Classe
- **`__init__`**`(project_data, output_dir, lang, ai_provider)`
- **`generate_all`**`(single_file, single_file_name)` -> `List[str]`
  - *Gera todos os arquivos e retorna a lista de caminhos gravados.*
- **`_build_index`**`()` -> `str`
- **`_build_architecture`**`()` -> `str`
- **`_build_dependencies`**`()` -> `str`
- **`_build_metrics`**`()` -> `str`
- **`_build_consolidated_documentation`**`()` -> `str`
  - *Gera um único arquivo DOCUMENTATION.md contendo todas as seções.*

---

<a id='docgen-generators-static_site_generator-py'></a>
## Arquivo: `docgen/generators/static_site_generator.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 280

### Descrição do Módulo
> Gerador de site estático HTML para publicação direta no GitHub Pages, GitLab Pages ou navegação offline.
Inclui visualizador completo, tema dark mode, renderizador de Mermaid e dados pré-embutidos.

### `function` build_static_html_viewer
```python
build_static_html_viewer(project_name: str, doc_contents: Dict[str, str]) -> str
```

Gera um index.html autossuficiente contendo todos os Markdowns embutidos.
Funciona 100% estático em qualquer servidor (como GitHub Pages) ou via file://.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project_name` | `str` | - |
| `doc_contents` | `Dict[str, str]` | - |

---

<a id='docgen-generators-mermaid-py'></a>
## Arquivo: `docgen/generators/mermaid.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 144

### Descrição do Módulo
> Gerador de diagramas Mermaid para arquitetura, componentes, dependências e classes.

### `function` sanitize_id
```python
sanitize_id(text: str) -> str
```

Sanitiza strings para identificadores válidos em nós Mermaid.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `text` | `str` | - |

### `function` generate_architecture_diagram
```python
generate_architecture_diagram(project: ProjectData) -> str
```

Gera um diagrama de arquitetura em alto nível agrupando módulos em subgraphs.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |

### `constant` IGNORED_BASE_CLASSES
```python
IGNORED_BASE_CLASSES()
```

### `function` is_test_file
```python
is_test_file(path: str) -> bool
```

Verifica se o arquivo é um arquivo de teste.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `path` | `str` | - |

### `function` sanitize_method_for_mermaid
```python
sanitize_method_for_mermaid(method) -> str
```

Sanitiza o nome e retorno do método para sintaxe estrita do Mermaid classDiagram.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `method` | *any* | - |

### `function` generate_class_diagram
```python
generate_class_diagram(files: List[FileInfo]) -> str
```

Gera um diagrama de classes Mermaid válido para entidades e classes de domínio.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `files` | `List[FileInfo]` | - |

### `function` generate_dependency_graph
```python
generate_dependency_graph(internal_deps: Dict[str, List[str]]) -> str
```

Gera o grafo de dependências internas entre módulos do projeto.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `internal_deps` | `Dict[str, List[str]]` | - |

---

<a id='docgen-generators-architecture_generator-py'></a>
## Arquivo: `docgen/generators/architecture_generator.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 144

### Descrição do Módulo
> Gerador de documentação arquitetural avançada:
- HLD (High-Level Design)
- LLD (Low-Level Design)
- DAS (Documento de Arquitetura de Software / Modelo 4+1 & Arc42)

### `function` generate_hld
```python
generate_hld(project: ProjectData, lang: str = 'pt') -> str
```

Gera o documento High-Level Design (HLD.md).

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |
| `lang` | `str` | `'pt'` |

### `function` generate_das
```python
generate_das(project: ProjectData, lang: str = 'pt') -> str
```

Gera o Documento de Arquitetura de Software (DAS.md) no padrão Arc42 / 4+1 Views.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `project` | `ProjectData` | - |
| `lang` | `str` | `'pt'` |

---

<a id='docgen-parsers-base-py'></a>
## Arquivo: `docgen/parsers/base.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 18

### Descrição do Módulo
> Classe base para parsers de linguagem do DocGen.

### `class` BaseParser
```python
class BaseParser(ABC)
```

Contrato base para analisadores de código fonte.

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
  - *Retorna True se o parser suporta o arquivo informado.*
- **`parse`**`(file_info)` -> `FileInfo`
  - *Executa a análise sintática e semântica do arquivo,*

---

<a id='docgen-parsers-js_ts_parser-py'></a>
## Arquivo: `docgen/parsers/js_ts_parser.py`
**Linguagem:** Python | **Linhas de Código:** 48 | **Comentários:** 221

### Descrição do Módulo
> Parser para JavaScript e TypeScript (incluindo TSX/JSX).
Extrai classes, interfaces, tipos, funções, imports, exports, JSDoc e rotas Express/Next.js.

### `class` JsTsParser
```python
class JsTsParser(BaseParser)
```

Parser estrutural e regex para JavaScript e TypeScript.

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
- **`parse`**`(file_info)` -> `FileInfo`
- **`_extract_imports`**`(content, file_info)` -> `None`
  - *Extrai declarações import e require.*
- **`_extract_jsdocs`**`(content)` -> `dict[int, str]`
  - *Associa blocos de comentário JSDoc à linha subsequente de código.*
- **`_parse_ts_params`**`(raw)` -> `List[ParameterInfo]`
  - *Faz o parse de parâmetros tipados de TypeScript/JavaScript.*

---

<a id='docgen-parsers-go_parser-py'></a>
## Arquivo: `docgen/parsers/go_parser.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 147

### Descrição do Módulo
> Parser para a linguagem Go.
Extrai pacotes, structs, interfaces, funções, métodos (com receivers) e imports.

### `class` GoParser
```python
class GoParser(BaseParser)
```

Parser estrutural para código Go.

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
- **`parse`**`(file_info)` -> `FileInfo`
- **`_extract_imports`**`(content, file_info)` -> `None`
- **`_parse_go_params`**`(raw)` -> `list[ParameterInfo]`

---

<a id='docgen-parsers-rust_parser-py'></a>
## Arquivo: `docgen/parsers/rust_parser.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 128

### Descrição do Módulo
> Parser para a linguagem Rust.
Extrai structs, enums, traits, blocos impl, funções e comentários rustdoc (///).

### `class` RustParser
```python
class RustParser(BaseParser)
```

Parser estrutural para código Rust.

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
- **`parse`**`(file_info)` -> `FileInfo`
- **`_parse_rust_params`**`(raw)` -> `list[ParameterInfo]`

---

<a id='docgen-parsers-java_parser-py'></a>
## Arquivo: `docgen/parsers/java_parser.py`
**Linguagem:** Python | **Linhas de Código:** 85 | **Comentários:** 46

### Descrição do Módulo
> Parser para Java, C# e Kotlin.
Extrai classes, interfaces, records, métodos, anotações e comentários Javadoc.

### `class` JavaParser
```python
class JavaParser(BaseParser)
```

Parser para linguagens orientadas a objetos baseadas em classes (Java, C#, Kotlin).

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
- **`parse`**`(file_info)` -> `FileInfo`
- **`_parse_params`**`(raw)` -> `list[ParameterInfo]`

---

<a id='docgen-parsers-generic_parser-py'></a>
## Arquivo: `docgen/parsers/generic_parser.py`
**Linguagem:** Python | **Linhas de Código:** 23 | **Comentários:** 26

### Descrição do Módulo
> Parser genérico para arquivos de configuração, scripts shell, SQL, Dockerfile, etc.
Extrai comentários de cabeçalho, instruções principais e variáveis.

### `class` GenericParser
```python
class GenericParser(BaseParser)
```

Parser de fallback para qualquer arquivo de código ou configuração.

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
- **`parse`**`(file_info)` -> `FileInfo`

---

<a id='docgen-parsers-python_parser-py'></a>
## Arquivo: `docgen/parsers/python_parser.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 180

### Descrição do Módulo
> Parser de código Python utilizando o módulo AST nativo.
Extrai classes, herança, métodos, funções, decoradores, anotações de tipo e imports.

### `function` _format_annotation
```python
_format_annotation(node: Optional[ast.AST]) -> str
```

Converte um nó AST de anotação de tipo em string legível.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `node` | `Optional[ast.AST]` | - |

### `function` _format_decorator
```python
_format_decorator(node: ast.AST) -> str
```

Converte um nó AST de decorador em string.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `node` | `ast.AST` | - |

### `class` PythonParser
```python
class PythonParser(BaseParser)
```

Parser para arquivos Python usando AST.

#### Métodos da Classe
- **`can_parse`**`(file_info)` -> `bool`
- **`parse`**`(file_info)` -> `FileInfo`
- **`_extract_import`**`(node, file_info)` -> `None`
- **`_extract_class`**`(node)` -> `SymbolInfo`
- **`_extract_function`**`(node, is_method)` -> `SymbolInfo`

---

<a id='docgen-parsers-__init__-py'></a>
## Arquivo: `docgen/parsers/__init__.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 35

### Descrição do Módulo
> Registro e orquestração de parsers de código.

### `class` ParserRegistry
```python
class ParserRegistry
```

Gerencia a lista de parsers disponíveis e aplica o mais adequado a cada arquivo.

#### Métodos da Classe
- **`__init__`**`()`
- **`parse_file`**`(file_info)` -> `FileInfo`
  - *Aplica o primeiro parser que aceitar o arquivo.*
- **`parse_all`**`(files)` -> `List[FileInfo]`
  - *Processa todos os arquivos da lista.*

---

<a id='docgen-ai-context_builder-py'></a>
## Arquivo: `docgen/ai/context_builder.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 84

### Descrição do Módulo
> Construtor de contexto semântico do repositório para o modelo de IA.
Extrai metadados, árvore de módulos, contratos do AST e trechos essenciais de código.

### `class` CodebaseContextBuilder
```python
class CodebaseContextBuilder
```

Monta o contexto técnico completo do repositório para ingestão por LLMs.

#### Métodos da Classe
- **`__init__`**`(project_data, max_char_budget)`
- **`build_context`**`()` -> `str`
  - *Produz uma representação densa e estruturada do repositório.*

---

<a id='docgen-ai-prompts-py'></a>
## Arquivo: `docgen/ai/prompts.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 94

### Descrição do Módulo
> Engenharia de prompts para o arquiteto de software de IA.
Instruções rigorosas para geração de Modelo C4, HLD, LLD, DAS, ADRs e Linguagem Ubíqua.

### `constant` SYSTEM_ARCHITECT_PROMPT
```python
SYSTEM_ARCHITECT_PROMPT()
```

### `constant` C4_PROMPT
```python
C4_PROMPT()
```

### `constant` HLD_PROMPT
```python
HLD_PROMPT()
```

### `constant` DAS_PROMPT
```python
DAS_PROMPT()
```

### `constant` UBIQUITOUS_LANGUAGE_PROMPT
```python
UBIQUITOUS_LANGUAGE_PROMPT()
```

---

<a id='docgen-ai-provider-py'></a>
## Arquivo: `docgen/ai/provider.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 258

### Descrição do Módulo
> Provedores de LLM para o DocGen.
Suporta Google Gemini, OpenAI, Anthropic Claude e Ollama local,
utilizando exclusivamente a biblioteca padrão (urllib) para zero dependências externas.

### `class` LLMProvider
```python
class LLMProvider(ABC)
```

Interface abstrata para provedores de inteligência artificial generativa.

#### Métodos da Classe
- **`generate`**`(prompt, system_prompt)` -> `str`
  - *Gera resposta a partir de um prompt e instrução de sistema.*
- **`name`**`()` -> `str`
  - *Nome do provedor.*
- **`model_name`**`()` -> `str`
  - *Nome do modelo utilizado.*

### `class` GeminiProvider
```python
class GeminiProvider(LLMProvider)
```

Integração com Google Gemini API via REST nativo.

#### Métodos da Classe
- **`__init__`**`(api_key, model)`
- **`name`**`()` -> `str`
- **`model_name`**`()` -> `str`
- **`generate`**`(prompt, system_prompt)` -> `str`

### `class` OpenAIProvider
```python
class OpenAIProvider(LLMProvider)
```

Integração com OpenAI (GPT-4o, GPT-4o-mini) via REST nativo.

#### Métodos da Classe
- **`__init__`**`(api_key, model)`
- **`name`**`()` -> `str`
- **`model_name`**`()` -> `str`
- **`generate`**`(prompt, system_prompt)` -> `str`

### `class` AnthropicProvider
```python
class AnthropicProvider(LLMProvider)
```

Integração com Anthropic Claude via REST nativo.

#### Métodos da Classe
- **`__init__`**`(api_key, model)`
- **`name`**`()` -> `str`
- **`model_name`**`()` -> `str`
- **`generate`**`(prompt, system_prompt)` -> `str`

### `class` OllamaProvider
```python
class OllamaProvider(LLMProvider)
```

Integração com LLM local via Ollama (DeepSeek-R1, Llama 3, Qwen, etc.).

#### Métodos da Classe
- **`__init__`**`(base_url, model)`
- **`name`**`()` -> `str`
- **`model_name`**`()` -> `str`
- **`generate`**`(prompt, system_prompt)` -> `str`

### `class` MockProvider
```python
class MockProvider(LLMProvider)
```

Provedor mock utilizado para testes unitários ou modo determinístico.

#### Métodos da Classe
- **`__init__`**`(model)`
- **`name`**`()` -> `str`
- **`model_name`**`()` -> `str`
- **`generate`**`(prompt, system_prompt)` -> `str`

### `function` get_ai_provider
```python
get_ai_provider(provider_name: Optional[str] = None, model: Optional[str] = None, api_key: Optional[str] = None, ollama_url: Optional[str] = None) -> Optional[LLMProvider]
```

Fábrica inteligente de provedores de IA.
Detecta automaticamente com base em flags e variáveis de ambiente:
1. Flag explícita --provider
2. GEMINI_API_KEY -> Gemini
3. OPENAI_API_KEY -> OpenAI
4. ANTHROPIC_API_KEY -> Anthropic
5. Ollama local (se especificado ou rodando)

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `provider_name` | `Optional[str]` | `None` |
| `model` | `Optional[str]` | `None` |
| `api_key` | `Optional[str]` | `None` |
| `ollama_url` | `Optional[str]` | `None` |

---

<a id='docgen-ai-architect-py'></a>
## Arquivo: `docgen/ai/architect.py`
**Linguagem:** Python | **Linhas de Código:** 0 | **Comentários:** 62

### Descrição do Módulo
> Orquestrador de IA do DocGen (AI Architect Engine).
Executa as cadeias de raciocínio arquitetural com o LLM sobre o contexto do repositório.

### `function` _clean_llm_markdown
```python
_clean_llm_markdown(text: str) -> str
```

Remove blocos de markdown envolventes desnecessários retornados por LLMs.

#### Parâmetros
| Nome | Tipo | Default |
|---|---|---|
| `text` | `str` | - |

### `class` AIArchitect
```python
class AIArchitect
```

Agente de arquitetura de software alimentado por IA Generativa.

#### Métodos da Classe
- **`__init__`**`(project_data, provider, lang)`
- **`get_context`**`()` -> `str`
  - *Gera ou recupera o contexto técnico do repositório.*
- **`_call_llm`**`(prompt_template, task_name)` -> `str`
  - *Executa a chamada para o provedor de IA com contexto preenchido.*
- **`synthesize_c4`**`()` -> `str`
  - *Gera o documento C4_MODEL.md via raciocínio de IA.*
- **`synthesize_hld`**`()` -> `str`
  - *Gera o documento HLD.md via raciocínio de IA.*
- **`synthesize_das`**`()` -> `str`
  - *Gera o documento DAS.md via raciocínio de IA.*
- **`synthesize_ubiquitous_language`**`()` -> `str`
  - *Gera a Linguagem Ubíqua e Bounded Contexts via raciocínio de IA.*

---


---

# Dependências do Projeto: doc-gen

## Grafo de Dependências Internas
```mermaid
graph LR
    tests_test_cli_py["test_cli.py"] --> docgen_cli_py["cli.py"]
    tests_test_python_parser_py["test_python_parser.py"] --> docgen_models_py["models.py"]
    tests_test_python_parser_py["test_python_parser.py"] --> docgen_parsers_python_parser_py["python_parser.py"]
    tests_test_js_parser_py["test_js_parser.py"] --> docgen_models_py["models.py"]
    tests_test_js_parser_py["test_js_parser.py"] --> docgen_parsers_js_ts_parser_py["js_ts_parser.py"]
    tests_test_ai_py["test_ai.py"] --> docgen_models_py["models.py"]
    tests_test_ai_py["test_ai.py"] --> docgen_ai_provider_py["provider.py"]
    tests_test_ai_py["test_ai.py"] --> docgen_ai_context_builder_py["context_builder.py"]
    tests_test_ai_py["test_ai.py"] --> docgen_ai_architect_py["architect.py"]
    tests_test_ai_py["test_ai.py"] --> docgen_generators_doc_suite_py["doc_suite.py"]
    tests_test_ai_py["test_ai.py"] --> docgen_cli_py["cli.py"]
    tests_test_generators_py["test_generators.py"] --> docgen_models_py["models.py"]
    tests_test_generators_py["test_generators.py"] --> docgen_generators_c4_generator_py["c4_generator.py"]
    tests_test_generators_py["test_generators.py"] --> docgen_generators_architecture_generator_py["architecture_generator.py"]
    tests_test_generators_py["test_generators.py"] --> docgen_generators_ubiquitous_language_generator_py["ubiquitous_language_generator.py"]
    tests_test_generators_py["test_generators.py"] --> docgen_generators_doc_suite_py["doc_suite.py"]
    tests_test_scanner_py["test_scanner.py"] --> docgen_scanner_py["scanner.py"]
    tests_test_scanner_py["test_scanner.py"] --> docgen_models_py["models.py"]
    docgen_scanner_py["scanner.py"] --> docgen_config_py["config.py"]
    docgen_scanner_py["scanner.py"] --> docgen_models_py["models.py"]
    docgen___main___py["__main__.py"] --> docgen_cli_py["cli.py"]
    docgen_cli_py["cli.py"] --> docgen_scanner_py["scanner.py"]
    docgen_cli_py["cli.py"] --> docgen___main___py["__main__.py"]
    docgen_cli_py["cli.py"] --> docgen_models_py["models.py"]
    docgen_cli_py["cli.py"] --> docgen_config_py["config.py"]
    docgen_cli_py["cli.py"] --> docgen_server_py["server.py"]
    docgen_cli_py["cli.py"] --> docgen_ui_py["ui.py"]
    docgen_cli_py["cli.py"] --> docgen___init___py["__init__.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_c4_generator_py["c4_generator.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_ubiquitous_language_generator_py["ubiquitous_language_generator.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_api_reference_generator_py["api_reference_generator.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_doc_suite_py["doc_suite.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_static_site_generator_py["static_site_generator.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_mermaid_py["mermaid.py"]
    docgen_cli_py["cli.py"] --> docgen_generators_architecture_generator_py["architecture_generator.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_base_py["base.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_js_ts_parser_py["js_ts_parser.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_go_parser_py["go_parser.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_rust_parser_py["rust_parser.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_java_parser_py["java_parser.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_generic_parser_py["generic_parser.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers_python_parser_py["python_parser.py"]
    docgen_cli_py["cli.py"] --> docgen_parsers___init___py["__init__.py"]
    docgen_cli_py["cli.py"] --> docgen_ai_context_builder_py["context_builder.py"]
    docgen_cli_py["cli.py"] --> docgen_ai_prompts_py["prompts.py"]
    docgen_cli_py["cli.py"] --> docgen_ai_provider_py["provider.py"]
    docgen_cli_py["cli.py"] --> docgen_ai_architect_py["architect.py"]
    docgen_cli_py["cli.py"] --> docgen_ai___init___py["__init__.py"]
    docgen_server_py["server.py"] --> docgen_ui_py["ui.py"]
    docgen_generators_c4_generator_py["c4_generator.py"] --> docgen_models_py["models.py"]
    docgen_generators_c4_generator_py["c4_generator.py"] --> docgen_config_py["config.py"]
    docgen_generators_c4_generator_py["c4_generator.py"] --> docgen_generators_mermaid_py["mermaid.py"]
    docgen_generators_ubiquitous_language_generator_py["ubiquitous_language_generator.py"] --> docgen_models_py["models.py"]
    docgen_generators_ubiquitous_language_generator_py["ubiquitous_language_generator.py"] --> docgen_generators_mermaid_py["mermaid.py"]
    docgen_generators_api_reference_generator_py["api_reference_generator.py"] --> docgen_models_py["models.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_models_py["models.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_ai_provider_py["provider.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_ai_architect_py["architect.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_ui_py["ui.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_generators_mermaid_py["mermaid.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_generators_c4_generator_py["c4_generator.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_generators_architecture_generator_py["architecture_generator.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_generators_ubiquitous_language_generator_py["ubiquitous_language_generator.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_generators_api_reference_generator_py["api_reference_generator.py"]
    docgen_generators_doc_suite_py["doc_suite.py"] --> docgen_generators_static_site_generator_py["static_site_generator.py"]
    docgen_generators_mermaid_py["mermaid.py"] --> docgen_models_py["models.py"]
    docgen_generators_architecture_generator_py["architecture_generator.py"] --> docgen_models_py["models.py"]
    docgen_generators_architecture_generator_py["architecture_generator.py"] --> docgen_config_py["config.py"]
    docgen_parsers_base_py["base.py"] --> docgen_models_py["models.py"]
    docgen_parsers_js_ts_parser_py["js_ts_parser.py"] --> docgen_models_py["models.py"]
    docgen_parsers_js_ts_parser_py["js_ts_parser.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers_go_parser_py["go_parser.py"] --> docgen_models_py["models.py"]
    docgen_parsers_go_parser_py["go_parser.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers_rust_parser_py["rust_parser.py"] --> docgen_models_py["models.py"]
    docgen_parsers_rust_parser_py["rust_parser.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers_java_parser_py["java_parser.py"] --> docgen_models_py["models.py"]
    docgen_parsers_java_parser_py["java_parser.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers_generic_parser_py["generic_parser.py"] --> docgen_models_py["models.py"]
    docgen_parsers_generic_parser_py["generic_parser.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers_python_parser_py["python_parser.py"] --> docgen_models_py["models.py"]
    docgen_parsers_python_parser_py["python_parser.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_models_py["models.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_base_py["base.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_python_parser_py["python_parser.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_js_ts_parser_py["js_ts_parser.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_go_parser_py["go_parser.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_rust_parser_py["rust_parser.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_java_parser_py["java_parser.py"]
    docgen_parsers___init___py["__init__.py"] --> docgen_parsers_generic_parser_py["generic_parser.py"]
    docgen_ai_context_builder_py["context_builder.py"] --> docgen_models_py["models.py"]
    docgen_ai_architect_py["architect.py"] --> docgen_models_py["models.py"]
    docgen_ai_architect_py["architect.py"] --> docgen_ai_provider_py["provider.py"]
    docgen_ai_architect_py["architect.py"] --> docgen_ai_context_builder_py["context_builder.py"]
    docgen_ai_architect_py["architect.py"] --> docgen_ai_prompts_py["prompts.py"]
    docgen_ai_architect_py["architect.py"] --> docgen_ui_py["ui.py"]
    docgen_ai___init___py["__init__.py"] --> docgen_ai_provider_py["provider.py"]
    docgen_ai___init___py["__init__.py"] --> docgen_ai_architect_py["architect.py"]
```

---

## Dependências Externas Registradas
*Nenhuma dependência externa registrada em arquivos de manifesto.*


---

# Métricas de Código e Estatísticas: doc-gen

## Resumo Geral
- **Arquivos Totais Analisados:** 42
- **Linhas Totais:** 7,612
- **Linhas de Código Efetivo (SLOC):** 2,039
- **Linhas de Comentários:** 4,337
- **Linhas em Branco:** 1,236
- **Taxa de Documentação / Comentários:** 212.7%

---

## Distribuição por Linguagem

| Linguagem | Arquivos | Linhas de Código | Total Linhas | % Código |
|---|---|---|---|---|
| **Markdown** | 3 | 1,597 | 2,309 | 78.3% |
| **Python** | 35 | 305 | 5,132 | 15.0% |
| **YAML** | 2 | 85 | 107 | 4.2% |
| **Other** | 1 | 30 | 38 | 1.5% |
| **TOML** | 1 | 22 | 26 | 1.1% |
