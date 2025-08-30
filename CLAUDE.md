# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project aimed at implementing a ChatGPT-style deep research functionality. The system should accept questions, perform iterative searches, display the research process, and provide comprehensive summaries.

## Architecture

The project references three key components:

1. **LLM Integration** (`llm.py`) - Custom LLM API client using a gateway service
2. **Agent Workflow** (`search_help.html`) - DeepSeek's deepresearcher implementation showing multi-step search agent patterns
3. **Paper Search** (`arixv_search_tool.html`) - ArXiv MCP server for academic paper retrieval

## Key Components

### LLM Module (`llm.py`)
- Uses custom gateway at `http://llm-gateway.jiunile.com/`
- Supports multiple models (gpt-4o, claude, gemini)
- Implements Bearer token authentication
- Auto-detects correct API endpoints from multiple paths

### Reference Implementations
- **Agent Pattern**: Multi-step search with iterative refinement (from `search_help.html`)
- **Citation Format**: Uses `[citation:x]` format for webpage references
- **Search Strategy**: Generates up to 5 parallel search queries, uses keyword optimization
- **Paper Integration**: ArXiv MCP server for academic research capabilities

## Development Commands

**Note**: This project doesn't have standard package managers or build tools. Development appears to be direct Python script execution.

### Running the LLM Client
```bash
python llm.py
```

## Project Goal

Build a deep research system that:
1. Accepts user questions
2. Performs iterative searches when information is insufficient
3. Shows the research process step-by-step
4. Provides final comprehensive summaries
5. References the workflow patterns from `search_help.html`

## Security Note

The `llm.py` file contains hardcoded API keys. In production, these should be moved to environment variables or secure configuration files.