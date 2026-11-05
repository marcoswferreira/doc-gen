"""
Gerador de documentação arquitetural avançada:
- HLD (High-Level Design)
- LLD (Low-Level Design)
- DAS (Documento de Arquitetura de Software / Modelo 4+1 & Arc42)
"""

from typing import List
from pathlib import Path
from docgen.models import ProjectData, SymbolType


def generate_hld(project: ProjectData, lang: str = "pt") -> str:
    """Gera o documento High-Level Design (HLD.md)."""
    pname = project.project_name
    primary_lang = list(project.metrics.language_distribution.keys())[0] if project.metrics.language_distribution else "Multi-language"
    total_loc = project.metrics.total_code_lines

    md = []
    md.append(f"# High-Level Design (HLD): {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> O **High-Level Design (HLD)** documenta a arquitetura macro, o estilo arquitetural, as fronteiras do sistema e os requisitos não-funcionais que orientam a engenharia da solução.")
    md.append("")
    md.append("---")
    md.append("")

    # 1. Visão Geral
    md.append("## 1. Visão Geral da Solução")
    md.append(f"O projeto **{pname}** foi projetado como uma solução modular desenvolvida principalmente em **{primary_lang}**, totalizando aproximadamente **{total_loc:,} linhas de código** distribuídas em **{project.metrics.total_files} arquivos**.")
    md.append("")
    md.append("### Objetivos Principais")
    md.append("- Fornecer processamento confiável, previsível e desacoplado.")
    md.append("- Permitir fácil extensão para novas linguagens e formatos sem quebrar contratos existentes.")
    md.append("- Garantir portabilidade multiplataforma sem necessidade de dependências pesadas de terceiros.")
    md.append("")

    # 2. Estilo Arquitetural
    md.append("## 2. Estilo Arquitetural")
    md.append("A solução adota uma **Arquitetura em Camadas (Layered Architecture)** combinada com o padrão **Pipeline / Filter**, onde o fluxo de dados passa por etapas sequenciais bem definidas:")
    md.append("")
    md.append("```mermaid")
    md.append("flowchart LR")
    md.append("    A[Input: Repositório] --> B[Camada de Descoberta / Scanner]")
    md.append("    B --> C[Camada de Análise / Parsers]")
    md.append("    C --> D[Camada de Modelo / Grafo de Dados]")
    md.append("    D --> E[Camada de Geração / Renderers]")
    md.append("    E --> F[Output: Markdown / Web]")
    md.append("```")
    md.append("")
    md.append("### Benefícios do Estilo Adotado")
    md.append("- **Separação de Responsabilidades (SoC)**: O módulo de varredura não sabe como gerar Markdown; o gerador não sabe como o AST foi extraído.")
    md.append("- **Testabilidade Isolada**: Cada camada pode ser testada unitariamente com fixtures e dados mockados.")
    md.append("- **Extensibilidade**: Novos parsers e novos geradores podem ser adicionados plugando-se nas fábricas correspondentes.")
    md.append("")

    # 3. Requisitos Não-Funcionais
    md.append("## 3. Requisitos Não-Funcionais (RNFs)")
    md.append("| Categoria | Requisito | Estratégia de Implementação |")
    md.append("|---|---|---|")
    md.append("| **Portabilidade** | Executar em Linux, macOS e Windows sem compilação nativa externa | Uso de módulos padrão (`pathlib`, `os`, `sys`, `ast`) compatíveis entre SOs. |")
    md.append("| **Performance** | Analisar repositórios em tempo inferior a poucos segundos | Otimização de varredura de diretórios com poda rápida via `.gitignore` e regex pré-compiladas. |")
    md.append("| **Autonomia** | Funcionamento 100% offline (Zero dependência de rede obrigatória) | Motor sintático nativo que dispensa conexões remotas ou APIs externas para gerar a documentação completa. |")
    md.append("| **Manutenibilidade** | Código limpo, tipado e com alta taxa de documentação | Dataclasses estritas, contratos abstratos (`BaseParser`) e modularização em submódulos. |")
    md.append("")

    # 4. Integrações
    md.append("## 4. Integrações e Fronteiras Externas")
    md.append("- **Sistema Operacional & File System**: Acesso a diretórios locais com permissão de leitura/escrita.")
    if project.external_dependencies:
        md.append("- **Bibliotecas Externas Registradas**:")
        for dep in project.external_dependencies[:10]:
            md.append(f"  - `{dep}`")
    else:
        md.append("- **Bibliotecas Externas**: Autossuficiente utilizando exclusivamente a runtime padrão.")

    return "\n".join(md)


