"""
Core module for StripComment.

Provides the main comment stripping functionality with intelligent
string preservation and multi-language support.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from stripcomment.languages import LanguageConfig, get_language_by_extension


@dataclass
class StripResult:
    """Result of stripping comments from source code."""

    original_code: str
    stripped_code: str
    comments_removed: int
    lines_removed: int
    bytes_saved: int
    preserved_docstrings: int = 0
    errors: List[str] = field(default_factory=list)


@dataclass
class StripOptions:
    """Options for comment stripping."""

    preserve_docstrings: bool = False
    preserve_copyright: bool = False
    preserve_todos: bool = False
    preserve_license: bool = False
    preserve_patterns: List[str] = field(default_factory=list)
    remove_blank_lines: bool = False
    minify: bool = False
    dry_run: bool = False


class StripComment:
    """
    Main class for stripping comments from source code.

    Uses a line-by-line approach with regex for accurate comment detection
    while preserving string literals.
    """

    # Patterns for preservation
    COPYRIGHT_PATTERNS = [
        r"copyright",
        r"\(c\)",
        r"©",
        r"all rights reserved",
    ]

    TODO_PATTERNS = [
        r"todo",
        r"fixme",
        r"hack",
        r"xxx",
        r"note",
        r"bug",
    ]

    LICENSE_PATTERNS = [
        r"license",
        r"mit",
        r"apache",
        r"bsd",
        r"gpl",
        r"lgpl",
        r"mozilla",
    ]

    def __init__(self, config: Optional[LanguageConfig] = None):
        """
        Initialize StripComment with optional language configuration.

        Args:
            config: Language configuration. If None, auto-detection will be used.
        """
        self.config = config

    def strip(
        self,
        code: str,
        options: Optional[StripOptions] = None,
        config: Optional[LanguageConfig] = None,
    ) -> StripResult:
        """
        Strip comments from source code.

        Args:
            code: Source code to process
            options: Stripping options
            config: Language configuration (overrides instance config)

        Returns:
            StripResult with processed code and statistics
        """
        options = options or StripOptions()
        config = config or self.config

        if config is None:
            raise ValueError("No language configuration provided")

        result = self._process_code(code, options, config)
        return result

    def strip_file(
        self,
        file_path: Path,
        options: Optional[StripOptions] = None,
        output_path: Optional[Path] = None,
    ) -> StripResult:
        """
        Strip comments from a file.

        Args:
            file_path: Path to source file
            options: Stripping options
            output_path: Output file path (if None, modifies in place)

        Returns:
            StripResult with processed code and statistics
        """
        file_path = Path(file_path)

        # Auto-detect language from extension
        config = get_language_by_extension(file_path.suffix)
        if config is None:
            return StripResult(
                original_code="",
                stripped_code="",
                comments_removed=0,
                lines_removed=0,
                bytes_saved=0,
                errors=[f"Unsupported file extension: {file_path.suffix}"],
            )

        try:
            original_code = file_path.read_text(encoding="utf-8")
        except Exception as e:
            return StripResult(
                original_code="",
                stripped_code="",
                comments_removed=0,
                lines_removed=0,
                bytes_saved=0,
                errors=[f"Failed to read file: {e}"],
            )

        result = self.strip(original_code, options, config)

        if not options or not options.dry_run:
            output = output_path or file_path
            if result.stripped_code != original_code:
                output.write_text(result.stripped_code, encoding="utf-8")

        return result

    def _process_code(
        self,
        code: str,
        options: StripOptions,
        config: LanguageConfig,
    ) -> StripResult:
        """Process code using line-by-line parsing with string awareness."""
        original_lines = code.split("\n")
        output_lines = []
        comments_removed = 0
        preserved_docstrings = 0
        errors = []

        in_multiline_comment = False
        multiline_delimiter = None
        in_string = False
        string_delimiter = None
        in_docstring = False

        for line in original_lines:
            processed_line = ""
            i = 0
            n = len(line)

            while i < n:
                char = line[i]
                remaining = line[i:]

                # Handle multiline comment state
                if in_multiline_comment:
                    # Check for end of multiline comment
                    end_found = False
                    for start, end in config.multi_line:
                        if remaining.startswith(end):
                            in_multiline_comment = False
                            multiline_delimiter = None
                            i += len(end)
                            if not options.minify:
                                processed_line += " "
                            end_found = True
                            break
                    if not end_found:
                        i += 1
                    continue

                # Handle string state
                if in_string:
                    processed_line += char
                    if char == "\\" and i + 1 < n:
                        # Escape sequence
                        processed_line += line[i + 1]
                        i += 2
                        continue
                    elif in_docstring:
                        # Check for docstring end (triple quotes)
                        if remaining.startswith(string_delimiter):
                            processed_line += string_delimiter[1:] if len(string_delimiter) > 1 else ""
                            in_string = False
                            in_docstring = False
                            preserved_docstrings += 1
                            i += len(string_delimiter)
                            continue
                    elif char == string_delimiter:
                        in_string = False
                        string_delimiter = None
                    i += 1
                    continue

                # Check for string start
                for delim in ['"""', "'''", '"', "'", "`"]:
                    if remaining.startswith(delim):
                        # Check if it's a docstring
                        is_docstring = False
                        if config.preserves_docstrings and delim in config.docstring_markers:
                            # Check if at start of line or after certain patterns
                            stripped_so_far = processed_line.strip()
                            if not stripped_so_far or stripped_so_far.endswith(":"):
                                is_docstring = True
                                in_docstring = True
                                preserved_docstrings += 1

                        in_string = True
                        string_delimiter = delim
                        processed_line += delim
                        i += len(delim)
                        break
                else:
                    # Check for single-line comment
                    comment_found = False
                    for comment_start in config.single_line:
                        if remaining.startswith(comment_start):
                            # Check if we should preserve this comment
                            comment_content = remaining[len(comment_start):]
                            if self._should_preserve_comment(comment_content, options):
                                processed_line += remaining
                            else:
                                comments_removed += 1
                            comment_found = True
                            i = n  # Skip rest of line
                            break

                    if not comment_found:
                        # Check for multi-line comment start
                        ml_found = False
                        for start, end in config.multi_line:
                            if remaining.startswith(start):
                                # Check if we should preserve this comment
                                end_idx = line.find(end, i + len(start))
                                if end_idx != -1:
                                    # Comment ends on same line
                                    comment_content = line[i + len(start):end_idx]
                                    if self._should_preserve_comment(comment_content, options):
                                        processed_line += remaining[:end_idx + len(end)]
                                        i = end_idx + len(end)
                                    else:
                                        comments_removed += 1
                                        i = end_idx + len(end)
                                        if not options.minify:
                                            processed_line += " "
                                else:
                                    # Comment continues to next line
                                    in_multiline_comment = True
                                    multiline_delimiter = (start, end)
                                    comments_removed += 1
                                    i = n
                                ml_found = True
                                break

                        if not ml_found:
                            processed_line += char
                            i += 1

            output_lines.append(processed_line)

        result_code = "\n".join(output_lines)

        # Remove blank lines if requested
        if options.remove_blank_lines:
            lines = result_code.split("\n")
            result_code = "\n".join(line for line in lines if line.strip())

        # Calculate statistics
        result_lines_count = result_code.count("\n") + 1 if result_code else 0

        return StripResult(
            original_code=code,
            stripped_code=result_code,
            comments_removed=comments_removed,
            lines_removed=len(original_lines) - result_lines_count,
            bytes_saved=len(code) - len(result_code),
            preserved_docstrings=preserved_docstrings,
            errors=errors,
        )

    def _should_preserve_comment(
        self,
        comment_content: str,
        options: StripOptions,
    ) -> bool:
        """Check if a comment should be preserved based on options."""
        content_lower = comment_content.lower()

        # Check custom preserve patterns
        for pattern in options.preserve_patterns:
            if re.search(pattern, comment_content, re.IGNORECASE):
                return True

        # Check copyright
        if options.preserve_copyright:
            for pattern in self.COPYRIGHT_PATTERNS:
                if re.search(pattern, content_lower):
                    return True

        # Check TODOs
        if options.preserve_todos:
            for pattern in self.TODO_PATTERNS:
                if re.search(pattern, content_lower):
                    return True

        # Check license
        if options.preserve_license:
            for pattern in self.LICENSE_PATTERNS:
                if re.search(pattern, content_lower):
                    return True

        return False

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        from stripcomment.languages import get_supported_languages

        return get_supported_languages()

    def get_supported_extensions(self) -> Set[str]:
        """Get set of supported file extensions."""
        from stripcomment.languages import get_supported_extensions

        return get_supported_extensions()
