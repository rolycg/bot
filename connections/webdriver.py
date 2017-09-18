from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Selenium driver
CHROMEDRIVER = "/Users/rolycg89/Downloads/chromedriver"


class Webdriver:
    def __init__(self):
        self.driver = None

    def open_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        os.environ["webdriver.chrome.driver"] = CHROMEDRIVER
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER, chrome_options=chrome_options)
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()

    def navigate(self, url):
        self.driver.get(url)
