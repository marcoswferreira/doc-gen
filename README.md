# DocGen (CLI) ⚡

[English](README.md) | [Português](README.pt-BR.md)

> **Automated Technical Documentation & Software Architecture Generator for Code Repositories.**
> Analyzes entire codebases and automatically generates comprehensive Markdown documentation featuring the **C4 Model**, **HLD/LLD**, **SAD (Software Architecture Document)**, **ADRs**, **DDD Ubiquitous Language**, **Mermaid diagrams**, and code metrics.

---

## 🌟 Key Highlights

- **Zero External Dependencies Required**: Built in Python 3.12 strictly using the standard library (`ast`, `argparse`, `pathlib`, `http.server`, etc.). Runs out of the box on Linux, macOS, and Windows without requiring any internet connection or heavy downloads.
- **Complete Software Architecture Suite**:
  - 🏛️ **C4 Model (Simon Brown)**: Level 1 (System Context), Level 2 (Containers), Level 3 (Components), and Level 4 (Code).
  - 📐 **High-Level Design (HLD)**: Macro architectural style, system boundaries, and Non-Functional Requirements (NFRs).
  - ⚙️ **Low-Level Design (LLD)**: Detected design patterns, data contracts, and interactive Mermaid sequence diagrams (`sequenceDiagram`).
  - 📋 **Software Architecture Document (SAD / DAS)**: Based on **Arc42** and the **4+1 View Model** (Logical, Process, Physical, and Technical Risk views).
  - ⚖️ **Architecture Decision Records (ADRs)**: Automatic cataloging and synthesis of ADRs (Michael Nygard format) plus a standard ADR template.
  - 💡 **Ubiquitous Language (DDD)**: Domain glossary identifying business entities, value objects, domain services, enums, and a Mermaid concept map.
- **Multi-Language Support**:
  - **Python**: Deep extraction via native AST (modules, classes, inheritance, async methods, type annotations, default parameters, decorators, docstrings, and FastAPI/Flask routes).
  - **TypeScript & JavaScript**: Structural parser for ES6+, interfaces, types, classes, functions, arrow functions, JSDoc comments (`/** ... */`), and Express/Next.js routes.
  - **Go**: Packages, structs, interfaces, functions, receiver methods, and godoc comments.
  - **Rust**: Modules, structs, enums, traits, `impl` blocks, `pub fn`, and rustdoc `///` comments.
  - **Java / C# / Kotlin**: Classes, records, interfaces, annotations, typed methods, and Javadoc.
  - **Shell / Docker / SQL / Configs**: Fallback parser extracting header documentation and instructions.
- **Integrated Visual Diagrams**: Automatic generation of Mermaid diagrams (system flowcharts, class diagrams, dependency graphs, and sequence workflows).
- **Codebase Metrics & Insights**: Accurate computation of Source Lines of Code (SLOC), blank lines, comment lines, documentation ratios, and language distribution.
- **Built-in Documentation Server (`docgen serve`)**: Embedded zero-dependency HTTP server with a modern dark-mode reader, sidebar navigation, and client-side Mermaid rendering.

---

## 🚀 Installation & Quickstart

### Direct Execution (No Installation Required)
```bash
./bin/docgen [PATH]
# or
python3 -m docgen [PATH]
```

### Install into Current Environment
```bash
pip install -e .
```

---

## 🛠️ CLI Usage & Commands

### 1. Generate Complete Documentation Suite (Default: `docs/`)
Scans the repository and outputs all 11 technical artifacts into the `docs/` folder:
```bash
docgen
# or pointing to a specific repository
docgen /path/to/project --output ./docs
```

### 2. Generate Single Consolidated Master File (`--single-file`)
Generates a single, self-contained Markdown file combining all architectural sections and API reference:
```bash
docgen . --single-file --output DOCUMENTATION.md
```

### 3. Quick Terminal Statistics (`stats`)
Prints language distribution tables, SLOC, and documentation ratios directly in the terminal without writing files:
```bash
docgen stats .
```

### 4. Interactive Browser Viewer (`serve`)
Spins up a lightweight local HTTP server with instant search, sidebar navigation, and diagram rendering:
```bash
docgen serve ./docs --port 8080
```

### 5. Initialize Configuration (`init`)
Generates `.docgen.json` and `.docgenignore` files in your repository:
```bash
docgen init
```

---

## 📂 Generated Documentation Artifacts

| Document | Description |
|---|---|
| `INDEX.md` | Executive overview, tech stack badges, directory tree, and quick links. |
| `ARCHITECTURE.md` | Architecture overview, Mermaid module diagram, and class hierarchy. |
| `C4_MODEL.md` | C4 Model in 4 levels: System Context, Containers, Components, and Code. |
| `HLD.md` | High-Level Design: macro architectural style, system boundaries, and NFRs. |
| `LLD.md` | Low-Level Design: design patterns, contracts, and execution sequence diagrams. |
| `DAS.md` | Software Architecture Document based on Arc42 and the 4+1 View Model. |
| `UBIQUITOUS_LANGUAGE.md` | DDD Glossary: business terms, conceptual map, and codebase definitions. |
| `ADRS.md` & `adrs/` | Cataloged and synthesized Architecture Decision Records + ADR template. |
| `API_REFERENCE.md` | Complete API signatures, classes, methods, parameters, return types, and docstrings. |
| `DEPENDENCIES.md` | Internal module dependency graph and detected external package manifests. |
| `METRICS.md` | Source Lines of Code (SLOC), comments, documentation ratios, and language statistics. |

---

## 🧪 Automated Testing

DocGen includes an automated test suite utilizing Python's built-in `unittest` runner:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 License
Distributed under the MIT License.
