from bs4 import BeautifulSoup as btfs
import requests, re

email_id = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
emailList = []

targetUrl = "https://www.eq3.com/"
urlsToVisit = [targetUrl]
seenUrls = []

MAX_CRAWLS = 50

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def emailScraper(soup):
    return soup.find_all(string=email_id)

def crawler():
    crawlCount = 0
    while urlsToVisit and crawlCount < MAX_CRAWLS:

        currentUrl = urlsToVisit.pop(0)
        print(f"||| crawling {currentUrl}... |||" )

        response = requests.get(currentUrl, headers=headers)
        if "text/html" not in response.headers.get("Content-Type", ""):
            continue

        response.raise_for_status()

        soup = btfs(response.text, 'html.parser')

        emails = emailScraper(soup)
        links = soup.select("a[href]")

        for email in emails:
            if not email in emailList:
                emailList.append(email)

        for link in links:
            unprocessedUrl = link["href"]

            if not unprocessedUrl.startswith("http"):
                url = requests.compat.urljoin(targetUrl, unprocessedUrl)
            else: 
                url = unprocessedUrl
        
            if url.startswith(targetUrl) and url not in seenUrls:
                seenUrls.append(url)
                urlsToVisit.append(url)
        crawlCount += 1
crawler()

for email in emailList:
    print(email)