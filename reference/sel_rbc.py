from api.sel.banks.fetch import download_rbc_mf_quotes
from selenium import webdriver
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": os.getcwd(),
  "download.prompt_for_download": False,
  "download.directory_upgrade": False,
  "safebrowsing_for_trusted_sources_enabled": False,
  "safebrowsing.enabled": False
})
browser = webdriver.Chrome(chrome_options=chrome_options)
td_test = download_rbc_mf_quotes(browser)