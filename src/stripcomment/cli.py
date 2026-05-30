"""
Command-line interface for StripComment.

Provides a powerful CLI with rich output, batch processing,
and flexible configuration options.
"""

import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text

from stripcomment import __version__
from stripcomment.core import StripComment, StripOptions
from stripcomment.languages import get_language_by_extension, get_supported_languages

console = Console()


def print_banner():
    """Print the application banner."""
    banner = Text()
    banner.append("🧹 StripComment ", style="bold cyan")
    banner.append(f"v{__version__}", style="dim")
    banner.append(" - Intelligently strip comments from source code", style="dim")
    console.print(banner)
    console.print()


def create_options(
    preserve_docstrings: bool,
    preserve_copyright: bool,
    preserve_todos: bool,
    preserve_license: bool,
    remove_blank_lines: bool,
    minify: bool,
    dry_run: bool,
    preserve: List[str],
) -> StripOptions:
    """Create StripOptions from CLI arguments."""
    return StripOptions(
        preserve_docstrings=preserve_docstrings,
        preserve_copyright=preserve_copyright,
        preserve_todos=preserve_todos,
        preserve_license=preserve_license,
        remove_blank_lines=remove_blank_lines,
        minify=minify,
        dry_run=dry_run,
        preserve_patterns=preserve,
    )


def process_single_file(
    file_path: Path,
    options: StripOptions,
    output: Optional[Path],
    backup: bool,
) -> tuple:
    """Process a single file and return results."""
    stripper = StripComment()
    result = stripper.strip_file(file_path, options, output)

    if result.errors:
        return False, result

    # Create backup if requested
    if backup and not options.dry_run and result.stripped_code != result.original_code:
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        backup_path.write_text(result.original_code, encoding="utf-8")

    return True, result


def print_summary(results: List[tuple], verbose: bool):
    """Print processing summary."""
    total_files = len(results)
    successful = sum(1 for success, _ in results if success)
    failed = total_files - successful

    total_comments = sum(r.comments_removed for _, r in results if _)
    total_bytes = sum(r.bytes_saved for _, r in results if _)
    total_lines = sum(r.lines_removed for _, r in results if _)

    # Summary table
    table = Table(title="\n📊 Processing Summary", show_header=False, box=None)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")

    table.add_row("Files Processed", str(successful))
    if failed > 0:
        table.add_row("Files Failed", f"[red]{failed}[/red]")
    table.add_row("Comments Removed", str(total_comments))
    table.add_row("Lines Removed", str(total_lines))
    table.add_row("Bytes Saved", f"{total_bytes:,}")

    console.print(table)

    # Detailed results if verbose
    if verbose and results:
        detail_table = Table(title="\n📝 Detailed Results", box=None)
        detail_table.add_column("File", style="cyan")
        detail_table.add_column("Comments", justify="right")
        detail_table.add_column("Lines", justify="right")
        detail_table.add_column("Bytes", justify="right")
        detail_table.add_column("Status", justify="center")

        for success, result in results:
            status = "✅" if success else "❌"
            detail_table.add_row(
                getattr(result, "file_path", "unknown"),
                str(result.comments_removed),
                str(result.lines_removed),
                str(result.bytes_saved),
                status,
            )

        console.print(detail_table)


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit")
@click.pass_context
def main(ctx, version):
    """🧹 StripComment - Intelligently strip comments from source code."""
    if version:
        console.print(f"StripComment v{__version__}")
        return

    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@main.command()
