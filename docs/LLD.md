# Low-Level Design (LLD): doc-gen

> [!NOTE]
> O **Low-Level Design (LLD)** detalha as estruturas de dados, assinaturas de contratos, padrões de projeto aplicados e fluxos de execução sequenciais detalhados.

---

## 1. Padrões de Projeto (Design Patterns) Aplicados

### A. Factory Method / Registry Pattern (`ParserRegistry`)
Gerencia a lista de analisadores especializados e instancia o parser correto com base na linguagem ou extensão detectada.

### B. Strategy Pattern (`BaseParser`)
Cada analisador de linguagem (`PythonParser`, `JsTsParser`, `GoParser`, `RustParser`, `JavaParser`, `GenericParser`) implementa a interface comum `BaseParser`, permitindo troca dinâmica de estratégias de parsing.

### C. Builder / Pipeline Pattern (`DocSuiteGenerator`)
Constrói a suíte completa de documentação (`INDEX`, `ARCHITECTURE`, `C4`, `HLD`, `LLD`, `DAS`, `ADRS`, `API`) passo a passo a partir do modelo unificado `ProjectData`.

## 2. Diagrama de Sequência do Fluxo de Execução

```mermaid
sequenceDiagram
    autonumber
    actor User as Desenvolvedor (CLI)
    participant CLI as CLI Entrypoint
    participant Scanner as Repository Scanner
    participant Registry as Parser Registry
    participant Parser as Language Parser
    participant Model as ProjectData
    participant Suite as DocSuiteGenerator
    participant FS as File System (docs/)

    User->>CLI: executa docgen [PATH]
    CLI->>Scanner: scan(path, ignore_rules)
    Scanner->>Scanner: filtra .gitignore e calcula linhas
    Scanner-->>CLI: lista de FileInfo descobertos
    CLI->>Registry: parse_all(files)
    loop Para cada arquivo
        Registry->>Parser: parse(file_info)
        Parser->>Parser: extrai AST, docstrings, classes, rotas
        Parser-->>Registry: FileInfo enriquecido
    end
    Registry-->>CLI: todos os arquivos parseados
    CLI->>Model: compila ProjectData (métricas, grafo, termos)
    CLI->>Suite: generate(project_data)
    Suite->>FS: grava INDEX, ARCHITECTURE, C4, HLD, LLD, DAS, ADRs
    FS-->>Suite: OK
    Suite-->>CLI: resumo da geração
    CLI-->>User: exibe tabela de resumo e caminho dos arquivos
```

## 3. Estruturas de Dados e Entidades do Núcleo
- `FileInfo`: Encapsula caminho relativo, linguagem, contagem de linhas e lista de símbolos extraídos.
- `SymbolInfo`: Modela classes, métodos, interfaces, funções e rotas com assinaturas, docstrings e decoradores.
- `ParameterInfo`: Modela parâmetros formais, tipagem estática e valores default.
- `ProjectData`: Agrega métricas, listas de arquivos, grafos de importação e termos da linguagem ubíqua.