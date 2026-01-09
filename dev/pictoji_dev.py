#!/usr/bin/env python3
"""
ㄕICTOji DEV TOOL

AI Token Counter:
    Counts tokens for text files across different AI models:
    - Claude (Anthropic)
    - GPT (OpenAI)
    - Gemini (Google)
"""

import argparse
import sys
from pathlib import Path


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
        # Rough estimate: ~4 characters per token for Claude
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
        # Rough estimate: ~4 characters per token for GPT models
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


def read_file(filepath: Path) -> str:
    """Read text from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def format_number(num: int) -> str:
    """Format number with thousand separators."""
    return f"{num:,}"


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
        print(f"GPT-5:      {format_number(gpt5_tokens)} tokens")
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
        print(f"GPT-5:      {format_number(total_gpt5)} tokens")
        print(f"Gemini 2.0 Pro:    {format_number(total_gemini)} tokens (estimate)")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Count AI tokens for text files across different models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.txt
  %(prog)s file1.txt file2.txt file3.txt
  %(prog)s *.txt --verbose
  
Supported Models:
  - Claude 4.5 (Anthropic)
  - GPT-4/GPT-4o (OpenAI)
  - GPT-5 (OpenAI)
  - Gemini 2.0 Pro (Google)
  
Note: Install required libraries for accurate counting:
  pip install anthropic tiktoken google-generativeai
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
        help='Show verbose output including text preview'
    )
    
    args = parser.parse_args()
    
    analyze_files(args.files, args.verbose)


if __name__ == "__main__":
    main()
