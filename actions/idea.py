from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from connections.webdriver import Webdriver
from output import print_task, print_result, print_error
from static_vars import TEST_EMAIL, TEST_PASSWORD, SUCCESS, FAIL, ASSET, LINK_ASSET

IDEA_TITLE = 'Idea Bot Title Test'
IDEA_DESCRIPTION = 'Idea Bot Title Description'


class Idea:
    def __init__(self, url):
        self.webdriver = Webdriver()
        self.webdriver.open_browser()
        self.driver = self.webdriver.driver
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

        print()

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

        self.webdriver.close()
