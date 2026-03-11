# md-mermaid-to-img

Prepares Markdown files containing ` ```mermaid ` code blocks for Confluence and other platforms. Mermaid source code is preserved as-is so diagrams render natively on the destination platform while the code remains editable.

Nothing is sent to any external server. No image conversion, no static assets.

## Prerequisites

- Python 3.8+
- A Mermaid-capable renderer on the destination platform (e.g., Confluence with a Mermaid plugin, GitHub, GitLab)

## Usage

### Copy to clipboard

```bash
python3 render-mermaid.py my-doc.md -c
```

### Write to file

```bash
# Default output: my-doc-confluence.md
python3 render-mermaid.py my-doc.md

# Custom output path
python3 render-mermaid.py my-doc.md -o output.md
```

## Shell alias

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias md2img='python3 ~/path/to/md-mermaid-to-img/render-mermaid.py'
```

Then:

```bash
md2img my-rfc.md -c   # validate + copy to clipboard
```

## How it works

1. Finds all ` ```mermaid ` code blocks in the input
2. Validates that blocks are non-empty
3. Preserves the mermaid source code in the output (no conversion to images or URLs)
4. Outputs to clipboard (`-c`) or file (`-o`)

The destination platform handles rendering. On Confluence, this requires a Mermaid plugin (e.g., Mermaid Chart, Mermaid Diagrams for Confluence). On GitHub and GitLab, mermaid blocks render natively.

## Why keep the source code?

- Edit diagrams later without recreating them from scratch
- Use existing diagrams as templates for new ones
- Code and visualization live in the same document
- No dependency on external rendering services
