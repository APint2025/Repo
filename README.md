# PDF to CSV Converter

A powerful Python tool that converts unstructured text from PDF files into structured CSV format. The converter supports multiple extraction methods and intelligent text processing strategies to handle various types of PDF content.

## Features

- **Multiple PDF text extraction methods**: PyPDF2 and pdfplumber
- **Intelligent table detection**: Automatically detects and extracts structured tables
- **Multiple text processing strategies**:
  - Lines: Each line becomes a row
  - Key-Value: Extracts key-value pairs
  - Patterns: Detects emails, phones, dates, currency, etc.
  - Columns: Intelligently splits text into columns
  - Auto: Automatically selects the best strategy
- **Flexible output options**: Customizable CSV output with headers
- **Command-line interface**: Easy-to-use CLI with various options
- **Robust error handling**: Graceful fallbacks and detailed logging

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies

- PyPDF2: PDF text extraction
- pdfplumber: Advanced PDF processing and table extraction
- pandas: Data manipulation and CSV output
- numpy: Numerical operations
- Additional standard libraries: argparse, re, logging, pathlib

## Usage

### Command Line Interface

Basic usage:
```bash
python pdf_to_csv_converter.py input.pdf
```

With custom output file:
```bash
python pdf_to_csv_converter.py input.pdf -o output.csv
```

With specific extraction method:
```bash
python pdf_to_csv_converter.py input.pdf -m pdfplumber -o output.csv
```

With specific processing strategy:
```bash
python pdf_to_csv_converter.py input.pdf -s key_value -o output.csv
```

Force unstructured text processing (skip table detection):
```bash
python pdf_to_csv_converter.py input.pdf -f -s columns
```

Verbose logging:
```bash
python pdf_to_csv_converter.py input.pdf -v
```

### Command Line Options

- `pdf_path`: Path to the input PDF file (required)
- `-o, --output`: Output CSV file path (optional, defaults to `{input_name}_converted.csv`)
- `-m, --method`: Text extraction method (`auto`, `pypdf2`, `pdfplumber`, default: `auto`)
- `-s, --strategy`: Text processing strategy (`auto`, `lines`, `key_value`, `patterns`, `columns`, default: `auto`)
- `-f, --force-unstructured`: Skip table detection and force unstructured text processing
- `-v, --verbose`: Enable verbose logging

### Python API

```python
from pdf_to_csv_converter import PDFToCSVConverter

# Basic usage
converter = PDFToCSVConverter("input.pdf", "output.csv")
output_file = converter.convert()

# With specific method and strategy
converter = PDFToCSVConverter("input.pdf", "output.csv", extraction_method="pdfplumber")
output_file = converter.convert(strategy="key_value")

# Force unstructured processing
output_file = converter.convert(strategy="columns", force_unstructured=True)
```

## Processing Strategies

### Auto Strategy (Recommended)
The converter automatically tries different strategies and selects the one that produces the most structured output.

### Lines Strategy
Each line of text becomes a separate row in the CSV with a single "Text" column.

**Best for:**
- Simple text documents
- Lists
- Line-by-line data

### Key-Value Strategy
Extracts key-value pairs from text (patterns like "Key: Value" or "Key = Value").

**Best for:**
- Forms
- Configuration files
- Structured documents with labeled data

### Patterns Strategy
Detects and extracts common patterns like emails, phone numbers, dates, currency amounts.

**Best for:**
- Contact information
- Financial documents
- Documents with mixed data types

### Columns Strategy
Attempts to split text into columns using various delimiters (tabs, pipes, commas, semicolons, multiple spaces).

**Best for:**
- Tabular data
- Reports with column-based layout
- Structured text files

## Examples

### Example 1: Simple Text Document
Input PDF contains:
```
Name: John Doe
Email: john.doe@email.com
Phone: (555) 123-4567
Address: 123 Main St, City, State
```

Command:
```bash
python pdf_to_csv_converter.py document.pdf -s key_value
```

Output CSV:
```csv
Key,Value
Name,John Doe
Email,john.doe@email.com
Phone,(555) 123-4567
Address,"123 Main St, City, State"
```

### Example 2: Tabular Data
Input PDF contains:
```
Product	Price	Quantity
Laptop	$999.99	5
Mouse	$29.99	15
Keyboard	$79.99	8
```

Command:
```bash
python pdf_to_csv_converter.py inventory.pdf -s columns
```

Output CSV:
```csv
Product,Price,Quantity
Laptop,$999.99,5
Mouse,$29.99,15
Keyboard,$79.99,8
```

### Example 3: Mixed Content with Auto Detection
Input PDF contains various types of data.

Command:
```bash
python pdf_to_csv_converter.py mixed_document.pdf -s auto
```

The converter will automatically select the best strategy based on the content structure.

## Error Handling

The converter includes robust error handling:

- **File not found**: Clear error message if PDF doesn't exist
- **Extraction failures**: Automatic fallback between extraction methods
- **Processing errors**: Graceful handling with informative logs
- **Empty content**: Validation and appropriate error messages

## Logging

Use the `-v` flag for detailed logging information:

```bash
python pdf_to_csv_converter.py document.pdf -v
```

Log levels include:
- INFO: General progress information
- WARNING: Non-critical issues (fallbacks, etc.)
- ERROR: Critical errors that prevent processing

## Limitations

- **Complex layouts**: Very complex PDF layouts may not extract perfectly
- **Scanned PDFs**: OCR is not included; text must be selectable
- **Password-protected PDFs**: Not currently supported
- **Large files**: Memory usage scales with file size

## Advanced Usage

### Custom Processing
For advanced use cases, you can extend the `TextProcessor` class:

```python
from pdf_to_csv_converter import TextProcessor

class CustomProcessor(TextProcessor):
    @staticmethod
    def custom_pattern_extraction(text):
        # Your custom logic here
        pass
```

### Batch Processing
Process multiple PDFs:

```bash
for pdf in *.pdf; do
    python pdf_to_csv_converter.py "$pdf" -o "${pdf%.pdf}.csv"
done
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and practical use.

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **Empty output**: Try different extraction methods (`-m pypdf2` or `-m pdfplumber`)
3. **Poor structure**: Try different strategies (`-s lines`, `-s key_value`, etc.)
4. **Memory issues**: Process smaller PDF files or implement chunking for large files

### Getting Help

1. Run with verbose logging (`-v`) to see detailed information
2. Try different extraction methods and strategies
3. Check that the PDF contains selectable text (not just images)

## Version History

- v1.0: Initial release with multiple extraction methods and processing strategies