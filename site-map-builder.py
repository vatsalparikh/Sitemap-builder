import string
from collections import deque
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def build_site_map(starting_url: string, max_depth: int = 10):
    json_site_map = {}
    # YOUR code here

    new_urls = deque([starting_url])
    base = urlparse(starting_url)
    base_url = '{}://{}'.format(base.scheme, base.netloc)
    crawled_urls = set()
    # pages_indexed = 0

    # go max_depth levels deep
    while len(new_urls) and (max_depth > 0):
        local_urls = set()
        # go through all urls at each level
        while len(new_urls):
            page_url = new_urls.popleft()
            crawled_urls.add(page_url)
            links = []
            images = []

            # ignore invalid urls
            try:
                response = requests.get(page_url)
            except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
                continue

            parsed = urlparse(page_url)
            path = parsed.path

            soup = BeautifulSoup(response.text, 'lxml')
            for link in soup.find_all('a', href=True):
                curr_link = link.get('href')
                links.append(curr_link)
                if curr_link.startswith('/'):
                    local_link = base_url + curr_link
                    local_urls.add(local_link)
                elif not curr_link.startswith('http'):
                    local_link = path + curr_link
                    local_urls.add(local_link)
                elif base_url in curr_link:
                    local_urls.add(curr_link)

            for image in soup.find_all('img'):
                images.append(image.get('src'))

            json_site_map['page_url'] = page_url
            json_site_map['links'] = links
            json_site_map['images'] = images
            # pages_indexed += 1
            # print(page_url)

        # add same domain urls to new_urls to continue crawling
        for i in local_urls:
            if not i in new_urls and not i in crawled_urls:
                new_urls.append(i)
        # print(pages_indexed)
        max_depth -= 1

    return json_site_map

# build_site_map('https://www.mozilla.org/en-US/')
json_site = build_site_map('http://desireeadaway.com/')
print(json_site)