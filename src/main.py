import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

class ScoutScraper:
    def __init__(self, urls):
        self.urls = urls
        self.results = []

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                html = await response.text()
                return html
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse(self, html, url):
        if not html: return
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        self.results.append({"url": url, "title": title})
        print(f"Parsed: {url}")

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            responses = await asyncio.gather(*tasks)
            for i, html in enumerate(responses):
                self.parse(html, self.urls[i])

if __name__ == "__main__":
    urls = ["https://python.org", "https://github.com", "https://google.com"]
    scraper = ScoutScraper(urls)
    asyncio.run(scraper.run())
