#!/usr/bin/env python3
"""
ipynb2pdf: Convert Jupyter notebooks to A4 PDF files
"""
import argparse
import os
import sys
import nbformat
from nbconvert import HTMLExporter
from subprocess import run, CalledProcessError


def check_wkhtmltopdf():
    """Check if wkhtmltopdf is installed"""
    try:
        result = run(['wkhtmltopdf', '--version'], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def convert_ipynb_to_pdf(ipynb_path, output_path=None, margin_mm=25):
    """
    Convert a Jupyter notebook to A4 PDF

    Args:
        ipynb_path: Path to the input .ipynb file
        output_path: Path to the output .pdf file (optional)
        margin_mm: Margin size in millimeters (default: 25)

    Returns:
        Path to the generated PDF file
    """
    # Check if input file exists
    if not os.path.exists(ipynb_path):
        raise FileNotFoundError(f"Input file not found: {ipynb_path}")

    # Check if wkhtmltopdf is installed
    if not check_wkhtmltopdf():
        raise RuntimeError(
            "wkhtmltopdf is not installed. Please install it:\n"
            "  Ubuntu/Debian: sudo apt-get install -y wkhtmltopdf\n"
            "  macOS: brew install wkhtmltopdf\n"
            "  Windows: Download from https://wkhtmltopdf.org/downloads.html"
        )

    # Determine output path
    if output_path is None:
        output_path = ipynb_path.replace('.ipynb', '.pdf')

    # Read the notebook
    print(f"Reading notebook: {ipynb_path}")
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Setup HTML exporter with embed_images enabled
    html_exporter = HTMLExporter()
    html_exporter.exclude_input = False
    html_exporter.embed_images = True

    # Custom CSS for A4 formatting
    custom_css = """
<style>
    /* Page margins and layout */
    body {
        margin: 0;
        padding: 10px;
        font-family: Arial, sans-serif;
    }

    /* Ensure images fit on A4 page */
    img, .output {
        max-width: 90%;
        height: auto;
    }

    /* Compact cell spacing */
    .input, .output {
        margin: 5px 0;
        padding: 5px;
        font-size: 12px;
    }

    /* Code block styling */
    .input_area {
        background-color: #f5f5f5;
        border-left: 3px solid #3b7ea1;
        padding: 10px;
        overflow-x: auto;
    }

    /* Output area styling */
    .output_area {
        padding: 5px;
    }

    /* Prevent page breaks inside code blocks */
    .cell {
        page-break-inside: avoid;
    }
</style>
"""

    # Convert to HTML
    print("Converting to HTML...")
    html_data, _ = html_exporter.from_notebook_node(notebook_content)
    html_data = custom_css + html_data

    # Save HTML temporarily
    html_temp_path = ipynb_path.replace('.ipynb', '_temp.html')
    with open(html_temp_path, 'w', encoding='utf-8') as f:
        f.write(html_data)

    # Convert HTML to PDF using wkhtmltopdf with A4 settings
    print(f"Converting to A4 PDF: {output_path}")
    try:
        run([
            'wkhtmltopdf',
            '--margin-top', f'{margin_mm}mm',
            '--margin-bottom', f'{margin_mm}mm',
            '--margin-left', f'{margin_mm}mm',
            '--margin-right', f'{margin_mm}mm',
            '--page-size', 'A4',
            '--encoding', 'UTF-8',
            '--enable-local-file-access',
            '--disable-external-links',
            '--disable-javascript',
            '--no-stop-slow-scripts',
            html_temp_path,
            output_path
        ], check=True, capture_output=True)
    except CalledProcessError as e:
        print(f"Error during PDF conversion: {e.stderr.decode()}")
        raise
    finally:
        # Clean up temporary HTML file
        if os.path.exists(html_temp_path):
            os.remove(html_temp_path)

    print(f"✓ PDF generated successfully: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert Jupyter notebook (.ipynb) to A4 PDF'
    )
    parser.add_argument(
        'input',
        help='Input .ipynb file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output .pdf file path (default: same name as input with .pdf extension)'
    )
    parser.add_argument(
        '-m', '--margin',
        type=int,
        default=25,
        help='Page margin in millimeters (default: 25)'
    )

    args = parser.parse_args()

    try:
        convert_ipynb_to_pdf(args.input, args.output, args.margin)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
