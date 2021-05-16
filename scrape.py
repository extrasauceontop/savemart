from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sgselenium.sgselenium import SgChrome
from webdriver_manager.chrome import ChromeDriverManager
# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context

user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
with SgChrome(executable_path=ChromeDriverManager().install(), user_agent=user_agent, is_headless=True).driver() as driver:
    driver.get("https://www.savemart.com/stores/?coordinates=39.64096403685537,-112.39632159999998&zoom=5")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "store-list__store"))
    )
    soup = bs(driver.page_source, 'html.parser')
    locations = soup.find('div', class_='store-list__scroll-container').find_all('li')
    print(len(locations))