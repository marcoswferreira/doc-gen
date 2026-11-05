# DocGen (CLI) ⚡

> **Gerador Automático de Documentação Técnica e Arquitetura para Repositórios de Código.**
> Analisa repositórios inteiros e gera documentação completa em Markdown com suporte nativo ao **Modelo C4**, **HLD/LLD**, **DAS**, **ADRs**, **Linguagem Ubíqua (DDD)**, diagramas **Mermaid** e métricas de código.

---

## 🌟 Destaques

- **Zero Dependências Externas Obrigatórias**: Desenvolvido em Python 3.12 usando estritamente a biblioteca padrão (`ast`, `argparse`, `pathlib`, `http.server`, etc.). Funciona em qualquer ambiente Linux, macOS ou Windows sem necessidade de conexões de rede ou compilação.
- **Suíte Arquitetural Completa**:
  - 🏛️ **Modelo C4 (Simon Brown)**: Nível 1 (Contexto), Nível 2 (Containers), Nível 3 (Componentes) e Nível 4 (Código).
  - 📐 **High-Level Design (HLD)**: Estilo arquitetural, escopo, fronteiras e requisitos não-funcionais (RNFs).
  - ⚙️ **Low-Level Design (LLD)**: Padrões de projeto, estruturas de dados e diagrama de sequência (`sequenceDiagram`).
  - 📋 **Documento de Arquitetura de Software (DAS)**: Baseado nos modelos **Arc42** e **4+1 Visões de Kruchten**.
  - ⚖️ **Registro de Decisões de Arquitetura (ADRs)**: Catalogação e síntese de ADRs (formato Michael Nygard) com template padronizado.
  - 💡 **Linguagem Ubíqua (DDD)**: Glossário de termos de domínio, entidades, value objects, serviços e mapa conceitual.
- **Suporte Multi-Linguagem**:
  - **Python**: Extração via AST nativo (módulos, classes, herança, métodos assíncronos, type hints, decoradores, docstrings e rotas FastAPI/Flask).
  - **TypeScript & JavaScript**: Parser estrutural para ES6+, interfaces, tipos, classes, funções, JSDoc e rotas Express/Next.js.
  - **Go**: Structs, interfaces, funções, métodos com receivers e comentários godoc.
  - **Rust**: Módulos, structs, enums, traits, blocos `impl`, `pub fn` e docstrings `///`.
  - **Java / C#**: Classes, records, interfaces, anotações, métodos tipados e Javadoc.
  - **Shell / Docker / SQL / Configs**: Parser de fallback para scripts e manifests.
- **Diagramas Visuais Integrados**: Geração automática de diagramas Mermaid (arquitetura em fluxo, grafo de classes, grafo de dependências e diagramas de sequência).
- **Métricas do Repositório**: Contagem de SLOC, linhas em branco, linhas de comentários, taxa de documentação e distribuição de linguagens.
- **Servidor Web Embutido (`docgen serve`)**: Leitor interativo de Markdown com tema escuro, sidebar navegável e renderização dinâmica de Mermaid no navegador.

---

## 🚀 Instalação e Execução

### Execução Direta (Sem Instalação)
```bash
./bin/docgen [PATH]
# ou
python3 -m docgen [PATH]
```

### Instalação no Ambiente
```bash
pip install -e .
```

---

## 🛠️ Modos de Uso da CLI

### 1. Gerar Suíte Completa de Documentação (Padrão: `docs/`)
Analisa o repositório atual e grava os 11 artefatos técnicos na pasta `docs/`:
```bash
docgen
# ou indicando um repositório específico
docgen /caminho/do/projeto --output ./docs
```

### 2. Gerar Documento Único Consolidado (`--single-file`)
Gera um único arquivo Markdown contendo todas as seções (visão geral, C4, HLD/LLD, DAS, ADRs, DDD, métricas):
```bash
docgen . --single-file --output DOCUMENTATION.md
```

### 3. Exibir Métricas no Terminal (`stats`)
Exibe no próprio terminal tabelas de distribuição de linguagens, SLOC e taxa de comentários sem gravar arquivos:
```bash
docgen stats .
```

### 4. Visualizar no Navegador (`serve`)
Inicia um servidor web local com interface moderna para leitura e renderização de diagramas:
```bash
docgen serve ./docs --port 8080
```

### 5. Inicializar Configuração (`init`)
Cria os arquivos `.docgen.json` e `.docgenignore` no repositório:
```bash
docgen init
```

---

## 📂 Documentos Gerados na Suíte

| Arquivo | Descrição |
|---|---|
| `INDEX.md` | Sumário de navegação executivo, badges de tecnologias e árvore de diretórios. |
| `ARCHITECTURE.md` | Visão geral da arquitetura, diagrama Mermaid de módulos e classes. |
| `C4_MODEL.md` | Modelo C4 em 4 níveis: Contexto, Containers, Componentes e Código. |
| `HLD.md` | High-Level Design: estilo arquitetural, fronteiras e requisitos não-funcionais. |
| `LLD.md` | Low-Level Design: padrões de projeto, contratos e diagrama de sequência. |
| `DAS.md` | Documento de Arquitetura de Software: Visão Lógica, de Processo e Implantação (Arc42 / 4+1). |
| `UBIQUITOUS_LANGUAGE.md` | Glossário DDD: termos de negócio, mapa conceitual e definições no código. |
| `ADRS.md` & `adrs/` | Registro de decisões arquiteturais com índice e template para novas decisões. |
| `API_REFERENCE.md` | Assinaturas de classes, métodos, parâmetros, retornos, rotas e docstrings. |
| `DEPENDENCIES.md` | Grafo de dependências internas e lista de pacotes externos identificados. |
| `METRICS.md` | Estatísticas de linhas de código (SLOC), comentários e distribuição por linguagem. |

---

## 🧪 Testes Automatizados

A suíte de testes utiliza o módulo padrão `unittest`:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 Licença
Distribuído sob a licença MIT.

