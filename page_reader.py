from playwright.sync_api import sync_playwright
from typing import Dict, List, Optional, Union
import json
import logging

class PageReader:
    def __init__(self, headless: bool = True):
        """Initialize the PageReader with browser settings.
        
        Args:
            headless: Whether to run browser in headless mode (default: True)
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close browser and cleanup resources."""
        self.context.close()
        self.browser.close()
        self.playwright.stop()
    
    def _extract_element_data(self, element) -> Optional[Dict]:
        """Extract text and styling information from an element."""
        try:
            # Check if element is an HTML element
            is_html = element.evaluate('''
                (element) => element instanceof HTMLElement
            ''')
            
            if not is_html:
                return None
            
            # Get computed styles
            styles = element.evaluate("""
                (element) => {
                    const style = window.getComputedStyle(element);
                    return {
                        fontWeight: style.fontWeight,
                        fontStyle: style.fontStyle,
                        textDecoration: style.textDecoration,
                        fontSize: style.fontSize,
                        color: style.color
                    };
                }
            """)
            
            # Get element metadata
            tag_name = element.evaluate('element => element.tagName.toLowerCase()')
            
            # Get text content safely
            text = element.evaluate('element => element.textContent || ""')
            
            return {
                'tag': tag_name,
                'text': text.strip(),
                'styles': styles
            }
            
        except Exception as e:
            logging.warning(f"Error extracting element data: {str(e)}")
            return None
    
    def _process_element(self, element) -> Optional[Dict]:
        """Process an element and its children recursively."""
        try:
            # Skip hidden elements
            if not element.is_visible():
                return None
            
            # Get element data
            data = self._extract_element_data(element)
            if not data:
                return None
            
            # Process children (only direct children)
            children = []
            try:
                for child in element.query_selector_all(':scope > *'):
                    child_data = self._process_element(child)
                    if child_data:
                        children.append(child_data)
            except Exception as e:
                logging.warning(f"Error processing children: {str(e)}")
            
            if children:
                data['children'] = children
            
            return data
            
        except Exception as e:
            logging.warning(f"Error processing element: {str(e)}")
            return None
    
    def read_page(self, url: str) -> Dict:
        """Read a webpage and return its content structure.
        
        Args:
            url: The URL of the webpage to process
            
        Returns:
            Dict containing the structured content of the page
        """
        page = self.context.new_page()
        try:
            # Set a reasonable timeout for page load
            page.set_default_timeout(30000)  # 30 seconds
            
            # Navigate to the page
            page.goto(url, wait_until='domcontentloaded')
            page.wait_for_load_state('networkidle')
            
            # Get main content areas (skip navigation, footer, etc)
            main_elements = page.query_selector_all('main, article, .main-content, #main-content')
            if not main_elements:
                # Fallback to body if no main content areas found
                body = page.query_selector('body')
                main_elements = [body] if body else []
            
            result = {
                'url': url,
                'title': page.title() or url,
                'content': []
            }
            
            for element in main_elements:
                content = self._process_element(element)
                if content:
                    result['content'].append(content)
            
            return result
            
        except Exception as e:
            logging.error(f"Error processing page {url}: {str(e)}")
            return {
                'url': url,
                'title': 'Error loading page',
                'content': [],
                'error': str(e)
            }
        finally:
            try:
                page.close()
            except:
                pass

    def read_page_to_file(self, url: str, output_file: str):
        """Read a webpage and save its content structure to a JSON file.
        
        Args:
            url: The URL of the webpage to process
            output_file: Path to the output JSON file
        """
        data = self.read_page(url)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

