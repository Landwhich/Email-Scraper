from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as btfs
import requests
import re
import time

# Setup Chrome WebDriver
options = Options()
options.add_argument("--headless")  # Run in background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# Regex for email addresses
email_id = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

targetUrls = ["",
              ]


visitedUrls = set()
emailList = []

MAX_CRAWLS = 50

def emailScraper(html):
    return email_id.findall(html)

def crawler(num):
    crawlCount = 0

    while urlsToVisit and crawlCount < MAX_CRAWLS:
        currentUrl = urlsToVisit.pop(0)
        if currentUrl in visitedUrls:
            continue
        visitedUrls.add(currentUrl)

        try:
            print(f"{crawlCount} of {MAX_CRAWLS}")
            # if emailList:
            #     print("--- emails are now ---")
            #     for email in emailList:
            #         print(email)
            driver.get(currentUrl)
            time.sleep(2)  # Let JS load

            html = driver.page_source
            soup = btfs(html, 'html.parser')

            # Extract and store emails
            emails = emailScraper(html)
            if(emails): print(currentUrl)
            for email in emails:
                if email not in emailList:
                    emailList.append(email)

            # Extract links
            links = soup.select("a[href]")
            for link in links:
                href = link.get("href")
                if href:
                    if not href.startswith("http"):
                        full_url = requests.compat.urljoin(currentUrl, href)
                    else:
                        full_url = href

                    if full_url.startswith(targetUrls[num]) and full_url not in visitedUrls:
                        urlsToVisit.append(full_url)

            crawlCount += 1

        except Exception as e:
            print(f"Error loading {currentUrl}: {e}")
            continue

    

for i in range(len(targetUrls)):
    urlsToVisit = [targetUrls[i]]
    crawler(i)
driver.quit()

print("\n--- Emails Found ---")
for email in emailList:
    print(email)
