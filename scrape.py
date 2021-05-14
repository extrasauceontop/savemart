from sgselenium.sgselenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import ssl
import time
from sgselenium import SgChrome
ssl._create_default_https_context = ssl._create_unverified_context

options = webdriver.ChromeOptions()

options.add_argument("--remote-debugging-port=9222")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# with webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options) as driver:
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

with SgChrome(executable_path=ChromeDriverManager().install(), is_headless=False, chrome_options=options).driver() as driver:
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get("https://whatismyipaddress.com/")
    html = driver.page_source

    with open("file.txt", "w", encoding="utf-8") as output:
        print(html, file=output)
    print(html)
    time.sleep(5)

soup = bs(html, "html.parser")

ip = soup.find("span", attrs={"id": "ipv4"}).find("a").text.strip()

print(ip)

