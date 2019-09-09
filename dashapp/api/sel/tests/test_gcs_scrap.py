import unittest
from ..banks.fetch import get_mf_data, parse_td_soup, parse_rbc_soup
import json
import os
from ..banks.util.get_env import get_env
import sys
from ..calc_profit import calc_profit
curr_env = get_env()
if curr_env == "production":
    import HtmlTestRunner

class TestParseJSON(unittest.TestCase):
    def test_rbc_json(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'ref/sample_rbc_data.json')
        with open(filename, 'r', errors='replace') as f:
            rbc_data_json = json.load(f)
        td_df = parse_td_soup(rbc_data_json["rbc_html"])
        self.assertTrue(len(td_df.columns) >= 7)
        self.assertTrue(len(td_df.index) >= 200)

    def test_td_json(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'ref/sample_td_data.json')
        with open(filename, 'r', errors='replace') as f:
            rbc_data_json = json.load(f)
        td_df = parse_td_soup(rbc_data_json["td_html"])
        self.assertTrue(len(td_df.columns) >= 7)
        self.assertTrue(len(td_df.index) >= 150)

    def test_calc_profit(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'ref/sample_td_data.json')
        with open(filename, 'r', errors='replace') as f:
            td_data_json = json.load(f)
        td_df = parse_td_soup(td_data_json["td_html"])

        filename = os.path.join(dirname, 'ref/sample_rbc_data.json')
        with open(filename, 'r', errors='replace') as f:
            rbc_data_json = json.load(f)
        rbc_df = parse_rbc_soup(rbc_data_json["rbc_html"])
        calc_profit(rbc_df, td_df)
        
if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()