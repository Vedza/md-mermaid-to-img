# md-mermaid-to-img

Renders ` ```mermaid ` code blocks locally to SVG using [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) and prepares the markdown for Confluence and other platforms. Each rendered diagram is followed by a collapsible toggle containing the source code for easy editing and reuse.

Nothing is sent to any external server. All rendering happens on your machine.

## Prerequisites

- Python 3.8+
- Node.js with mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`

## Usage

### Copy to clipboard

Inlines the SVG directly in the markdown (no files to manage):

```bash
python3 render-mermaid.py my-doc.md -c
```

### Write to file

Saves SVGs to a `diagrams/` directory next to the output file:

```bash
# Default output: my-doc-confluence.md + diagrams/
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
md2img my-rfc.md -c   # render + copy to clipboard
```

## How it works

1. Finds all ` ```mermaid ` code blocks in the input
2. Renders each diagram to SVG locally via `mmdc`
3. Replaces each block with the rendered SVG + a collapsible source toggle
4. Outputs to clipboard (`-c`) with inline SVGs, or to file (`-o`) with SVG files in `diagrams/`

## Output format

Each mermaid block becomes:

- The rendered SVG diagram (inline or as a file reference)
- A `<details>` toggle containing the original mermaid source code

This way the visualization is always visible, and the code is one click away for editing or reuse as a template.
