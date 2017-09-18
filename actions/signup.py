
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from connections.webdriver import Webdriver
from output import print_task, print_result, print_error, SUCCESS, FAIL

LOGGED_URL = 'https://jazwings.com/discover#discHcont'


class Signup:
    def __init__(self, url):
        self.url = url
        self.webdriver = Webdriver()
        self.webdriver.open_browser()
        self.driver = self.webdriver.driver
        self.result = {}

    def start(self):
        pass
