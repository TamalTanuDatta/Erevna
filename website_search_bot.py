import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Set, List, Union
import concurrent.futures
import time

class WebsiteSearchBot:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.visited_urls: Set[str] = set()
        self.session = requests.Session()
        self.should_stop = False
        # Add common headers to mimic a browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Disable SSL verification for local development servers
        if self._is_local_url(base_url):
            self.session.verify = False

    def _is_local_url(self, url: str) -> bool:
        """Check if the URL is a local development server."""
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname or ""
        port = parsed_url.port
        
        local_hostnames = {'localhost', '127.0.0.1', '0.0.0.0'}
        dev_ports = {3000, 4200, 5000, 5173, 8000, 8080, 8081, 8888, 9000}  # Common development ports
        
        return (
            hostname in local_hostnames or
            hostname.startswith('192.168.') or
            hostname.startswith('10.') or
            (port in dev_ports) or
            hostname.endswith('.local')
        )

    def is_valid_url(self, url: str) -> bool:
        """Check if the URL belongs to the same domain and is a valid web page."""
        try:
            parsed_base = urlparse(self.base_url)
            parsed_url = urlparse(url)
            
            # For local development, consider all local URLs as valid
            if self._is_local_url(self.base_url) and self._is_local_url(url):
                return True
            
            # Check if URLs belong to the same domain
            same_domain = parsed_base.netloc == parsed_url.netloc
            
            # Check if the path looks like a web page or directory
            valid_path = (
                parsed_url.path.lower().endswith(('.html', '.htm', '/')) or
                '.' not in parsed_url.path.split('/')[-1] or
                parsed_url.path.lower().endswith(('.php', '.asp', '.jsx', '.tsx'))  # Common web extensions
            )
            
            return same_domain and valid_path
        except Exception as e:
            print(f"Error validating URL {url}: {str(e)}")
            return False

    def get_page_content(self, url: str) -> tuple[str, str]:
        """Fetch page content and return both HTML and text content."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if not ('text/html' in content_type or 'application/json' in content_type):
                return "", ""
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'meta', 'noscript', 'header', 'footer']):
                element.decompose()
            
            # Get text content
            text_content = soup.get_text(separator='\n')
            
            # Clean up text content
            text_content = '\n'.join(
                line.strip() for line in text_content.split('\n')
                if line.strip() and len(line.strip()) > 3
            )
            
            return html_content, text_content
            
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return "", ""

    def extract_links(self, url: str, html_content: str) -> List[str]:
        """Extract all valid links from the page."""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Find all elements that might contain links
        for element in soup.find_all(['a', 'link', 'area', 'base', 'iframe', 'frame']):
            # Check for href attribute
            href = element.get('href')
            if href:
                if href.startswith('#') or href.startswith('javascript:'):
                    continue
                links.append(href)
            
            # Check for src attribute
            src = element.get('src')
            if src:
                links.append(src)
        
        # Process all found links
        valid_links = []
        for link in links:
            try:
                absolute_url = urljoin(url, link)
                if self.is_valid_url(absolute_url) and absolute_url not in self.visited_urls:
                    valid_links.append(absolute_url)
            except Exception as e:
                print(f"Error processing link {link}: {str(e)}")
        
        return valid_links

    def search_content(self, content: str, search_term: str) -> List[str]:
        """Search for matches in the content with context."""
        matches = []
        search_terms = search_term.lower().split()
        lines = content.split('\n')
        
        # Create a window of lines for context
        window_size = 2  # lines before and after the match
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if any of the search terms are in the line
            if any(term in line_lower for term in search_terms):
                # Get context lines
                start = max(0, i - window_size)
                end = min(len(lines), i + window_size + 1)
                context_lines = lines[start:end]
                
                # Clean and join context lines
                context = ' ▸ '.join(
                    line.strip() for line in context_lines 
                    if line.strip() and len(line.strip()) > 3
                )
                
                if context:
                    matches.append(context)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_matches = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique_matches.append(match)
        
        return unique_matches

    def stop_search(self):
        """Stop the ongoing search."""
        self.should_stop = True

    def crawl_and_search(self, search_term: str, max_pages: int = 100) -> dict:
        """Crawl the website and search for the given term."""
        self.should_stop = False
        results = {}
        urls_to_visit = [self.base_url]
        processed_count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while urls_to_visit and len(self.visited_urls) < max_pages and not self.should_stop:
                current_url = urls_to_visit.pop(0)
                if current_url in self.visited_urls:
                    continue
                
                self.visited_urls.add(current_url)
                processed_count += 1
                
                html_content, text_content = self.get_page_content(current_url)
                if not html_content:
                    continue
                
                # Search in both HTML and text content
                html_matches = self.search_content(html_content, search_term)
                text_matches = self.search_content(text_content, search_term)
                
                if html_matches or text_matches:
                    results[current_url] = {
                        'html_matches': html_matches,
                        'text_matches': text_matches
                    }
                
                # Extract and add new links to visit
                new_links = self.extract_links(current_url, html_content)
                # Prioritize links that might be more relevant
                new_links.sort(key=lambda x: search_term.lower() in x.lower(), reverse=True)
                urls_to_visit.extend([link for link in new_links if link not in self.visited_urls])
                
                # Add a small delay to be respectful to the server
                time.sleep(0.2)  # Reduced delay further for better performance
        
        return results

def main():
    # Example usage
    website_url = input("Enter the website URL to search (e.g., https://example.com): ")
    search_term = input("Enter the search term: ")
    max_pages = int(input("Enter maximum number of pages to search (default 100): ") or "100")
    
    bot = WebsiteSearchBot(website_url)
    results = bot.crawl_and_search(search_term, max_pages)
    
    print("\nSearch Results:")
    print("-" * 50)
    
    if not results:
        print(f"No matches found for '{search_term}'")
        return
    
    for url, matches in results.items():
        print(f"\nURL: {url}")
        if matches['text_matches']:
            print("\nText Matches:")
            for match in matches['text_matches'][:5]:  # Limit to 5 matches per URL
                print(f"- {match}")
        if matches['html_matches']:
            print("\nHTML Matches:")
            for match in matches['html_matches'][:5]:  # Limit to 5 matches per URL
                print(f"- {match}")
        print("-" * 50)

if __name__ == "__main__":
    main()
