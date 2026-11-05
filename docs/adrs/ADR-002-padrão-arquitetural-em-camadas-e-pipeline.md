# ADR-002: Padrão Arquitetural em Camadas e Pipeline

## Status
`Aceito`

## Contexto
Necessidade de separar as fases de entrada, descoberta, parseamento de código e geração de resultados para viabilizar testes independentes.

## Decisão
Adotar uma arquitetura orientada a Pipeline (Scanner -> Parsers -> Model -> Generators), desacoplando a camada de entrada da camada de geração.

## Consequências
Positivo: alta testabilidade, baixo acoplamento e suporte plugável a novas linguagens. Negativo: necessidade de manter um modelo de dados intermediário representativo.

## Data
2026
