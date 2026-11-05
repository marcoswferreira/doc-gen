# Registro de Decisões Arquiteturais (ADRs): doc-gen

> [!NOTE]
> **Architecture Decision Records (ADRs)** capturam decisões arquiteturais significativas tomadas ao longo da evolução do software, seus contextos e consequências.

---

## Lista de Decisões Arquiteturais Registradas

| # | Decisão | Status | Data |
|---|---|---|---|
| **ADR-001** | [Adoção da Stack Tecnológica Principal: Python](#adr-001-adoção-da-stack-tecnológica-principal:-python) | `Aceito` | 2026 |
| **ADR-002** | [Padrão Arquitetural em Camadas e Pipeline](#adr-002-padrão-arquitetural-em-camadas-e-pipeline) | `Aceito` | 2026 |
| **ADR-003** | [Estratégia Híbrida de Análise Sintática (AST + Parsing Estrutural)](#adr-003-estratégia-híbrida-de-análise-sintática-(ast-+-parsing-estrutural)) | `Aceito` | 2026 |
| **ADR-004** | [Padronização da Suíte de Documentação (C4, HLD/LLD, DAS e Linguagem Ubíqua)](#adr-004-padronização-da-suíte-de-documentação-(c4,-hld/lld,-das-e-linguagem-ubíqua)) | `Aceito` | 2026 |

---

## ADR-001: Adoção da Stack Tecnológica Principal: Python
**Status:** `Aceito` | **Data:** 2026

### Contexto
O projeto doc-gen necessita de alta confiabilidade, manutenibilidade e suporte consistente a ecossistema de desenvolvimento.

### Decisão
Padronizar o desenvolvimento do núcleo em Python, priorizando convenções consolidadas e tipagem consistente.

### Consequências
Positivo: facilidade de integração, ecossistema maduro e ampla base de conhecimento. Negativo: exige observância de boas práticas para manter o desempenho com bases volumosas.

---

## ADR-002: Padrão Arquitetural em Camadas e Pipeline
**Status:** `Aceito` | **Data:** 2026

### Contexto
Necessidade de separar as fases de entrada, descoberta, parseamento de código e geração de resultados para viabilizar testes independentes.

### Decisão
Adotar uma arquitetura orientada a Pipeline (Scanner -> Parsers -> Model -> Generators), desacoplando a camada de entrada da camada de geração.

### Consequências
Positivo: alta testabilidade, baixo acoplamento e suporte plugável a novas linguagens. Negativo: necessidade de manter um modelo de dados intermediário representativo.

---

## ADR-003: Estratégia Híbrida de Análise Sintática (AST + Parsing Estrutural)
**Status:** `Aceito` | **Data:** 2026

### Contexto
O sistema precisa analisar múltiplas linguagens (Python, TypeScript, Go, Rust, etc.) sem depender de ferramentas nativas externas pesadas.

### Decisão
Utilizar o módulo nativo AST onde disponível (ex: Python) e analisadores léxicos/estruturais robustos baseados em padrões formais para linguagens adicionais.

### Consequências
Positivo: execução ultra-rápida, zero dependências obrigatórias e compatibilidade imediata. Negativo: para sintaxes muito dinâmicas e metaprogramação, a análise foca em símbolos declarados explicitamente.

---

## ADR-004: Padronização da Suíte de Documentação (C4, HLD/LLD, DAS e Linguagem Ubíqua)
**Status:** `Aceito` | **Data:** 2026

### Contexto
Documentações puramente descritivas falham em comunicar a arquitetura de software para diferentes perfis de engenharia e liderança.

### Decisão
Padronizar a geração de documentos seguindo os padrões C4 Model, High-Level e Low-Level Design, Documento de Arquitetura de Software (DAS) e glossário de Linguagem Ubíqua (DDD).

### Consequências
Positivo: comunicação clara em múltiplos níveis de abstração (executivo, arquitetural e técnico). Negativo: volume maior de documentação gerada, mitigado pela navegação via sumário e servidor web.

---
