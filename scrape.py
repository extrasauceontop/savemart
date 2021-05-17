# import os

# os.system("pip uninstall -y sgselenium")
# os.system("pip install sgselenium==0.0.15")

from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sgselenium.sgselenium import SgChrome
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

locator_domains = []
page_urls = []
location_names = []
street_addresses = []
citys = []
states = []
zips = []
country_codes = []
store_numbers = []
phones = []
location_types = []
latitudes = []
longitudes = []
hours_of_operations = []

user_agent = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
)
with SgChrome(
    executable_path=ChromeDriverManager().install(),
    user_agent=user_agent,
    is_headless=True,
).driver() as driver:
    driver.get(
        "https://www.savemart.com/stores/?coordinates=39.64096403685537,-112.39632159999998&zoom=5"
    )
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "store-list__store"))
    )
    soup = bs(driver.page_source, "html.parser")
    grids = soup.find("div", class_="store-list__scroll-container").find_all("li")

    for grid in grids:
        name = grid.find("span", attrs={"class": "name"}).text.strip()
        number = grid.find("span", attrs={"class": "number"}).text.strip()
        page_url = (
            "https://www.savemart.com/stores/"
            + name.split("\n")[0].replace(" ", "-").replace(".", "").lower()
            + "-"
            + number.split("\n")[0].split("#")[-1]
            + "/"
            + grid["id"].split("-")[-1]
        )

        driver.get(page_url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "store-details-store-hours__content")
            )
        )
        location_soup = bs(driver.page_source, "html.parser")

        locator_domain = "savemart.com"
        location_name = location_soup.find("meta", attrs={"property": "og:title"})[
            "content"
        ]
        address = location_soup.find("meta", attrs={"property": "og:street-address"})[
            "content"
        ]
        city = location_soup.find("meta", attrs={"property": "og:locality"})["content"]
        state = location_soup.find("meta", attrs={"property": "og:region"})["content"]
        zipp = location_soup.find("meta", attrs={"property": "og:postal-code"})[
            "content"
        ]
        country_code = location_soup.find(
            "meta", attrs={"property": "og:country-name"}
        )["content"]
        store_number = location_name.split("#")[-1]
        phone = location_soup.find("meta", attrs={"property": "og:phone_number"})[
            "content"
        ]
        location_type = "<MISSING>"
        latitude = location_soup.find(
            "meta", attrs={"property": "og:location:latitude"}
        )["content"]
        longitude = location_soup.find(
            "meta", attrs={"property": "og:location:longitude"}
        )["content"]

        hours = ""
        days = location_soup.find("dl", attrs={"aria-label": "Store Hours"}).find_all(
            "dt"
        )
        hours_list = location_soup.find(
            "dl", attrs={"aria-label": "Store Hours"}
        ).find_all("dd")

        for x in range(len(days)):
            day = days[x].text.strip()
            hour = hours_list[x].text.strip()
            hours = hours + day + " " + hour + ", "

        hours = hours[:-2]

        locator_domains.append(locator_domain)
        page_urls.append(page_url)
        location_names.append(location_name)
        street_addresses.append(address)
        citys.append(city)
        states.append(state)
        zips.append(zipp)
        country_codes.append(country_code)
        store_numbers.append(store_number)
        phones.append(phone)
        location_types.append(location_type)
        latitudes.append(latitude)
        longitudes.append(longitude)
        hours_of_operations.append(hours)

df = pd.DataFrame(
    {
        "locator_domain": locator_domains,
        "page_url": page_urls,
        "location_name": location_names,
        "street_address": street_addresses,
        "city": citys,
        "state": states,
        "zip": zips,
        "store_number": store_numbers,
        "phone": phones,
        "latitude": latitudes,
        "longitude": longitudes,
        "hours_of_operation": hours_of_operations,
        "country_code": country_codes,
        "location_type": location_types,
    }
)

df = df.fillna("<MISSING>")
df = df.replace(r"^\s*$", "<MISSING>", regex=True)

df["dupecheck"] = (
    df["location_name"]
    + df["street_address"]
    + df["city"]
    + df["state"]
    + df["location_type"]
)

df = df.drop_duplicates(subset=["dupecheck"])
df = df.drop(columns=["dupecheck"])
df = df.replace(r"^\s*$", "<MISSING>", regex=True)
df = df.fillna("<MISSING>")

df.to_csv("data.csv", index=False)
