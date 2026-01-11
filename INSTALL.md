# Pictoji 1.0 - Installation Guide

## Package Structure

Pictoji v1.0 uses the modern Python packaging standard:
- **pyproject.toml** - PEP 621 compliant configuration
- **setuptools** - Build backend (the most compatible/standard choice)
- **wheel** - Distribution format (standard for PyPI)

## What's Included

- ✅ `pictoji.md` - Complete language specifications (144KB)
- ✅ `pictoji` CLI tool - AI token counter and Unicode analyzer
- ✅ Python library functions for programmatic access

## Installation Methods

### From Source (Development)

```bash
# Install in editable mode
pip install -e .

# Now you can use the CLI
pictoji --help
```

### Build Distribution

```bash
# Install build tool
pip install build

# Build wheel and source distribution
python -m build

# This creates:
# - dist/pictoji-1.0.0-py3-none-any.whl (wheel - standard format)
# - dist/pictoji-1.0.0.tar.gz (source distribution)
```

### Install from Built Wheel

```bash
pip install dist/pictoji-1.0.0-py3-none-any.whl
```

### Upload to PyPI (when ready)

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*
```

## Usage

### As a CLI Tool

```bash
# Token counting
pictoji document.txt
pictoji *.md

# Unicode analysis
pictoji document.txt --unicode-blocks
pictoji *.md --unicode-blocks --spaces
```

### As a Python Library

```python
import pictoji

# Count tokens
text = "Hello, world!"
tokens = pictoji.count_claude_tokens(text)
print(f"Claude tokens: {tokens}")

# Analyze Unicode blocks
pictoji.analyze_unicode_blocks(text)

# Get Unicode block for a character
block = pictoji.get_unicode_block("😀")
print(f"Block: {block}")  # Emoticons
```

### Access the Specs

```python
from pathlib import Path
import pictoji

# Specs are bundled in the package
specs_dir = Path(pictoji.__file__).parent / "specs"
specs_file = specs_dir / "pictoji.md"

with open(specs_file) as f:
    specs = f.read()
    print(f"Loaded {len(specs)} characters of Pictoji specs")
```

## PyScript Compatibility (Future 2.0)

The current structure is PyScript-ready! Once Pictoji is on PyPI:

```html
<py-config>
packages = ["pictoji"]
</py-config>

<py-script>
import pictoji
print(pictoji.__version__)
</py-script>
```

## Verification

Test that everything works:

```bash
# Quick verification
python3 -c "import pictoji; print(f'✓ Pictoji {pictoji.__version__} installed')"

# CLI test
pictoji --help
```

## File Structure

```
pictoji/
├── pyproject.toml          # Modern packaging config (PEP 621)
├── MANIFEST.in             # Include additional files
├── README.md               # Project description
├── LICENSE.txt             # MIT License
├── pictoji.md              # Specs (also in package)
├── dev/                    # Development files (not packaged)
│   ├── pictoji.py          # Original tool
│   └── requirements.txt    # Original requirements
└── src/
    └── pictoji/            # The actual package
        ├── __init__.py     # Package metadata & exports
        ├── cli.py          # CLI tool implementation
        └── specs/
            └── pictoji.md  # Bundled specs
```

## Why This Approach?

1. **Standard**: Uses setuptools (most widely adopted build backend)
2. **Modern**: Uses pyproject.toml (PEP 621 - the new standard)
3. **Compatible**: Wheel format works everywhere
4. **Future-proof**: Structure supports:
   - PyScript (2.0) - just install from PyPI
   - C extensions (3.0) - setuptools supports native code
   - WASM compilation - wheel format is portable

This is the best foundation for your vision!
