#!/usr/bin/env python3
"""
Renders mermaid diagrams locally and prepares markdown for Confluence and
other platforms. Each diagram is rendered to SVG via mermaid-cli (mmdc), and
the source code is added in a collapsible <details> toggle underneath.

Nothing is sent to any external server.

Usage:
    python3 render-mermaid.py <input.md> -c          # output to clipboard
    python3 render-mermaid.py <input.md> [-o out.md]  # output to file
"""

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def check_mmdc():
    """Check that mermaid-cli (mmdc) is installed."""
    if shutil.which("mmdc") is None:
        print(
            "Error: mmdc not found. Install mermaid-cli:\n"
            "  npm install -g @mermaid-js/mermaid-cli",
            file=sys.stderr,
        )
        sys.exit(1)


def render_mermaid_to_svg(mermaid_code: str) -> str:
    """Render mermaid code to SVG using mmdc. Returns SVG content."""
    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, "diagram.mmd")
        output_path = os.path.join(tmp, "diagram.svg")

        with open(input_path, "w") as f:
            f.write(mermaid_code)

        result = subprocess.run(
            ["mmdc", "-i", input_path, "-o", output_path, "-b", "transparent"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"mmdc error: {result.stderr.strip()}", file=sys.stderr)
            return None

        with open(output_path, "r") as f:
            return f.read()


def process_content(content: str, diagrams_dir: str | None) -> str:
    """Render mermaid blocks to SVG and add source toggles."""
    blocks = list(MERMAID_BLOCK_RE.finditer(content))
    if not blocks:
        print("No mermaid blocks found.", file=sys.stderr)
        sys.exit(0)

    use_inline = diagrams_dir is None
    if not use_inline:
        os.makedirs(diagrams_dir, exist_ok=True)

    print(f"Found {len(blocks)} mermaid block(s). Rendering locally...", file=sys.stderr)

    result = content
    total = len(blocks)
    for idx, match in enumerate(reversed(blocks)):
        diagram_num = total - idx
        mermaid_code = match.group(1)
        code_stripped = mermaid_code.strip()

        if not code_stripped:
            print(f"  Skipping empty block {diagram_num}/{total}", file=sys.stderr)
            continue

        svg = render_mermaid_to_svg(code_stripped)
        if svg is None:
            print(f"  Failed to render block {diagram_num}/{total}, keeping as code block", file=sys.stderr)
            continue

        if use_inline:
            img_part = svg
        else:
            svg_filename = f"diagram-{diagram_num}.svg"
            svg_path = os.path.join(diagrams_dir, svg_filename)
            with open(svg_path, "w") as f:
                f.write(svg)
            rel_path = os.path.join("diagrams", svg_filename)
            img_part = f"![diagram]({rel_path})"

        replacement = (
            f"{img_part}\n\n"
            f"<details>\n"
            f"<summary>Diagram source</summary>\n\n"
            f"```mermaid\n{code_stripped}\n```\n\n"
            f"</details>"
        )
        result = result[:match.start()] + replacement + result[match.end():]
        print(f"  Rendered diagram {diagram_num}/{total}", file=sys.stderr)

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
        description="Render mermaid diagrams locally and prepare markdown for Confluence"
    )
    parser.add_argument("input", help="Input markdown file")

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="Output markdown file (default: <input>-confluence.md)")
    output_group.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard instead of writing a file")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    check_mmdc()

    with open(args.input, "r") as f:
        content = f.read()

    if args.clipboard:
        # Clipboard mode: inline SVG directly in the markdown
        result = process_content(content, diagrams_dir=None)
        copy_to_clipboard(result)
        print("Done. Output copied to clipboard.", file=sys.stderr)
    else:
        output = args.output
        if not output:
            base, ext = os.path.splitext(args.input)
            output = f"{base}-confluence{ext}"
        output_dir = os.path.dirname(os.path.abspath(output))
        diagrams_dir = os.path.join(output_dir, "diagrams")
        result = process_content(content, diagrams_dir=diagrams_dir)
        with open(output, "w") as f:
            f.write(result)
        print(f"Done. Output written to: {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
