import unittest
import sys
from ..banks.fetch import gcf_td, gcf_rbc

from ..banks.util.get_env import get_env
curr_env = get_env()
if curr_env == "production":
    import HtmlTestRunner

class TestGCFScrap(unittest.TestCase):
    def test_gcf_rbc(self):
        rbc_df = gcf_rbc()
        self.assertTrue(len(rbc_df.columns) >= 7)
        print(len(rbc_df.index))
        self.assertTrue(len(rbc_df.index) >= 250)

    def test_gcf_td(self):
        td_df = gcf_td()
        self.assertTrue(len(td_df.columns) >= 7)
        self.assertTrue(len(td_df.index) >= 150)
        
if __name__ == '__main__':
    if sys.platform in [None,'','linux']:
        unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='docs'))
    else:
        unittest.main()
