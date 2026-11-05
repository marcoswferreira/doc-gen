"""
Gerador de documentação no Modelo C4 (Contexto, Containers, Componentes e Código).
Gera diagramas Mermaid e detalhamento textual baseado na arquitetura de Simon Brown.
"""

from pathlib import Path
from docgen.models import ProjectData, SymbolType
from docgen.generators.mermaid import sanitize_id


def generate_c4_documentation(project: ProjectData, lang: str = "pt") -> str:
    """Gera o documento completo C4_MODEL.md."""
    pname = project.project_name
    primary_lang = list(project.metrics.language_distribution.keys())[0] if project.metrics.language_distribution else "Multi-language"

    # Detecta se é CLI, Web, API ou Biblioteca
    is_cli = any("cli" in f.path.lower() or "bin" in f.path.lower() or "argparse" in str(f.imports) for f in project.files)
    is_web = any(f.language in ("HTML", "CSS", "TypeScript (React)", "JavaScript (React)") for f in project.files)
    has_api = any(s.symbol_type == SymbolType.ROUTE for f in project.files for s in f.symbols)

    system_nature = "Ferramenta de Linha de Comando (CLI)" if is_cli else ("Aplicação Web / Fullstack" if is_web else ("API / Microsserviço" if has_api else "Biblioteca / Módulo de Software"))

    md = []
    md.append(f"# Modelo C4: {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> O **Modelo C4** (Context, Containers, Components, Code) fornece uma maneira hierárquica e padronizada de mapear e comunicar a arquitetura de software em diferentes níveis de abstração.")
    md.append("")
    md.append("---")
    md.append("")

    # ==================== NÍVEL 1: CONTEXTO ====================
    md.append("## Nível 1: Diagrama de Contexto do Sistema (System Context)")
    md.append("")
    md.append("O diagrama de contexto estabelece as fronteiras do sistema, destacando os usuários (atores humanos) e as interações com sistemas e plataformas externas.")
    md.append("")
    md.append("```mermaid")
    md.append("flowchart TB")
    md.append('    user["👤 Usuário / Desenvolvedor<br/>[Pessoa]<br/>Executa e interage com o sistema"]')
    md.append(f'    sys["🏢 {pname}<br/>[{system_nature}]<br/>Sistema principal"]')
    md.append('    fs["📁 Sistema de Arquivos / Repositório<br/>[Sistema Externo]<br/>Armazena código-fonte e saídas"]')
    
    if project.external_dependencies:
        deps_summary = ", ".join(project.external_dependencies[:4])
        md.append(f'    ext_deps["📦 Dependências e Ecossistema<br/>[Bibliotecas Externas]<br/>{deps_summary}"]')
        md.append("    sys -.->|Utiliza| ext_deps")

    md.append("    user -->|Interage / Executa| sys")
    md.append("    sys -->|Lê e Grava dados| fs")
    md.append("```")
    md.append("")
    md.append("### Atores e Fronteiras")
    md.append(f"- **Usuário / Desenvolvedor**: Opera o sistema {pname} para realizar tarefas e consultar informações.")
    md.append(f"- **{pname}**: O software sob análise, responsável pela lógica principal, orquestração e fluxos.")
    md.append("- **Sistema de Arquivos / Repositório**: Provedor de entrada (código, configurações) e destino de artefatos gerados.")
    md.append("")
    md.append("---")
    md.append("")

    # ==================== NÍVEL 2: CONTAINERS ====================
    md.append("## Nível 2: Diagrama de Containers (Containers)")
    md.append("")
    md.append("Containers representam as unidades executáveis ou de armazenamento independentes que compõem a solução (aplicações, bancos de dados, serviços, file systems).")
    md.append("")
    md.append("```mermaid")
    md.append("flowchart LR")
    md.append(f'    subgraph boundary["Fronteira do Sistema: {pname}"]')
    if is_cli:
        md.append(f'        cli["💻 Interface CLI<br/>[{primary_lang}]<br/>Interface de terminal e parser de comandos"]')
        md.append(f'        core["⚙️ Motor de Processamento<br/>[{primary_lang}]<br/>Lógica de negócio e transformações"]')
        md.append(f'        server["🌐 Servidor Web Local<br/>[HTTP / HTML]<br/>Visualização interativa"]')
        md.append("        cli -->|Invoca| core")
        md.append("        cli -.->|Inicializa| server")
    else:
        md.append(f'        app["⚙️ Aplicação Principal<br/>[{primary_lang}]<br/>Controladores e serviços de negócio"]')
        md.append(f'        core["🧩 Componentes de Domínio<br/>[{primary_lang}]<br/>Entidades, regras e utilitários"]')
        md.append("        app -->|Executa| core")
    md.append("    end")
    md.append('    disk["💾 Disco Local / Repositório<br/>[File System]<br/>Arquivos de entrada e documentação gerada"]')
    if is_cli:
        md.append("    core -->|Varre e Escreve| disk")
        md.append("    server -->|Lê documentos de| disk")
    else:
        md.append("    core -->|Persiste / Lê| disk")
    md.append("```")
    md.append("")
    md.append("### Descrição dos Containers")
    md.append(f"| Container | Tecnologia | Responsabilidade |")
    md.append("|---|---|---|")
    if is_cli:
        md.append(f"| **Interface CLI** | {primary_lang} / CLI | Receber argumentos do usuário, configurar modos de execução e exibir status formatado. |")
        md.append(f"| **Motor de Processamento** | {primary_lang} | Analisar estruturas, parsear ASTs, compilar grafos e gerar relatórios. |")
        md.append(f"| **Servidor Web Local** | HTTP / HTML5 / JS | Servir e renderizar os documentos Markdown e diagramas interativos localmente. |")
    else:
        md.append(f"| **Aplicação Principal** | {primary_lang} | Ponto de entrada, rotas e orquestração de requisições. |")
        md.append(f"| **Componentes de Domínio** | {primary_lang} | Execução de regras de negócio, validações e manipulação de dados. |")
    md.append("| **Disco / Storage** | File System Local | Armazenar fontes, configurações e saídas de documentação. |")
    md.append("")
    md.append("---")
    md.append("")

    # ==================== NÍVEL 3: COMPONENTES ====================
    md.append("## Nível 3: Diagrama de Componentes (Components)")
    md.append("")
    md.append("Exibe a decomposição interna dos módulos de software que formam o container principal e como eles colaboram entre si.")
    md.append("")

    # Módulos detectados
    module_names = set()
    for f in project.files:
        p = Path(f.path)
        if len(p.parts) > 1:
            module_names.add(p.parts[0])

    md.append("```mermaid")
    md.append("flowchart TD")
    md.append(f'    subgraph core_container["Container: {pname} Core"]')
    md.append('        scanner["Scanner & Ignore Matcher<br/>[Varredura de arquivos]"]')
    md.append('        parser_reg["Parser Registry<br/>[Fábrica de analisadores]"]')
    md.append('        ast_parsers["Parsers de Linguagem<br/>[Python, JS/TS, Go, Rust, Java]"]')
    md.append('        model_store["Data Models<br/>[FileInfo, SymbolInfo, ProjectData]"]')
    md.append('        generators["Geradores de Documentação<br/>[C4, HLD/LLD, DAS, ADR, API, Mermaid]"]')
    md.append('        ui_engine["UI & Formatter Engine<br/>[Saída em terminal e Markdown]"]')
    md.append("        scanner -->|Lista de arquivos| parser_reg")
    md.append("        parser_reg -->|Delega para| ast_parsers")
    md.append("        ast_parsers -->|Popula| model_store")
    md.append("        model_store -->|Alimenta| generators")
    md.append("        generators -->|Exporta| ui_engine")
    md.append("    end")
    md.append("```")
    md.append("")
    md.append("### Catálogo de Componentes Chave")
    md.append("- **Scanner & Ignore Matcher**: Responsável por navegar recursivamente pelos diretórios, respeitando regras do `.gitignore` e contabilizando linhas de código.")
    md.append("- **Parser Registry & Analyzers**: Fábrica polimórfica que seleciona o parser adequado para cada linguagem e extrai símbolos, classes, métodos e tipos.")
    md.append("- **Data Models**: Dataclasses imutáveis que garantem integridade estrutural em toda a pipeline.")
    md.append("- **Generators Suite**: Conjunto de especialistas em formatar saídas técnicas (C4, HLD, LLD, DAS, ADRs, Glossário DDD e API).")
    md.append("")
    md.append("---")
    md.append("")

    # ==================== NÍVEL 4: CÓDIGO ====================
    md.append("## Nível 4: Diagrama de Código (Code / Class Diagram)")
    md.append("")
    md.append("Mapeamento das principais classes, interfaces e tipos estruturais que implementam as regras de domínio.")
    md.append("")

    # Diagrama de classes
    classes_code = []
    for f in project.files:
        for s in f.symbols:
            if s.symbol_type == SymbolType.CLASS:
                classes_code.append((f, s))

    if classes_code:
        md.append("```mermaid")
        md.append("classDiagram")
        for f, cls in classes_code[:15]:
            cid = sanitize_id(cls.name)
            md.append(f"    class {cid} {{")
            for m in cls.children[:4]:
                md.append(f"        +{m.name}()")
            md.append("    }")
            for b in cls.base_classes:
                md.append(f"    {sanitize_id(b)} <|-- {cid}")
        md.append("```")
    else:
        md.append("> [!NOTE]")
        md.append("> Repositório predominantemente procedural ou modular sem classes de domínio complexas mapeadas.")

    return "\n".join(md)

