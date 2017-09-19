from time import sleep
import requests
import json

from selenium.common.exceptions import NoSuchElementException
import psycopg2


from connections.database import PostgresProd
from connections.webdriver import Webdriver
from static_vars import FAIL, SUCCESS
from output import print_task, print_result, print_error
from static_vars import CONFIRM_URL, REGISTER_URL, CREATED_EMAIL, CREATED_FIRST_NAME, CREATED_LAST_NAME, \
    CREATED_PASSWORD, CREATED_USERNAME, CREATED_SOURCE


class Signup:
    def __init__(self, url):
        self.url = url
        self.webdriver = Webdriver()
        self.webdriver.open_browser()
        self.driver = self.webdriver.driver
        self.result = {}
        self.database = PostgresProd()
        self.database.open_database()
        self.cc_api_key = '8frjx94rfxgfkxt6c75usrrw'
        self.cc_token = 'ef2ab36e-f853-4546-8ebe-e0113e85cb5b'

    @staticmethod
    def fill_field(field, value):
        field.clear()
        field.send_keys(value)

    def select_option(self, element, value):
        try:
            select = self.driver.find_element_by_id(element)
        except NoSuchElementException:
            select = self.driver.find_element_by_xpath('//select[@name="' + element + '"]')
        all_options = select.find_elements_by_tag_name("option")
        for option in all_options:
            if option.text.lower().strip() == value.lower():
                option.click()
                break

    def create_account(self):
        account_link = self.driver.find_element_by_xpath('//a[@ui-sref="createAccount"]')
        self.driver.execute_script("arguments[0].click();", account_link)
        # account_link.click()
        sleep(2)
        try:
            assert self.driver.current_url == REGISTER_URL
            self.result['Creation link'] = SUCCESS
            print_result('Creation link Succeed')
        except AssertionError:
            self.result['Creation link'] = FAIL
            print_error('Creation link Failed')

        first_name = self.driver.find_element_by_id('firstName')
        self.fill_field(first_name, CREATED_FIRST_NAME)
        sleep(1)
        last_name = self.driver.find_element_by_xpath('//input[@name="lastName"]')
        self.fill_field(last_name, CREATED_LAST_NAME)
        sleep(1)
        self.select_option('birthday-month', 'January')
        sleep(1)
        self.select_option('birthday-day', '01')
        sleep(1)
        self.select_option('birthday-year', '1980')
        sleep(1)
        email = self.driver.find_element_by_xpath('//input[@name="email"]')
        self.fill_field(email, CREATED_EMAIL)
        sleep(1)
        password = self.driver.find_element_by_xpath('//input[@name="password"]')
        self.fill_field(password, CREATED_PASSWORD)
        sleep(1)
        username = self.driver.find_element_by_id('displayName')
        self.fill_field(username, CREATED_USERNAME)
        sleep(1)
        self.select_option('country', CREATED_SOURCE)
        sleep(1)
        rules = self.driver.find_element_by_xpath('//input[@name="rules"]')
        rules.click()
        sleep(2)
        submit = self.driver.find_element_by_id('create-login-bt')
        self.driver.execute_script("arguments[0].click();", submit)
        sleep(5)

        check = False
        username_links = self.driver.find_elements_by_xpath('//a[@href="#"]')
        for username_link in username_links:
            if username_link.text == CREATED_USERNAME:
                check = True
        try:
            assert self.driver.current_url == CONFIRM_URL
            assert check
            print_result('Create User Succeed')
            self.result['Create User'] = SUCCESS
        except AssertionError:
            print_result('Create User Failed')
            self.result['Create User'] = FAIL

        print()

    def get_id_user(self):
        return self.database.cursor.execute('SELECT id FROM auth_user WHERE username=%s' % CREATED_USERNAME)

    def delete_user(self):
        select_query = "SELECT id FROM auth_user WHERE username='%s'" % CREATED_USERNAME
        user_id = None
        self.database.cursor.execute(select_query)
        for _id in self.database.cursor.fetchall():
            user_id = _id[0]

        gamification_query = "DELETE FROM gamification_pointactionperson WHERE user_id='%s'" % user_id
        self.database.cursor.execute(gamification_query)

        query = "DELETE FROM people_person WHERE user_ptr_id IN (SELECT id FROM auth_user WHERE username='%s')" % CREATED_USERNAME
        self.database.cursor.execute(query)
        self.database.prod.commit()

        self.database.cursor.execute(select_query)
        exist = False
        try:
            for _ in self.database.cursor.fetchall():
                exist = True
                break
        except psycopg2.ProgrammingError:
            pass

        self.database.cursor.execute("SELECT dob FROM people_person WHERE user_ptr_id='%s'" % str(user_id))
        try:
            for _ in self.database.cursor.fetchall():
                exist = True
                break
        except psycopg2.ProgrammingError:
            pass
        try:
            assert exist is False
            print_result('Delete User Succeed')
            self.result['Delete User'] = SUCCESS
        except AssertionError:
            print_error('Delete User Failed')
            self.result['Delete User'] = FAIL

    def check_cc(self):
        get_url = 'https://api.constantcontact.com/v2/contacts?api_key=8frjx94rfxgfkxt6c75usrrw&email=' + CREATED_EMAIL
        get_data = {
            'headers': {
                'Authorization': 'Bearer ef2ab36e-f853-4546-8ebe-e0113e85cb5b',
                'Content-Type': 'application/json'
            }
        }
        r = requests.request('GET', get_url, **get_data)
        if r.status_code == 200:
            user = json.loads(r.content)
            contacts_id = None
            try:
                contacts_id = user['results'][0]['id']
            except:
                pass
            try:
                assert contacts_id is not None
                print_result('Contact Contact User Added Succeed')
                self.result['Contact Contact User Added'] = SUCCESS
            except AssertionError:
                print_error('Contact Contact User Added Fail')
                self.result['Contact Contact User Added'] = FAIL

            delete_url = 'https://api.constantcontact.com/v2/contacts/' + contacts_id + '?api_key=8frjx94rfxgfkxt6c75usrrw'
            rd = requests.request('DELETE', delete_url, **get_data)
            try:
                assert str(rd.status_code) == '204'
                print_result('Contact Contact User Delete Succeed')
                self.result['Contact Contact User Delete'] = SUCCESS
            except AssertionError:
                print_error('Contact Contact User Delete Fail')
                self.result['Contact Contact User Delete'] = FAIL

    def check_points(self):
        toggle = self.driver.find_elements_by_xpath('//a[@class="dropdown-toggle"]')[0]
        toggle.click()
        links = self.driver.find_elements_by_xpath('//ul[@class="dropdown-menu"]/li/a')
        for link in links:
            if link.text == 'Profile':
                link.click()
        sleep(5)
        span = self.driver.find_element_by_id('creator_pts')
        try:
            assert '100' in span.text
            print_result('User Points Succeed')
            self.result['User Points'] = SUCCESS
        except AssertionError:
            self.result['User Points'] = FAIL
            print_error('User Points Failed')

    def start(self):
        self.webdriver.navigate(self.url)
        sleep(5)
        login_element = self.driver.find_element_by_id('login')
        login_element.click()
        sleep(2)
        print_task('Testing Create Account')
        self.create_account()
        sleep(3)
        print_task('Testing Contact Constant')
        self.check_cc()
        sleep(3)
        print_task('Testing User Points')
        self.check_points()
        sleep(3)
        print_task('Testing Delete User')
        self.delete_user()

        self.database.close()
