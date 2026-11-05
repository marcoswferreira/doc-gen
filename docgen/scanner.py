"""
Scanner de repositório e analisador de arquivos.
Varre a árvore de diretórios respeitando regras do .gitignore,
calcula linhas de código (SLOC), comentários e identifica manifests.
"""

import os
import re
import fnmatch
from pathlib import Path
from typing import List, Set, Tuple, Dict, Any

from docgen.config import (
    LANGUAGE_EXTENSIONS,
    SPECIAL_FILENAMES,
    DEFAULT_IGNORES,
    DEFAULT_IGNORE_PATTERNS,
    MANIFEST_FILES,
)
from docgen.models import FileInfo, ProjectMetrics


class IgnoreMatcher:
    """Implementa correspondência de padrões estilo .gitignore."""

    def __init__(self, root_dir: Path, custom_patterns: List[str] = None):
        self.root_dir = root_dir.resolve()
        self.patterns: List[str] = []
        self.dir_patterns: List[str] = []

        # 1. Padrões padrão
        for ignore_dir in DEFAULT_IGNORES:
            self.dir_patterns.append(ignore_dir)
            self.patterns.append(f"*/{ignore_dir}/*")
            self.patterns.append(f"{ignore_dir}/*")
            self.patterns.append(ignore_dir)

        self.patterns.extend(DEFAULT_IGNORE_PATTERNS)

        # 2. Carrega .gitignore se existir
        gitignore_path = self.root_dir / ".gitignore"
        if gitignore_path.is_file():
            self._load_file(gitignore_path)

        # 3. Carrega .docgenignore se existir
        docgenignore_path = self.root_dir / ".docgenignore"
        if docgenignore_path.is_file():
            self._load_file(docgenignore_path)

        # 4. Padrões customizados fornecidos pela CLI
        if custom_patterns:
            for p in custom_patterns:
                p = p.strip()
                if p:
                    self.patterns.append(p)

    def _load_file(self, filepath: Path) -> None:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.endswith("/"):
                        self.dir_patterns.append(line[:-1])
                        self.patterns.append(line[:-1])
                        self.patterns.append(f"*/{line[:-1]}/*")
                    else:
                        self.patterns.append(line)
        except Exception:
            pass

    def is_ignored(self, path: Path) -> bool:
        """Verifica se um determinado Path deve ser ignorado."""
        try:
            rel_path = path.resolve().relative_to(self.root_dir).as_posix()
        except ValueError:
            rel_path = path.as_posix()

        # Checa componentes de pasta
        parts = rel_path.split("/")
        for part in parts:
            if part in self.dir_patterns or part in DEFAULT_IGNORES:
                return True

        filename = path.name

        for pattern in self.patterns:
            # Se o padrão tiver barra, compara com rel_path
            if "/" in pattern:
                p = pattern.lstrip("/")
                if fnmatch.fnmatch(rel_path, p) or fnmatch.fnmatch(rel_path, f"*{p}*"):
                    return True
            else:
                if fnmatch.fnmatch(filename, pattern):
                    return True

        return False


def detect_language(path: Path) -> str:
    """Identifica a linguagem pelo nome ou extensão do arquivo."""
    name_lower = path.name.lower()
    if name_lower in SPECIAL_FILENAMES:
        return SPECIAL_FILENAMES[name_lower]

    suffix = path.suffix.lower()
    return LANGUAGE_EXTENSIONS.get(suffix, "Other")


def count_file_lines(path: Path, language: str) -> Tuple[int, int, int, int]:
    """
    Analisa as linhas de um arquivo e retorna:
    (total_lines, code_lines, comment_lines, blank_lines)
    """
    total = 0
    blank = 0
    comment = 0
    code = 0

    single_line_comment_prefixes = {
        "Python": ["#"],
        "JavaScript": ["//"],
        "JavaScript (React)": ["//"],
        "TypeScript": ["//"],
        "TypeScript (React)": ["//"],
        "Go": ["//"],
        "Rust": ["//"],
        "Java": ["//"],
        "C#": ["//"],
        "C": ["//", "/*"],
        "C++": ["//", "/*"],
        "Shell": ["#"],
        "Bash": ["#"],
        "Zsh": ["#"],
        "Ruby": ["#"],
        "PHP": ["//", "#"],
        "SQL": ["--"],
        "YAML": ["#"],
        "TOML": ["#"],
        "Docker": ["#"],
    }

    prefixes = single_line_comment_prefixes.get(language, ["#", "//"])

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            in_block_comment = False
            for line in f:
                total += 1
                stripped = line.strip()
                if not stripped:
                    blank += 1
                    continue

                # Bloco de comentários multi-linha (C-style, JS, TS, Java, Rust, Go)
                if in_block_comment:
                    comment += 1
                    if "*/" in stripped:
                        in_block_comment = False
                    continue

                if "/*" in stripped:
                    comment += 1
                    if "*/" not in stripped:
                        in_block_comment = True
                    continue

                # Python docstrings multi-linha (aproximado)
                if language == "Python" and (stripped.startswith('"""') or stripped.startswith("'''")):
                    comment += 1
                    quote = stripped[:3]
                    if stripped.count(quote) < 2:
                        in_block_comment = True
                    continue

                # Comentários de linha única
                is_comment = any(stripped.startswith(p) for p in prefixes)
                if is_comment:
                    comment += 1
                else:
                    code += 1
    except Exception:
        pass

    return total, code, comment, blank


