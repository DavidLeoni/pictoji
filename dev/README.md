Stuff in this folder is only for development purposes, may collect old stuff and MUST be ignored by AI parsers.


## pictoji.py

Python tools for Pictoji project management

NOTE: Python tools are only needed for Pictoji development, if you instead just want to use Pictoji simply copy-paste [pictoji.md](../pictoji.md) in your favorite AI chatbot.

Dev features:

Currently not much:

- unicode chars statistics
- token counts

Continuous integration reports:  https://DavidLeoni.github.io/pictoji/ci/


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


## Dev workflow

Although we use Github extensively, workflows should be independent of it as much as possible. 

Developing occurs in dev branch
    - pyproject.toml is the single source of truth for versioning 
    - dev files version labels (including the one in pyproject.toml) MUST be marked as PICTOJI-vx.y.z+1-DEV where z+1 is the bump of the last published version

To release, a developer with write privileges to main branch locally runs a python script dev/release.py which takes as input:
    1. a version tag in the format vx.y.z[-DESC] (DESC is optional)
    2. (optional) a version tag of the next bump, if not provided assume vx.y.z+1-DEV

Steps sketch:
- verify tags format is valid, if not communicate the proper one
- Install dependencies:
    python -m pip install --upgrade pip
    pip install -e ".[cli]"
- git checkout dev branch
- stamp the version *only* of the files marked for inclusion in pyproject.toml (and pyproject.toml itself), replacing the pattern PICTOJI-vx.y.z[-DESC]  with the version tag
- Run pictoji CLI on pictoji.md
    echo "🔍 Running pictoji CLI analysis on pictoji.md..."
    pictoji pictoji.md > report.txt 2>&1 || true
    echo "✅ Report generated"
    cat report.txt
- commit, tags with version 
- push tag to origin triage branch (can do it while remaining in dev branch)
- while still in dev branch, bump version to vx.y.z+1-DEV, stamping the version *only* of the files marked for inclusion in pyproject.toml (and pyproject.toml itself), replacing the pattern PICTOJI-vx.y.z[-DESC]  with the bumped version tag
- commit to dev branch
- push to origin dev branch

        
Desiderata:
- find the best python console management tool
- git commands in the python script should still look as much as possible as regular bash ones
- all written files to be UTF-8 with BOM