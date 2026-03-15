#!/usr/bin/env python3
"""
ipynb2py: Convert between Jupyter notebooks (.ipynb) and Python scripts (.py)

Conversion rules:
  ipynb -> py: Markdown cells are commented with '# ' prefix per line.
               Code cells are kept as-is.
  py -> ipynb: Lines starting with '# ' become markdown cells.
               Other lines become code cells.
"""
import argparse
import json
import os
import sys


def ipynb_to_py(ipynb_path, output_path=None):
    """
    Convert a Jupyter notebook (.ipynb) to a Python script (.py).

    Markdown cells are converted to comments with '# ' prefix.
    Code cells are kept as-is.
    Cells are separated by a blank line.
    """
    if not os.path.exists(ipynb_path):
        raise FileNotFoundError(f"Input file not found: {ipynb_path}")

    if output_path is None:
        base, _ = os.path.splitext(ipynb_path)
        output_path = base + '.py'

    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    lines = []
    cells = notebook.get('cells', [])

    for i, cell in enumerate(cells):
        cell_type = cell.get('cell_type', 'code')
        source = cell.get('source', [])

        # source can be a list of strings or a single string
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source

        if not source_text:
            continue

        if cell_type == 'markdown':
            # Prefix each line with '# '
            for line in source_text.split('\n'):
                lines.append('# ' + line)
        else:
            # Code cell: keep as-is
            lines.append(source_text)

        # Add blank line between cells
        if i < len(cells) - 1:
            lines.append('')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Converted: {ipynb_path} -> {output_path}")
    return output_path


def py_to_ipynb(py_path, output_path=None):
    """
    Convert a Python script (.py) to a Jupyter notebook (.ipynb).

    Lines starting with '# ' become markdown cells (the '# ' prefix is stripped).
    Other lines become code cells.
    Consecutive lines of the same type are grouped into one cell.
    """
    if not os.path.exists(py_path):
        raise FileNotFoundError(f"Input file not found: {py_path}")

    if output_path is None:
        base, _ = os.path.splitext(py_path)
        output_path = base + '.ipynb'

    with open(py_path, 'r', encoding='utf-8') as f:
        content = f.read()

    source_lines = content.split('\n')

    # Remove trailing empty line if present
    if source_lines and source_lines[-1] == '':
        source_lines = source_lines[:-1]

    cells = []
    current_type = None  # 'markdown' or 'code'
    current_lines = []

    def flush_cell():
        nonlocal current_type, current_lines
        if current_lines is None or current_type is None:
            return
        # Remove trailing empty lines from the cell
        while current_lines and current_lines[-1] == '':
            current_lines.pop()
        if not current_lines:
            current_type = None
            current_lines = []
            return
        source_text = '\n'.join(current_lines)
        cell = {
            'cell_type': current_type,
            'metadata': {},
            'source': source_text,
        }
        if current_type == 'code':
            cell['execution_count'] = None
            cell['outputs'] = []
        cells.append(cell)
        current_type = None
        current_lines = []

    for line in source_lines:
        if line.startswith('# '):
            # Markdown line - strip the '# ' prefix
            md_line = line[2:]
            if current_type == 'markdown':
                current_lines.append(md_line)
            else:
                flush_cell()
                current_type = 'markdown'
                current_lines = [md_line]
        elif line == '#':
            # A lone '#' in a markdown block is an empty line
            if current_type == 'markdown':
                current_lines.append('')
            else:
                flush_cell()
                current_type = 'markdown'
                current_lines = ['']
        elif line == '':
            # Empty line: could be separator between cells or within a code block
            if current_type == 'code':
                current_lines.append('')
            else:
                # End of markdown block or separator
                flush_cell()
        else:
            # Code line
            if current_type == 'code':
                current_lines.append(line)
            else:
                flush_cell()
                current_type = 'code'
                current_lines = [line]

    flush_cell()

    notebook = {
        'nbformat': 4,
        'nbformat_minor': 5,
        'metadata': {
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            },
            'language_info': {
                'name': 'python',
                'version': '3.10.0'
            }
        },
        'cells': cells
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)

    print(f"Converted: {py_path} -> {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert between Jupyter notebook (.ipynb) and Python script (.py)'
    )
    parser.add_argument(
        'input',
        help='Input file path (.ipynb or .py)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: auto-detect from input extension)'
    )

    args = parser.parse_args()

    input_ext = os.path.splitext(args.input)[1].lower()

    try:
        if input_ext == '.ipynb':
            ipynb_to_py(args.input, args.output)
        elif input_ext == '.py':
            py_to_ipynb(args.input, args.output)
        else:
            print(f"Error: Unsupported file extension '{input_ext}'. Use .ipynb or .py",
                  file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
