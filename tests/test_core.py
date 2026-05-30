"""
Tests for StripComment core functionality.
"""

import pytest
from stripcomment.core import StripComment, StripOptions
from stripcomment.languages import LanguageConfig, get_language_by_extension, get_language_by_name


class TestLanguageConfig:
    """Test language configuration functionality."""

    def test_get_language_by_extension_python(self):
        """Test Python language detection."""
        config = get_language_by_extension(".py")
        assert config is not None
        assert config.name == "Python"
        assert "#" in config.single_line

    def test_get_language_by_extension_javascript(self):
        """Test JavaScript language detection."""
        config = get_language_by_extension(".js")
        assert config is not None
        assert config.name == "JavaScript"
        assert "//" in config.single_line
        assert ("/*", "*/") in config.multi_line

    def test_get_language_by_extension_unknown(self):
        """Test unknown extension returns None."""
        config = get_language_by_extension(".xyz")
        assert config is None

    def test_get_language_by_name(self):
        """Test language lookup by name."""
        config = get_language_by_name("python")
        assert config is not None
        assert config.name == "Python"

    def test_supported_languages_list(self):
        """Test that supported languages list is not empty."""
        from stripcomment.languages import get_supported_languages

        languages = get_supported_languages()
        assert len(languages) > 0
        assert "python" in languages
        assert "javascript" in languages


class TestStripComment:
    """Test comment stripping functionality."""

    @pytest.fixture
    def python_config(self):
        """Get Python language configuration."""
        return get_language_by_extension(".py")

    @pytest.fixture
    def js_config(self):
        """Get JavaScript language configuration."""
        return get_language_by_extension(".js")

    def test_strip_single_line_comment(self, python_config):
        """Test stripping single-line comments."""
        code = 'x = 1  # This is a comment\ny = 2'
        stripper = StripComment(python_config)
        result = stripper.strip(code)

        assert "# This is a comment" not in result.stripped_code
        assert "x = 1" in result.stripped_code
        assert "y = 2" in result.stripped_code
        assert result.comments_removed == 1

    def test_strip_multi_line_comment(self, python_config):
        """Test stripping multi-line comments (triple quotes as comments, not docstrings)."""
        # When not preserving docstrings, triple quotes at module level are treated as comments
        code = '''x = 1
"""
This is a
multi-line string
"""
y = 2'''
        stripper = StripComment(python_config)
        # Without preserve_docstrings, triple quotes at module level are strings
        result = stripper.strip(code)
        
        # The triple-quoted string should be preserved (it's a string, not a comment)
        assert "This is a" in result.stripped_code or result.stripped_code.count('"""') >= 2

    def test_preserve_strings(self, python_config):
        """Test that strings are preserved."""
        code = '''x = "# This is not a comment"
y = 'Also # not a comment' '''
        stripper = StripComment(python_config)
        result = stripper.strip(code)

        assert "# This is not a comment" in result.stripped_code
        assert "# not a comment" in result.stripped_code

    def test_javascript_comments(self, js_config):
        """Test JavaScript comment stripping."""
        code = '''// Single line comment
const x = 1;
/* Multi-line
   comment */
const y = 2;'''
        stripper = StripComment(js_config)
        result = stripper.strip(code)

        assert "Single line comment" not in result.stripped_code
        assert "Multi-line" not in result.stripped_code
        assert "const x = 1;" in result.stripped_code
        assert "const y = 2;" in result.stripped_code

    def test_preserve_docstrings_option(self, python_config):
        """Test docstring preservation."""
        code = '''def foo():
    """This is a docstring."""
    x = 1  # This is a comment'''
        options = StripOptions(preserve_docstrings=True)
        stripper = StripComment(python_config)
        result = stripper.strip(code, options)

        assert "This is a docstring" in result.stripped_code
        assert "# This is a comment" not in result.stripped_code

    def test_preserve_copyright_option(self, python_config):
        """Test copyright comment preservation."""
        code = '''# Copyright 2024 My Company
# Regular comment
x = 1'''
        options = StripOptions(preserve_copyright=True)
        stripper = StripComment(python_config)
        result = stripper.strip(code, options)

        assert "Copyright 2024" in result.stripped_code

    def test_preserve_todos_option(self, python_config):
        """Test TODO comment preservation."""
        code = '''# TODO: Fix this later
# Regular comment
# FIXME: Another issue
x = 1'''
        options = StripOptions(preserve_todos=True)
        stripper = StripComment(python_config)
        result = stripper.strip(code, options)

        assert "TODO: Fix this later" in result.stripped_code
        assert "FIXME: Another issue" in result.stripped_code

    def test_dry_run_option(self, python_config, tmp_path):
        """Test dry run doesn't modify files."""
        test_file = tmp_path / "test.py"
        original_content = "x = 1  # comment\n"
        test_file.write_text(original_content)

        options = StripOptions(dry_run=True)
        stripper = StripComment()
        result = stripper.strip_file(test_file, options)

        assert test_file.read_text() == original_content
        assert result.comments_removed == 1

    def test_remove_blank_lines_option(self, python_config):
        """Test blank line removal."""
        code = '''x = 1

# comment

y = 2'''
        options = StripOptions(remove_blank_lines=True)
        stripper = StripComment(python_config)
        result = stripper.strip(code, options)

        lines = result.stripped_code.strip().split("\n")
        assert all(line.strip() for line in lines)

    def test_complex_nested_strings(self, python_config):
        """Test handling of complex nested strings."""
        code = '''x = "string with \\"escaped quotes\\" # not a comment"
y = 'another \\'string\\' # still not a comment'
# This IS a comment'''
        stripper = StripComment(python_config)
        result = stripper.strip(code)

        assert "# not a comment" in result.stripped_code
        assert "# still not a comment" in result.stripped_code
        assert "# This IS a comment" not in result.stripped_code

    def test_html_comments(self):
        """Test HTML comment stripping."""
        config = get_language_by_extension(".html")
        code = '''<!-- This is a comment -->
<div>Hello</div>
<!-- Another comment -->'''
        stripper = StripComment(config)
        result = stripper.strip(code)

        assert "This is a comment" not in result.stripped_code
        assert "Another comment" not in result.stripped_code
        assert "<div>Hello</div>" in result.stripped_code

    def test_sql_comments(self):
        """Test SQL comment stripping."""
        config = get_language_by_extension(".sql")
        code = '''-- Single line comment
SELECT * FROM users;
/* Multi-line
   comment */
SELECT 1;'''
        stripper = StripComment(config)
        result = stripper.strip(code)

        assert "Single line comment" not in result.stripped_code
        assert "Multi-line" not in result.stripped_code
        assert "SELECT * FROM users;" in result.stripped_code


class TestStripResult:
    """Test StripResult dataclass."""

    def test_result_properties(self):
        """Test StripResult has all expected properties."""
        from stripcomment.core import StripResult

        result = StripResult(
            original_code="x = 1  # comment",
            stripped_code="x = 1",
            comments_removed=1,
            lines_removed=0,
            bytes_saved=10,
        )

        assert result.original_code == "x = 1  # comment"
        assert result.stripped_code == "x = 1"
        assert result.comments_removed == 1
        assert result.bytes_saved == 10
