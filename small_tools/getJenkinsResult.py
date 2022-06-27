'''
域名
https://tester.tranderpay.com/job
构建历史，获取最新的期号
https://tester.tranderpay.com/job/Spring1/buildTimeGraph/map
UI测试获取error_report测试报告
https://tester.tranderpay.com/job/Spring1/_e99499_e8afaf_e6b58b_e8af95_e68aa5_e5918a/error_report.html
接口测试测试报告
https://tester.tranderpay.com/job/Test_API/_e6b58b_e8af95_e68aa5_e5918a/testreport.html
'''
import time

import requests
import logging
import re
import os
from time import sleep
import webbrowser

def getCookie():
    s = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    logging.captureWarnings(True)
    base_url = 'https://tester.tranderpay.com/j_spring_security_check'
    data = {'j_username': 'yanzhuping', 'j_password': '12345678', 'Submit': '登录', 'remember_me': 'on'}
    r1 = s.post(base_url, headers=header, data=data, verify=False, allow_redirects=False)
    location = r1.headers['Location']

    r2 = s.request('GET', location, headers=header, allow_redirects=False, verify=False)
    result = r2.headers['Set-Cookie']
    header['Cookie'] = result.split(';')[0]
    s.headers.update(header)

    r3 = s.request('GET', location, headers=header, allow_redirects=False, verify=False)

    return s

def getHistory(s,projectName):
    url4 = f'https://tester.tranderpay.com/job/{projectName}/buildTimeGraph/map'
    r4 = s.request('GET', url4, verify=False)
    pat1 = r'alt="" href="(.*?)"/'
    num = re.findall(pat1, r4.text)[0]
    return num

def getResult(s, projectNames):
    resultList = []
    for task in projectNames:
        projectName=task[0]
        ty = task[1]
        note = task[2]
        num = getHistory(s, projectName)
        result = ''
        url = ''
        url1 = ''
        resultDict = {'name':'','type':'','result':'','url':'','url1':'','note':''}
        try:
            if ty == 'API':
                url = f'https://tester.tranderpay.com/job/{projectName}/{num}/_e6b58b_e8af95_e68aa5_e5918a/testreport.html'
                url1 = f'https://tester.tranderpay.com/job/{projectName}/{num}/_e6b58b_e8af95_e68aa5_e5918a/testreport.html'
                r = s.request('GET', url, verify=False)
                pat = r"<p class='attribute'><strong>Status:</strong> (.*?)</p>"
                result = re.findall(pat, r.text)[0]
            if ty == 'UI':
                url = f'https://tester.tranderpay.com/job/{projectName}/{num}/_e99499_e8afaf_e6b58b_e8af95_e68aa5_e5918a/error_report.html'
                url1 = f'https://tester.tranderpay.com/job/{projectName}/{num}/_e5ae8c_e695b4_e6b58b_e8af95_e68aa5_e5918a/report.html'
                r = s.request('GET', url,  verify=False)
                pat1 = r'执行结果 total:(.*?) , failed:'
                pat2 =''', failed: (.*?)
    </div>'''
                result1 = re.findall(pat1, r.text)[0]
                result2 = re.findall(pat2, r.text)[0]
                result = '共执行用例数量'+result1+',失败用例数量'+result2
        except:
            result = '查询运行结果失败，请检查原因！！！'
        resultDict['name'] = projectName
        resultDict['type'] = ty
        resultDict['result'] = result
        resultDict['url'] = url
        resultDict['url1'] = url1
        resultDict['note'] = note
        resultList.append(resultDict)
    return resultList

def generate_test_report(result):
    '''
    生成测试报告
    :param result:
    :return:
    '''
    get_root_path = os.path.dirname(os.path.dirname(__file__))
    final_path = os.path.join(get_root_path, "test_report", "testResultSummary.html")
    origin_path = os.path.join(get_root_path, "test_report",
                               "testResult_temp.html")
    table_str = ""
    for testResult in result:
        if testResult.get('type') == 'API':
            flag = '成功' if testResult.get("result").find('Failure') == -1 and testResult.get("result").find('Error') == -1 else '失败'
        else:
            flag = '成功' if testResult.get("result").split(',')[1] == '失败用例数量0' else '失败'
        table_str += f""" <tr>
            <td {'class="red"' if flag=='失败' else ''}>{flag}</td>
            <td>{testResult.get("name")}</td>
            <td>{testResult.get("type")}</td>
            <td>{testResult.get("result")}</td>
            <td><a href={testResult.get("url")} target="_blank">错误测试报告</a></td>
            <td><a href={testResult.get("url1")} target="_blank">完整测试报告</a></td>
            <td>{testResult.get("note")}</td>
        </tr>"""
    with open(origin_path, 'r', encoding="utf-8") as temp:
        with open(final_path, "w", encoding="utf-8") as final_f:
            for line in temp:
                line = line.replace("__result_table_info__", table_str)
                final_f.write(line)

def outPutResult(projectNames, url):
    s = getCookie()
    result = getResult(s,projectNames)
    print(result)
    generate_test_report(result)
    sleep(3)
    webbrowser.open(url, new=2)

if __name__ == '__main__':
    url = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_report', "testResultSummary.html")
    projectNames = [
        ['Test_API','API','接口测试'],
        ['StaffManagement','UI','员工管理'],
        ['SalaryCalculation', 'UI','薪资计算'],
        ['SalaryServiceConfiguration', 'UI','薪资业务配置'],
        ['CommonServiceConfiguration','UI','公共业务配置'],
        ['CommonSystemConfiguration', 'UI','公共系统配置'],
        ['SalaryCalculationProcess','UI','薪资计算流程'],
        ['DeclarationProcessFull', 'UI','员工信息申报完整流程'],
        ['DeclarationProcessSuccessful', 'UI','员工信息申报仅成功流程'],
        ['InServiceProcessFail', 'UI','在职服务申请完整流程'],
        ['InServiceProcessSuc', 'UI','在职服务申请成功流程'],
        ['PersonnelServiceConfiguration', 'UI','人事业务配置'],
        ['SocialSecurityServiceApplication', 'UI','社保业务申请'],
        ['SocialSecuritySystemConfiguration', 'UI','社保系统配置'],
        ['EmployeeOnboardingProcess', 'UI','自主入职流程'],
        ['PermissionsValidation', 'UI','各种账号的权限校验'],
    ]
    outPutResult(projectNames, url)
