"""
Engenharia de prompts para o arquiteto de software de IA.
Instruções rigorosas para geração de Modelo C4, HLD, LLD, DAS, ADRs e Linguagem Ubíqua.
"""

SYSTEM_ARCHITECT_PROMPT = """Você é um Arquiteto de Software Principal (Principal Software Architect) e Especialista em Engenharia de Software e Domain-Driven Design (DDD).
Sua missão é analisar profundamente o contexto técnico do repositório de código fornecido e sintetizar documentações técnicas ricas, precisas, aprofundadas e sem clichês.

DIRETRIZES FUNDAMENTAIS:
1. Baseie-se ESTRITAMENTE no código-fonte, nos contratos de AST, nas dependências e na arquitetura reais do repositório fornecido.
2. NUNCA gere respostas genéricas ou fictícias; cite arquivos, classes, métodos, frameworks e bibliotecas reais do projeto.
3. Utilize formatação GitHub Flavored Markdown de alto nível com alertas (> [!NOTE], > [!TIP], > [!IMPORTANT]).
4. Todos os diagramas Mermaid gerados devem possuir sintaxe 100% válida e estrita:
   - Em 'classDiagram', NUNCA utilize colons (:) antes de tipos de retorno de métodos (use '+metodo() TipoRetorno' e não '+metodo(): TipoRetorno').
   - NUNCA use palavras-chave primitivas como 'str', 'int', 'bool', 'object', 'enum' como classes base de herança (<|--).
   - Não use colchetes, vírgulas ou tipos aninhados em retornos de métodos no Mermaid.
   - Em 'flowchart' e 'sequenceDiagram', use quebras de linha com <br/> e sanitize identificadores de nós.
5. Escreva no idioma solicitado ({lang}).
"""

C4_PROMPT = """Gere o documento completo **Modelo C4 (C4_MODEL.md)** para o repositório abaixo.
Estruture o documento exatamente nas seguintes seções:
# Modelo C4: {project_name}

> [!NOTE]
> Breve introdução conceitual do Modelo C4 aplicado a este projeto.

## Nível 1: Diagrama de Contexto do Sistema (System Context)
- Descreva os atores humanos reais que utilizam este sistema.
- Descreva as fronteiras do sistema e sistemas externos reais com os quais ele interage (File System, APIs, Cloud, etc.).
- Inclua um diagrama Mermaid `flowchart TB` com os atores, o sistema e as integrações externas.
- Tabela descritiva de atores e fronteiras.

## Nível 2: Diagrama de Containers (Containers)
- Mapeie as aplicações executáveis, serviços, CLI, web servers e storages que compõem o sistema.
- Inclua um diagrama Mermaid `flowchart LR` detalhando os containers e suas tecnologias reais.
- Tabela de containers (Container, Tecnologia, Responsabilidade).

## Nível 3: Diagrama de Componentes (Components)
- Decomponha o container principal nos módulos internos reais (Scanner, Parsers, Models, Generators, CLI, etc.).
- Inclua um diagrama Mermaid `flowchart TD` das interações entre os componentes.
- Catálogo descritivo dos componentes chave citando os arquivos correspondentes.

## Nível 4: Diagrama de Código (Code / Class Diagram)
- Mapeie as principais classes de domínio, interfaces e suas relações de herança reais.
- Inclua um diagrama Mermaid `classDiagram` estritamente válido (sem herdar de str/int/enum, métodos formatados com +metodo() TipoRetorno).

CONTEXTO DO REPOSITÓRIO:
{context}
"""

HLD_PROMPT = """Gere o documento **High-Level Design (HLD.md)** para o repositório abaixo.
Estruture o documento nas seguintes seções:
# High-Level Design (HLD): {project_name}

> [!NOTE]
> Introdução ao High-Level Design e escopo do documento.

## 1. Visão Geral da Solução
- O que o sistema faz, qual problema resolve e seus objetivos centrais de engenharia.

## 2. Estilo Arquitetural e Decisões de Design
- Identifique o estilo arquitetural real (ex: Layered, Pipeline, Hexagonal/Ports and Adapters, Clean Architecture, Microservices, Event-Driven, CLI).
- Justifique tecnicamente por que este estilo foi adotado com base no código analisado.
- Diagrama Mermaid de fluxo macro de dados.

## 3. Requisitos Não-Funcionais (RNFs) e Metas de Engenharia
- Tabela detalhando requisitos de Portabilidade, Desempenho, Autonomia (offline), Segurança e Manutenibilidade, associando-os com as decisões tomadas no código.

## 4. Fronteiras do Sistema e Integrações
- Mapeamento das integrações com o sistema operacional, APIs externas ou bibliotecas do ecossistema.

CONTEXTO DO REPOSITÓRIO:
{context}
"""

DAS_PROMPT = """Gere o **Documento de Arquitetura de Software (DAS.md)** completo para o repositório abaixo, seguindo o padrão **Arc42** e o **Modelo 4+1 Visões de Kruchten**.
Estruture nas seguintes seções:
# Documento de Arquitetura de Software (DAS): {project_name}

> [!NOTE]
> Contexto normativo do documento baseado no Arc42 e 4+1 Visões.

## 1. Introdução e Metas Arquiteturais
- Metas de qualidade prioritárias para a solução.

## 2. Restrições e Premissas Técnicas
- Runtimes suportados, compatibilidade multiplataforma e restrições de ambiente.

## 3. Visão Lógica (Logical View)
- Decomposição em camadas funcionais com diagrama Mermaid `graph TD`.

## 4. Visão de Processos (Process View)
- Ciclo de vida da execução, sincronismo/assincronismo, concorrência e gerenciamento de memória.

## 5. Visão de Implantação e Execução (Deployment View)
- Topologia de implantação (local CLI, containers Docker, pipelines de CI/CD).

## 6. Riscos Arquiteturais e Débitos Técnicos
- Tabela com riscos reais identificados na arquitetura, severidade e recomendações técnicas de mitigação.

CONTEXTO DO REPOSITÓRIO:
{context}
"""

UBIQUITOUS_LANGUAGE_PROMPT = """Analise o repositório abaixo sob a ótica do **Domain-Driven Design (DDD)** e extraia a **Linguagem Ubíqua (UBIQUITOUS_LANGUAGE.md)** do sistema.

Estruture exatamente nas seções:
# Linguagem Ubíqua (Glossário DDD): {project_name}

> [!NOTE]
> Explicação da Linguagem Ubíqua como ferramenta para unificar a terminologia do domínio.

## 1. Mapa Conceitual do Domínio
- Diagrama Mermaid `graph TD` conectando os conceitos centrais do negócio/sistema.

## 2. Glossário de Termos do Domínio
- Tabela completa contendo:
  | Termo / Conceito | Categoria DDD (Entidade, Value Object, Serviço de Domínio, Enumeração, Operação) | Definição Semântica no Contexto do Projeto | Arquivos de Origem |

## 3. Detalhamento dos Bounded Contexts e Entidades Centrais
- Explicação aprofundada de cada conceito chave, suas regras de validação e papéis na arquitetura.

CONTEXTO DO REPOSITÓRIO:
{context}
"""

