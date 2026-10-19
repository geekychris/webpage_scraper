<p align="center">
  <img src="assets/logo.png" alt="Webpage Scraper logo" width="180">
</p>

# Web Page Content Extractor

A Python API for extracting structured text content from web pages, preserving document hierarchy and styling information. This tool uses Playwright for reliable web page rendering and content extraction.

## Features

- Extracts readable text content while preserving document structure
- Captures text styling information (font properties, colors)
- Maintains heading hierarchy and section organization
- Handles dynamic content through proper page loading
- Focuses on main content areas, avoiding navigation and footer sections
- Provides both programmatic and file-based output options
- Supports headless operation for automation scenarios

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd page_scrape
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install playwright
```

4. Install browser binaries:
```bash
playwright install
```

## API Design

The API consists of two main components:

### PageReader Class

The core API class that handles web page content extraction:

```python
class PageReader:
    def __init__(self, headless: bool = True)
    def read_page(self, url: str) -> Dict
    def read_page_to_file(self, url: str, output_file: str)
```

#### Output Structure

The extracted content is structured as follows:

```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "content": [
    {
      "tag": "main",
      "text": "Main content text",
      "styles": {
        "fontWeight": "400",
        "fontStyle": "normal",
        "textDecoration": "none",
        "fontSize": "16px",
        "color": "rgb(0, 0, 0)"
      },
      "children": [...]
    }
  ]
}
```

## Usage

### Basic Usage

```python
from page_reader import PageReader

# Using context manager (recommended)
with PageReader() as reader:
    # Get content as Python dictionary
    content = reader.read_page("https://example.com")
    
    # Or save directly to file
    reader.read_page_to_file("https://example.com", "output.json")
```

### Running the Demo

The included demo script processes example URLs and demonstrates the API's capabilities:

```bash
python demo.py
```

The demo will:
1. Process multiple example URLs
2. Save the structured content to JSON files
3. Display a formatted version of the content structure

### Custom Implementation

You can extend the API by modifying the `_extract_element_data` method in `PageReader` class to capture additional styling or structural information:

```python
def _extract_element_data(self, element) -> Dict:
    # Add custom style extraction logic here
    styles = element.evaluate("""
        (element) => {
            const style = window.getComputedStyle(element);
            return {
                // Add more style properties as needed
                customProperty: style.customProperty
            };
        }
    """)
    # ... rest of the method
```

## Technical Details

### Content Extraction Strategy

1. The API focuses on semantic content areas using selectors like `main`, `article`, and common content class names
2. Falls back to `body` if no semantic content areas are found
3. Recursively processes the DOM tree while preserving hierarchy
4. Skips hidden elements to avoid extracting irrelevant content
5. Captures computed styles to preserve text formatting information

### Browser Handling

- Uses Playwright's Chromium browser (can be extended to support Firefox or WebKit)
- Runs in headless mode by default for better performance
- Properly handles page loading and dynamic content
- Automatically manages browser resources through context manager

## Limitations

- Does not process iframes or embedded content
- JavaScript execution might be required for some dynamic content
- Style extraction is limited to common text properties
- Image content is not processed (only alt text if present)

## License

[Add your chosen license here]

