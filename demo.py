#!/usr/bin/env python3

from page_reader import PageReader
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def print_content_structure(content, indent=0):
    """Pretty print the content structure."""
    indent_str = '  ' * indent
    
    if isinstance(content, list):
        for item in content:
            print_content_structure(item, indent)
        return
    
    # Print tag and text
    tag = content.get('tag', '')
    text = content.get('text', '').strip()
    if text:
        print(f"{indent_str}{tag}: {text}")
    
    # Print styles
    styles = content.get('styles', {})
    if styles:
        print(f"{indent_str}Styles:")
        for key, value in styles.items():
            print(f"{indent_str}  {key}: {value}")
    
    # Process children
    children = content.get('children', [])
    if children:
        print(f"{indent_str}Children:")
        print_content_structure(children, indent + 1)

def main():
    # Example URLs to demonstrate different types of content
    urls = [
        'https://cnn.com',  # Very simple static page
        'https://httpbin.org/html',  # Simple test HTML page
    ]
    
    logging.info("Starting page processing...")
    
    with PageReader() as reader:
        for url in urls:
            logging.info(f"Processing {url}...")
            print(f"\nProcessing {url}...\n")
            
            # Read page and save to file
            output_file = f"output_{url.replace('https://', '').replace('/', '_')}.json"
            reader.read_page_to_file(url, output_file)
            
            # Read and display the content
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"Title: {data['title']}")
            print("\nContent Structure:")
            print_content_structure(data['content'])
            print(f"\nDetailed output saved to {output_file}")

if __name__ == '__main__':
    main()