def generate_lld(project: ProjectData, lang: str = "pt") -> str:
    """Gera o documento Low-Level Design (LLD.md)."""
    pname = project.project_name

    md = []
    md.append(f"# Low-Level Design (LLD): {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> O **Low-Level Design (LLD)** detalha as estruturas de dados, assinaturas de contratos, padrões de projeto aplicados e fluxos de execução sequenciais detalhados.")
    md.append("")
    md.append("---")
    md.append("")

    # 1. Padrões de Projeto Identificados
    md.append("## 1. Padrões de Projeto (Design Patterns) Aplicados")
    md.append("")
    md.append("### A. Factory Method / Registry Pattern (`ParserRegistry`)")
    md.append("Gerencia a lista de analisadores especializados e instancia o parser correto com base na linguagem ou extensão detectada.")
    md.append("")
    md.append("### B. Strategy Pattern (`BaseParser`)")
    md.append("Cada analisador de linguagem (`PythonParser`, `JsTsParser`, `GoParser`, `RustParser`, `JavaParser`, `GenericParser`) implementa a interface comum `BaseParser`, permitindo troca dinâmica de estratégias de parsing.")
    md.append("")
    md.append("### C. Builder / Pipeline Pattern (`DocSuiteGenerator`)")
    md.append("Constrói a suíte completa de documentação (`INDEX`, `ARCHITECTURE`, `C4`, `HLD`, `LLD`, `DAS`, `ADRS`, `API`) passo a passo a partir do modelo unificado `ProjectData`.")
    md.append("")

    # 2. Diagrama de Sequência de Execução
    md.append("## 2. Diagrama de Sequência do Fluxo de Execução")
    md.append("")
    md.append("```mermaid")
    md.append("sequenceDiagram")
    md.append("    autonumber")
    md.append("    actor User as Desenvolvedor (CLI)")
    md.append("    participant CLI as CLI Entrypoint")
    md.append("    participant Scanner as Repository Scanner")
    md.append("    participant Registry as Parser Registry")
    md.append("    participant Parser as Language Parser")
    md.append("    participant Model as ProjectData")
    md.append("    participant Suite as DocSuiteGenerator")
    md.append("    participant FS as File System (docs/)")
    md.append("")
    md.append("    User->>CLI: executa docgen [PATH]")
    md.append("    CLI->>Scanner: scan(path, ignore_rules)")
    md.append("    Scanner->>Scanner: filtra .gitignore e calcula linhas")
    md.append("    Scanner-->>CLI: lista de FileInfo descobertos")
    md.append("    CLI->>Registry: parse_all(files)")
    md.append("    loop Para cada arquivo")
    md.append("        Registry->>Parser: parse(file_info)")
    md.append("        Parser->>Parser: extrai AST, docstrings, classes, rotas")
    md.append("        Parser-->>Registry: FileInfo enriquecido")
    md.append("    end")
    md.append("    Registry-->>CLI: todos os arquivos parseados")
    md.append("    CLI->>Model: compila ProjectData (métricas, grafo, termos)")
    md.append("    CLI->>Suite: generate(project_data)")
    md.append("    Suite->>FS: grava INDEX, ARCHITECTURE, C4, HLD, LLD, DAS, ADRs")
    md.append("    FS-->>Suite: OK")
    md.append("    Suite-->>CLI: resumo da geração")
    md.append("    CLI-->>User: exibe tabela de resumo e caminho dos arquivos")
    md.append("```")
    md.append("")

    # 3. Modelos de Dados e Contratos
    md.append("## 3. Estruturas de Dados e Entidades do Núcleo")
    md.append("- `FileInfo`: Encapsula caminho relativo, linguagem, contagem de linhas e lista de símbolos extraídos.")
    md.append("- `SymbolInfo`: Modela classes, métodos, interfaces, funções e rotas com assinaturas, docstrings e decoradores.")
    md.append("- `ParameterInfo`: Modela parâmetros formais, tipagem estática e valores default.")
    md.append("- `ProjectData`: Agrega métricas, listas de arquivos, grafos de importação e termos da linguagem ubíqua.")

    return "\n".join(md)


