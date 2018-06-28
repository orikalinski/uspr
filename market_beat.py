import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import close_popup


class MarketBeat(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome()#chrome_options=chrome_options)
        self.browser.set_window_size(1920, 1080)

    def click_on_top(self):
        action = ActionChains(self.browser)
        action.move_to_element_with_offset(el, 5, 5)
        action.click()
        action.perform()

    def find_displayed_element(self, xpath):
        elements = self.browser.find_elements_by_xpath(xpath)
        elements = [element for element in elements if element.is_displayed()]
        if elements:
            return elements[0]

    def scrape_url(self, url, expert):
        self.browser.get(url)
        try:
            WebDriverWait(self.browser, 15) \
                .until(EC.presence_of_element_located((By.XPATH, ".//input[@placeholder='Find a Company']")))
        except TimeoutException:
            print("Warning!")
            return

        close_popup(self.browser)
        search_box = self.find_displayed_element(".//input[@placeholder='Find a Company']")
        if search_box:
            search_box.send_keys(expert)
            time.sleep(5)
            search_option = self.browser.find_element_by_xpath(".//li[contains(@id, 'ui-id')]")
            search_option.click()


if __name__ == '__main__':
    market_beat = MarketBeat()
    market_beat.scrape_url("https://marketbeat.com", "Google")
