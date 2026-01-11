#!/usr/bin/env python3
"""
ㄕICTOji CLI - Development Tools

AI Token Counter:
    Counts tokens for text files across different AI models:
    - Claude (Anthropic)
    - GPT (OpenAI)
    - Gemini (Google)

Unicode Block Analyzer:
    Analyzes Unicode block distribution in text files:
    - Groups characters by Unicode block
    - Shows occurrence counts per block
    - Lists unique characters per block
    - Provides summary statistics
"""

import argparse
import sys
from pathlib import Path
import unicodedata
from collections import defaultdict, Counter


def count_claude_tokens(text: str) -> int:
    """Count tokens using tiktoken as a proxy for Claude's tokenizer."""
    try:
        import tiktoken
        # cl100k_base is used by GPT-4 and is very similar to Claude's tokenizer
        # This provides a good estimate without requiring API calls
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except ImportError:
        print("Warning: tiktoken library not installed. Using character-based estimate.", file=sys.stderr)
        return len(text) // 4
    except Exception as e:
        print(f"Warning: Could not use tiktoken ({e}). Using estimate.", file=sys.stderr)
        return len(text) // 4


def count_gpt_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens using OpenAI's tiktoken."""
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except ImportError:
        print("Warning: tiktoken library not installed. Using character-based estimate.", file=sys.stderr)
        return len(text) // 4
    except Exception as e:
        print(f"Warning: Could not use tiktoken ({e}). Using estimate.", file=sys.stderr)
        return len(text) // 4


def count_gemini_tokens(text: str) -> int:
    """Count tokens for Gemini models."""
    try:
        import google.genai as genai
        # Gemini uses similar tokenization to GPT models
        # Using character-based estimate as Google's SDK token counting
        # requires API key and model initialization

        return len(text) // 4
    except ImportError:
        print("Warning: google-generativeai library not installed. Using estimate.", file=sys.stderr)
        return len(text) // 4


# Unicode block ranges (source: https://www.unicode.org/Public/UNIDATA/Blocks.txt)
UNICODE_BLOCKS = [
    (0x0000, 0x007F, 'ASCII'),
    (0x0080, 0x00FF, 'Latin-1 Supplement'),
    (0x0100, 0x024F, 'Latin Extended'),
    (0x0250, 0x02AF, 'IPA Extensions'),
    (0x0370, 0x03FF, 'Greek'),
    (0x0400, 0x04FF, 'Cyrillic'),
    (0x0530, 0x058F, 'Armenian'),
    (0x0590, 0x05FF, 'Hebrew'),
    (0x0600, 0x06FF, 'Arabic'),
    (0x0900, 0x097F, 'Devanagari'),
    (0x0E00, 0x0E7F, 'Thai'),
    (0x10A0, 0x10FF, 'Georgian'),
    (0x1100, 0x11FF, 'Hangul Jamo'),
    (0x2000, 0x206F, 'General Punctuation'),
    (0x2070, 0x209F, 'Superscripts & Subscripts'),
    (0x20A0, 0x20CF, 'Currency Symbols'),
    (0x2100, 0x214F, 'Letterlike Symbols'),
    (0x2190, 0x21FF, 'Arrows'),
    (0x2200, 0x22FF, 'Mathematical Operators'),
    (0x2300, 0x23FF, 'Miscellaneous Technical'),
    (0x2460, 0x24FF, 'Enclosed Alphanumerics'),
    (0x2500, 0x257F, 'Box Drawing'),
    (0x2580, 0x259F, 'Block Elements'),
    (0x25A0, 0x25FF, 'Geometric Shapes'),
    (0x2600, 0x26FF, 'Miscellaneous Symbols'),
    (0x2700, 0x27BF, 'Dingbats'),
    (0x27C0, 0x27EF, 'Miscellaneous Mathematical Symbols-A'),
    (0x2980, 0x29FF, 'Miscellaneous Mathematical Symbols-B'),
    (0x2A00, 0x2AFF, 'Supplemental Mathematical Operators'),
    (0x3040, 0x309F, 'Hiragana'),
    (0x30A0, 0x30FF, 'Katakana'),
    (0x3100, 0x312F, 'Bopomofo'),
    (0x3130, 0x318F, 'Hangul Compatibility Jamo'),
    (0x3200, 0x32FF, 'Enclosed CJK Letters & Months'),
    (0x4E00, 0x9FFF, 'CJK Unified Ideographs'),
    (0xAC00, 0xD7AF, 'Hangul Syllables'),
    (0xFE30, 0xFE4F, 'CJK Compatibility Forms'),
    (0xFF00, 0xFFEF, 'Halfwidth & Fullwidth Forms'),
    (0x1F300, 0x1F5FF, 'Miscellaneous Symbols & Pictographs'),
    (0x1F600, 0x1F64F, 'Emoticons'),
    (0x1F680, 0x1F6FF, 'Transport & Map Symbols'),
    (0x1F700, 0x1F77F, 'Alchemical Symbols'),
    (0x1F780, 0x1F7FF, 'Geometric Shapes Extended'),
    (0x1F800, 0x1F8FF, 'Supplemental Arrows-C'),
    (0x1F900, 0x1F9FF, 'Supplemental Symbols & Pictographs'),
    (0x1FA00, 0x1FA6F, 'Chess Symbols'),
    (0x1FA70, 0x1FAFF, 'Symbols & Pictographs Extended-A'),
]


