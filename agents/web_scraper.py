from bs4 import BeautifulSoup
import requests

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_website(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant content
            content = {
                'title': soup.title.string if soup.title else '',
                'description': self._get_meta_description(soup),
                'main_content': self._extract_main_content(soup),
                'products': self._extract_product_info(soup)
            }
            
            return content
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

    def _get_meta_description(self, soup):
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta['content'] if meta else ''

    def _extract_main_content(self, soup):
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        return ' '.join(chunk for chunk in lines if chunk)

    def _extract_product_info(self, soup):
        # This would need to be customized based on the website structure
        products = []
        # Add product extraction logic here
        return products 