# High-Level Design (HLD): doc-gen

> [!NOTE]
> O **High-Level Design (HLD)** documenta a arquitetura macro, o estilo arquitetural, as fronteiras do sistema e os requisitos não-funcionais que orientam a engenharia da solução.

---

## 1. Visão Geral da Solução
O projeto **doc-gen** foi projetado como uma solução modular desenvolvida principalmente em **Python**, totalizando aproximadamente **357 linhas de código** distribuídas em **31 arquivos**.

### Objetivos Principais
- Fornecer processamento confiável, previsível e desacoplado.
- Permitir fácil extensão para novas linguagens e formatos sem quebrar contratos existentes.
- Garantir portabilidade multiplataforma sem necessidade de dependências pesadas de terceiros.

## 2. Estilo Arquitetural
A solução adota uma **Arquitetura em Camadas (Layered Architecture)** combinada com o padrão **Pipeline / Filter**, onde o fluxo de dados passa por etapas sequenciais bem definidas:

```mermaid
flowchart LR
    A[Input: Repositório] --> B[Camada de Descoberta / Scanner]
    B --> C[Camada de Análise / Parsers]
    C --> D[Camada de Modelo / Grafo de Dados]
    D --> E[Camada de Geração / Renderers]
    E --> F[Output: Markdown / Web]
```

### Benefícios do Estilo Adotado
- **Separação de Responsabilidades (SoC)**: O módulo de varredura não sabe como gerar Markdown; o gerador não sabe como o AST foi extraído.
- **Testabilidade Isolada**: Cada camada pode ser testada unitariamente com fixtures e dados mockados.
- **Extensibilidade**: Novos parsers e novos geradores podem ser adicionados plugando-se nas fábricas correspondentes.

## 3. Requisitos Não-Funcionais (RNFs)
| Categoria | Requisito | Estratégia de Implementação |
|---|---|---|
| **Portabilidade** | Executar em Linux, macOS e Windows sem compilação nativa externa | Uso de módulos padrão (`pathlib`, `os`, `sys`, `ast`) compatíveis entre SOs. |
| **Performance** | Analisar repositórios em tempo inferior a poucos segundos | Otimização de varredura de diretórios com poda rápida via `.gitignore` e regex pré-compiladas. |
| **Autonomia** | Funcionamento 100% offline (Zero dependência de rede obrigatória) | Motor sintático nativo que dispensa conexões remotas ou APIs externas para gerar a documentação completa. |
| **Manutenibilidade** | Código limpo, tipado e com alta taxa de documentação | Dataclasses estritas, contratos abstratos (`BaseParser`) e modularização em submódulos. |

## 4. Integrações e Fronteiras Externas
- **Sistema Operacional & File System**: Acesso a diretórios locais com permissão de leitura/escrita.
- **Bibliotecas Externas**: Autossuficiente utilizando exclusivamente a runtime padrão.