# ipynb2pdf

Convert Jupyter notebooks (.ipynb) to A4 PDF format with proper formatting and margins.

## Features

- Converts .ipynb files to A4-sized PDF documents
- Preserves code, markdown, and output cells
- Customizable page margins (default: 25mm)
- Command-line interface for easy usage

## Installation

### 1. Install wkhtmltopdf

**Ubuntu/Debian:**
```bash
sudo apt-get install -y wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Windows:**
Download and install from [wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic usage

```bash
python ipynb2pdf.py notebook.ipynb
```

This will create `notebook.pdf` in the same directory.

### Specify output file

```bash
python ipynb2pdf.py notebook.ipynb -o output.pdf
```

### Custom margins

```bash
python ipynb2pdf.py notebook.ipynb -m 20
```

This sets all margins to 20mm (default is 25mm).

### All options

```bash
python ipynb2pdf.py [-h] [-o OUTPUT] [-m MARGIN] input

Arguments:
  input                 Input .ipynb file path
  -o, --output OUTPUT   Output .pdf file path
  -m, --margin MARGIN   Page margin in millimeters (default: 25)
  -h, --help           Show help message
```

## Example

```bash
# Convert notebook to PDF with default settings (A4, 25mm margins)
python ipynb2pdf.py my_notebook.ipynb

# Convert with custom output path and smaller margins
python ipynb2pdf.py my_notebook.ipynb -o results/report.pdf -m 15
```

## Requirements

- Python 3.6+
- nbformat
- nbconvert
- wkhtmltopdf

## License

MIT
