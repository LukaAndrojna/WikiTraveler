import re
import random
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, steps):
        self._base_url = 'https://en.wikipedia.org'
        self._headers = requests.utils.default_headers()
        self._headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        self._steps = steps
        self._urls = []

    def validHref(self, href):
        is_wiki_link = re.match(r'^/wiki/.*', href)
        is_not_middle_page = ':' not in href
        return is_wiki_link and is_not_middle_page

    def getNextUrl(self, soup):
        hrefs = [el.get('href') for el in soup.find_all('a', href=True) if self.validHref(el.get('href'))]
        href = random.choice(hrefs)
        while self._base_url + href in self._urls:
            href = random.choice(hrefs)
        return self._base_url + href

    def run(self, start_url):
        URL = self._base_url + start_url
        self._urls.append(URL)
        for _ in range(self._steps):
            page = requests.get(URL, self._headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            URL = self.getNextUrl(soup)
            self._urls.append(URL)
    
    def getUrls(self):
        return self._urls


def main():
    scraper = Scraper(20)
    scraper.run('/wiki/Labrador_Retriever')
    pprint(scraper.getUrls())

if __name__ == '__main__':
    main()