Stuff in this folder is only for development purposes, may collect old stuff and MUST be ignored by AI parsers.


## pictoji.py

Python tools for Pictoji project management

NOTE: Python tools are only needed for Pictoji development, if you instead just want to use Pictoji simply copy-paste [pictoji.md](../pictoji.md) in your favorite AI chatbot.


Dev features:

Currently not much:

- unicode chars statistics
- token counts

## Installation

```bash
pip install -e .           # Base
pip install -e ".[cli]"    # With CLI deps (for basic 1.0)
```
<!-- pip install -e ".[all]"    # Everything  (future)  -->

## Usage

### Basic Usage

Count tokens in a single file:
```bash
python pictoji.py document.txt
```

### Multiple Files

Count tokens across multiple files:
```bash
python pictoji.py file1.txt file2.txt file3.txt
```

Use wildcards:
```bash
python pictoji.py *.txt
```

### Verbose Mode

Show text preview:
```bash
python pictoji.py document.txt --verbose
```

## Supported Models

- **Claude 4.5** (Anthropic) - Uses Anthropic's official tokenizer
- **GPT-5/GPT-4/GPT-4o** (OpenAI) - Uses tiktoken for accurate counting
- **Gemini 2.0 Pro** (Google) - Character-based estimate

## Roadmap

- 0.x natural language vs algebra exploration
- 1.0 (Will happen)
    - hopefully rigorous core algebra
    - proper testing
    - main unicode issues identified
        - stable set of core characters
        - most issues fixed or workaround found 
    - python tools packaging
    - github actions 
- 2.0 (Could happen) something on the web with Pyscript
- 3.0 (Wonderland) High performance GraphBLAS C Pictoji interpreter/compiler with Python bindings, WASM target, semantic engine with wikidata ingestion, and what not..
