# DocGen (CLI) ⚡🧠

[English](README.md) | [Português](README.pt-BR.md)

> **AI-Powered Technical Documentation & Software Architecture Generator for Code Repositories.**
> Ingests and deeply comprehends entire codebases through multi-language AST extraction and Generative AI (Google Gemini, OpenAI, Claude, Ollama/DeepSeek-R1) to synthesize comprehensive **C4 Models**, **HLD**, **SAD (Software Architecture Documents)**, and **DDD Ubiquitous Language**.

---

## 🌟 AI Engineering & Key Highlights

- 🧠 **Deep AI Architectural Synthesis (LLM-Driven)**:
  - **No Static Boilerplates**: Analyzes the semantic reality of your code to deduce true business domain rules, system boundaries, architectural trade-offs, and design patterns.
  - **Multi-Provider Engine**: Supports **Google Gemini** (`gemini-2.5-flash`, `gemini-1.5-pro`), **OpenAI** (`gpt-4o`, `gpt-4o-mini`), **Anthropic Claude** (`claude-3-5-sonnet`), and **Local Ollama** (`deepseek-r1`, `llama3.3`, `qwen2.5-coder`).
  - **Zero External Dependencies Required**: Communicates with AI REST APIs and local models natively using standard Python (`urllib.request`), requiring **0 pip downloads**.
  - **Resilient Architecture**: Combines AI cognitive reasoning with deterministic AST static analysis.
- 🏛️ **Complete Software Architecture Suite**:
  - **C4 Model (Simon Brown)**: Level 1 (System Context), Level 2 (Containers), Level 3 (Components), and Level 4 (Code).
  - **High-Level Design (HLD)**: Architectural style, data flow, boundaries, and Non-Functional Requirements (NFRs).
  - **Software Architecture Document (SAD / DAS)**: Based on **Arc42** and the **4+1 View Model** (Logical, Process, Physical, and Technical Risk views).
  - **Ubiquitous Language (DDD)**: Domain glossary identifying business entities, value objects, domain services, enums, and a Mermaid concept map.
- 🔍 **Multi-Language AST Analysis**:
  - **Python** (native AST), **TypeScript & JavaScript** (ES6+, interfaces, types, JSDoc, routes), **Go**, **Rust**, **Java / C#**, and generic script/config parsers.
- 📊 **Static Web Viewer & GitHub Pages**:
  - Self-contained `index.html` with Dark Mode, sidebar navigation, live search, and client-side Mermaid.js rendering.

---

## 🚀 Installation & Execution

### Direct Execution (No Installation Required)
```bash
./bin/docgen [PATH]
# or
python3 -m docgen [PATH]
```

### Install CLI Locally
```bash
pip install -e .
```

---

## 🤖 Running with AI Providers

DocGen automatically activates the AI Architect when an API key or local Ollama is detected:

### 1. Google Gemini (Default Cloud Provider)
```bash
export GEMINI_API_KEY="your-api-key"
docgen . --ai --provider gemini --model gemini-2.5-flash
```

### 2. OpenAI (GPT-4o / GPT-4o-mini)
```bash
export OPENAI_API_KEY="your-api-key"
docgen . --ai --provider openai --model gpt-4o-mini
```

### 3. Anthropic Claude (Claude 3.5 Sonnet)
```bash
export ANTHROPIC_API_KEY="your-api-key"
docgen . --ai --provider anthropic --model claude-3-5-sonnet-20241022
```

### 4. Local & Private LLMs with Ollama (DeepSeek-R1 / Llama 3 / Qwen)
Run completely offline and free on your own GPU/CPU:
```bash
# Start Ollama
ollama serve

# Run DocGen with DeepSeek-R1
docgen . --ai --provider ollama --model deepseek-r1
```

---

## 🛠️ CLI Commands & Flags

### Generate Documentation Suite (`docs/`)
```bash
docgen [PATH] --output docs/
```

### Generate Single Master File (`--single-file`)
```bash
docgen . --single-file --output DOCUMENTATION.md
```

### Quick Codebase Statistics (`stats`)
```bash
docgen stats .
```

### Local Interactive Viewer (`serve`)
```bash
docgen serve ./docs --port 8080
```

---

## 📂 Generated Documentation Artifacts

| Document | Description |
|---|---|
| `INDEX.md` | Executive overview, tech stack badges, directory tree, and AI generation metadata. |
| `ARCHITECTURE.md` | Architecture overview, Mermaid module diagram, and domain class hierarchy. |
| `C4_MODEL.md` | C4 Model: System Context, Containers, Components, and Code with Mermaid diagrams. |
| `HLD.md` | High-Level Design: architectural style, system boundaries, and NFRs. |
| `DAS.md` | Software Architecture Document based on Arc42 and the 4+1 View Model. |
| `UBIQUITOUS_LANGUAGE.md` | DDD Glossary: domain entities, value objects, services, and concept map. |
| `API_REFERENCE.md` | Complete API signatures, classes, methods, parameters, return types, and docstrings. |
| `DEPENDENCIES.md` | Internal module dependency graph and detected external package manifests. |
| `METRICS.md` | Source Lines of Code (SLOC), comments, documentation ratios, and language statistics. |
| `index.html` | Self-contained static SPA viewer ready for GitHub Pages. |

---

## 🧪 Automated Testing

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 License
Distributed under the MIT License.
