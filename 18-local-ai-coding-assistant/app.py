from rich.console import Console
from rich.table import Table

from src.scanner.repository_scanner import RepositoryScanner

console = Console()


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

stats = scanner.get_statistics()

console.print(table)

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