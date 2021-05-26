import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock
from queue import Queue
import furl


class Crawler:

    def __init__(self, allowed_domains, start_url):
        self.visited_urls = []
        self.allowed_domains = allowed_domains
        self.queue = Queue()
        self.queue.put(start_url)
        self.lock = Lock()

    # clean all urls found in html
    def clean(self, paths):
        results = []
        for path in paths:
            if path is not None:
                if self.allowed_domains:
                    for domain in self.allowed_domains:
                        if domain in path and path.startswith("http"):
                            results.append(furl.furl(path).remove(args=True, fragment=True).url)
                else:
                    if path.startswith("http"):
                        results.append(furl.furl(path).remove(args=True, fragment=True).url)

        return results

    # get html from url
    @staticmethod
    def download_url(url):
        response = requests.get(url)
        return response.text

    # get request response and run through pipeline
    def get_urls(self, url):
        response = self.download_url(url)
        print(f'{url}')
        for url in self.get_linked_urls(url, response):
            print(f'\t{url}')
            self.add_url_to_visit(url)

    # add url to visited list
    def add_url_to_visit(self, url):
        if url not in self.visited_urls:
            self.queue.put(url)

    # extract all urls found in html
    def get_linked_urls(self, url, html):
        paths = []
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            paths.append(path)
        return self.clean(paths)

    # queue calls this function one by one
    def crawl(self, url):
        try:
            self.get_urls(url)
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
        finally:
            self.visited_urls.append(url)

    # thread worker
    def worker(self):
        while True:
            link = self.queue.get()
            with self.lock:
                self.crawl(link)
            self.queue.task_done()

    def run(self):
        num_threads = 10

        for i in range(num_threads):
            thread = Thread(target=self.worker)
            thread.daemon = True
            thread.start()

        self.queue.join()
        print("Ending script.")


if __name__ == '__main__':
    starting_url = input('Enter start url (Eg: https://www.rescale.com) - ')
    allowed_domain = input('Enter the name of domain allowed (Eg: rescale.com) -')
    if allowed_domain:
        crawler = Crawler([allowed_domain], starting_url)
    else:
        crawler = Crawler([], starting_url)
    crawler.run()
