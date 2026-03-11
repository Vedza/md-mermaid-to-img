#!/usr/bin/env python3
"""
Prepares markdown with mermaid diagrams for Confluence and other platforms.

Each mermaid code block is kept for native rendering, and the source code is
added in a collapsible <details> toggle underneath so it stays editable.
Nothing is sent to any external server.

Usage:
    python3 render-mermaid.py <input.md> -c          # output to clipboard
    python3 render-mermaid.py <input.md> [-o out.md]  # output to file
"""

import argparse
import os
import platform
import re
import subprocess
import sys

MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def process_content(content: str) -> str:
    """Add a collapsible source toggle after each mermaid block."""
    blocks = list(MERMAID_BLOCK_RE.finditer(content))
    if not blocks:
        print("No mermaid blocks found.", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(blocks)} mermaid block(s). Adding source toggles...", file=sys.stderr)

    result = content
    for match in reversed(blocks):
        mermaid_code = match.group(1)
        code_stripped = mermaid_code.strip()

        if not code_stripped:
            print("Warning: skipping empty mermaid block.", file=sys.stderr)
            continue

        replacement = (
            f"```mermaid\n{mermaid_code}```\n\n"
            f"<details>\n"
            f"<summary>Diagram source</summary>\n\n"
            f"```\n{code_stripped}\n```\n\n"
            f"</details>"
        )
        result = result[:match.start()] + replacement + result[match.end():]

    return result


def copy_to_clipboard(text: str) -> None:
    """Copy text to system clipboard."""
    system = platform.system()
    if system == "Darwin":
        cmd = ["pbcopy"]
    elif system == "Linux":
        cmd = ["xclip", "-selection", "clipboard"]
    else:
        print("ERROR: Clipboard not supported on this OS. Use -o instead.", file=sys.stderr)
        sys.exit(1)

    subprocess.run(cmd, input=text.encode("utf-8"), check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare markdown with mermaid diagrams for Confluence"
    )
    parser.add_argument("input", help="Input markdown file")

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="Output markdown file (default: <input>-confluence.md)")
    output_group.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard instead of writing a file")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r") as f:
        content = f.read()

    result = process_content(content)

    if args.clipboard:
        copy_to_clipboard(result)
        print("Done. Output copied to clipboard.", file=sys.stderr)
    else:
        output = args.output
        if not output:
            base, ext = os.path.splitext(args.input)
            output = f"{base}-confluence{ext}"
        with open(output, "w") as f:
            f.write(result)
        print(f"Done. Output written to: {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
