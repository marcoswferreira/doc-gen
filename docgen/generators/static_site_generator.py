"""
Gerador de site estático HTML para publicação direta no GitHub Pages, GitLab Pages ou navegação offline.
Inclui visualizador completo, tema dark mode, renderizador de Mermaid e dados pré-embutidos.
"""

import json
from typing import Dict


def build_static_html_viewer(project_name: str, doc_contents: Dict[str, str]) -> str:
    """
    Gera um index.html autossuficiente contendo todos os Markdowns embutidos.
    Funciona 100% estático em qualquer servidor (como GitHub Pages) ou via file://.
    """
    json_docs = json.dumps(doc_contents, ensure_ascii=False)
    initial_file = "INDEX.md" if "INDEX.md" in doc_contents else (list(doc_contents.keys())[0] if doc_contents else "")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Documentação: {project_name}</title>
  <!-- Marked.js para renderizar Markdown -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <!-- Mermaid.js para renderizar diagramas interativos -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    :root {{
      --bg: #090d16;
      --sidebar: #111827;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-hover: #0284c7;
      --border: #334155;
      --code-bg: #030712;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }}
    #sidebar {{
      width: 320px;
      background: var(--sidebar);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .brand {{
      padding: 20px;
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .search-box {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
    }}
    .search-input {{
      width: 100%;
      padding: 8px 12px;
      background: #1f2937;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      font-size: 0.85rem;
      outline: none;
    }}
    .search-input:focus {{
      border-color: var(--accent);
    }}
    .file-list {{
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      list-style: none;
    }}
    .file-item {{
      padding: 10px 14px;
      margin-bottom: 4px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.88rem;
      color: var(--text-muted);
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .file-item:hover {{
      background: rgba(56, 189, 248, 0.12);
      color: var(--text);
    }}
    .file-item.active {{
      background: var(--accent);
      color: #090d16;
      font-weight: 600;
    }}
    #content-pane {{
      flex: 1;
      overflow-y: auto;
      padding: 40px 60px;
      scroll-behavior: smooth;
    }}
    .markdown-body {{
      max-width: 960px;
      margin: 0 auto;
      line-height: 1.75;
      font-size: 1rem;
    }}
    .markdown-body h1, .markdown-body h2, .markdown-body h3 {{
      color: var(--text);
      margin-top: 2rem;
      margin-bottom: 0.8rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.4rem;
    }}
    .markdown-body h1 {{ color: var(--accent); font-size: 1.9rem; }}
    .markdown-body h2 {{ font-size: 1.45rem; }}
    .markdown-body h3 {{ font-size: 1.2rem; }}
    .markdown-body p {{ margin-bottom: 1.2rem; color: #cbd5e1; }}
    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
    }}
    .markdown-body th, .markdown-body td {{
      border: 1px solid var(--border);
      padding: 10px 14px;
      text-align: left;
    }}
    .markdown-body th {{ background: rgba(255,255,255,0.06); color: var(--accent); font-weight: 600; }}
    .markdown-body pre {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
      margin: 1.4rem 0;
    }}
    .markdown-body code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.9em;
    }}
    .markdown-body pre code {{
      background: transparent;
      padding: 0;
      color: #f1f5f9;
    }}
    .mermaid {{
      background: #030712;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px;
      margin: 1.6rem 0;
      text-align: center;
      overflow-x: auto;
    }}
    blockquote {{
      border-left: 4px solid var(--accent);
      color: #cbd5e1;
      margin: 1.2rem 0;
      background: rgba(56, 189, 248, 0.06);
      padding: 12px 16px;
      border-radius: 0 6px 6px 0;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      font-size: 0.75rem;
      border-radius: 12px;
      background: rgba(56, 189, 248, 0.2);
      color: var(--accent);
      margin-left: auto;
    }}
  </style>
</head>
<body>
  <div id="sidebar">
    <div class="brand">⚡ DocGen: {project_name}</div>
    <div class="search-box">
      <input type="text" id="search-input" class="search-input" placeholder="Filtrar documentos...">
    </div>
    <ul class="file-list" id="file-list"></ul>
  </div>
  <div id="content-pane">
    <div id="doc-render" class="markdown-body">Carregando documentação...</div>
  </div>

  <script id="docs-data" type="application/json">
{json_docs}
  </script>

  <script>
    mermaid.initialize({{ startOnLoad: false, theme: 'dark', securityLevel: 'loose' }});

    const docsData = JSON.parse(document.getElementById("docs-data").textContent);
    const fileListEl = document.getElementById("file-list");
    const docRenderEl = document.getElementById("doc-render");
    const searchInput = document.getElementById("search-input");

    const fileIcons = {{
      "INDEX.md": "📌",
      "C4_MODEL.md": "🏛️",
      "HLD.md": "📐",
      "DAS.md": "📋",
      "UBIQUITOUS_LANGUAGE.md": "💡",
      "ARCHITECTURE.md": "🗺️",
      "API_REFERENCE.md": "📖",
      "DEPENDENCIES.md": "📦",
      "METRICS.md": "📊",
    }};

    function renderNav(filter = "") {{
      fileListEl.innerHTML = "";
      const lowerFilter = filter.toLowerCase();

      Object.keys(docsData).forEach((filename) => {{
        if (filter && !filename.toLowerCase().includes(lowerFilter)) return;

        const li = document.createElement("li");
        li.className = "file-item" + (window.location.hash.slice(1) === filename || (!window.location.hash && filename === "{initial_file}") ? " active" : "");
        const icon = fileIcons[filename] || "📄";
        li.innerHTML = `<span>${{icon}} ${{filename}}</span>`;
        li.onclick = () => selectFile(filename, li);
        fileListEl.appendChild(li);
      }});
    }}

    async function selectFile(filename, element) {{
      document.querySelectorAll(".file-item").forEach(el => el.classList.remove("active"));
      if (element) element.classList.add("active");
      window.location.hash = filename;
      await renderDocument(filename);
    }}

    async function renderDocument(filename) {{
      const markdown = docsData[filename];
      if (!markdown) {{
        docRenderEl.innerHTML = `<h2>Documento não encontrado: ${{filename}}</h2>`;
        return;
      }}

      // Scroll to top
      document.getElementById("content-pane").scrollTop = 0;

      // Renderiza Markdown com Marked
      docRenderEl.innerHTML = marked.parse(markdown);

      // Converte blocos de código com linguagem 'mermaid' em tags div.mermaid
      const preCodes = docRenderEl.querySelectorAll("pre code.language-mermaid");
      for (const codeBlock of preCodes) {{
        const pre = codeBlock.parentElement;
        const mermaidDiv = document.createElement("div");
        mermaidDiv.className = "mermaid";
        mermaidDiv.textContent = codeBlock.textContent;
        pre.parentNode.replaceChild(mermaidDiv, pre);
      }}

      // Executa Mermaid render nos diagramas
      try {{
        await mermaid.run({{ nodes: docRenderEl.querySelectorAll(".mermaid") }});
      }} catch (err) {{
        console.warn("Erro ao renderizar diagrama Mermaid:", err);
      }}
    }}

    searchInput.addEventListener("input", (e) => {{
      renderNav(e.target.value);
    }});

    // Trata hash inicial ou padrão
    const initialDoc = window.location.hash ? window.location.hash.slice(1) : "{initial_file}";
    renderNav();
    if (initialDoc && docsData[initialDoc]) {{
      renderDocument(initialDoc);
    }} else if ("{initial_file}" && docsData["{initial_file}"]) {{
      renderDocument("{initial_file}");
    }}
  </script>
</body>
</html>
"""