@click.argument("path", type=click.Path(exists=True), required=False)
@click.option("--output", "-o", type=click.Path(), help="Output file or directory")
@click.option(
    "--language",
    "-l",
    type=click.Choice(get_supported_languages()),
    help="Force language (auto-detected by default)",
)
@click.option("--preserve-docstrings", is_flag=True, help="Preserve docstrings")
@click.option("--preserve-copyright", is_flag=True, help="Preserve copyright comments")
@click.option("--preserve-todos", is_flag=True, help="Preserve TODO/FIXME comments")
@click.option("--preserve-license", is_flag=True, help="Preserve license comments")
@click.option(
    "--preserve",
    "-p",
    multiple=True,
    help="Preserve comments matching regex pattern",
)
@click.option("--remove-blank-lines", is_flag=True, help="Remove blank lines after stripping")
@click.option("--minify", is_flag=True, help="Minify output (remove extra whitespace)")
@click.option("--dry-run", "-d", is_flag=True, help="Preview changes without modifying files")
@click.option("--backup", "-b", is_flag=True, help="Create .bak backup files")
@click.option("--recursive", "-r", is_flag=True, help="Process directories recursively")
@click.option(
    "--extensions",
    "-e",
    help="Comma-separated list of extensions to process (e.g., .py,.js,.ts)",
)
@click.option("--verbose", "-V", is_flag=True, help="Show detailed output")
def strip(
    path,
    output,
    language,
    preserve_docstrings,
    preserve_copyright,
    preserve_todos,
    preserve_license,
    preserve,
    remove_blank_lines,
    minify,
    dry_run,
    backup,
    recursive,
    extensions,
    verbose,
):
    """
    Strip comments from source code files.

    PATH can be a file or directory. If not provided, reads from stdin.
    """
    print_banner()

    options = create_options(
        preserve_docstrings=preserve_docstrings,
        preserve_copyright=preserve_copyright,
        preserve_todos=preserve_todos,
        preserve_license=preserve_license,
        remove_blank_lines=remove_blank_lines,
        minify=minify,
        dry_run=dry_run,
        preserve=list(preserve),
    )

    # Handle stdin input
    if path is None:
        if sys.stdin.isatty():
            console.print("[red]Error: No input provided. Specify a file or pipe input.[/red]")
            console.print("\nExample: cat file.py | stripcomment strip")
            sys.exit(1)

        code = sys.stdin.read()
        if not language:
            console.print("[red]Error: --language is required when reading from stdin[/red]")
            sys.exit(1)

        from stripcomment.languages import get_language_by_name

        config = get_language_by_name(language)
        if not config:
            console.print(f"[red]Error: Unknown language: {language}[/red]")
            sys.exit(1)

        stripper = StripComment(config)
        result = stripper.strip(code, options)
        console.print(result.stripped_code)
        return

    path = Path(path)

    # Collect files to process
    files_to_process = []

    if path.is_file():
        files_to_process = [path]
    elif path.is_dir():
        if extensions:
            ext_list = [e.strip() if e.startswith(".") else f".{e.strip()}" for e in extensions.split(",")]
        else:
            from stripcomment.languages import get_supported_extensions

            ext_list = list(get_supported_extensions())

        if recursive:
            for ext in ext_list:
                files_to_process.extend(path.rglob(f"*{ext}"))
        else:
            for ext in ext_list:
                files_to_process.extend(path.glob(f"*{ext}"))

        files_to_process = list(set(files_to_process))

    if not files_to_process:
        console.print("[yellow]No matching files found to process.[/yellow]")
        return

    # Process files with progress bar
    results = []
    output_path = Path(output) if output else None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(files_to_process))

        for file_path in files_to_process:
            progress.update(task, description=f"Processing {file_path.name}")

            file_output = None
            if output_path:
                if output_path.is_dir():
                    file_output = output_path / file_path.name
                else:
                    file_output = output_path

            success, result = process_single_file(file_path, options, file_output, backup)
            result.file_path = str(file_path)
            results.append((success, result))

            progress.advance(task)

    # Print summary
    print_summary(results, verbose)


@main.command()
def languages():
    """List all supported programming languages."""
    print_banner()

    table = Table(title="📚 Supported Languages", show_lines=True)
    table.add_column("Language", style="cyan")
    table.add_column("Extensions", style="green")
    table.add_column("Single-line", style="yellow")
    table.add_column("Multi-line", style="magenta")

    from stripcomment.languages import LANGUAGE_CONFIGS

    for name, config in sorted(LANGUAGE_CONFIGS.items()):
        ext_str = ", ".join(sorted(config.extensions)[:5])
        if len(config.extensions) > 5:
            ext_str += f" (+{len(config.extensions) - 5} more)"

        single = ", ".join(config.single_line) if config.single_line else "-"
        multi = ", ".join(f"{s}...{e}" for s, e in config.multi_line) if config.multi_line else "-"

        table.add_row(config.name, ext_str, single, multi)

    console.print(table)
    console.print(f"\n[dim]Total: {len(LANGUAGE_CONFIGS)} languages supported[/dim]")


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--verbose", "-V", is_flag=True, help="Show detailed statistics")
def stats(path, verbose):
    """Show comment statistics for a file without modifying it."""
    print_banner()

    path = Path(path)
    stripper = StripComment()
    options = StripOptions(dry_run=True)

    result = stripper.strip_file(path, options)

    if result.errors:
        for error in result.errors:
            console.print(f"[red]Error: {error}[/red]")
        return

    # Statistics table
    table = Table(title=f"📊 Statistics for {path.name}", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")

    original_lines = result.original_code.count("\n") + 1
    comment_lines = result.lines_removed
    code_lines = original_lines - comment_lines
    comment_percentage = (comment_lines / original_lines * 100) if original_lines > 0 else 0

    table.add_row("Total Lines", str(original_lines))
    table.add_row("Code Lines", str(code_lines))
    table.add_row("Comment Lines", str(comment_lines))
    table.add_row("Comment Percentage", f"{comment_percentage:.1f}%")
    table.add_row("Comments Removed", str(result.comments_removed))
    table.add_row("Bytes Saved", f"{result.bytes_saved:,}")
    table.add_row("Docstrings Preserved", str(result.preserved_docstrings))

    console.print(table)

    if verbose:
        console.print("\n[dim]Original code preview:[/dim]")
        console.print(result.original_code[:500] + "..." if len(result.original_code) > 500 else result.original_code)


if __name__ == "__main__":
    main()
