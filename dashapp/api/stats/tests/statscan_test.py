import requests
import json
import pandas as pd
import unittest
import os 

try:
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open('{}/{}'.format(dir_path,'ind-econ0430.json'), errors='ignore') as json_file:  
		data = json.load(json_file)
	results = data['results']
except Exception as e:
	print(e)

from ....api.sel.banks.util.get_env import get_env
curr_env = get_env()
if curr_env == "production":
    import HtmlTestRunner
class TestStats(unittest.TestCase):
	def test_stock_profit(self):
		geocode = results['geo']
		region_list = ['Canada', 'British Columbia', 'Alberta', 'Ontario', 'Quebec']
		my_filter_iter = filter(lambda x: x['label']['en'] in region_list, geocode)
		my_list = list(my_filter_iter)
		self.assertEqual(my_list[0]['label']['en'], 'Canada')

	def test_stock_format(self):
		registry_num = [3555, 4822]
		indicators = results['indicators']
		val_list = filter(lambda x: x['registry_number'] in registry_num, indicators)
		ind_list = list(val_list)
		self.assertNotEqual(len(ind_list), 0)

	def test_live_data():
		response = requests.get('https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/ind-econ.json')
		data = response.json()
		results = data['results']
		geocode = results['geo']
		region_list = ['Canada', 'British Columbia', 'Alberta', 'Ontario', 'Quebec']
		my_filter_iter = filter(lambda x: x['label']['en'] in region_list, geocode)
		my_list = list(my_filter_iter)
		self.assertEqual(my_list[0]['label']['en'], 'Canada')

if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()
