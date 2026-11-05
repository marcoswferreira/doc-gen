# ADR-003: Estratégia Híbrida de Análise Sintática (AST + Parsing Estrutural)

## Status
`Aceito`

## Contexto
O sistema precisa analisar múltiplas linguagens (Python, TypeScript, Go, Rust, etc.) sem depender de ferramentas nativas externas pesadas.

## Decisão
Utilizar o módulo nativo AST onde disponível (ex: Python) e analisadores léxicos/estruturais robustos baseados em padrões formais para linguagens adicionais.

## Consequências
Positivo: execução ultra-rápida, zero dependências obrigatórias e compatibilidade imediata. Negativo: para sintaxes muito dinâmicas e metaprogramação, a análise foca em símbolos declarados explicitamente.

## Data
2026
