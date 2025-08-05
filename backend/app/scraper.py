import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import json
import re
from typing import List, Dict
import time

class WebsiteScraper:
    def __init__(self, base_url: str, output_dir: str = "data/scraped"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.domain = urlparse(base_url).netloc
        os.makedirs(self.output_dir, exist_ok=True)
        self.headers = {
            'User-Agent': 'CompanyChatbotScraper/1.0 (https://github.com/BusulwaJordan/OTICTECH)'
        }

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return (parsed.netloc == self.domain 
                and not parsed.fragment 
                and not any(ext in parsed.path for ext in ['.pdf', '.jpg', '.png']))

    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\[[^\]]+\]', '', text)  # Remove footnotes
        return text

    def scrape_page(self, url: str) -> Dict[str, str]:
        try:
            time.sleep(0.5)  # Rate limiting
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
                element.decompose()
            
            title = soup.title.string if soup.title else url
            main_content = soup.find('main') or soup.find('article') or soup.body
            text = self.clean_text(main_content.get_text()) if main_content else ""
            
            links = set()
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                if self.is_valid_url(absolute_url):
                    links.add(absolute_url)
            
            return {
                'url': url,
                'title': title,
                'text': text,
                'links': list(links)
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def scrape_site(self, max_pages: int = 100):
        queue = [self.base_url]
        scraped_data = []
        
        while queue and len(self.visited_urls) < max_pages:
            current_url = queue.pop(0)
            
            if current_url in self.visited_urls:
                continue
                
            print(f"Scraping: {current_url}")
            page_data = self.scrape_page(current_url)
            
            if page_data and page_data['text']:
                self.visited_urls.add(current_url)
                scraped_data.append(page_data)
                
                filename = f"{urlparse(current_url).path.replace('/', '_')[1:] or 'home'}.json"
                with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                    json.dump(page_data, f, ensure_ascii=False, indent=2)
                
                for link in page_data['links']:
                    if link not in self.visited_urls and link not in queue:
                        queue.append(link)
        
        print(f"Scraped {len(scraped_data)} pages")
        return scraped_data

if __name__ == "__main__":
    # REPLACE WITH YOUR COMPANY URL
    scraper = WebsiteScraper("https://oticfoundation.org/")
    scraper.scrape_site()