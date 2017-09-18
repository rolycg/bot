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

    def login_link(self):
        login_element = self.driver.find_element_by_id('login')
        login_element.click()
        sleep(2)

        self.email = self.driver.find_element_by_id('exampleInputEmail1')
        self.password = self.driver.find_element_by_id('exampleInputPassword1')
        self.submit = self.driver.find_element_by_id('bt-login')

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

    def invalid_email(self, username, password, task):
        self.email.send_keys(username)
        self.password.send_keys(password)
        self.submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.driver, 2)
        alert = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="toast-container"]')))
        try:
            assert alert.text == 'Unable to log in with provided credentials.'
            self.result[task] = SUCCESS
        except AssertionError:
            print_error('Login with random text raises an error')
            self.result[task] = FAIL
        sleep(1)

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

        self.driver.quit()
