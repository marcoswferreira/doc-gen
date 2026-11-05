# Modelo C4 (Contexto, Containers, Componentes e Código): doc-gen

> [!NOTE]
> 🧠 **Síntese de IA Pendente**: No DocGen, documentos de arquitetura cognitiva e semântica de domínio (C4 Model) são gerados exclusivamente pelo motor de Inteligência Artificial para garantir rigor conceitual e evitar templates genéricos.

## Como gerar este documento com IA

Execute o DocGen habilitando um provedor de IA suportado:

### 1. Google Gemini (Recomendado na Nuvem)
```bash
export GEMINI_API_KEY="sua_chave_aqui"
docgen generate . --ai --provider gemini
```

### 2. Ollama Local (100% Offline e Privado)
```bash
ollama run deepseek-r1
docgen generate . --ai --provider ollama --model deepseek-r1
```

### 3. OpenAI ou Anthropic Claude
```bash
export OPENAI_API_KEY="sk-..."
docgen generate . --ai --provider openai

export ANTHROPIC_API_KEY="sk-ant-..."
docgen generate . --ai --provider anthropic
```
