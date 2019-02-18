from seleniumrequests import Chrome
from selenium.webdriver import ChromeOptions

from fake_useragent import UserAgent
import csv
import os
import re

YEAR = '2019'
FED_TAX_URL = f'https://taxfoundation.org/{YEAR}-tax-brackets/'
TABLE_CAPTION_TEXT = f"Table 1. Tax Brackets and Rates, {YEAR}"
FILENAME = f'federal_tax_rates_{YEAR}.csv'


class FedScrape(object):
    """
    Scraper to scrape the federal tax bracket information for each status type
    """

    def __init__(self, data_dir='data/', filename=FILENAME):
        self.data_dir = data_dir
        self.filename = filename
        self._rate_dict = dict()
        self.header_fields = []

    def setup_driver(self, headless=True):
        """Establish chrome options for and instantiate driver"""

        ua = UserAgent().chrome
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument(f'--user-agent={ua}')
        if headless: chrome_options.add_argument('headless')

        driver = Chrome(options=chrome_options)

        return driver

    def get_data_from_row(self, row):
        """Get data from a given row"""
        for field in self.header_fields:
            field_elem = row.find_element_by_xpath(
                f'./td[@data-title="{field}"]'
            )
            self._rate_dict[field] = re.sub('[\$|\%|,]', '', field_elem.text)

    def get_data_from_table(self, table):
        """Get data from the table element to write to csv"""
        print("Find Header fields")
        header_fields_list = table.find_elements_by_xpath('./thead/tr/th')
        self.header_fields = [field.text for field in header_fields_list]

        print("Find Rows and iterate through them")
        rows = table.find_elements_by_xpath('./tbody/tr')

        count = 1
        for row in rows:
            print(f"iterating through row {count}")
            self.get_data_from_row(row)
            self._write_data()
            count += 1

    def _write_data(self):
        """Write individual line to CSV"""
        dir = self.data_dir
        outfile = dir+self.filename
        if not os.path.exists(dir):
            print(f"Creating {dir}")
            os.makedirs(dir)

        # write the header if it's a new file
        if not os.path.isfile(outfile):
            print(f"Creating {outfile} and writing the header")
            with open(outfile, 'w') as fou:
                dw = csv.DictWriter(fou, delimiter=',',
                                    fieldnames=self.header_fields)
                dw.writeheader()

        # write the output of the dictionary to the file
        with open(outfile, 'a') as fou:
            dw = csv.DictWriter(fou, delimiter=',',
                                fieldnames=self.header_fields)
            dw.writerow(self._rate_dict)
            self._rate_dict.clear()

    def run(self):
        """Workhorse function"""
        print("Set Up Driver")
        self.driver = self.setup_driver()

        print("Go to URL")
        self.driver.get(FED_TAX_URL)

        print("Find the correct table")
        tables = self.driver.find_elements_by_xpath('//table')
        table = [
            table for table in tables if
            table.find_element_by_xpath('./caption').text==TABLE_CAPTION_TEXT
        ][0]

        print("Get the data from the table")
        self.get_data_from_table(table)

        print("Scrape Complete")
        self.driver.close()


if __name__ == '__main__':
    fed_scrape = FedScrape()
    fed_scrape.run()
