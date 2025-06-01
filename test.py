from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")

# REPLACE THIS with the actual path if different
chrome_driver_path = "/usr/local/bin/chromedriver"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://google.com")
print(driver.title)
driver.quit()
