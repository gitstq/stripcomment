"""
Language configuration module for StripComment.

Defines comment syntax rules for various programming languages.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class LanguageConfig:
    """Configuration for a programming language's comment syntax."""

    name: str
    extensions: Set[str]
    single_line: List[str] = field(default_factory=list)
    multi_line: List[tuple] = field(default_factory=list)
    preserves_strings: bool = True
    preserves_docstrings: bool = False
    docstring_markers: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.extensions:
            raise ValueError(f"Language {self.name} must have at least one extension")


# Language definitions with comprehensive comment syntax support
LANGUAGE_CONFIGS: Dict[str, LanguageConfig] = {
    # C-style languages
    "python": LanguageConfig(
        name="Python",
        extensions={".py", ".pyw", ".pyi"},
        single_line=["#"],
        multi_line=[('"""', '"""'), ("'''", "'''")],
        preserves_docstrings=True,
        docstring_markers=['"""', "'''"],
    ),
    "javascript": LanguageConfig(
        name="JavaScript",
        extensions={".js", ".mjs", ".cjs", ".jsx"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "typescript": LanguageConfig(
        name="TypeScript",
        extensions={".ts", ".tsx", ".mts", ".cts"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "java": LanguageConfig(
        name="Java",
        extensions={".java"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "c": LanguageConfig(
        name="C",
        extensions={".c", ".h"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "cpp": LanguageConfig(
        name="C++",
        extensions={".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "csharp": LanguageConfig(
        name="C#",
        extensions={".cs"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "go": LanguageConfig(
        name="Go",
        extensions={".go"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "rust": LanguageConfig(
        name="Rust",
        extensions={".rs"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "swift": LanguageConfig(
        name="Swift",
        extensions={".swift"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "kotlin": LanguageConfig(
        name="Kotlin",
        extensions={".kt", ".kts"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "scala": LanguageConfig(
        name="Scala",
        extensions={".scala", ".sc"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    # Shell scripting
    "bash": LanguageConfig(
        name="Bash",
        extensions={".sh", ".bash", ".zsh"},
        single_line=["#"],
    ),
    "powershell": LanguageConfig(
        name="PowerShell",
        extensions={".ps1", ".psm1", ".psd1"},
        single_line=["#"],
        multi_line=[("<#", "#>")],
    ),
    # Scripting languages
    "ruby": LanguageConfig(
        name="Ruby",
        extensions={".rb", ".rake", ".gemspec"},
        single_line=["#"],
        multi_line=[("=begin", "=end")],
    ),
    "perl": LanguageConfig(
        name="Perl",
        extensions={".pl", ".pm", ".t"},
        single_line=["#"],
        multi_line=[("=pod", "=cut")],
    ),
    "php": LanguageConfig(
        name="PHP",
        extensions={".php", ".phtml", ".php3", ".php4", ".php5"},
        single_line=["//", "#"],
        multi_line=[("/*", "*/")],
    ),
    "lua": LanguageConfig(
        name="Lua",
        extensions={".lua"},
        single_line=["--"],
        multi_line=[("--[[", "]]"), ("--[=[", "]=]")],
    ),
    "r": LanguageConfig(
        name="R",
        extensions={".r", ".rmd"},
        single_line=["#"],
    ),
    # Data/Config languages
    "yaml": LanguageConfig(
        name="YAML",
        extensions={".yaml", ".yml"},
        single_line=["#"],
    ),
    "toml": LanguageConfig(
        name="TOML",
        extensions={".toml"},
        single_line=["#"],
    ),
    "ini": LanguageConfig(
        name="INI",
        extensions={".ini", ".cfg", ".conf"},
        single_line=["#", ";"],
    ),
    # Web languages
    "html": LanguageConfig(
        name="HTML",
        extensions={".html", ".htm", ".xhtml"},
        multi_line=[("<!--", "-->")],
    ),
    "css": LanguageConfig(
        name="CSS",
        extensions={".css", ".scss", ".sass", ".less"},
        multi_line=[("/*", "*/")],
    ),
    "xml": LanguageConfig(
        name="XML",
        extensions={".xml", ".xsl", ".xslt", ".svg"},
        multi_line=[("<!--", "-->")],
    ),
    # Other languages
    "sql": LanguageConfig(
        name="SQL",
        extensions={".sql"},
        single_line=["--"],
        multi_line=[("/*", "*/")],
    ),
    "haskell": LanguageConfig(
        name="Haskell",
        extensions={".hs", ".lhs"},
        single_line=["--"],
        multi_line=[("{-", "-}")],
    ),
    "elixir": LanguageConfig(
        name="Elixir",
        extensions={".ex", ".exs"},
        single_line=["#"],
    ),
    "erlang": LanguageConfig(
        name="Erlang",
        extensions={".erl", ".hrl"},
        single_line=["%"],
    ),
    "dart": LanguageConfig(
        name="Dart",
        extensions={".dart"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "jsonc": LanguageConfig(
        name="JSON with Comments",
        extensions={".jsonc", ".json5"},
        single_line=["//"],
        multi_line=[("/*", "*/")],
    ),
    "dockerfile": LanguageConfig(
        name="Dockerfile",
        extensions={"Dockerfile", ".dockerfile"},
        single_line=["#"],
    ),
    "makefile": LanguageConfig(
        name="Makefile",
        extensions={"Makefile", ".mk"},
        single_line=["#"],
    ),
    "vim": LanguageConfig(
        name="Vim Script",
        extensions={".vim", ".vimrc"},
        single_line=['"'],
    ),
    "matlab": LanguageConfig(
        name="MATLAB",
        extensions={".m"},
        single_line=["%"],
        multi_line=[("%{", "%}")],
    ),
    "julia": LanguageConfig(
        name="Julia",
        extensions={".jl"},
        single_line=["#"],
        multi_line=[("#=", "=#")],
    ),
    "fortran": LanguageConfig(
        name="Fortran",
        extensions={".f", ".f90", ".f95", ".f03", ".f08"},
        single_line=["!"],
    ),
    "assembly": LanguageConfig(
        name="Assembly",
        extensions={".asm", ".s", ".S"},
        single_line=[";", "#", "//"],
    ),
}


def get_language_by_extension(extension: str) -> Optional[LanguageConfig]:
    """
    Get language configuration by file extension.

    Args:
        extension: File extension (with or without leading dot)

    Returns:
        LanguageConfig if found, None otherwise
    """
    ext = extension.lower()
    if not ext.startswith("."):
        ext = "." + ext

    for config in LANGUAGE_CONFIGS.values():
        if ext in config.extensions or ext.lstrip(".") in config.extensions:
            return config

    return None


def get_language_by_name(name: str) -> Optional[LanguageConfig]:
    """
    Get language configuration by language name.

    Args:
        name: Language name (case-insensitive)

    Returns:
        LanguageConfig if found, None otherwise
    """
    name_lower = name.lower()
    return LANGUAGE_CONFIGS.get(name_lower)


def get_supported_extensions() -> Set[str]:
    """Get all supported file extensions."""
    extensions = set()
    for config in LANGUAGE_CONFIGS.values():
        extensions.update(config.extensions)
    return extensions


def get_supported_languages() -> List[str]:
    """Get list of supported language names."""
    return list(LANGUAGE_CONFIGS.keys())
