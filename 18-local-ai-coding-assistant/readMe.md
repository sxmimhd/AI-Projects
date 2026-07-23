# 🤖 Local AI Coding Assistant (Prototype)

> **A modular Local AI Coding Assistant that understands Python repositories using AST parsing, semantic code embeddings, FAISS vector search, Retrieval-Augmented Generation (Code RAG), and a local Qwen2.5-Coder language model.**

---

## 🚀 Overview

This project demonstrates how modern AI coding assistants such as **Cursor**, **GitHub Copilot Chat**, **Claude Code**, and **Continue.dev** work internally.

Instead of sending an entire repository to a language model, the assistant:

- Scans a Python project
- Parses its source code using Python AST
- Extracts classes, methods and functions
- Converts code into semantic embeddings
- Indexes everything with FAISS
- Retrieves only the most relevant code
- Builds a context-aware prompt
- Generates repository-aware answers using a local LLM

Everything runs **locally**, making the assistant fast, private and completely offline after the embedding model is downloaded.

---

# ✨ Features

- Repository scanning
- Python AST parsing
- Function extraction
- Class extraction
- Method extraction
- Import extraction
- Semantic code chunking
- Code embeddings using Sentence Transformers
- FAISS vector database
- Semantic repository search
- Retrieval-Augmented Generation (Code RAG)
- Interactive developer chat
- Local Qwen2.5-Coder integration
- Repository statistics
- Rich terminal interface

---

# 🏗️ Architecture

```text
                    Python Repository
                            │
                            ▼
                 Repository Scanner
                            │
                            ▼
                     Python AST Parser
                            │
                            ▼
        Functions • Classes • Methods • Imports
                            │
                            ▼
                    Semantic Chunk Builder
                            │
                            ▼
                  Sentence Transformer
                            │
                            ▼
                     Vector Embeddings
                            │
                            ▼
                       FAISS Vector DB
                            │
                            ▼
                  Semantic Code Retriever
                            │
                            ▼
                      Prompt Builder
                            │
                            ▼
                    Qwen2.5-Coder (Local)
                            │
                            ▼
                     Repository Answers
```

---

# 🧠 Code RAG Pipeline

Unlike a traditional document RAG system, this project indexes source code.

```text
Python Repository

        │

        ▼

Repository Scanner

        │

        ▼

AST Parser

        │

        ▼

Classes
Functions
Methods

        │

        ▼

Semantic Code Chunks

        │

        ▼

Sentence Embeddings

        │

        ▼

FAISS

        │

        ▼

Top-K Relevant Code

        │

        ▼

Prompt Builder

        │

        ▼

Qwen2.5-Coder

        │

        ▼

Repository-Aware Response
```

---

# 📂 Project Structure

```text
18-local-ai-coding-assistant/
│
├── app.py
├── config.py
├── requirements.txt
│
├── models/
│   ├── embeddings.npy
│   ├── faiss.index
│   └── metadata.pkl
│
│
└── src/
    ├── chunks/
    │     chunk_builder.py
    │
    ├── embeddings/
    │     embedding_generator.py
    │
    ├── llm/
    │     client.py
    │
    ├── parser/
    │     ast_parser.py
    │
    ├── prompting/
    │     prompt_builder.py
    │
    ├── retriever/
    │     retriever.py
    │
    ├── scanner/
    │     repository_scanner.py
    │
    └── vectorstore/
          faiss_store.py
```

---

# ⚙️ System Workflow

```text
Scan Repository
        │
        ▼
Analyze Python Files
        │
        ▼
Extract AST Nodes
        │
        ▼
Build Semantic Chunks
        │
        ▼
Generate Embeddings
        │
        ▼
Create FAISS Index
        │
        ▼
Wait For User Query
        │
        ▼
Retrieve Similar Code
        │
        ▼
Build Prompt
        │
        ▼
Generate Answer
```

---

# 📚 Modules

## Repository Scanner

Scans the repository and collects:

- Supported source files
- Line counts
- File sizes
- Repository statistics

Supported extensions include:

- Python
- Markdown
- Text
- JSON
- YAML
- TOML

