# from cloud_apis import *

# Selenium scrapping tests
from .sel.tests.rbc_mf_test import *
from .sel.tests.td_mf_test import *
from .sel.tests.test_gcs_scrap import *
from .sel.banks.util.get_env import get_env
# Yahoo Tests
from .yahoo.tests.yahoo_test import *
# Stats tests
# from .stats.tests.statscan_test import *
import unittest
import os
# maybe rename to route util folder with the code refactor
import sys
curr_env = get_env()
if curr_env == "production":
    import HtmlTestRunner

if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()
    unittest.main()