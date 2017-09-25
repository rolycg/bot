import psycopg2
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from connections.database import PostgresProd
from connections.webdriver import Webdriver
from output import print_task, print_result, print_error
from static_vars import TEST_EMAIL, TEST_PASSWORD, TEST_USERNAME, SUCCESS, FAIL, ASSET, LINK_ASSET

IDEA_TITLE = 'Idea Bot Title Test'
IDEA_SLUG = 'idea-bot-title-test'
IDEA_DESCRIPTION = 'Idea Bot Title Description'
COMMENT = 'Test Comment'


class Idea:
    def __init__(self, url):
        self.webdriver = Webdriver()
        self.webdriver.open_browser()
        self.driver = self.webdriver.driver
        self.database = PostgresProd()
        self.database.open_database()
        self.url = url
        self.result = {}

    def login(self):
        email = self.driver.find_element_by_id('exampleInputEmail1')
        email.send_keys(TEST_EMAIL)
        sleep(1)
        password = self.driver.find_element_by_id('exampleInputPassword1')
        password.send_keys(TEST_PASSWORD)
        sleep(1)
        submit = self.driver.find_element_by_id('bt-login')
        submit.click()

    def check_idea_popup(self):
        next_button = self.driver.find_element_by_xpath('//button[@class="btn btn-j create-next"]')
        try:
            assert next_button is not None
            print_result('Idea Popup Succeed')
            self.result['Idea popup'] = SUCCESS
        except AssertionError:
            print_error('Idea Popup fail')
            self.result['Idea popup'] = FAIL
        next_button.click()

    def mark_checkbox(self, checkboxs, value):
        for checkbox in checkboxs:
            parent = checkbox.find_element_by_xpath('..')
            if parent.text.strip().lower() == value.lower():
                self.driver.execute_script('arguments[0].click();', checkbox)
                sleep(2)
                break

    def check_tab(self, text, stage):
        marked_tab = self.driver.find_element_by_xpath(
            '//li[@class="uib-tab nav-item ng-scope ng-isolate-scope active"]/a')
        try:
            assert marked_tab.text == text
            print_result(stage + ' Succeed')
            self.result[stage] = SUCCESS
        except AssertionError:
            print_error(stage + ' Fail')
            self.result[stage] = FAIL
        print()

    def create_stage(self):
        title = self.driver.find_element_by_xpath('//input[@name="title"]')
        title.send_keys(IDEA_TITLE)
        description = self.driver.find_element_by_xpath('//textarea[@name="description"]')
        description.send_keys(IDEA_DESCRIPTION)

        checkboxs = self.driver.find_elements_by_xpath('//input[@type="checkbox"]')
        self.mark_checkbox(checkboxs, 'Animation')
        self.mark_checkbox(checkboxs, '0-5')
        sleep(1)
        checkboxs = self.driver.find_elements_by_xpath('//input[@type="checkbox"]')
        self.mark_checkbox(checkboxs, 'Action')

        continue_btn = self.driver.find_element_by_xpath('//div[@id="cont-bt"]/button')
        continue_btn.click()

        self.check_tab('2. Upload Media', 'Idea Create Stage')
        print()

    def upload_media(self):
        upload_file = self.driver.find_element_by_xpath('//input[@class="dz-hidden-input"]')
        upload_file.send_keys(ASSET)

        sleep(5)
        link = self.driver.find_element_by_id('add_link_btn')
        link.click()

        wait = WebDriverWait(self.driver, 3)
        alert = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="row toolKitModalW ng-scope"]')))
        sleep(1)
        link_input = alert.find_element_by_xpath(
            '//input[@class="form-control loginInput ng-pristine ng-untouched ng-valid ng-empty"]')
        link_input.send_keys(LINK_ASSET)
        sleep(1)
        button_add_link = alert.find_element_by_id('add_link_btn_modal')
        button_add_link.click()
        sleep(1)
        continue_btns = self.driver.find_elements_by_xpath('//button[@type="button"]')
        for continue_btn in continue_btns:
            if continue_btn.text.strip().lower() == 'continue':
                self.driver.execute_script('arguments[0].click();', continue_btn)
                break
        sleep(5)
        self.check_tab('3. Preview', 'Upload Media')

    def preview(self):
        title = self.driver.find_element_by_id('pdescr')
        title_header = self.driver.find_element_by_xpath('//h1[@class="ng-binding"]')
        try:
            assert title.text == IDEA_TITLE
            assert title_header.text == IDEA_TITLE
            print_result('Preview Succeed')
            self.result['Preview'] = SUCCESS
        except AssertionError:
            print_error('Preview Failed')
            self.result['Preview'] = FAIL

        save_as_draft_buttons = self.driver.find_elements_by_xpath('//button[@type="button"]')
        for save_as_draft_button in save_as_draft_buttons:
            if save_as_draft_button.text.strip().lower() == 'save as draft and continue':
                save_as_draft_button.click()
                break
        sleep(4)
        print()

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

    def fill(self, placeholder, value):
        address_line_1 = self.driver.find_element_by_xpath('//input[@placeholder="' + placeholder + '"]')
        address_line_1.send_keys(value)

    def submit(self):
        self.check_tab('4. Submit', 'Submit')
        sleep(1)
        self.select_option('country', 'United States')
        sleep(1)
        self.fill('Address Line 1...', '963 Shotgun Road')
        sleep(1)
        self.fill('City...', 'Miami')
        sleep(1)
        self.fill('State...', 'Florida')
        sleep(1)
        self.fill('Zip code...', '33326')
        sleep(1)
        self.fill('Phone number...', '9548451367')
        sleep(1)

        checkbox = self.driver.find_element_by_xpath('//input[@aria-label="I agree"]')
        self.driver.execute_script('arguments[0].click();', checkbox)

        signature = self.driver.find_element_by_xpath('//input[@name="signature"]')
        signature.send_keys('SIGNATURE NAME SIGNATURE LAST NAME')

        sleep(1)

        publish_btns = self.driver.find_elements_by_xpath('//button[@class="btn btn-j"]')
        for publish_btn in publish_btns:
            if publish_btn.text.strip().lower() == 'publish':
                publish_btn.click()
                break
        sleep(6)
        h1 = self.driver.find_element_by_id('usernameEdit')
        try:
            assert 'profile' in self.driver.current_url
            assert h1.text.strip() == TEST_USERNAME
            print_result('Submit Stage Succeed')
            self.result['Submit stage'] = SUCCESS
        except AssertionError:
            print_error('Submit Stage Failed')
            self.result['Submit stage'] = FAIL

    def delete_idea(self):
        delete_sql = "DELETE FROM ideas_idea WHERE ideas_idea.title='%s'" % IDEA_TITLE
        self.database.cursor.execute(delete_sql)
        self.database.commit()
        query_sql = "SELECT * FROM ideas_idea WHERE ideas_idea.title='%s'" % IDEA_TITLE
        self.database.cursor.execute(query_sql)
        exist = False
        try:
            for _ in self.database.cursor.fetchall():
                exist = True
                break
        except psycopg2.ProgrammingError:
            pass

        try:
            assert exist is False
            print_result('Delete Idea Succeed')
            self.result['Delete Idea'] = SUCCESS
        except AssertionError:
            print_error('Delete Idea Failed')
            self.result['Delete Idea'] = FAIL

    def comment_idea(self):
        self.webdriver.navigate('https://jazwings.com/ideas/%s' % IDEA_SLUG)
        text_area = self.driver.find_element_by_id('comment-textarea')
        text_area.send_keys(COMMENT)
        sleep(2)
        button = self.driver.find_element_by_id('sub-comm-btn')
        button.click()

        wait = WebDriverWait(self.driver, 3)
        alert = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="points_earned"]')))
        sleep(1)
        link_input = alert.find_element_by_id('points_anchor')
        try:
            assert link_input.text == '20 points.'
            print_result('Comment Idea Points Succeed')
            self.result['Comment Idea Points'] = SUCCESS
        except AssertionError:
            print_error('Comment Idea Points Failed')
            self.result['Comment Idea Points'] = FAIL

        sleep(2)
        comments = self.driver.find_elements_by_xpath('//div[@id="user-comment"]/p')
        tmp_comment = None
        for comment in comments:
            if comment.text == COMMENT:
                tmp_comment = True
        try:
            assert tmp_comment is not None
            print_result('Comment Idea Succeed')
            self.result['Comment Idea'] = SUCCESS
        except AssertionError:
            print_error('Comment Idea Failed')
            self.result['Comment Idea'] = FAIL

    def start(self):
        self.webdriver.navigate(self.url)
        sleep(5)
        login_element = self.driver.find_element_by_id('login')
        login_element.click()
        sleep(3)
        self.login()
        sleep(5)

        submit_idea = self.driver.find_element_by_id('submit-nav')
        self.driver.execute_script("arguments[0].click();", submit_idea)
        sleep(4)
        print_task('Testing Idea Popup')
        self.check_idea_popup()
        sleep(2)
        print_task('Testing Idea Create Stage')
        self.create_stage()
        sleep(2)
        print_task('Testing Upload Media Stage')
        self.upload_media()
        sleep(2)
        print_task('Testing Preview Stage')
        self.preview()
        sleep(2)
        self.submit()
        sleep(2)
        # self.delete_idea()
        self.webdriver.close()