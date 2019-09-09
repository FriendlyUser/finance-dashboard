""" ..todo:: Fetch performance on a individual fund level, probably add a fricking tab for that
to search by fund name and/or do it myself.

Also RBC can link to files, but TD bank cannot no chance of scrapping individual consistenly, unless I click and
copy the url, too much effort.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

import time
import pandas as pd
import sys
import requests

from util.get_env import get_env
from .parse_raw_html import parse_rbc_soup, parse_td_soup
from util.parse_config import get_config
def get_mf_data(browser, screenshot_name="td_bank_error.png"):
    """Selenium browser that is headless used locally

    ..todo:: move the hardcoded urls to the config file
    """
    browser.get("https://www.td.com/ca/en/asset-management/funds/solutions/mutual-funds/")
    try:
        # Ensure that the format of the web page hasn't changed
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, "tabsCarousel0_tab0"))
        )
        if get_env() not in ["production"]:
            # let additionally time for CI/CD 
            time.sleep(15)
        else:
            time.sleep(10)
    except TimeoutException as ex:
        # These general exceptions are probably selenium ones, include timeout
        print(ex)
        assert False

    td_bank_df = pd.DataFrame()
    try:
        td_bank_df = parse_td_soup(browser.page_source)
    except AssertionError as error:
        print(error)
        print('The parse_td_soup() function was not executed')
        browser.save_screenshot(screenshot_name)
    return td_bank_df

def download_rbc_mf_quotes(browser):
    """Selenium browser that is headless
    Gets data from rbc page by clicking on download button

    ..todo:: figure out why it doesn't work on headless
    """
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "/path/to/download/dir"}}
    command_result = browser.execute("send_command", params)
    browser.get("https://www.rbcgam.com/en/ca/products/mutual-funds/index?series=a,t&tab=prices")
    try:
        # Ensure that the format of the web page hasn't changed
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, "fundListMainTable"))
        )
    except TimeoutException as ex:
        # These general exceptions are probably selenium ones, include timeout
        print(ex)
        assert False
    
    elem = browser.find_element_by_xpath('//*[@id="app"]/main/div[3]/div/div[3]/div[3]/span[1]/a')
    elem.click()
    # Should be saved as Prices.csv

def scrap_rbc_data(browser, screenshot_name="rbc_data.png"):
    """Selenium browser that is headless
    """
    browser.get("https://www.rbcgam.com/en/ca/products/mutual-funds/index?series=a,t&tab=prices")
    try:
        # Ensure that the format of the web page hasn't changed
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, "fundListMainTable"))
        )
    except TimeoutException as ex:
        # These general exceptions are probably selenium ones, include timeout
        print(ex)
        assert False
    # print("Getting TD PAGE source")
    
    rbc_bank_df = pd.DataFrame()
    try:
        rbc_bank_df = parse_rbc_soup(browser.page_source)
    except AssertionError as error:
        print(error)
        print('The parse_rbc_soup() function was not executed')
        browser.save_screenshot(screenshot_name)
    print("Got values of interest")
    return rbc_bank_df

def gcf_td():
    config = get_config()
    gcf_base_url = config["gcs_api"]
    api_url = '{}/tdbank-data'.format(gcf_base_url)

    response = requests.get(api_url)
    # Errors usually happen due to hitting the wrong endpoint
    td_data_json = response.json()
    if response.status_code == 200:
        return parse_td_soup(td_data_json["td_html"])
    else:
        print("Fricking Error")
        return None

def gcf_rbc():
    config = get_config()
    gcf_base_url = config["gcs_api"]
    api_url = '{}/rbc_data'.format(gcf_base_url)

    response = requests.get(api_url)
    rbc_data_json = response.json()
    if response.status_code == 200:
        return parse_rbc_soup(rbc_data_json["rbc_html"])
    else:
        return None
