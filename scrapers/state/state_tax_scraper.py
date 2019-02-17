from seleniumrequests import Chrome
from selenium.webdriver import ChromeOptions

from fake_useragent import UserAgent
import csv
import os
import re
import time
import random


class StateScrape(object):
    """
    Scraper to scrape the state tax bracket information for each status type
    """

    def __init__(self, data_dir: str = "data/", year: str = "2019"):
        self.year = year
        self.data_dir = data_dir
        self._rate_dict = dict()
        self.header_fields = []

    def __del__(self):
        print("Closing Driver")
        self.driver.close()

    def random_wait(self, wait_min=1.5, wait_max=3, verbose=False):
        """Wait for a random amount of time"""
        random_time = random.uniform(wait_min, wait_max)
        if verbose: print(f"Sleeping for {random_time:.2f} seconds")
        time.sleep(random_time)

    def setup_driver(self, headless: bool = True) -> Chrome:
        """Establish chrome options for, and instantiate, the driver"""
        ua = UserAgent().chrome

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument(f'--user-agent={ua}')
        if headless: chrome_options.add_argument('headless')

        driver = Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)

        return driver

    def get_data_from_row(self, row):
        """Get data from a given row"""

        # get all td rows and then for each,
        # assign it to the proper header
        # you'll have to do this via index since no string indicators in there
        field_elems = row.find_elements_by_xpath('./td')
        for i in range(len(field_elems)):
            field_text = re.sub('[\+|\$|\%|,]', '', field_elems[i].text)
            self._rate_dict[self.header_fields[i]] = field_text

    def get_data_from_table(self, table):
        """Get the information from the tax table"""

        print("Find Header fields")
        header_fields_list = table.find_elements_by_xpath(
            './thead/tr/th'
        )
        self.header_fields = [field.text for field in header_fields_list]

        print("Find Rows and iterate through them")
        rows = table.find_elements_by_xpath('./tbody/tr')

        count = 1
        for row in rows:
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
        self.driver = self.setup_driver(headless=False)  # change to True once done

        # go to main site
        self.driver.get('https://www.tax-brackets.org/')

        # click drop down button
        self.driver.find_element_by_xpath(
            '//a[contains(text(), "State Tax Brackets")]'
        ).click()

        # get list of states and put into dict
        states = self.driver.find_elements_by_xpath(
            '//ul[@class="dropdown-menu"]/li/a' +
            '[starts-with(@href, "https://www.tax-brackets.org")]'
        )
        states_dict = {elem.text: elem.get_attribute('href')+'/single'
                       for elem in states}

        # iterate through states and make new file with data for each
        for key, val in states_dict.items():

            # set state and filename
            print(f"Looking through {key}")
            self.state = key.lower().strip().replace(' ', '_')
            self.filename = f'state_tax_rates_{self.state}_{self.year}.json'

            print(f"Go to URL {val}")
            self.driver.get(val)

            print("Get the table stuff")
            table = self.driver.find_element_by_xpath('//table')
            self.get_data_from_table(table)

            # wait random period of time
            self.random_wait(wait_min=5, wait_max=10, verbose=True)

        print("Scrape Complete")


if __name__ == '__main__':

    state_scrape = StateScrape()
    state_scrape.run()