def generate_das(project: ProjectData, lang: str = "pt") -> str:
    """Gera o Documento de Arquitetura de Software (DAS.md) no padrão Arc42 / 4+1 Views."""
    pname = project.project_name
    primary_lang = list(project.metrics.language_distribution.keys())[0] if project.metrics.language_distribution else "Multi-language"

    md = []
    md.append(f"# Documento de Arquitetura de Software (DAS): {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> Este **Documento de Arquitetura de Software (DAS)** foi estruturado com base nas melhores práticas do padrão **Arc42** e do **Modelo 4+1 Visões de Philippe Kruchten**, registrando decisões, restrições, visões de processo e de implantação.")
    md.append("")
    md.append("---")
    md.append("")

    # 1. Introdução e Metas
    md.append("## 1. Introdução e Metas Arquiteturais")
    md.append(f"O objetivo do software **{pname}** é fornecer análise estática e geração estruturada de documentação técnica para bases de código heterogêneas.")
    md.append("")
    md.append("### Metas de Qualidade Prioritárias")
    md.append("1. **Alta Acurácia**: Extração fidedigna de tipos, classes, funções e comentários de documentação.")
    md.append("2. **Velocidade de Execução**: Varredura ágil mesmo em repositórios de grande porte.")
    md.append("3. **Legibilidade e Riqueza Visual**: Geração de Markdown estruturado com suporte nativo a diagramas Mermaid.")
    md.append("")

    # 2. Restrições Arquiteturais
    md.append("## 2. Restrições e Premissas Arquiteturais")
    md.append(f"- **Runtime Principal**: {primary_lang}.")
    md.append("- **Independência de Ambiente**: Compatibilidade direta com ambientes isolados (containers, sandboxes e pipelines de CI/CD).")
    md.append("- **Respeito a Políticas de Código**: Conformidade total com regras de exclusão (`.gitignore`, `.docgenignore`).")
    md.append("")

    # 3. Visão Lógica (Logical View)
    md.append("## 3. Visão Lógica (Logical View)")
    md.append("Mapeia a organização modular do software e como as responsabilidades são divididas entre os subsistemas:")
    md.append("")
    md.append("```mermaid")
    md.append("graph TD")
    md.append("    subgraph Presentation_Layer[\"Camada de Apresentação e CLI\"]")
    md.append("        CLI[\"CLI Controller / Terminal UI\"]")
    md.append("        Web[\"Built-in HTTP Server\"]")
    md.append("    end")
    md.append("    subgraph Core_Layer[\"Camada de Negócio e Processamento\"]")
    md.append("        Scanner[\"Repository Scanner\"]")
    md.append("        Parsers[\"AST & Structural Parsers\"]")
    md.append("        Analyzers[\"Metrics & Graph Analyzer\"]")
    md.append("    end")
    md.append("    subgraph Generation_Layer[\"Camada de Geração de Documentos\"]")
    md.append("        C4[\"C4 Model Generator\"]")
    md.append("        HLD_LLD[\"HLD & LLD Generator\"]")
    md.append("        DAS_Gen[\"DAS & ADR Generator\"]")
    md.append("        API_Gen[\"API Reference & Ubiquitous Language\"]")
    md.append("    end")
    md.append("    CLI --> Scanner")
    md.append("    CLI --> Parsers")
    md.append("    Parsers --> Analyzers")
    md.append("    Analyzers --> Generation_Layer")
    md.append("    Web -.-> Generation_Layer")
    md.append("```")
    md.append("")

    # 4. Visão de Processo (Process View)
    md.append("## 4. Visão de Processo (Process View)")
    md.append("- **Ciclo de Vida Síncrono e Determinístico**: Cada execução do pipeline opera em batch síncrono, garantindo idempotência (a mesma base de código gera o mesmo conjunto de documentações).")
    md.append("- **Uso de Memória**: O modelo `ProjectData` é retido em memória apenas durante o ciclo de execução e liberado após a escrita em disco.")
    md.append("")

    # 5. Visão de Implantação (Deployment View)
    md.append("## 5. Visão de Implantação e Execução (Deployment View)")
    md.append("O sistema pode ser distribuído e executado das seguintes maneiras:")
    md.append("1. **Executável Local**: Via CLI empacotada (`docgen`).")
    md.append("2. **Pipeline de CI/CD**: Executado em GitHub Actions, GitLab CI ou Jenkins para atualizar os documentos a cada pull request ou push.")
    md.append("3. **Container Docker**: Executável dentro de imagens base mínimas.")
    md.append("")

    # 6. Riscos e Débitos Técnicos
    md.append("## 6. Riscos Arquiteturais e Mitigações")
    md.append("| Risco Identificado | Impacto | Estratégia de Mitigação |")
    md.append("|---|---|---|")
    md.append("| Arquivos com sintaxe inválida no repositório | Falha durante o parseamento | Parsers implementados com blocos `try/except` resilientes e fallback para `GenericParser`. |")
    md.append("| Repositórios gigantescos com milhões de linhas | Lentidão ou estouro de memória | Limitação de tamanho individual de arquivo (5MB) e poda de diretórios ignorados antes do parse. |")
    md.append("| Falta de tipagem estática no código analisado | Documentação com tipos vazios | Detecção heurística de valores default e docstrings para enriquecer assinaturas. |")

    return "\n".join(md)

