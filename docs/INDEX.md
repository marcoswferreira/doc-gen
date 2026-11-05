# Documentação Técnica: doc-gen

> [!TIP]
> Documentação gerada automaticamente pelo **DocGen**. Repositório analisado com **37 arquivos**, **2,022 linhas de código** e **61 termos conceituais**.

---

## Sumário de Navegação da Documentação

| Documento | Escopo e Conteúdo |
|---|---|
| 🏛️ **[Modelo C4 (C4_MODEL.md)](./C4_MODEL.md)** | Visão em 4 níveis: Contexto, Containers, Componentes e Código. |
| 📐 **[High-Level Design (HLD.md)](./HLD.md)** | Arquitetura macro, estilo arquitetural, fronteiras e RNFs. |
| ⚙️ **[Low-Level Design (LLD.md)](./LLD.md)** | Padrões de projeto, estruturas de dados e diagrama de sequência. |
| 📋 **[Documento de Arquitetura (DAS.md)](./DAS.md)** | Visão 4+1 e Arc42: lógica, processos, física e riscos. |
| 💡 **[Linguagem Ubíqua (UBIQUITOUS_LANGUAGE.md)](./UBIQUITOUS_LANGUAGE.md)** | Glossário DDD com entidades, value objects, serviços e mapa conceitual. |
| ⚖️ **[Decisões de Arquitetura (ADRS.md)](./ADRS.md)** | Registro formal de ADRs (Architecture Decision Records) e template. |
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
  ├── cli.py
  ├── config.py
  ├── generators
  ├── models.py
  ├── parsers
  ├── scanner.py
  ├── server.py
  ├── ui.py
  ├── test_cli.py
  ├── test_generators.py
  ├── test_js_parser.py
  ├── test_python_parser.py
  ├── test_scanner.py
    ├── ci.yml
    ├── deploy-docs.yml
    ├── adr_generator.py
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
