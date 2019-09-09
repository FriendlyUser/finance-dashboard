
from ..api.sel.banks.fetch import gcf_rbc, gcf_td
import pandas as pd
import time

def gen_bank_info_gcf():
    # https://community.plot.ly/t/display-tables-in-dash/4707/13
    # Dynamic update https://dash.plot.ly/live-updates
    # add parameter to stub out values and run quickly :D
    rbc_data = pd.DataFrame()
    try:
        rbc_data = gcf_rbc()
        # rbc_data = rbc_data.drop(['Price ($)'], axis=1)
        print("Got here")
    except Exception as e:
        print(e)
    td_data = pd.DataFrame()
    try:
        td_data =  gcf_td()
        # td_data = td_data.drop(['Risk'], axis=1)
    except Exception as e:
        print(e)
    return rbc_data, td_data
