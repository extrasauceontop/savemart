import undetected_chromedriver as uc
from sgselenium.sgselenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import ssl
import time
ssl._create_default_https_context = ssl._create_unverified_context

options = webdriver.ChromeOptions()

options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("--headless")
uc.TARGET_VERSION = 89
with uc.Chrome(options=options) as driver:
    driver.get("https://www.savemart.com/stores/?coordinates=37.88151857835088,-100.44300299999999&zoom=5")
    html = driver.page_source

    with open("file.txt", "w", encoding="utf-8") as output:
        print(html, file=output)
    
    time.sleep(5)

soup = bs(html, "html.parser")

grids = soup.find("div", attrs={"class": "store-list__scroll-container"}).find_all("li")

print(len(grids))

