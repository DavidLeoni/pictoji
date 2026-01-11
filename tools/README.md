# Pictoji Development Tools (v1.0)

Python development tools for working with Pictoji:
- AI token counter for Claude, GPT, and Gemini models
- Unicode block analyzer

## Installation

```bash
# From the tools/ directory
pip install -e .

# Or with optional AI dependencies
pip install -e ".[ai]"
```

## Usage

### As a CLI Tool

```bash
# Token counting
pictoji document.txt
pictoji file1.txt file2.txt file3.txt
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
claude_tokens = pictoji.count_claude_tokens(text)
gpt_tokens = pictoji.count_gpt_tokens(text)
gemini_tokens = pictoji.count_gemini_tokens(text)

# Analyze Unicode blocks
pictoji.analyze_unicode_blocks(text)

# Get Unicode block for a character
block = pictoji.get_unicode_block("😀")
print(block)  # "Emoticons"
```

## Supported Models

- **Claude 4.5** (Anthropic) - tiktoken estimate
- **GPT-4/GPT-4o/GPT-5** (OpenAI) - accurate tiktoken counting
- **Gemini 2.0 Pro** (Google) - character-based estimate

## Requirements

- Python 3.8+
- tiktoken (for token counting)
- anthropic, google-genai (optional, for AI features)

## License

MIT - See ../LICENSE.txt
