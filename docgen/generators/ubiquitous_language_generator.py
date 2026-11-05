"""
Gerador de Linguagem Ubíqua (Ubiquitous Language / Glossário de Domínio - DDD).
Extrai conceitos centrais do negócio, entidades, value objects, enums e operações do código.
"""

import re
from typing import List, Dict, Set
from pathlib import Path
from docgen.models import ProjectData, SymbolType, UbiquitousTerm
from docgen.generators.mermaid import sanitize_id


def extract_ubiquitous_terms(project: ProjectData) -> List[UbiquitousTerm]:
    """Analisa as definições de classes, tipos e enums para compor a Linguagem Ubíqua."""
    terms_dict: Dict[str, UbiquitousTerm] = {}

    for f in project.files:
        for s in f.symbols:
            name = s.name
            # Ignora nomes genéricos de utilitários
            if name.startswith("_") or len(name) < 3 or name.lower() in ("test", "main", "init"):
                continue

            category = "Entidade"
            definition = s.docstring or "Elemento estrutural do domínio do sistema."

            if s.symbol_type == SymbolType.ENUM:
                category = "Enumeração de Domínio"
                definition = s.docstring or f"Conjunto fixo de estados e variações permitidas para {name}."
            elif s.symbol_type in (SymbolType.INTERFACE, SymbolType.TRAIT):
                category = "Contrato de Domínio"
                definition = s.docstring or f"Interface que dita o comportamento esperado para componentes {name}."
            elif s.symbol_type == SymbolType.STRUCT:
                category = "Estrutura / Value Object"
                definition = s.docstring or f"Estrutura que encapsula atributos e dados de {name}."
            elif s.symbol_type == SymbolType.CLASS:
                # Heurística para Service / Scanner / Registry / Manager
                if any(suffix in name for suffix in ("Service", "Scanner", "Registry", "Generator", "Manager", "Engine", "Handler")):
                    category = "Serviço de Domínio"
                    definition = s.docstring or f"Serviço responsável por executar operações e orquestrações de {name}."
                elif any(suffix in name for suffix in ("Info", "Data", "Metrics", "Config", "DTO")):
                    category = "Objeto de Valor (Value Object)"
                    definition = s.docstring or f"Representação imutável com propriedades e métricas de {name}."
                else:
                    category = "Entidade de Domínio"
                    definition = s.docstring or f"Entidade central com ciclo de vida e estado gerenciado em {name}."
            elif s.symbol_type == SymbolType.ROUTE:
                category = "Operação de API / Rota"
                definition = f"Endpoint exposto que fornece acesso a recursos de {name}."

            # Limpa docstrings muito longas para uma frase concisa de glossário
            first_sentence = definition.strip().split("\n")[0].split(". ")[0]
            if not first_sentence.endswith("."):
                first_sentence += "."

            if name not in terms_dict:
                terms_dict[name] = UbiquitousTerm(
                    term=name,
                    category=category,
                    definition=first_sentence,
                    source_files=[f.path],
                )
            else:
                if f.path not in terms_dict[name].source_files:
                    terms_dict[name].source_files.append(f.path)

    return sorted(list(terms_dict.values()), key=lambda t: (t.category, t.term))


def generate_ubiquitous_language_markdown(project: ProjectData, lang: str = "pt") -> str:
    """Gera o documento UBIQUITOUS_LANGUAGE.md."""
    pname = project.project_name
    terms = extract_ubiquitous_terms(project)

    md = []
    md.append(f"# Linguagem Ubíqua (Glossário DDD): {pname}")
    md.append("")
    md.append("> [!NOTE]")
    md.append("> No **Domain-Driven Design (DDD)**, a **Linguagem Ubíqua** (Ubiquitous Language) é o vocabulário compartilhado e rigoroso utilizado tanto por especialistas de negócio quanto pela equipe técnica para eliminar ambiguidades no software.")
    md.append("")
    md.append("---")
    md.append("")

    # Mapa Conceitual em Mermaid
    md.append("## 1. Mapa Conceitual do Domínio")
    md.append("Relação visual dos termos mais representativos identificados na base de código:")
    md.append("")

    # Seleciona os top 12 termos
    main_terms = terms[:12]
    if main_terms:
        md.append("```mermaid")
        md.append("graph TD")
        for t in main_terms:
            tid = sanitize_id(t.term)
            md.append(f'    {tid}["<b>{t.term}</b><br/><i>({t.category})</i>"]')
        
        # Conecta termos que compartilham palavras ou arquivos
        for i, t1 in enumerate(main_terms):
            for t2 in main_terms[i+1:]:
                # Se compartilham algum arquivo de origem
                common_files = set(t1.source_files).intersection(set(t2.source_files))
                if common_files:
                    t1_id = sanitize_id(t1.term)
                    t2_id = sanitize_id(t2.term)
                    md.append(f"    {t1_id} -.->|Relacionado| {t2_id}")
        md.append("```")
        md.append("")

    # Tabela consolidada
    md.append("## 2. Glossário de Termos do Negócio")
    md.append("")
    md.append("| Termo / Conceito | Categoria DDD | Definição / Papel no Sistema | Ocorrências |")
    md.append("|---|---|---|---|")

    for t in terms:
        sources_str = ", ".join(f"`{Path(s).name}`" for s in t.source_files[:3])
        if len(t.source_files) > 3:
            sources_str += f" (+{len(t.source_files) - 3})"
        md.append(f"| **{t.term}** | `{t.category}` | {t.definition} | {sources_str} |")

    md.append("")
    md.append("---")
    md.append("")

    # Detalhamento por Categoria
    categories = sorted(list(set(t.category for t in terms)))
    for cat in categories:
        cat_terms = [t for t in terms if t.category == cat]
        md.append(f"### {cat} ({len(cat_terms)})")
        for t in cat_terms:
            md.append(f"- **{t.term}**: {t.definition}")
            md.append(f"  - *Arquivos*: {', '.join(f'`{s}`' for s in t.source_files)}")
        md.append("")

    return "\n".join(md)
