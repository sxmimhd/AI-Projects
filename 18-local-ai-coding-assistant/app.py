from config import settings
from rich.console import Console
from rich.table import Table

from src.chunks.chunk_builder import ChunkBuilder
from src.parser.ast_parser import ASTParser
from src.scanner.repository_scanner import RepositoryScanner
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.faiss_store import FAISSStore
from src.retriever.retriever import Retriever
from src.prompting.prompt_builder import PromptBuilder
from src.llm.client import LLMClient

settings.MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

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

console.print(table)

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

parser = ASTParser()
builder = ChunkBuilder()

all_chunks = []

console.rule("[bold green]Repository Structure[/bold green]")

for file in files:

    if file.extension != ".py":
        continue

    full_path = settings.REPOSITORY_PATH / file.path

    functions, classes, imports = parser.parse(full_path)

    console.print(f"\n[bold cyan]File:[/bold cyan] {file.relative_path}")

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

    if functions:

        console.print("\n[bold yellow]Functions[/bold yellow]")

        for function in functions:

            console.print(
                f"  • {function.name}({', '.join(function.arguments)})"
            )

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

    chunks = builder.build_chunks(
        file_path=full_path,
        functions=functions,
        classes=classes,
    )

    all_chunks.extend(chunks)

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

generator = EmbeddingGenerator()

embeddings = generator.generate(all_chunks)

console.rule("[bold green]Embeddings[/bold green]")

console.print(
    f"Embedding Shape : {embeddings.shape}"
)

store = FAISSStore()

store.build(
    embeddings,
    all_chunks,
)

store.save(
    settings.FAISS_INDEX_PATH,
    settings.EMBEDDINGS_PATH,
    settings.METADATA_PATH,
    embeddings,
)

console.rule("[bold green]Vector Store[/bold green]")

console.print(
    f"Indexed Chunks : {len(store.metadata)}"
)

console.print(
    f"Embedding Dimension : {embeddings.shape[1]}"
)

console.print(
    f"FAISS Vectors : {store.index.ntotal}"
)

retriever = Retriever(store)
query = "How does repository scanning work?"

results = retriever.retrieve(query)

console.rule("[bold cyan]Retriever[/bold cyan]")

console.print(f"Query : {query}\n")

for chunk, score in results:

    title = chunk.name

    if chunk.parent_class:

        title = f"{chunk.parent_class}.{chunk.name}"

    console.print(
        f"[green]{title}[/green]"
    )

    console.print(
        f"Type : {chunk.chunk_type}"
    )

    console.print(
        f"Distance : {score:.4f}"
    )

    console.print(
        f"File : {chunk.file_path}"
    )

    console.print("-" * 60)

builder = PromptBuilder()

prompt = builder.build(
    question=query,
    chunks=[chunk for chunk, _ in results],
)

console.rule("[bold green]Prompt[/bold green]")

console.print(prompt[:2500])

client = LLMClient()

answer = client.generate(prompt)

console.rule("[bold green]Assistant[/bold green]")

console.print(answer)