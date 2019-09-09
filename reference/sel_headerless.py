from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup, Comment, NavigableString
import pandas as pd

pd.set_option('display.width', 150)
pd.set_option('display.max_colwidth', 300)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://www.td.com/ca/en/asset-management/funds/solutions/mutual-funds/")
try:
    # Ensure that the format of the web page hasn't changed
    test_div = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.ID, "tabsCarousel0_tab0"))
    )
except TimeoutException as ex:
    # These general exceptions are probably selenium ones, include timeout
    print(ex)
print("Getting source")
browser_text = browser.page_source
# print(browser_text)

soup = BeautifulSoup(browser_text)
# remove scripts
def _remove_attrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = {}
    return soup

def stripTags(html, invalid_tags):
    soup = BeautifulSoup(html, features="lxml")
    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = stripTags(str(c), invalid_tags)
                s += str(c)
            tag.replaceWith(s)
    return soup

def stripOther(html):
    soup = BeautifulSoup(html,features="lxml")
    for script in soup(["img"]): # remove all javascript and stylesheet code
        script.extract()

    for tag in soup:
        for attribute in ["class", "data-aria"]: # You can also add id,style,etc in the list
            del tag[attribute]

    for child in soup:
        if isinstance(child, Comment):
            child.extract()

    return soup

tables = soup.findAll("table")
tables = stripOther(str(tables))
tables = stripTags(str(tables), ["span", "div"])
tables = soup.findAll("table")
i = 0
td_bank_df = pd.DataFrame()
for table in tables:
     if table.findParent("table") is None:
        try:
            print(str(table).encode("utf-8"))
        except:
            print('e')
        i = i + 1
        data = pd.read_html(str(table))
        td_bank_df= td_bank_df.append(data)
        data[0].to_latex('testing-{}.tex'.format(i))
        # data = pd.read_html(table)
        # data.to_csv('testing.csv')

def get_fund_code(td_bank_fund_name):
    """Td bank fund name (leftmost column)

    Example: TD Balanced Growth Fund - I Fund Code Multiple TDB970
    """
    fund_list = str(td_bank_fund_name).split()
    return fund_list[-1]

def get_strip_fund_code(td_bank_fund_name):
    """Td bank fund name (leftmost column)

    Example: TD Balanced Growth Fund - I Fund Code Multiple TDB970
    """
    fund_list = td_bank_fund_name.split()
    return ' '.join(fund_list[:-4])

td_bank_df.drop_duplicates(keep = "first", inplace = True) 
td_bank_df.columns = td_bank_df.iloc[0]
td_bank_df = td_bank_df[1:]
# iterating the columns 
# for col in td_bank_df.columns: 
#     print(col)
td_bank_df['Fund Code'] = td_bank_df.apply(lambda x: get_fund_code(x[td_bank_df.columns[0]]),axis=1)
td_bank_df[td_bank_df.columns[0]] = td_bank_df.apply(lambda x: get_strip_fund_code(x[td_bank_df.columns[0]]),axis=1)
# 5 columns
# risk filled with na,
# column headers the same
# random entry fund code has 