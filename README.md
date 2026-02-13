# md-mermaid-to-img

Replaces ` ```mermaid ` code blocks in Markdown files with rendered image URLs via [mermaid.ink](https://mermaid.ink). The output is standard Markdown with `![diagram](url)` references that any Markdown renderer (Confluence, Notion, GitHub, etc.) will display as images.

No Docker, no local rendering, no image files to upload — just URLs.

## Prerequisites

- Python 3.8+

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
md2img my-rfc.md -c   # convert + copy to clipboard
```

## How it works

1. Finds all ` ```mermaid ` code blocks in the input
2. Base64-encodes each diagram into a `https://mermaid.ink/img/...` URL
3. Replaces each block with `![diagram](url)` Markdown
4. Outputs to clipboard (`-c`) or file (`-o`)

mermaid.ink renders the diagram server-side when the image URL is loaded. No assets to manage.
