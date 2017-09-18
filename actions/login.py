from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from connections.webdriver import Webdriver
from output import print_task, print_result, print_error, SUCCESS, FAIL


class Login:
    def __init__(self, url):
        self.url = url
        self.webdriver = Webdriver()
        self.webdriver.open_browser()
        self.driver = self.webdriver.driver

        self.email = None
        self.password = None
        self.submit = None

        self.result = {}

    def load_elements(self):
        self.email = self.driver.find_element_by_id('exampleInputEmail1')
        self.password = self.driver.find_element_by_id('exampleInputPassword1')
        self.submit = self.driver.find_element_by_id('bt-login')

    def login_link(self):
        login_element = self.driver.find_element_by_id('login')
        login_element.click()
        sleep(2)

        self.load_elements()

        try:
            assert self.driver.current_url == 'https://jazwings.com/login'
            assert self.email is not None
            assert self.password is not None
            assert self.submit is not None
            self.result['Login link'] = SUCCESS
        except AssertionError:
            print_error('Login link raises an error')
            self.result['Login link'] = FAIL

        print_result('Login link Succeed')
        print()

    @staticmethod
    def clear_input(element, content):
        element.clear()
        element.send_keys(content)

    def invalid_email(self, username, password, task):
        self.clear_input(self.email, username)
        self.clear_input(self.password, password)
        self.submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.driver, 2)
        alert = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="toast-container"]')))
        text = alert.text
        sleep(5)
        try:
            assert text == 'Unable to log in with provided credentials.'
            self.result[task] = SUCCESS
            print_result('Invalid email Succeed')
        except AssertionError:
            print_error('Login with random text raises an error')
            self.result[task] = FAIL
        sleep(1)
        print()

    def valid_login(self, username=False):
        self.load_elements()

        if username:
            self.clear_input(self.email, 'testemail')
        else:
            self.clear_input(self.email, 'testemail1989@gmail.com')
        self.clear_input(self.password, '123456abc')

        self.submit.send_keys(Keys.RETURN)

        logged_url = 'https://jazwings.com/discover#discHcont'
        wait = WebDriverWait(self.driver, 3)
        alert = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="toast-container"]')))
        text = alert.text
        sleep(5)

        try:
            assert self.driver.current_url == logged_url
            assert text == 'cool, have fun!!'
            self.result['Valid Login'] = SUCCESS
            if username:
                print_result('Valid Login with username Succeed')
            else:
                print_result('Valid Login with email Succeed')
        except AssertionError:
            if username:
                print_error('Valid Login with username raises an error')
            else:
                print_error('Valid Login with email raises an error')
            self.result['Valid Login'] = FAIL
        sleep(1)
        print()

    def logout(self, redirect=True):
        toggle = self.driver.find_elements_by_xpath('//a[@class="dropdown-toggle"]')[0]
        toggle.click()
        links = self.driver.find_elements_by_xpath('//ul[@class="dropdown-menu"]/li/a')
        for link in links:
            if link.text == 'Logout':
                link.click()
        sleep(5)
        login = self.driver.find_element_by_id('login')
        try:
            assert self.driver.current_url == self.url
            assert login is not None
            if redirect:
                login.click()
            sleep(1)
            self.result['Valid Logout'] = SUCCESS
            print_result('Valid logout Succeed')
        except AssertionError:
            print_error('Logout raises an error')
            self.result['Valid Logout'] = FAIL
        sleep(1)
        print()

    def start(self):
        self.webdriver.navigate(self.url)
        sleep(5)
        print_task('Testing login link')
        self.login_link()
        print_task('Testing invalid email - Random Text')
        self.invalid_email(username='not_a_valid_email', password='random_password', task='Invalid email - Random Text')
        print_task('Testing invalid email - Valid Username Wrong Password')
        self.invalid_email(username='rolycg89@gmail.com', password='random_password',
                           task='Invalid email - Valid Username Wrong Password')
        print_task('Testing valid credentials - Email')
        self.valid_login()
        print_task('Testing valid logout')
        self.logout()
        print_task('Testing valid credentials - username')
        self.valid_login(username=True)
        self.logout()

        self.driver.quit()
