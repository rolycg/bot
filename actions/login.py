
from connections.database import PostgresProd
from connections.webdriver import Webdriver
from output import print_task, print_result, print_error, SUCCESS, FAIL
from time import sleep


class Login:

    def __init__(self, url):
        # self.postgres = PostgresProd()
        # self.postgres.open_database()

        self.driver = Webdriver()
        self.driver.open_browser()
        self.driver.navigate(url)
        self.result = {}

    def start(self):
        print_task('Testing invalid email')

        login_element = self.driver.find_element_by_id('login')
        login_element.click()
        sleep(2)

        email = self.driver.find_element_by_id('exampleInputEmail1')
        password = self.driver.find_element_by_id('exampleInputPassword1')
        try:
            assert self.driver.getCurrentUrl() == 'https://jazwings.com/login'
            assert email is not None
            assert password is not None
            self.result['Login link'] = SUCCESS
        except AssertionError:
            print_error('Login link raises an error')
            self.result['Login link'] = FAIL

        print_result('Login link Succeed')

        self.driver.close()