class RepositoryScanner:
    """Escaneia o repositório e constrói a lista inicial de arquivos e métricas."""

    def __init__(self, root_dir: str, custom_ignores: List[str] = None):
        self.root_path = Path(root_dir).resolve()
        self.matcher = IgnoreMatcher(self.root_path, custom_ignores)

    def scan(self) -> List[FileInfo]:
        """Varre o repositório retornando FileInfo para todos os arquivos válidos."""
        discovered_files: List[FileInfo] = []

        for root, dirs, files in os.walk(self.root_path):
            current_dir = Path(root)

            # Filtra diretórios in-place para que os ignorados não sejam visitados
            dirs[:] = [
                d for d in dirs
                if not self.matcher.is_ignored(current_dir / d)
            ]

            for file_name in files:
                file_path = current_dir / file_name
                if self.matcher.is_ignored(file_path):
                    continue

                # Ignora arquivos binários conhecidos ou maiores que 5MB
                try:
                    size = file_path.stat().st_size
                    if size > 5 * 1024 * 1024:  # > 5MB
                        continue
                except Exception:
                    continue

                rel_path = file_path.relative_to(self.root_path).as_posix()
                lang = detect_language(file_path)

                total, code, comment, blank = count_file_lines(file_path, lang)

                file_info = FileInfo(
                    path=rel_path,
                    absolute_path=str(file_path),
                    language=lang,
                    lines_total=total,
                    lines_code=code,
                    lines_comment=comment,
                    lines_blank=blank,
                    file_size_bytes=size,
                )
                discovered_files.append(file_info)

        return discovered_files

    def calculate_metrics(self, files: List[FileInfo]) -> ProjectMetrics:
        """Gera as métricas agregadas do projeto."""
        metrics = ProjectMetrics()
        metrics.total_files = len(files)

        lang_stats: Dict[str, Dict[str, Any]] = {}
        symbol_counts: Dict[str, int] = {}

        for f in files:
            metrics.total_lines += f.lines_total
            metrics.total_code_lines += f.lines_code
            metrics.total_comment_lines += f.lines_comment
            metrics.total_blank_lines += f.lines_blank

            if f.language not in lang_stats:
                lang_stats[f.language] = {
                    "files": 0,
                    "code_lines": 0,
                    "total_lines": 0,
                    "comment_lines": 0,
                }
            lang_stats[f.language]["files"] += 1
            lang_stats[f.language]["code_lines"] += f.lines_code
            lang_stats[f.language]["total_lines"] += f.lines_total
            lang_stats[f.language]["comment_lines"] += f.lines_comment

            for s in f.symbols:
                st = s.symbol_type.value
                symbol_counts[st] = symbol_counts.get(st, 0) + 1
                for c in s.children:
                    ct = c.symbol_type.value
                    symbol_counts[ct] = symbol_counts.get(ct, 0) + 1

        # Calcula porcentagens de linguagem por linhas de código
        total_code = max(metrics.total_code_lines, 1)
        for lang, data in lang_stats.items():
            pct = round((data["code_lines"] / total_code) * 100, 1)
            data["percentage"] = pct

        metrics.language_distribution = dict(
            sorted(lang_stats.items(), key=lambda item: item[1]["code_lines"], reverse=True)
        )
        metrics.symbol_counts = symbol_counts

        if metrics.total_code_lines > 0:
            metrics.docstring_ratio = round(
                (metrics.total_comment_lines / metrics.total_code_lines) * 100, 1
            )

        return metrics

    def detect_manifests(self) -> Tuple[Dict[str, str], List[str]]:
        """
        Localiza manifests e extrai lista de dependências externas.
        Retorna (manifests_encontrados, dependencias_externas).
        """
        found_manifests: Dict[str, str] = {}
        external_deps: Set[str] = set()

        for filename, desc in MANIFEST_FILES.items():
            p = self.root_path / filename
            if p.is_file():
                found_manifests[filename] = desc

                # Extrai dependências do package.json
                if filename == "package.json":
                    try:
                        import json
                        with open(p, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            for dep in data.get("dependencies", {}).keys():
                                external_deps.add(dep)
                            for dep in data.get("devDependencies", {}).keys():
                                external_deps.add(f"{dep} (dev)")
                    except Exception:
                        pass

                # Extrai dependências de requirements.txt
                elif filename == "requirements.txt":
                    try:
                        with open(p, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith("#") and not line.startswith("-"):
                                    pkg = re.split(r"[=<>~!]", line)[0].strip()
                                    if pkg:
                                        external_deps.add(pkg)
                    except Exception:
                        pass

                # Extrai dependências de Cargo.toml
                elif filename == "Cargo.toml":
                    try:
                        in_deps = False
                        with open(p, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                stripped = line.strip()
                                if stripped == "[dependencies]":
                                    in_deps = True
                                    continue
                                elif stripped.startswith("["):
                                    in_deps = False
                                if in_deps and "=" in stripped:
                                    pkg = stripped.split("=")[0].strip()
                                    if pkg:
                                        external_deps.add(pkg)
                    except Exception:
                        pass

                # Extrai dependências de go.mod
                elif filename == "go.mod":
                    try:
                        in_require = False
                        with open(p, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                stripped = line.strip()
                                if stripped.startswith("require ("):
                                    in_require = True
                                    continue
                                elif in_require and stripped == ")":
                                    in_require = False
                                    continue
                                if in_require or stripped.startswith("require "):
                                    parts = stripped.replace("require ", "").split()
                                    if parts:
                                        external_deps.add(parts[0])
                    except Exception:
                        pass

        return found_manifests, sorted(list(external_deps))
