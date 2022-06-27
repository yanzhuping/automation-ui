from libs.interface_fun import *
import sys
from libs.test_utils import get_opt,get_global_config
import os
from libs.test_utils import get_root_path
from libs.global_vars import global_vals
import random
import datetime
from libs.test_utils import getlogger

def sendRequests(s, apiData):
    '''
    发送请求
    :param s:
    :param apiData:数据字典
    :return:
    '''
    t_opt = get_opt(sys.argv[1:])
    g_config = get_global_config(t_opt.get("env"))
    clientCode = eval(g_config.get('customer')).get(t_opt.get('customer'))

    false = False
    true = True
    null = None
    randomNo = str(random.randint(100000,999999))
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    day = datetime.datetime.now().day
    curDay = str(year) + '-' + str(month) + '-' + str(day)

    try:
        method = apiData['method']
        url = apiData['url']
        params = apiData['params']
        data = apiData['data']
        files = apiData['files']
        json = apiData['json']
        is_global = apiData['is_global']

        if params == '':
            params = None
        else:
            params = eval(params)

        if data == "":
            data = None
        else:
            data = eval(data)
            print(data)

        if json == "":
            json = None
        else:
            json = eval(json)

        if files == '':
            files = None
        else:
            # files = eval(files)
            files = {'file':(f'{files}',open(
                                 os.path.join(
                                 get_root_path(),'test_data','interfaceRequiredData',f'{files}'), 'rb')
                             )
                     }
            print(files)

        res = s.request(method=method,
                        url=url,
                        params=params,
                        data=data,
                        json=json,
                        files=files,
                        verify=False,
                        timeout=20
                        )
        if is_global == '':
            pass
        else:
            is_global = eval(is_global)
            set_global(is_global, res.json())
        getlogger().info(f'接口 {url} 的返回状态是 {res.status_code}')
        return res
    except:
        traceback_info = traceback.format_exc()
        print(traceback_info)
        getlogger().debug(traceback_info)

if __name__ == '__main__':
    num = 1
    # s = createSession('trdp-yzp', 'yzp19930422', '*')
    s = createSession('trdp-yzp', 'yzp19930422', '2021060101')
    testData = readExcel(os.path.join(get_root_path(),'tranderpay_api','api_data', 'emDataManage.xls'))
    execute = testData[num - 1]
    print(execute)
    response = sendRequests(s, execute)
    print(response.elapsed.total_seconds())  #响应时间
    print(type(response.elapsed.total_seconds()))  #响应时间
    print(response.status_code)
    print('返回值:',response.json())
    Assert_result().assert_result(execute, response)