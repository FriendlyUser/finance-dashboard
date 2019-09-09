"""Refactor to calc at some point
"""
from banks.util.parse_config import get_config
import pandas as pd
import re
from ..yahoo.ticker import get_ticker_data
def calc_stock_profit():
    """Calculating profit with ticker first indexes

    Input: None

    Output: 
        stocks_df --- list of stocks with profit only Open and Profit
        profit_values --- list of profits
    """
    profit_values = []
    config = get_config()
    # keys for td mutual funds
    yahoo_keys = list(config["stocks"].keys())
    stocks_df = get_ticker_data(yahoo_keys)
    for stock in config["stocks"].keys():
        buy_price = config["stocks"][stock]["buy_price"]
        num_units = config["stocks"][stock]["num_units"]
        stocks_df["Profit", stock] = ( stocks_df["Open", stock] - buy_price) * num_units
        profit_values.append(stocks_df["Profit", stock])
    stocks_df = stocks_df.drop(columns=["Adj Close", "Close", "High", "Low", "Volume"], axis=1)
    return stocks_df, profit_values

def calc_stock_profit_ticker():
    """Calculating profit with ticker first indexes
        Not used anymore
    """
    config = get_config()
    # keys for td mutual funds
    yahoo_keys = list(config["stocks"].keys())
    stocks_df = get_ticker_data(yahoo_keys)
    for stock in config["stocks"].keys():
        buy_price = config["stocks"][stock]["buy_price"]
        num_units = config["stocks"][stock]["num_units"]
        stocks_df[stock, "Profit"] = ( stocks_df[stock, "Close"] - buy_price) * num_units
    return stocks_df


def calc_profit(rbc_df, td_df):
    # Get rows of interest
    # reads mf keys from config
    config = get_config()
    # keys for td mutual funds
    td_keys = config["mf"]["td"].keys()
    # get prices of interest
    profit_values = []
    td_profit_df = pd.DataFrame(columns=["Fund Code", "Fund Name", 
        "Buy Price", "Units", "Current Price", "Profit"])
    for mf_sum in td_keys:
        mf_data = config["mf"]["td"][mf_sum]
        mf_row = td_df.loc[td_df['Fund Code'] == mf_sum]
        curr_price = mf_row.iloc[0][1]
        curr_profit = (curr_price - mf_data["buy_price"]) * mf_data["num_units"]
        mf_df_temp = pd.DataFrame([[mf_sum, mf_data["name"], 
            mf_data["buy_price"], mf_data["num_units"],
            curr_price,
            curr_profit
        ]], columns=["Fund Code", "Fund Name", 
        "Buy Price", "Units", "Current Price", "Profit"])
        td_profit_df=td_profit_df.append(mf_df_temp)
        profit_values.append(curr_profit)

    rbc_keys = config["mf"]["rbc"].keys()
    rbc_profit_df = pd.DataFrame(columns=["Fund Code", "Fund Name", 
        "Buy Price", "Units", "Current Price", "Profit"])
    for mf_sum in rbc_keys:
        mf_data = config["mf"]["rbc"][mf_sum]
        mf_row = rbc_df.loc[rbc_df['Code'] == mf_sum]
        curr_price_whole = mf_row.iloc[0][4]
        # remove everything that isn't a number
        trim = re.compile(r'[^\d.,]+')
        curr_price = float(trim.sub('', curr_price_whole))
        curr_profit = (curr_price - mf_data["buy_price"]) * mf_data["num_units"]
        mf_df_temp = pd.DataFrame([[mf_sum, mf_data["name"], 
            mf_data["buy_price"], mf_data["num_units"],
            curr_price,
            curr_profit
        ]], columns=["Fund Code", "Fund Name", 
        "Buy Price", "Units", "Current Price", "Profit"])
        profit_values.append(curr_profit)
        rbc_profit_df=rbc_profit_df.append(mf_df_temp)
    return td_profit_df.append(rbc_profit_df), profit_values
