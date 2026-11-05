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
    class TestCLI {
        +setUp()
        +tearDown()
        +test_cli_stats()
        +test_cli_generate_multi()
    }
    unittest_TestCase <|-- TestCLI
    class TestPythonParser {
        +setUp()
        +tearDown()
        +test_parse_classes_and_methods()
        +test_parse_routes()
    }
    unittest_TestCase <|-- TestPythonParser
    class TestJsTsParser {
        +setUp()
        +tearDown()
        +test_parse_typescript_interfaces_and_classes()
        +test_parse_express_routes()
    }
    unittest_TestCase <|-- TestJsTsParser
    class TestGenerators {
        +setUp()
        +tearDown()
        +test_c4_model_generation()
        +test_hld_lld_das_generation()
    }
    unittest_TestCase <|-- TestGenerators
    class TestScanner {
        +setUp()
        +tearDown()
        +test_ignore_matcher()
        +test_detect_language()
    }
    unittest_TestCase <|-- TestScanner
    class IgnoreMatcher {
        +__init__()
        +_load_file()
        +is_ignored()
    }
    class RepositoryScanner {
        +__init__()
        +scan()
        +calculate_metrics()
        +detect_manifests()
    }
    class SymbolType {
    }
    str <|-- SymbolType
    Enum <|-- SymbolType
    class ParameterInfo {
        +formatted()
    }
    class SymbolInfo {
        +signature()
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
```