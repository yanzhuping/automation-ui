import unittest
from ddt import ddt,data,unpack
from tranderpay_api.send_requests import *
import os
from libs.test_utils import get_root_path
import sys
from libs.test_utils import get_opt,get_global_config
from time import sleep

testData1 = readExcel(os.path.join(get_root_path(),'tranderpay_api','api_data', 'InTheService.xls'))
t_opt = get_opt(sys.argv[1:])
g_config = get_global_config(t_opt.get("env"))

@ddt
class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s=createSession(g_config.get('username'),
                            g_config.get('password'),
                            eval(g_config.get('customer')).get(t_opt.get('customer'))
                            )

    @classmethod
    def tearDownClass(cls):
        pass
    @data(*testData1)
    def test_InTheService(self,data):
        print(data)
        res = sendRequests(self.s,data)
        Assert_result().assert_result(data,res)
        sleep(0.5)

if __name__ == '__main__':
    unittest.main()