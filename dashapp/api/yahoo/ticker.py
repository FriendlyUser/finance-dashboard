import yfinance as yf
from datetime import datetime
from datetime import date, timedelta
def get_ticker_metadata(ticker="AMZN"):
    ticker = yf.Ticker(ticker)
    return ticker.info

def get_ticker_history(ticker="AMZN", time_frame="max"):
    ticker = yf.Ticker(ticker)
    return ticker.history(period=time_frame)

def get_ticker_actions(ticker="AMZN"):
    ticker = yf.Ticker(ticker)
    return ticker.actions

def get_ticker_dividends(ticker="AMZN"):
    ticker = yf.Ticker(ticker)
    return ticker.dividends

def get_ticker_splits(ticker="AMZN"):
    ticker = yf.Ticker(ticker)
    return ticker.splits

def calculate_the_next_week_day(day_now):
    """utility function to get viable days: 
        sat -> fri
        sun -> fri
    """   
    if day_now.isoweekday()== 6:
        day_now -= timedelta(days=1)
    elif day_now.isoweekday()== 7:
        day_now -= timedelta(days=2)
    return day_now

def get_ticker_data(ticker_list=["SPY AAPL"], single_day=True, search_date=""):
    ticker_string = ' '.join(ticker_list)
    curr_date = calculate_the_next_week_day(datetime.today()).strftime('%Y-%m-%d')
    previous_date = calculate_the_next_week_day(date.today() - timedelta(1)).strftime('%Y-%m-%d')
    if single_day:
        # figure out way to round to last friday
        if search_date != "":
            curr_date = search_date
        data = yf.download(tickers=ticker_string, start=previous_date, end=curr_date)
        r, _ = data.shape
        if r > 1:
            # get the highest date
            print(data)
            # Assuming the data is ordered
            data = data.iloc[0]

    else:
        data = yf.download(ticker_string, start='2018-02-01', end=curr_date,
                   group_by="ticker")
    return data