def get_unicode_block(char: str) -> str:
    """Get the Unicode block for a character using code point ranges."""
    code = ord(char)

    # Special handling for whitespace and control chars
    category = unicodedata.category(char)
    if category == 'Zs':
        return 'Whitespace'
    elif category in ('Cc', 'Cf'):
        return 'Control Characters'

    # Find matching block from ranges
    for start, end, name in UNICODE_BLOCKS:
        if start <= code <= end:
            return name

    # Unknown block
    return f'Other (U+{code:04X})'


def read_file(filepath: Path) -> str:
    """Read text from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def format_number(num: int) -> str:
    """Format number with thousand separators."""
    return f"{num:,}"


def analyze_unicode_blocks(text: str, verbose: bool = False, space : bool = True):
    """Analyze and display Unicode block distribution in text."""

    # Count characters by block
    block_chars = defaultdict(set)
    block_counts = Counter()

    for char in text:
        if char not in '\n\r☐⍰◻️⧠':
            block = get_unicode_block(char)
            block_chars[block].add(char)
            block_counts[block] += 1


    sorted_blocks = sorted(block_chars.items(), key=lambda x: len(x[1]), reverse=True)
    print(f'{sorted_blocks}=')

    print("=" * 70)
    print("UNICODE BLOCK ANALYSIS")
    print("=" * 70)
    print()

    total_unique_chars = 0

    for block, cs in sorted_blocks:
        count = len(cs)
        unique_chars = len(block_chars[block])
        total_unique_chars += unique_chars

        chars_sorted = sorted(block_chars[block], key=ord)

        chars_display = (' ' if space else '').join(chars_sorted)

        print(f"{block}={format_number(unique_chars)}, occ={format_number(count)} : {chars_display}")

        if space:
            print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("-" * 70)
    print(f"Total Unicode Blocks: {format_number(len(sorted_blocks))}")
    print(f"Total Unique Characters: {format_number(total_unique_chars)}")
    print()


def analyze_files(filepaths: list[Path], verbose: bool = False):
    """Analyze token counts for given files."""

    print("=" * 70)
    print("ㄕICTOji DEV - AI TOKEN COUNTER")
    print("=" * 70)
    print()

    total_chars = 0
    total_claude = 0
    total_gpt4 = 0
    total_gpt5 = 0
    total_gemini = 0

    for filepath in filepaths:
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            continue

        print(f"📄 File: {filepath.name}")
        print("-" * 70)

        text = read_file(filepath)
        char_count = len(text)

        # Count tokens for each model
        claude_tokens = count_claude_tokens(text)
        gpt4_tokens = count_gpt_tokens(text, "gpt-4")
        gpt5_tokens = count_gpt_tokens(text, "gpt-5")
        gemini_tokens = count_gemini_tokens(text)

        # Display results
        print(f"Characters:        {format_number(char_count)}")
        print(f"Claude 4.5:        {format_number(claude_tokens)} tokens (tiktoken estimate)")
        print(f"GPT-4/GPT-4o:      {format_number(gpt4_tokens)} tokens")
        print(f"GPT-5:             {format_number(gpt5_tokens)} tokens")
        print(f"Gemini 2.0 Pro:    {format_number(gemini_tokens)} tokens (estimate)")

        if verbose:
            print(f"\nFirst 100 characters:")
            print(f"  {text[:100]}...")

        print()

        # Add to totals
        total_chars += char_count
        total_claude += claude_tokens
        total_gpt4 += gpt4_tokens
        total_gpt5 += gpt5_tokens
        total_gemini += gemini_tokens

    # Show totals if multiple files
    if len(filepaths) > 1:
        print("=" * 70)
        print("TOTALS")
        print("-" * 70)
        print(f"Total Characters:  {format_number(total_chars)}")
        print(f"Claude 4.5:        {format_number(total_claude)} tokens (tiktoken estimate)")
        print(f"GPT-4/GPT-4o:      {format_number(total_gpt4)} tokens")
        print(f"GPT-5:             {format_number(total_gpt5)} tokens")
        print(f"Gemini 2.0 Pro:    {format_number(total_gemini)} tokens (estimate)")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="ㄕICTOji development tools for token counting and Unicode analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.txt
  %(prog)s file1.txt file2.txt file3.txt
  %(prog)s *.txt --verbose
  %(prog)s document.txt --unicode-blocks
  %(prog)s *.md --unicode-blocks --verbose

Supported Models (Token Counter):
  - Claude 4.5 (Anthropic)
  - GPT-4/GPT-4o (OpenAI)
  - GPT-5 (OpenAI)
  - Gemini 2.0 Pro (Google)

Note: Install required libraries for accurate counting:
  pip install tiktoken
        """
    )

    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Text file(s) to analyze'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show verbose output including text preview and character lists'
    )

    parser.add_argument(
        '-u', '--unicode-blocks',
        action='store_true',
        help='Analyze Unicode block distribution in files'
    )

    parser.add_argument(
        '-s','--spaces',
        action='store_true',
        help='show a space and a return carriage between characters'
    )

    args = parser.parse_args()

    if args.unicode_blocks:
        # Unicode block analysis mode
        for filepath in args.files:
            if not filepath.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                continue

            print(f"📄 File: {filepath.name}")
            print()

            text = read_file(filepath)
            analyze_unicode_blocks(text, args.verbose, args.spaces)

            if len(args.files) > 1:
                print("\n" + "=" * 70 + "\n")
    else:
        # Token counting mode (original functionality)
        analyze_files(args.files, args.verbose)


if __name__ == "__main__":
    main()


# Export public API
__all__ = [
    "count_claude_tokens",
    "count_gpt_tokens",
    "count_gemini_tokens",
    "analyze_unicode_blocks",
    "get_unicode_block",
    "main",
]
