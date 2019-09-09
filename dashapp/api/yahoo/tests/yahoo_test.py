import unittest
from dashapp.api.sel.banks.fetch import get_mf_data, parse_td_soup, parse_rbc_soup
from dashapp.api.sel.banks.util.parse_config import get_config
import json
import os
from dashapp.api.sel.banks.util.get_env import get_env
import sys
from dashapp.api.sel.calc_profit import calc_stock_profit
from dashapp.api.yahoo.ticker import get_ticker_data
curr_env = get_env()
if curr_env == "production":
    import HtmlTestRunner

class TestYahoo(unittest.TestCase):
    def test_stock_profit(self):
        profit = calc_stock_profit()
        return profit

    def test_stock_format(self):
        config = get_config()
        yahoo_keys = list(config["stocks"].keys())
        stocks_df = get_ticker_data(ticker_list=yahoo_keys)
        for stock in config["stocks"].keys():
            buy_price = config["stocks"][stock]["buy_price"]
            num_units = config["stocks"][stock]["num_units"]
            stocks_df["Profit", stock] = ( stocks_df["Close", stock] - buy_price) * num_units
        stocks_df = stocks_df.drop(columns=["Adj Close", "Close", "High", "Low", "Volume"], axis=1)
        return stocks_df

if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()
