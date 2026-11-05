"""
Servidor HTTP embutido com visualizador interativo moderno de Markdown e Mermaid.
Zero dependências externas: utiliza http.server da biblioteca padrão.
"""

import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from docgen.ui import Colors, print_info, print_success


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DocGen Viewer</title>
  <!-- Marked.js para renderizar Markdown no browser -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <!-- Mermaid.js para renderizar diagramas -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    :root {
      --bg: #0f172a;
      --sidebar: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --border: #334155;
      --code-bg: #0b1120;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }
    #sidebar {
      width: 320px;
      background: var(--sidebar);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }
    .brand {
      padding: 20px;
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .file-list {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      list-style: none;
    }
    .file-item {
      padding: 10px 14px;
      margin-bottom: 4px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.9rem;
      color: var(--text-muted);
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .file-item:hover {
      background: rgba(56, 189, 248, 0.1);
      color: var(--text);
    }
    .file-item.active {
      background: var(--accent);
      color: #0f172a;
      font-weight: 600;
    }
    #content-pane {
      flex: 1;
      overflow-y: auto;
      padding: 40px 60px;
    }
    .markdown-body {
      max-width: 900px;
      margin: 0 auto;
      line-height: 1.7;
      font-size: 1rem;
    }
    .markdown-body h1, .markdown-body h2, .markdown-body h3 {
      color: var(--text);
      margin-top: 1.8rem;
      margin-bottom: 0.8rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.4rem;
    }
    .markdown-body h1 { color: var(--accent); }
    .markdown-body p { margin-bottom: 1rem; color: #cbd5e1; }
    .markdown-body table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
    }
    .markdown-body th, .markdown-body td {
      border: 1px solid var(--border);
      padding: 10px 14px;
      text-align: left;
    }
    .markdown-body th { background: rgba(255,255,255,0.05); color: var(--accent); }
    .markdown-body pre {
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
      margin: 1.2rem 0;
    }
    .markdown-body code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.9em;
    }
    .markdown-body pre code {
      background: transparent;
      padding: 0;
      color: #f1f5f9;
    }
    .mermaid {
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      margin: 1.5rem 0;
      text-align: center;
    }
    blockquote {
      border-left: 4px solid var(--accent);
      padding-left: 16px;
      color: var(--text-muted);
      margin: 1.2rem 0;
      background: rgba(56, 189, 248, 0.05);
      padding: 12px 16px;
      border-radius: 0 6px 6px 0;
    }
  </style>
</head>
<body>
  <div id="sidebar">
    <div class="brand">⚡ DocGen Viewer</div>
    <ul class="file-list" id="file-list"></ul>
  </div>
  <div id="content-pane">
    <div id="doc-render" class="markdown-body">Carregando documentação...</div>
  </div>

  <script>
    mermaid.initialize({ startOnLoad: false, theme: 'dark' });

    let currentFile = "";

    async function loadFileList() {
      try {
        const res = await fetch("/api/files");
        const files = await res.json();
        const listEl = document.getElementById("file-list");
        listEl.innerHTML = "";

        files.forEach((f, idx) => {
          const li = document.createElement("li");
          li.className = "file-item" + (idx === 0 ? " active" : "");
          li.textContent = f;
          li.onclick = () => selectFile(f, li);
          listEl.appendChild(li);
        });

        if (files.length > 0) {
          loadFileContent(files[0]);
        }
      } catch (err) {
        document.getElementById("doc-render").innerHTML = "<p>Erro ao carregar arquivos.</p>";
      }
    }

    async function selectFile(filename, element) {
      document.querySelectorAll(".file-item").forEach(el => el.classList.remove("active"));
      element.classList.add("active");
      await loadFileContent(filename);
    }

    async function loadFileContent(filename) {
      currentFile = filename;
      const renderEl = document.getElementById("doc-render");
      renderEl.innerHTML = "<p>Renderizando...</p>";

      try {
        const res = await fetch("/api/content?file=" + encodeURIComponent(filename));
        const markdown = await res.text();
        
        // Renderiza Markdown
        renderEl.innerHTML = marked.parse(markdown);

        // Processa blocos Mermaid
        const preCodes = renderEl.querySelectorAll("pre code.language-mermaid");
        for (const codeBlock of preCodes) {
          const pre = codeBlock.parentElement;
          const mermaidDiv = document.createElement("div");
          mermaidDiv.className = "mermaid";
          mermaidDiv.textContent = codeBlock.textContent;
          pre.parentNode.replaceChild(mermaidDiv, pre);
        }

        // Executa Mermaid render
        await mermaid.run({ nodes: renderEl.querySelectorAll(".mermaid") });
      } catch (err) {
        renderEl.innerHTML = "<p>Erro ao ler arquivo: " + err + "</p>";
      }
    }

    loadFileList();
  </script>
</body>
</html>
"""


class DocViewerHandler(BaseHTTPRequestHandler):
    """Handler HTTP para servir a UI interativa e os arquivos Markdown."""

    docs_dir: Path = Path(".")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            return

        if path == "/api/files":
            files = []
            if self.docs_dir.is_dir():
                for p in sorted(self.docs_dir.rglob("*.md")):
                    files.append(p.relative_to(self.docs_dir).as_posix())
            elif self.docs_dir.is_file():
                files.append(self.docs_dir.name)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode("utf-8"))
            return

        if path == "/api/content":
            params = urllib.parse.parse_qs(parsed.query)
            filename = params.get("file", [""])[0]

            target_file = (self.docs_dir / filename).resolve() if self.docs_dir.is_dir() else self.docs_dir
            if target_file.is_file():
                try:
                    content = target_file.read_text(encoding="utf-8", errors="ignore")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/markdown; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
                    return
                except Exception:
                    pass

            self.send_response(404)
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()


def start_doc_server(docs_path: str = "docs", port: int = 8080):
    """Inicia o servidor de visualização local."""
    target = Path(docs_path).resolve()
    DocViewerHandler.docs_dir = target

    server_address = ("", port)
    httpd = HTTPServer(server_address, DocViewerHandler)
    url = f"http://localhost:{port}"

    print(f"\n{Colors.GREEN}{Colors.BOLD}⚡ Servidor DocGen ativo!{Colors.RESET}")
    print(f" {Colors.CYAN}Navegue pela documentação interativa em:{Colors.RESET} {Colors.BOLD}{Colors.UNDERLINE}{url}{Colors.RESET}")
    print(f" {Colors.DIM}Pressione Ctrl+C para encerrar.{Colors.RESET}\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado.")
        httpd.server_close()

