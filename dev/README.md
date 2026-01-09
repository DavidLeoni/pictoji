Stuff in this folder is only for development purposes, may collect old stuff and MUST be ignored by AI parsers.


## pictoji_dev.py

Python tools for Pictoji project management.

## Installation

```bash
pip install -r requirements.txt
```
**Note:** The AI Token Counter will work without these libraries installed, but will use character-based estimates instead of precise token counts.

## AI Token Counter

Count tokens in text files for different AI models: Claude 4.5, GPT-4, and Gemini 2.0 Pro.

## Usage

### Basic Usage

Count tokens in a single file:
```bash
python pictoji_dev.py document.txt
```

### Multiple Files

Count tokens across multiple files:
```bash
python token_counter.py file1.txt file2.txt file3.txt
```

Use wildcards:
```bash
python token_counter.py *.txt
```

### Verbose Mode

Show text preview:
```bash
python token_counter.py document.txt --verbose
```

## Example Output

```
======================================================================
AI TOKEN COUNTER
======================================================================

📄 File: sample.txt
----------------------------------------------------------------------
Characters:        1,234
Claude 4.5:        298 tokens
GPT-4/GPT-4o:      312 tokens
Gemini 2.0 Pro:    308 tokens (estimate)

======================================================================
```

## Supported Models

- **Claude 4.5** (Anthropic) - Uses Anthropic's official tokenizer
- **GPT-4/GPT-4o** (OpenAI) - Uses tiktoken for accurate counting
- **Gemini 2.0 Pro** (Google) - Character-based estimate

## Notes

- For Claude token counting, no API key is needed for the `anthropic` library's token counter
- For GPT models, `tiktoken` provides accurate offline token counting
- Gemini token counts are estimates based on character length
- The tool handles both UTF-8 and Latin-1 encoded files

## License

Free to use and modify.