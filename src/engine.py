from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from typing import Dict, Union
from log import debug, info, error
from time import sleep
from bs4 import BeautifulSoup, Tag, NavigableString


def create_webdriver() -> WebDriver:
    info("Starting webdriver using 'Firefox'...")
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=opts)
    driver.delete_all_cookies()
    return driver


def connect(address: str, cred: Dict[str, str]) -> None:
    # Create webdriver
    driver: WebDriver = create_webdriver()
    # Connect to the website
    info(f"Accessing '{address}'...")
    try:
        driver.get(address)
    except WebDriverException as _error:
        if "?e=dnsNotFound" in str(_error):
            error("Website seems to be down!", 1)
        error("Failed to connect!", 1)
    sleep(0.25)  # NOTE: This gives enough time to account for slow machines/networks.

    # Verify that credential fields exist
    html: BeautifulSoup = BeautifulSoup(driver.page_source, "lxml")
    result: Union[Tag, NavigableString, None] = html.find("input", {"id": "password"})
    if result is None:
        error("Could not find credential fields, exiting!", 1)
    else:
        debug("Found input fields! Trying...")

    # Fill credentials
    debug("Filling credentials...")
    driver.find_element("xpath", r'//*[@id="username"]').send_keys(cred["username"])
    driver.find_element("xpath", r'//*[@id="password"]').send_keys(cred["password"])
    driver.find_element("xpath", r'//*[@type="submit"]').submit()

    # Close webdriver
    debug("Closing webdriver")
    driver.quit()
