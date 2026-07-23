from config import settings
from rich.console import Console
from rich.table import Table

from src.chunks.chunk_builder import ChunkBuilder
from src.parser.ast_parser import ASTParser
from src.scanner.repository_scanner import RepositoryScanner

console = Console()

# --------------------------------------------------
# Repository Scanner
# --------------------------------------------------

scanner = RepositoryScanner()
files = scanner.scan()

table = Table(title="Repository Files")

table.add_column("File")
table.add_column("Extension")
table.add_column("Lines", justify="right")
table.add_column("Size (Bytes)", justify="right")

for file in files:
    table.add_row(
        file.relative_path,
        file.extension,
        str(file.line_count),
        str(file.size_bytes),
    )

console.print(table)

# --------------------------------------------------
# Repository Statistics
# --------------------------------------------------

stats = scanner.get_statistics()

stats_table = Table(title="Repository Statistics")

stats_table.add_column("Metric")
stats_table.add_column("Value", justify="right")

stats_table.add_row("Total Files", str(stats["total_files"]))

for ext, count in sorted(stats["extensions"].items()):
    stats_table.add_row(f"{ext} Files", str(count))

stats_table.add_row("Total Lines", str(stats["total_lines"]))
stats_table.add_row(
    "Average Lines/File",
    f"{stats['average_lines']:.1f}"
)
stats_table.add_row(
    "Average Size/File",
    f"{stats['average_size']:.1f} Bytes"
)

console.print(stats_table)

# --------------------------------------------------
# Parser & Chunk Builder
# --------------------------------------------------

parser = ASTParser()
builder = ChunkBuilder()

all_chunks = []

console.rule("[bold green]Repository Structure[/bold green]")

for file in files:

    if file.extension != ".py":
        continue

    full_path = settings.REPOSITORY_PATH / file.path

    functions, classes, imports = parser.parse(full_path)

    # ------------------------
    # File Header
    # ------------------------

    console.print(f"\n[bold cyan]File:[/bold cyan] {file.relative_path}")

    # ------------------------
    # Imports
    # ------------------------

    if imports:

        console.print("[bold green]Imports[/bold green]")

        for imp in imports:

            if imp.name:
                console.print(
                    f"  from {imp.module} import {imp.name}"
                )
            else:
                console.print(
                    f"  import {imp.module}"
                )

    # ------------------------
    # Standalone Functions
    # ------------------------

    if functions:

        console.print("\n[bold yellow]Functions[/bold yellow]")

        for function in functions:

            console.print(
                f"  • {function.name}({', '.join(function.arguments)})"
            )

    # ------------------------
    # Classes
    # ------------------------

    if classes:

        console.print("\n[bold magenta]Classes[/bold magenta]")

        for cls in classes:

            console.print(
                f"  {cls.name}"
            )

            if cls.methods:

                console.print("      Methods:")

                for method in cls.methods:

                    console.print(
                        f"         • {method.name}({', '.join(method.arguments)})"
                    )

    # ------------------------
    # Build Chunks
    # ------------------------

    chunks = builder.build_chunks(
        file_path=full_path,
        functions=functions,
        classes=classes,
    )

    all_chunks.extend(chunks)

# --------------------------------------------------
# Repository Chunks
# --------------------------------------------------

console.rule("[bold cyan]Repository Chunks[/bold cyan]")

console.print(
    f"[bold green]Total Chunks:[/bold green] {len(all_chunks)}\n"
)

for chunk in all_chunks:

    title = chunk.name

    if chunk.parent_class:

        title = f"{chunk.parent_class}.{chunk.name}"

    console.print(
        f"[bold yellow]{chunk.chunk_type.upper()}[/bold yellow] : {title}"
    )

    console.print(
        f"Lines : {chunk.start_line}-{chunk.end_line}"
    )

    console.print(
        f"File  : {chunk.file_path}"
    )

    console.print("-" * 80)