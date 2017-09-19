from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from connections.webdriver import Webdriver
from output import print_task, print_result, print_error, SUCCESS, FAIL
from static_vars import FACEBOOK_EMAIL, FACEBOOK_PASSWORD, USERNAME, LOGGED_URL, PASSWORD, EMAIL


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
            print_result('Login link Succeed')
        except AssertionError:
            print_error('Login link raises an error')
            self.result['Login link'] = FAIL

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
            self.clear_input(self.email, USERNAME)
        else:
            self.clear_input(self.email, EMAIL)
        self.clear_input(self.password, PASSWORD)

        self.submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.driver, 3)
        alert = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="toast-container"]')))
        text = alert.text
        sleep(5)

        try:
            assert self.driver.current_url == LOGGED_URL
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

    def delete_cookies(self):
        self.driver.delete_all_cookies()

    def facebook(self, success=True):
        self.load_elements()
        main_handle = self.driver.current_window_handle

        facebook = self.driver.find_element_by_id('login-fb')
        facebook.click()
        another_window = list(set(self.driver.window_handles) - {main_handle})[0]
        self.driver.switch_to.window(another_window)
        sleep(3)
        email = self.driver.find_element_by_id('email')
        if success:
            email.send_keys('rcruz@jazwings.com')
        else:
            email.send_keys(FACEBOOK_EMAIL)
        sleep(1)
        password = self.driver.find_element_by_id('pass')
        if success:
            password.send_keys('Gerr@rd4')
        else:
            password.send_keys(FACEBOOK_PASSWORD)
        sleep(1)
        login = self.driver.find_element_by_xpath('//label[@id="loginbutton"]/input')
        login.click()
        sleep(5)
        self.driver.switch_to.window(main_handle)
        sleep(1)
        if success:
            try:
                assert self.driver.current_url == LOGGED_URL
                print_result('Facebook success Succeed')
                self.result['Facebook success'] = SUCCESS
            except AssertionError:
                print_error('Facebook success login raises an error')
                self.result['Facebook success'] = FAIL
        else:
            try:
                assert self.driver.current_url == 'https://jazwings.com/login'
                print_result('Facebook failed Succeed')
                self.result['Facebook failed'] = SUCCESS
            except AssertionError:
                print_error('Facebook failed login raises an error')
                self.result['Facebook failed'] = FAIL
        sleep(1)
        print()

    def google(self):
        self.load_elements()
        main_handle = self.driver.current_window_handle

        google = self.driver.find_element_by_id('login-gl')
        google.click()
        another_window = list(set(self.driver.window_handles) - {main_handle})[0]
        self.driver.switch_to.window(another_window)
        sleep(3)

        email = self.driver.find_element_by_id('identifierId')
        email.send_keys('rcruz@jazwings.com')
        next = self.driver.find_element_by_id('identifierNext')
        next.click()
        sleep(2)

        password = self.driver.find_element_by_xpath('//input[@name="password"]')
        password.send_keys('5DDydr9r')
        next = self.driver.find_element_by_id('passwordNext')
        next.click()
        sleep(5)
        self.driver.switch_to.window(main_handle)

        try:
            assert self.driver.current_url == LOGGED_URL
            print_result('Google + success Succeed')
            self.result['Google + success'] = SUCCESS
        except AssertionError:
            print_error('Google + success login raises an error')
            self.result['Google + success'] = FAIL

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
        print_task('Testing facebook login - Success')
        self.facebook()
        self.logout()
        print_task('Testing google + login - Success')
        self.google()
        self.logout()

        self.webdriver.close()
