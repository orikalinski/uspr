import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup

from utils import close_thanks_page


class MarketBeatBrokerage(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.expert_ids = {6401, 2, 11651, 132, 4, 25862, 263, 8, 3593, 10, 8841, 1, 8209, 273, 19, 149, 6550, 21,
                           6681, 157, 17831, 426, 43, 1069, 51, 436, 52, 56, 14650, 1218, 194, 5573, 71, 9928, 17096,
                           204, 4687, 24912, 1745, 724, 5717, 86, 6101, 4701, 26718, 96, 737, 741, 489, 26089, 28651,
                           3308, 109, 119, 121, 12026, 126}
        self.base_url = "https://www.marketbeat.com"
        self.url = "{}/ratings/by-issuer/%s/".format(self.base_url)
        self.relevant_fields = ["date", "brokerage", "action", "rating", "price_target"]
        self.already_called_companies = set()

    @staticmethod
    def parse_price_field_into_dollar_price(price_text, date_dollar_converters):
        new_price_field = price_text.split("➝")[-1].strip()
        if new_price_field:
            currency, price = new_price_field.split()
            price = price.replace(",", "")
            return float(price) * date_dollar_converters.get(currency, 1)

    def get_all_data(self):
        for expert_id in self.expert_ids:
            page = self.scrape_url(self.url % expert_id)
            brokerage_companies_expert_ratings = self.get_expert_ratings(page)
            # SAVE brokerage_companies_expert_ratings HERE
            print(len(brokerage_companies_expert_ratings))

    @staticmethod
    def get_row_data(headers, row):
        cells = row.find_all("td")
        row_data = list()
        for cell in cells:
            row_data.append(cell.text)

        return dict(zip(headers, row_data))

    def get_company_experts(self, company_page, company_short_name):
        company_experts = list()

        rows = company_page.find_all("tr", {"role": "row"})
        headers = [header.text.lower().replace(" ", "_").replace("\n", " ") for header in rows[0].find_all("th")]
        rows = rows[1:]
        for row in rows:
            company_expert_details = self.get_row_data(headers, row)
            date = company_expert_details["date"]
            # replace it with a call to a file / db that gives you the converter the pre calculated
            date_to_dollar_converters = dict()
            price = self.parse_price_field_into_dollar_price(company_expert_details["price_target"],
                                                             date_to_dollar_converters.get(date, {}))
            company_expert_details["price_target"] = price
            company_expert_details["company_name"] = company_short_name
            company_experts.append(company_expert_details)

        return company_experts

    def handle_single_brokerage_company(self, row):
        company_experts = list()
        company_cell = row.find_all("td")[3]
        company_name = re.search("[a-zA-Z\s]+\(([A-Z]+)\)", company_cell.text).group(1)
        if company_name not in self.already_called_companies:
            extension = company_cell.find("a")["href"]
            company_url = "{base_url}{extension}price-target/?MostRecent=0".format(base_url=self.base_url,
                                                                                   extension=extension)
            company_page = self.scrape_url(company_url)
            company_experts = self.get_company_experts(company_page, company_name)
            self.already_called_companies.add(company_name)
        return company_experts

    def get_expert_ratings(self, page):
        rows = page.find_all("tr", {"role": "row"})
        if rows:
            data = list()
            for row in rows[1:]:
                data.extend(self.handle_single_brokerage_company(row))

            return data

    def scrape_url(self, url):
        self.browser.get(url)
        try:
            WebDriverWait(self.browser, 10) \
                .until(EC.presence_of_element_located((By.XPATH, ".//tr[@role='row']")))
        except TimeoutException:
            pass

        close_thanks_page(self.browser)
        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page


if __name__ == '__main__':
    market_beat_brokerage = MarketBeatBrokerage()
    market_beat_brokerage.get_all_data()
