# 🤖 Agentic AI Assistant (Prototype)

> **A modular Agentic AI prototype that demonstrates planning, reasoning, tool selection, function calling, conversation memory, and autonomous tool execution using a local Large Language Model.**

---

# Overview

This project is a lightweight implementation of an **AI Agent** capable of selecting and executing external tools to solve user requests.

Instead of directly answering every prompt, the assistant follows an **agentic workflow**:

- analyzes the user's request
- creates an execution plan
- reasons about the next action
- selects the appropriate tool
- executes the tool
- observes the result
- stores the interaction in memory
- returns the final answer

The project focuses on demonstrating the **core architecture behind modern AI Agents** rather than building a production assistant.

Everything runs locally using **Ollama**, making the project fully offline.

---

# Features

- Modular Agent architecture
- Local LLM integration (Ollama)
- Automatic tool selection
- Tool execution engine
- Execution planning
- Think → Act → Observe reasoning loop
- Conversation memory
- Agent event memory
- Structured JSON function calling
- Rich terminal interface
- Automatic execution reports
- Modular tool registry
- Extensible architecture for adding new tools

---

# Current Tools

### Calculator Tool

Evaluates mathematical expressions.

Examples

- `15 + 6`
- `calculate 18 * 9`
- `that + 5`
- `minus 10`

---

### File Reader Tool

Reads local text files.

Supported formats

- TXT
- Markdown
- CSV

Examples

```
read README.md

open notes.txt

load dataset.csv
```

---

### System Information Tool

Returns information about the current machine.

Includes

- Operating System
- CPU
- RAM
- Python Version
- Working Directory

Example

```
how much ram?

show my system information
```

---

### Directory Tool

Lists folders and files inside a directory.

Example

```
list files

list project folder

show directory contents
```

---

# Agent Workflow

```text
                User
                  │
                  ▼
          User Question
                  │
                  ▼
        Conversation Memory
                  │
                  ▼
          Prompt Builder
                  │
                  ▼
            Local LLM
             (Ollama)
                  │
                  ▼
        Tool Selection Decision
                  │
                  ▼
         Execution Planner
                  │
                  ▼
       Think → Act → Observe
                  │
                  ▼
          Tool Executor
                  │
                  ▼
      Selected External Tool
                  │
                  ▼
          Tool Observation
                  │
                  ▼
          Agent Memory Update
                  │
                  ▼
           Final Response
```

---

# Project Architecture

```text
app.py
│
├── Agent
│
├── Planner
│
├── Prompt Builder
│
├── Conversation Memory
│
├── Reasoning Engine
│       │
│       ├── Think
│       ├── Act
│       └── Observe
│
├── Tool Executor
│
├── Tool Registry
│       │
│       ├── Calculator
│       ├── File Reader
│       ├── System
│       └── Directory
│
├── Local LLM
│
└── Agent State
```

---

# Think → Act → Observe Loop

Every request follows the same reasoning cycle.

## Think

The LLM analyzes

- user request
- available tools
- conversation history

and decides

- which tool to use
- required arguments
- reasoning behind the decision

---

## Act

The selected tool is executed.

Examples

- calculator
- file reader
- system information
- directory listing

---

## Observe

The tool result becomes the new observation.

The observation is

- stored in memory
- returned to the user
- available for future reasoning

---

# Conversation Memory

The assistant stores

- user messages
- assistant responses
- latest observations

This allows follow-up requests such as

```
What is 20 + 5

plus 10

minus 3
```

without repeating the previous expression.

---

# Execution Planning

Before reasoning begins, the Planner creates a lightweight execution plan.

Example

```
Goal

Solve the mathematical calculation.

Steps

1. Analyze request
2. Select Calculator
3. Execute calculation
4. Return answer
```

Different request categories generate different execution plans.

---

# Function Calling

The LLM never directly executes Python code.

Instead, it returns structured JSON describing

- selected tool
- arguments
- reasoning

Example

```json
{
  "tool": "calculator",
  "arguments": {
    "expression": "5 + 8"
  },
  "reason": "The user requested a mathematical calculation."
}
```

The executor then invokes the corresponding Python tool.

---

# Project Structure

```text
17-agentic-ai-assistant/

│
├── app.py
├── config.py
│
├── data/
├── datasets/
├── documents/
├── logs/
├── memory/
├── outputs/
│
├── src/
│   │
│   ├── agent/
│   ├── executor/
│   ├── LLM/
│   ├── memory/
│   ├── planner/
│   ├── prompting/
│   ├── reasoning/
│   ├── tools/
│   ├── utils/
│   └── models/
│
└── README.md
```

---

# Technologies

- Python
- Ollama
- Pydantic
- Rich
- JSON
- Modular Tool Architecture

---

# Learning Objectives

This prototype demonstrates many of the core concepts behind modern AI agents, including:

- Agent architecture
- Planning
- Reasoning loops
- Tool calling
- Function calling
- Structured LLM outputs
- Conversation memory
- Event memory
- Prompt engineering
- Local LLM integration
- Modular software design

---

# Future Improvements

Potential extensions include

- Web search tool
- Semantic search integration (RAG)
- Code execution tool
- Python REPL
- Multi-step planning
- Dynamic replanning
- Multi-tool execution
- Tool result summarization
- Long-term memory
- Vector database integration
- Autonomous task decomposition
- Streaming responses
- Multi-agent collaboration

---

# Example Workflow

```text
User
 │
 ▼
"Read README.md"

 ▼

Planner

 ▼

Execution Plan

 ▼

LLM Decision

 ▼

{
  Tool : file_reader
  filepath : README.md
}

 ▼

Tool Execution

 ▼

File Contents

 ▼

Observation Stored

 ▼

Final Response
```

---

# Project Status

**Prototype Complete**

This project demonstrates the core building blocks of an Agentic AI system, including planning, reasoning, tool orchestration, and memory. It is designed as a learning-focused implementation and a portfolio showcase, providing a modular foundation that can be extended into more advanced autonomous AI systems.