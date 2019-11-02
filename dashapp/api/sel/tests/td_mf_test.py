"""
A simple selenium test example written by python
"""

import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ..banks.fetch import get_mf_data, parse_td_soup
from ..banks.util.get_env import get_env
curr_env = get_env()
if curr_env == "production":
    import HtmlTestRunner

class TestRegexMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_error(self):
        """ This test should be marked as error one. """
        # raise ValueError

    def test_fail(self):
        """ This test should fail. Been alternated"""
        self.assertNotEqual(1, 2)

    @unittest.skip("This is a skipped test.")
    def test_skip(self):
        """ This test should be skipped. """
        pass

    def test_regex(self):
        td_fund_name = 'TD Global Entertainment and Communications Fund (US$) - I Fund Code Multiple TDB223'
        first, *middle, last = td_fund_name.split()
        # print(last)
        self.assertEqual(last, "TDB223")
            
class TestTDScrap(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(1)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_td_tabs(self):
        """Find carosuel tabs"""
        self.driver.get("https://www.td.com/ca/en/asset-management/funds/solutions/mutual-funds/")
        try:
            # Ensure that the format of the web page hasn't changed
            test_div = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "tabsCarousel0_tab0"))
            )
        except TimeoutException as ex:
            print("Couldn't find tabsCarousel0_tab0 for mutual fund data")
            self.fail(ex.msg)

    def test_case_2(self):
        """Find and click Learn more button"""
        td_bank_df = get_mf_data(self.driver)
        print(td_bank_df)
        if td_bank_df.empty == True:
            print("Empty Detected")
        else:
            # Should be at least 147
            self.assertTrue(len(td_bank_df.columns) >= 1)
            self.assertTrue(len(td_bank_df.index) >= 145)

if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()