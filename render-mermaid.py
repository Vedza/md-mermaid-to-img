#!/usr/bin/env python3
"""
Replaces ```mermaid blocks in a markdown file with mermaid.ink image URLs
that render on the fly. No Docker, no local rendering — just URLs.

Usage:
    python3 render-mermaid.py <input.md> -c          # output to clipboard
    python3 render-mermaid.py <input.md> [-o out.md]  # output to file

If neither -o nor -c is specified, outputs to <input>-confluence.md
"""

import argparse
import base64
import os
import platform
import re
import subprocess
import sys

MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def mermaid_to_ink_url(mermaid_code: str) -> str:
    """Convert mermaid source to a mermaid.ink PNG URL."""
    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    return f"https://mermaid.ink/img/{encoded}"


def render_all(content: str) -> str:
    """Replace all mermaid blocks with mermaid.ink image markdown."""
    blocks = list(MERMAID_BLOCK_RE.finditer(content))
    if not blocks:
        print("No mermaid blocks found.", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(blocks)} mermaid block(s). Converting...", file=sys.stderr)

    result = content
    for i, match in enumerate(reversed(blocks)):
        mermaid_code = match.group(1)
        url = mermaid_to_ink_url(mermaid_code)
        img_md = f"![diagram]({url})"
        result = result[:match.start()] + img_md + result[match.end():]
        print(f"  Converted diagram {len(blocks) - i}/{len(blocks)}", file=sys.stderr)

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
        description="Render mermaid blocks in markdown to mermaid.ink image URLs"
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

    result = render_all(content)

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
