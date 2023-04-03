from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from seleniumrequests.request import RequestsSessionMixin
from typing import Dict, Union
from log import debug, info, error
from time import sleep
from bs4 import BeautifulSoup, Tag, NavigableString


def create_webdriver() -> WebDriver:
    info("Starting webdriver using 'Firefox'...")
    driver = webdriver.Firefox()
    driver.delete_all_cookies()
    return driver


def connect(address: str, cred: Dict[str, str]) -> None:
    # Create webdriver (TODO: Make it headless)
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
    with open("../pages/page-login.php") as file:
        html: BeautifulSoup = BeautifulSoup(file.read(), "lxml")
    #html: BeautifulSoup = BeautifulSoup(driver.page_source)
    result: Union[Tag, NavigableString, None] = html.find("input", {"id": "lkfalkfaslfksdfl"})
    if result is None:
        error("Could not find credential fields, exiting!", 1)
    else:
        debug("Found input fields! Trying...")


    # Fill credentials
    driver.find_element("xpath", r'//*[@id="username"]').send_keys(cred["username"])
    driver.find_element("xpath", r'//*[@id="password"]').send_keys(cred["password"])
    driver.find_element("xpath", r'//*[@type="submit"]').submit()

    # Close webdriver
    driver.quit()
