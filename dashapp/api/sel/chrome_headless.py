from flask import Blueprint, render_template
from .banks.util.gen_webdriver import gen_test_driver
from .banks.fetch import scrap_rbc_data, get_mf_data
"""Scrapping endpoints for the flask server running in dash
"""
sel = Blueprint('api', __name__)
@sel.route('/api/rbc/mf')
def get_rbc_mf():
    browser = gen_test_driver()
    rbc_bank_df = scrap_rbc_data(browser)
    browser.close()
    browser.quit()
    return rbc_bank_df.to_html(classes='data')

@sel.route('/api/rbc/mf_temp')
def get_rbc_mf_template():
    browser = gen_test_driver()
    rbc_bank_df = scrap_rbc_data(browser)
    browser.close()
    return render_template('index.html',  tables=[rbc_bank_df.to_html(classes='data')], titles=rbc_bank_df.columns.values)

@sel.route('/api/td/mf')
def get_td_mf():
    browser = gen_test_driver()
    td_bank_df = get_mf_data(browser)
    browser.close()
    return td_bank_df.to_html(classes='data')

@sel.route('/api/td/mf_temp')
def get_td_mf_template():
    browser = gen_test_driver()
    td_bank_df = get_mf_data(browser)
    browser.close()
    return render_template('index.html',  tables=[td_bank_df.to_html(classes='data')], titles=td_bank_df.columns.values)
    