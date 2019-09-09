from bs4 import BeautifulSoup
import pandas as pd
from .util.mf_parsing import get_fund_code, get_strip_fund_code, stripCustom, stripTags, strip_rbc_footnote

def parse_td_soup(browser_text=""):
    """ Parse TD Mutual Fund Data
    """
    try:
        soup = BeautifulSoup(browser_text, features="lxml")
    except:
        print("Trying about")
        soup = BeautifulSoup(browser_text,features="lxml")
    tables = soup.findAll("table")
    tables = stripCustom(str(tables))
    tables = stripTags(str(tables), ["span", "div"])
    tables = soup.findAll("table")
    td_bank_df = pd.DataFrame()
    for table in tables:
        if table.findParent("table") is None:
            data = pd.read_html(str(table))
            td_bank_df= td_bank_df.append(data)
    # cleaning data, shifting headers to header row
    td_bank_df.drop_duplicates(keep = "first", inplace = True)
    td_bank_df = td_bank_df.reset_index(drop=True)
    if td_bank_df.empty == False:
        td_bank_df['Fund Code'] = td_bank_df.apply(lambda x: get_fund_code(x[td_bank_df.columns[0]]),axis=1)
        td_bank_df[td_bank_df.columns[0]] = td_bank_df.apply(lambda x: get_strip_fund_code(x[td_bank_df.columns[0]]),axis=1)
    else:
        print("Failed to retrieve data")
        assert (td_bank_df.empty == True), "TD INFO DID NOT BEHAVE AS EXPECTED"
    return td_bank_df

def parse_rbc_soup(browser_text=""):
    try:
        soup = BeautifulSoup(browser_text, features="lxml")
    except:
        soup = BeautifulSoup(browser_text, features="lxml")
    # Extract all tables from page, clean data and conver to single dataframe
    tables = soup.findAll("table")
    tables = stripCustom(str(tables))
    tables = stripTags(str(tables), ["span", "div"])
    tables = soup.findAll("table")
    rbc_bank_df = pd.DataFrame()
    for table in tables:
        if table.findParent("table") is None:
            data = pd.read_html(str(table))
            rbc_bank_df= rbc_bank_df.append(data)
    # cleaning data, shifting headers to header row
    rbc_bank_df.drop_duplicates(keep = "first", inplace = True)
    if rbc_bank_df.empty == False:
        rbc_bank_df['Fund name'] = rbc_bank_df.apply(lambda x: strip_rbc_footnote(x['Fund name']),axis=1)
    else:
        print("FAILED TAKING SCREENSHOT MAYBE SEND DISCORD MESSAGE")
        assert (rbc_bank_df.empty == True), "RBC INFO DID NOT BEHAVE AS EXPECTED"
    return rbc_bank_df
