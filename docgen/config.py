"""
Configurações, constantes e mapeamentos padrão do DocGen.
"""

from typing import Dict, List, Set, Any

# Extensões mapeadas para identificação de linguagens
LANGUAGE_EXTENSIONS: Dict[str, str] = {
    # Python
    ".py": "Python",
    ".pyw": "Python",
    ".pyi": "Python",
    # JavaScript & TypeScript
    ".js": "JavaScript",
    ".jsx": "JavaScript (React)",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    # Go
    ".go": "Go",
    # Rust
    ".rs": "Rust",
    # Java & JVM
    ".java": "Java",
    ".kt": "Kotlin",
    ".scala": "Scala",
    # C & C++
    ".c": "C",
    ".h": "C/C++ Header",
    ".cpp": "C++",
    ".hpp": "C++ Header",
    ".cc": "C++",
    # C#
    ".cs": "C#",
    # Web & Style
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    # Shell
    ".sh": "Shell",
    ".bash": "Bash",
    ".zsh": "Zsh",
    # Ruby & PHP
    ".rb": "Ruby",
    ".php": "PHP",
    # Data & Config
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
    ".sql": "SQL",
    ".graphql": "GraphQL",
    ".gql": "GraphQL",
    # Documentação
    ".md": "Markdown",
    ".rst": "reStructuredText",
}

# Arquivos especiais mapeados por nome exato
SPECIAL_FILENAMES: Dict[str, str] = {
    "dockerfile": "Docker",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
    "makefile": "Makefile",
    "jenkinsfile": "Jenkins",
    "procfile": "Procfile",
    "gemfile": "Ruby",
    "rakefile": "Ruby",
}

# Diretórios e arquivos ignorados por padrão
DEFAULT_IGNORES: Set[str] = {
    # Controle de versão
    ".git",
    ".svn",
    ".hg",
    # Dependências e caches de linguagens
    "node_modules",
    "bower_components",
    "vendor",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    # Ambientes virtuais
    "venv",
    ".venv",
    "env",
    ".env",
    # Builds e saídas
    "dist",
    "build",
    "out",
    "target",
    "bin",
    "obj",
    ".next",
    ".nuxt",
    ".output",
    # IDEs e editores
    ".idea",
    ".vscode",
    ".vs",
    # Cobertura de testes
    "coverage",
    ".coverage",
    "htmlcov",
    # Documentação gerada
    "docs",
    ".docgen",
}

# Padrões de arquivos a serem ignorados
DEFAULT_IGNORE_PATTERNS: List[str] = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.min.js",
    "*.min.css",
    "*.map",
    "*.lock",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Cargo.lock",
    "go.sum",
    "*.swp",
    "*.swo",
    "*.tmp",
    ".DS_Store",
    "Thumbs.db",
]

# Arquivos de manifesto para detecção de pacotes e frameworks
MANIFEST_FILES: Dict[str, str] = {
    "package.json": "Node.js / JavaScript",
    "requirements.txt": "Python (Pip)",
    "pyproject.toml": "Python (Modern PEP 518/621)",
    "Pipfile": "Python (Pipenv)",
    "setup.py": "Python (Setuptools)",
    "go.mod": "Go Modules",
    "Cargo.toml": "Rust (Cargo)",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java/Kotlin (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "composer.json": "PHP (Composer)",
    "Gemfile": "Ruby (Bundler)",
    "Dockerfile": "Docker Container",
    "docker-compose.yml": "Docker Compose Multi-Container",
    "docker-compose.yaml": "Docker Compose Multi-Container",
}

NON_CODE_LANGUAGES: Set[str] = {
    "Markdown",
    "reStructuredText",
    "JSON",
    "YAML",
    "TOML",
    "XML",
    "Other",
}


def get_primary_programming_language(language_dist: Dict[str, Any]) -> str:
    """Retorna a linguagem de programação principal, desconsiderando arquivos de doc/config."""
    for lang in language_dist.keys():
        if lang not in NON_CODE_LANGUAGES:
            return lang
    return list(language_dist.keys())[0] if language_dist else "Multi-language"


