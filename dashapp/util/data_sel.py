from ..api.sel.banks.util.gen_webdriver import gen_test_driver
from ..api.sel.banks.fetch import scrap_rbc_data, get_mf_data
import pandas as pd
import time
def gen_bank_info_sel():
    # https://community.plot.ly/t/display-tables-in-dash/4707/13
    # Dynamic update https://dash.plot.ly/live-updates
    # add parameter to stub out values and run quickly :D
    browser = gen_test_driver()
    rbc_data = pd.DataFrame()
    try:
        rbc_data = scrap_rbc_data(browser)
        # Don't drop anything
        # rbc_data = rbc_data.drop(['Price ($)'], axis=1)
        print("Got here")
    except Exception as e:
        print(e)
    finally:
        # browser.quit()
        time.sleep(5)
    # browser = gen_test_driver()
    td_data = pd.DataFrame()
    try:
        td_data =  get_mf_data(browser)
        td_data = td_data.drop(['Risk'], axis=1)
    except Exception as e:
        print(e)
    finally:
        browser.quit()
    # browser.quit()
    return rbc_data, td_data
