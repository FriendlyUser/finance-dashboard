from selenium import webdriver
import os
from sys import platform

def gen_test_driver():
    """gen
    """
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd()
    })
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-gpu') 
    return webdriver.Chrome(chrome_options=chrome_options)