Ignored directories include:

- `.git`
- `.venv`
- `__pycache__`
- `build`
- `dist`
- `models`
- `outputs`

---

## AST Parser

Uses Python's built-in `ast` module to understand the repository structure.

Extracts:

- Classes
- Methods
- Functions
- Imports
- Docstrings
- Line numbers

No regular expressions are used.

---

## Chunk Builder

Instead of splitting text every few hundred characters like traditional RAG systems, code is chunked by its logical structure.

Chunks include:

- Classes
- Methods
- Functions

Each chunk stores metadata including:

- File path
- Name
- Parent class
- Start line
- End line
- Source code

---

## Embedding Generator

Every code chunk is transformed into a semantic vector using:

- Sentence Transformers
- all-MiniLM-L6-v2

Each embedding contains **384 dimensions**.

---

## Vector Store

Embeddings are indexed using **FAISS**.

Stored artifacts include:

- `embeddings.npy`
- `faiss.index`
- `metadata.pkl`

This enables extremely fast semantic code retrieval.

---

## Retriever

Given a developer question, the retriever:

- embeds the query
- searches FAISS
- returns the most relevant code chunks
- ranks them by similarity

Only those chunks are passed to the language model.

---

## Prompt Builder

Constructs repository-aware prompts.

Template:

```text
You are an expert Python software engineer.

Repository Context:
...

User Question:
...

Answer:
```

This significantly reduces hallucinations.

---

## Local LLM

Uses:

- Ollama
- Qwen2.5-Coder

The model never receives the entire repository.

Only the retrieved code is included.

---

# 💬 Example Questions

The assistant can answer questions like:

```text
Explain RepositoryScanner

How does AST parsing work?

Where are embeddings generated?

Explain build_chunks()

How is FAISS used?

What does PromptBuilder do?

Where is semantic retrieval implemented?

Explain this repository.

Generate documentation.

Find duplicated code.

Suggest improvements.

Refactor this class.

Create unit tests.
```

---

# 🧩 Repository Context

Modern coding assistants rarely send an entire project to the language model.

Instead they retrieve only the most relevant code.

```text
User Question
        │
        ▼
Semantic Search
        │
        ▼
Top-K Code Chunks
        │
        ▼
Prompt
        │
        ▼
LLM
        │
        ▼
Answer
```

This approach:

- reduces hallucinations
- lowers token usage
- improves accuracy
- scales to very large repositories

---

# 📊 Outputs

## Models

```
embeddings.npy
faiss.index
metadata.pkl
```

---

## Reports

Repository statistics

Chunk statistics

Embedding statistics

Retrieval examples

Generated answers

---

## Figures

Repository overview

Project tree

Repository statistics

Chunk distribution

Function length distribution

Class distribution

Embedding PCA

Embedding t-SNE

Similarity heatmap

Repository dependency graph

---

# 🛠️ Technologies

- Python
- AST
- Sentence Transformers
- FAISS
- Ollama
- Qwen2.5-Coder
- Rich
- NumPy
- Pandas
- Scikit-learn
- Matplotlib

---

# 🎯 Learning Outcomes

This project demonstrates:

- Repository indexing
- Static code analysis
- Python AST parsing
- Semantic code chunking
- Code embeddings
- Vector databases
- Semantic retrieval
- Retrieval-Augmented Generation
- Prompt engineering
- Context management
- Local LLM development
- AI coding assistant architecture

---

# 🚀 Future Improvements

- Multi-language support
- Incremental indexing
- Git integration
- Automatic README generation
- Unit test generation
- Code refactoring suggestions
- Streaming LLM responses
- VS Code extension
- Cursor-style inline edits
- Dependency graph visualization
- Multi-file reasoning
- Tool-calling agent integration

---

# ✅ Project Status

**Prototype Completed**

This project successfully implements the core architecture of a modern local AI coding assistant by combining **repository analysis**, **AST parsing**, **semantic code embeddings**, **FAISS vector search**, **Retrieval-Augmented Generation**, and a **local Qwen2.5-Coder model** to provide accurate, repository-aware assistance while keeping all processing local.