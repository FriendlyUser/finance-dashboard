"""Get economic indicators from statscan data
"""
import requests
import pandas as pd
from ..sel.banks.util.parse_config import get_config
def get_statscan():
  """Gets statscan data of interest

  For details see the statistics canada documentation and api reference.
  """
  cfg = get_config()
  response = requests.get(cfg['stats_can_url'])
  data = response.json()
  # Name to label to column, find internal statscan data source or worst case just use a reference based approach
  registry_num = [3496, 3555, 3537, 3628, 3592, 3587, 3587, 3569, 3556, 3389, 5421, 3313, 3605, 3612, 3660, 4822, 19277]
  results = data['results']
  indicators = results['indicators']
  val_list = filter(lambda x: x['registry_number'] in registry_num, indicators)
  ind_list = list(val_list)
  # remove geocodes, refer to sample data from json file
  int_list = [0, 10]
  new_list = filter(lambda x: x['geo_code'] in int_list, ind_list)
  global_df = pd.DataFrame()
  for i in new_list:
    code = i['geo_code']
    val = i['value']['en']
    title = i['title']['en']#
    refper = i['refper']['en']
    growth = ''
    details = ''
    if i['growth_rate']:
      if i['growth_rate']['growth']:
        growth = i['growth_rate']['growth']['en']
        details = i['growth_rate']['details']['en']
    local_df = pd.DataFrame([[code,val,title,refper,growth,details]])
    global_df = global_df.append(local_df,ignore_index =True)
  return global_df

def exchange_rates():
  cfg = get_config()
  exchanges_prices_url = '{}/{}'.format(cfg['exchange_api'], 'latest?base=USD')
  response = requests.get(exchanges_prices_url)
  data = response.json()
  keep_keys = ['CAD', 'USD', 'EUR']
  rates = data['rates']
  # Clean up later
  rates_dict = {k: rates[k] for k in keep_keys}
  ex_rates_df = pd.Series(rates_dict).to_frame()
  return ex_rates_df
