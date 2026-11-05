"""
Gerador e catalogador de ADRs (Architecture Decision Records).
Lê ADRs existentes ou sintetiza decisões técnicas chave no formato padrão de Michael Nygard.
"""

import os
import re
from pathlib import Path
from typing import List, Dict
from docgen.models import ADRItem, ProjectData
from docgen.config import get_primary_programming_language


def find_existing_adrs(root_path: Path) -> List[ADRItem]:
    """Procura por ADRs já existentes em pastas comuns."""
    adrs = []
    adr_dirs = [
        root_path / "docs" / "adr",
        root_path / "doc" / "adr",
        root_path / "docs" / "decisions",
        root_path / "adr",
    ]

    for adr_dir in adr_dirs:
        if adr_dir.is_dir():
            for f in sorted(adr_dir.glob("*.md")):
                if f.name.lower().startswith("template"):
                    continue
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip() if title_match else f.stem
                    
                    status_match = re.search(r'##\s+Status\s*\n+([A-Za-zÀ-ÿ]+)', content, re.IGNORECASE)
                    status = status_match.group(1).strip() if status_match else "Aceito"

                    # Extrai número do arquivo se existir (ex: 0001-title.md)
                    num_match = re.search(r'^(\d+)', f.name)
                    number = int(num_match.group(1)) if num_match else len(adrs) + 1

                    adrs.append(
                        ADRItem(
                            number=number,
                            title=title,
                            status=status,
                            context="Extraído do repositório.",
                            decision="Consulte o arquivo original para detalhes.",
                            consequences="Consulte o arquivo original.",
                            date="Registrado",
                            source_file=str(f.relative_to(root_path)),
                        )
                    )
                except Exception:
                    pass

    return adrs


def synthesize_project_adrs(project: ProjectData) -> List[ADRItem]:
    """Gera ADRs sintetizados representativos do repositório se nenhum for encontrado."""
    existing = find_existing_adrs(Path(project.root_path))
    if existing:
        return existing

    primary_lang = get_primary_programming_language(project.metrics.language_distribution)
    pname = project.project_name

    adrs = [
        ADRItem(
            number=1,
            title=f"Adoção da Stack Tecnológica Principal: {primary_lang}",
            status="Aceito",
            date="2026",
            context=f"O projeto {pname} necessita de alta confiabilidade, manutenibilidade e suporte consistente a ecossistema de desenvolvimento.",
            decision=f"Padronizar o desenvolvimento do núcleo em {primary_lang}, priorizando convenções consolidadas e tipagem consistente.",
            consequences="Positivo: facilidade de integração, ecossistema maduro e ampla base de conhecimento. Negativo: exige observância de boas práticas para manter o desempenho com bases volumosas.",
        ),
        ADRItem(
            number=2,
            title="Padrão Arquitetural em Camadas e Pipeline",
            status="Aceito",
            date="2026",
            context="Necessidade de separar as fases de entrada, descoberta, parseamento de código e geração de resultados para viabilizar testes independentes.",
            decision="Adotar uma arquitetura orientada a Pipeline (Scanner -> Parsers -> Model -> Generators), desacoplando a camada de entrada da camada de geração.",
            consequences="Positivo: alta testabilidade, baixo acoplamento e suporte plugável a novas linguagens. Negativo: necessidade de manter um modelo de dados intermediário representativo.",
        ),
        ADRItem(
            number=3,
            title="Estratégia Híbrida de Análise Sintática (AST + Parsing Estrutural)",
            status="Aceito",
            date="2026",
            context="O sistema precisa analisar múltiplas linguagens (Python, TypeScript, Go, Rust, etc.) sem depender de ferramentas nativas externas pesadas.",
            decision="Utilizar o módulo nativo AST onde disponível (ex: Python) e analisadores léxicos/estruturais robustos baseados em padrões formais para linguagens adicionais.",
            consequences="Positivo: execução ultra-rápida, zero dependências obrigatórias e compatibilidade imediata. Negativo: para sintaxes muito dinâmicas e metaprogramação, a análise foca em símbolos declarados explicitamente.",
        ),
        ADRItem(
            number=4,
            title="Padronização da Suíte de Documentação (C4, HLD/LLD, DAS e Linguagem Ubíqua)",
            status="Aceito",
            date="2026",
            context="Documentações puramente descritivas falham em comunicar a arquitetura de software para diferentes perfis de engenharia e liderança.",
            decision="Padronizar a geração de documentos seguindo os padrões C4 Model, High-Level e Low-Level Design, Documento de Arquitetura de Software (DAS) e glossário de Linguagem Ubíqua (DDD).",
            consequences="Positivo: comunicação clara em múltiplos níveis de abstração (executivo, arquitetural e técnico). Negativo: volume maior de documentação gerada, mitigado pela navegação via sumário e servidor web.",
        ),
    ]

    return adrs


def generate_adr_template() -> str:
    """Gera o arquivo de template padrão para novas decisões arquiteturais."""
    return """# [Número]. [Título curto da decisão arquitetural]

## Status
[Proposto | Aceito | Rejeitado | Substituído por ADR-XXX]

## Contexto
Qual é o problema ou necessidade de negócio que motivou esta decisão? Quais restrições, hipóteses e alternativas foram avaliadas?

## Decisão
Qual é a mudança ou diretriz técnica adotada? Qual o escopo de aplicação?

## Consequências
### Positivas
- [Benefício ou ganho obtido]

### Negativas / Riscos
- [Compromisso assumido, complexidade adicional ou débitos técnicos aceitos]

## Data
YYYY-MM-DD
"""


def generate_adrs_index_markdown(adrs: List[ADRItem], pname: str) -> str:
    """Gera o índice consolidado de ADRs em Markdown."""
    md = []
    md.append(f"# Registro de Decisões Arquiteturais (ADRs): {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> **Architecture Decision Records (ADRs)** capturam decisões arquiteturais significativas tomadas ao longo da evolução do software, seus contextos e consequências.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Lista de Decisões Arquiteturais Registradas")
    md.append("")
    md.append("| # | Decisão | Status | Data |")
    md.append("|---|---|---|---|")
    for adr in adrs:
        md.append(f"| **ADR-{adr.number:03d}** | [{adr.title}](#adr-{adr.number:03d}-{adr.title.lower().replace(' ', '-')}) | `{adr.status}` | {adr.date} |")

    md.append("")
    md.append("---")
    md.append("")

    for adr in adrs:
        md.append(f"## ADR-{adr.number:03d}: {adr.title}")
        md.append(f"**Status:** `{adr.status}` | **Data:** {adr.date}")
        md.append("")
        md.append("### Contexto")
        md.append(adr.context)
        md.append("")
        md.append("### Decisão")
        md.append(adr.decision)
        md.append("")
        md.append("### Consequências")
        md.append(adr.consequences)
        md.append("")
        md.append("---")
        md.append("")

    return "\n".join(md)

