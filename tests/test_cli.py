"""
Tests for CLI functionality.
"""

import pytest
from click.testing import CliRunner

from stripcomment.cli import main


class TestCLI:
    """Test CLI commands."""

    @pytest.fixture
    def runner(self):
        """Create a CLI test runner."""
        return CliRunner()

    def test_version(self, runner):
        """Test version flag."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "StripComment" in result.output

    def test_languages_command(self, runner):
        """Test languages list command."""
        result = runner.invoke(main, ["languages"])
        assert result.exit_code == 0
        assert "Python" in result.output
        assert "JavaScript" in result.output

    def test_strip_file(self, runner, tmp_path):
        """Test stripping a file."""
        test_file = tmp_path / "test.py"
        test_file.write_text("x = 1  # comment\n")

        result = runner.invoke(main, ["strip", str(test_file), "--verbose"])

        assert result.exit_code == 0
        assert "Processing Summary" in result.output

    def test_strip_dry_run(self, runner, tmp_path):
        """Test dry run mode."""
        test_file = tmp_path / "test.py"
        original = "x = 1  # comment\n"
        test_file.write_text(original)

        result = runner.invoke(main, ["strip", str(test_file), "--dry-run"])

        assert result.exit_code == 0
        assert test_file.read_text() == original

    def test_strip_with_preserve_options(self, runner, tmp_path):
        """Test preserve options."""
        test_file = tmp_path / "test.py"
        test_file.write_text("# TODO: fix this\n# Copyright 2024\nx = 1\n")

        result = runner.invoke(
            main,
            [
                "strip",
                str(test_file),
                "--preserve-todos",
                "--preserve-copyright",
                "--dry-run",
            ],
        )

        assert result.exit_code == 0

    def test_stats_command(self, runner, tmp_path):
        """Test stats command."""
        test_file = tmp_path / "test.py"
        test_file.write_text("x = 1  # comment\ny = 2  # another\n")

        result = runner.invoke(main, ["stats", str(test_file)])

        assert result.exit_code == 0
        assert "Statistics" in result.output

    def test_help(self, runner):
        """Test help output."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "StripComment" in result.output

    def test_strip_help(self, runner):
        """Test strip command help."""
        result = runner.invoke(main, ["strip", "--help"])
        assert result.exit_code == 0
        assert "preserve" in result.output.lower()
