from flask import Blueprint, render_template, request, jsonify
yahoo = Blueprint('yahoo', __name__)
from .ticker import *

@yahoo.route('/yahoo/data')
def get_quote_data():
    # here we want to get the value of user (i.e. ?user=some-value)
    quotes = request.args.get('quotes')
    quote_list = quotes.split(",")
    data = get_ticker_data(quote_list)
    return data.to_html()

@yahoo.route('/yahoo/metadata/<stock>')
def flask_get_stock_metadata(stock):
    data = get_ticker_metadata(stock)
    return jsonify(data)

@yahoo.route('/yahoo/history/<stock>')
def flask_get_stock_history(stock):
    data = get_ticker_history(stock)
    return jsonify(data)

@yahoo.route('/yahoo/actions/<stock>')
def flask_get_stock_actions(stock):
    data = get_ticker_actions(stock)
    return jsonify(data)

@yahoo.route('/yahoo/dividends/<stock>')
def flask_get_stock_dividends(stock):
    data = get_ticker_dividends(stock)
    return jsonify(data)

@yahoo.route('/yahoo/splits/<stock>')
def flask_get_stock_splits(stock):
    data = get_ticker_dividends(stock)
    return jsonify(data)
