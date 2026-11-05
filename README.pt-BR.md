# DocGen (CLI) ⚡🧠

[English](README.md) | [Português](README.pt-BR.md)

> **Gerador de Documentação Técnica e Arquitetura com Inteligência Artificial.**
> Ingere e compreende profundamente bases de código completas combinando análise sintática via AST multi-linguagem e IA Generativa (Google Gemini, OpenAI, Claude, Ollama/DeepSeek-R1) para sintetizar **Modelo C4**, **HLD**, **DAS (Documento de Arquitetura de Software)** e **Linguagem Ubíqua (DDD)**.

---

## 🌟 Engenharia de IA & Destaques

- 🧠 **Síntese Arquitetural Profunda com IA (Baseada em LLMs)**:
  - **Sem Boilerplates Estáticos**: Analisa a semântica real do seu código para deduzir regras de negócio, limites de contexto, trade-offs de arquitetura e padrões de design adotados.
  - **Motor Multi-Provedor**: Suporta **Google Gemini** (`gemini-2.5-flash`, `gemini-1.5-pro`), **OpenAI** (`gpt-4o`, `gpt-4o-mini`), **Anthropic Claude** (`claude-3-5-sonnet`) e **Ollama Local** (`deepseek-r1`, `llama3.3`, `qwen2.5-coder`).
  - **Zero Dependências Externas Obrigatórias**: Comunica-se com as APIs REST de IA e modelos locais usando exclusivamente a biblioteca padrão do Python (`urllib.request`), sem exigir nenhum download via pip.
  - **Arquitetura Resiliente**: Combina o raciocínio cognitivo do LLM com análise estática de AST caso o modo offline seja desejado.
- 🏛️ **Suíte Completa de Arquitetura de Software**:
  - **Modelo C4 (Simon Brown)**: Nível 1 (Contexto), Nível 2 (Containers), Nível 3 (Componentes) e Nível 4 (Código).
  - **High-Level Design (HLD)**: Estilo arquitetural, fluxo macro de dados, fronteiras e Requisitos Não-Funcionais (RNFs).
  - **Documento de Arquitetura de Software (DAS)**: Baseado nos padrões **Arc42** e **4+1 Visões de Kruchten**.
  - **Linguagem Ubíqua (DDD)**: Glossário com entidades, value objects, serviços de domínio e mapa conceitual em Mermaid.
- 🔍 **Análise Sintática Multi-Linguagem via AST**:
  - **Python** (AST nativo), **TypeScript & JavaScript** (ES6+, interfaces, tipos, JSDoc, rotas), **Go**, **Rust**, **Java / C#** e scripts/configs.
- 📊 **Visualizador Web Estático & GitHub Pages**:
  - Gera automaticamente `index.html` autossuficiente com Dark Theme, navegação por sidebar, busca em tempo real e renderização dinâmica de Mermaid.js.

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

## 🤖 Executando com Motores de Inteligência Artificial

O DocGen ativa o Arquiteto de IA automaticamente ao detectar uma chave de API ou servidor Ollama local:

### 1. Google Gemini (Padrão em Nuvem)
```bash
export GEMINI_API_KEY="sua-chave-api"
docgen . --ai --provider gemini --model gemini-2.5-flash
```

### 2. OpenAI (GPT-4o / GPT-4o-mini)
```bash
export OPENAI_API_KEY="sua-chave-api"
docgen . --ai --provider openai --model gpt-4o-mini
```

### 3. Anthropic Claude (Claude 3.5 Sonnet)
```bash
export ANTHROPIC_API_KEY="sua-chave-api"
docgen . --ai --provider anthropic --model claude-3-5-sonnet-20241022
```

### 4. LLMs Locais e Gratuitos com Ollama (DeepSeek-R1 / Llama 3 / Qwen)
Execute localmente de forma privada no seu computador sem custo de API:
```bash
# Inicie o Ollama
ollama serve

# Execute o DocGen com DeepSeek-R1
docgen . --ai --provider ollama --model deepseek-r1
```

---

## 🛠️ Comandos e Opções da CLI

### Gerar Suíte Completa de Documentação (`docs/`)
```bash
docgen [PATH] --output docs/
```

### Gerar Arquivo Mestre Único Consolidado (`--single-file`)
```bash
docgen . --single-file --output DOCUMENTATION.md
```

### Exibir Estatísticas de Código no Terminal (`stats`)
```bash
docgen stats .
```

### Servidor Local Interativo (`serve`)
```bash
docgen serve ./docs --port 8080
```

---

## 📂 Documentos Gerados na Suíte

| Arquivo | Descrição |
|---|---|
| `INDEX.md` | Visão executiva, badges de tecnologias, árvore de diretórios e metadados de IA. |
| `ARCHITECTURE.md` | Visão de arquitetura, diagrama Mermaid de módulos e hierarquia de classes. |
| `C4_MODEL.md` | Modelo C4: Contexto, Containers, Componentes e Código com diagramas Mermaid. |
| `HLD.md` | High-Level Design: estilo arquitetural, fronteiras e requisitos não-funcionais. |
| `LLD.md` | Low-Level Design: padrões de projeto, contratos e diagramas de sequência. |
| `DAS.md` | Documento de Arquitetura de Software baseado em Arc42 e 4+1 Visões. |
| `UBIQUITOUS_LANGUAGE.md` | Glossário DDD: entidades de domínio, value objects, serviços e mapa conceitual. |
| `ADRS.md` & `adrs/` | Decisões arquiteturais sintetizadas do código no formato Michael Nygard. |
| `API_REFERENCE.md` | Assinaturas de classes, métodos, parâmetros, retornos, rotas e docstrings. |
| `DEPENDENCIES.md` | Grafo de dependências internas e lista de pacotes externos identificados. |
| `METRICS.md` | Linhas de código (SLOC), comentários, taxa de documentação e distribuição de linguagens. |
| `index.html` | SPA estática com Dark Mode e Mermaid pronta para o GitHub Pages. |

---

## 🧪 Testes Automatizados

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 Licença
Distribuído sob a licença MIT.
