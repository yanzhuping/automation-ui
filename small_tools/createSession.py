import json
import requests
import logging

def createSession():
    '''
    创建一个session
    :return:
    '''
    s = requests.session()
    logging.captureWarnings(True)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) App'
                      'leWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    payloadData = {
        'code': '1',
        'codeId': '81059e06-f4e2-4a5b-82e1-273ed286031d',
        'pwd': 'yzp19930422',
        'uname': 'trdp-yzp'}
    base_url = 'https://qa.tranderpay.com/'
    login_url = 'https://qa.tranderpay.com/api/v1/auth/login'
    selectUser_url = 'https://qa.tranderpay.com/api/v1/auth/info?clientCode=2021060101'
    r1 = s.get(base_url, headers=header, verify=False)
    r2 = s.post(login_url, json=payloadData, headers=header, allow_redirects=False, verify=False)
    header['Authorization'] = "Bearer " + json.loads(r2.text)['data']['token']
    r3 = s.get(selectUser_url, headers=header, allow_redirects=False, verify=False)

    return s

if __name__ == '__main__':
    s = createSession()
    #员工管理-员工数据维护
    url = 'https://qa.tranderpay.com/api/v1/clientPayrollCalculation/getPayrollCalcSuccStatus'
    #员工管理-薪资数据维护
    url1 = 'https://qa.tranderpay.com/api/v1/employeeMasterData/getCustomCondition'
    r1 = s.get(url)
    print(r1.status_code,r1.text)
    r2 = s.get(url1)
    print(r2.status_code,r2.text)

