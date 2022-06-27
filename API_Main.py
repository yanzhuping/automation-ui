import os
import unittest
from libs.HTMLTestRunner import HTMLTestRunner
from libs.test_utils import get_root_path
from libs.test_utils import get_opt,del_logs
import sys
from libs.interface_fun import sendEmail

def run():
    p=get_opt(sys.argv[1:]).get('pattern')
    case_dir = os.path.join(get_root_path(),'tranderpay_api','api_case')
    discover = unittest.defaultTestLoader.discover(
        case_dir, pattern=p, top_level_dir=None)
    report_path = os.path.join(get_root_path(), 'test_report', "testreport.html")
    fp = open(report_path, "wb")
    runner = HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u'接口测试', verbosity=2)
    runner.run(discover)
    fp.close()
    del_logs()
    # sendEmail()


if __name__ == '__main__':
    run()