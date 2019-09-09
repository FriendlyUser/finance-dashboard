"""
A simple selenium test example written by python
"""

import unittest
import os
import sys
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..banks.fetch import scrap_rbc_data, download_rbc_mf_quotes
if sys.platform in [None, 'linux']:
    import HtmlTestRunner

class TestRBC(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False
        })
        # https://stackoverflow.com/questions/45631715/downloading-with-chrome-headless-and-selenium
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(1)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_rbc_quote(self):
        """Find carosuel tabs"""
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.getcwd()}}
        self.driver.execute("send_command", params)
        download_rbc_mf_quotes(self.driver)
        """Make sure Quotes.csv exists"""
        time.sleep(2)
        # self.assertTrue(os.path.exists("Quotes.csv"))

    def test_case_2(self):
        """Find and click Learn more button"""
        rbc_bank_df = scrap_rbc_data(self.driver)
        self.assertTrue(len(rbc_bank_df.columns) > 4)
        self.assertTrue(len(rbc_bank_df.index) >= 150)

if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()