
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys

# Main URL
HOST = 'https://jazwings.com'

# Selenium driver
CHROMEDRIVER = "/Users/rolycg89/Downloads/chromedriver"

# Postgres configuration
USER = 'gEphephA6eWr'
PASSWORD = 'fUBanasp4fup'
NAME = 'prE8rufr7BUc'
POSTGRES_HOST = 'restfulapi-v2-prod02.ccoyoeut8gty.us-east-1.rds.amazonaws.com'


def open_browser():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    os.environ["webdriver.chrome.driver"] = CHROMEDRIVER
    _driver = webdriver.Chrome(executable_path=CHROMEDRIVER, chrome_options=chrome_options)
    # binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox-bin')

    _driver.maximize_window()
    return _driver


if __name__ == '__main__':
    if len(sys.argv):
        HOST = sys.argv[0]

