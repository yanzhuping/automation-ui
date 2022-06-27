import json
import unittest
import requests
import logging
import xlrd
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from libs.test_utils import get_root_path
from libs.global_vars import global_vals
import base64
import sys
from libs.test_utils import get_opt,get_global_config
import pymysql


def createSession(username, password, clientCode):
    '''
    获取身份信息，创建一个session
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
        'pwd': password,
        'uname': username}
    # print(payloadData)
    base_url = 'https://qa.tranderpay.com/'
    login_url = 'https://qa.tranderpay.com/api/v1/auth/login'
    selectUser_url = f'https://qa.tranderpay.com/api/v1/auth/info?clientCode={clientCode}'
    # print(selectUser_url)
    r1 = s.get(base_url, headers=header, verify=False)
    r2 = s.post(login_url, json=payloadData, headers=header, allow_redirects=False, verify=False)
    header['Authorization'] = "Bearer " + json.loads(r2.text)['data']['token']
    s.headers.update(header)
    try:
        r3 = s.get(selectUser_url, headers=header, allow_redirects=False, verify=False)
    except:
        pass

    return s

def readExcel(fileName, sheetName='Sheet1'):
    '''
    读取接口测试用例，excel表格
    :param fileName:
    :param sheetName:
    :return:
    '''
    data = xlrd.open_workbook(fileName)
    table = data.sheet_by_name(sheetName)
    nrows = table.nrows  # 行
    ncols = table.ncols  # 列
    listApiData = []
    if nrows > 1:
        # 获取第一行的内容，列表格式
        keys = table.row_values(0)
        # print(keys)
        for col in range(1, nrows):
            values = table.row_values(col)
            api_dict = dict(zip(keys, values))
            # listApiData.append(api_dict)
            if api_dict['is_run'] != '0':
                listApiData.append(api_dict)
    else:
        print("空表格，请检查")
        return None
    # print(listApiData)
    return listApiData

class Assert_result(unittest.TestCase):
    '''
    断言
    '''
    def assert_result(self, data, res):
        status_code = data['status_code']  #返回状态码
        message = data['message']  #返回的message
        error_code = data['error_code'] #返回的错误码
        check_FieldContent = data['check_FieldContent']  #校验指定的字段预期的值与接口返回的值是否一致
        check_sql = data['check_sql']  # 校验接口返回值与数据库存储的值是否一致
        # oper = data['oper']

        if status_code == '':
            pass
        else:
            status_code = eval(status_code)
            self.assertEqual(res.status_code, int(status_code),
                             f'返回【StatusCode】错误，实际结果是{res.status_code}')

        if message == '':
            pass
        else:
            self.assertEqual(res.json()['message'], message,
                             f'返回【message】错误，实际结果是{res.json()["message"]}')

        # if oper == '':
        #     pass
        # else:
        #     self.assertEqual(res.json()['oper'], oper,
        #                      f'返回【oper】错误，实际结果是{res.json()["oper"]}')

        if error_code == '':
            pass
        else:
            self.assertEqual(res.json()['error'], error_code,
                             f'返回【errorCode】错误，实际结果是{res.json()["error"]}')

        if check_FieldContent == '':
            pass
        else:
            check_FieldContent = eval(check_FieldContent)
            for key in check_FieldContent.keys():
                assert_value = check_FieldContent[key]
                return_value = get_value_from_json(key, res.json(), [])
                if len(return_value) == 1:
                    self.assertEqual(return_value[0], assert_value,
                                     f'接口返回的字段{key}值错误，正确的值是：{assert_value}')
                else:
                    for assert_value_1 in assert_value:
                        self.assertIn(assert_value_1,return_value,
                                         f'接口返回的字段{key}值未包含校验值，应该包含：{assert_value}')

        if check_sql == '':
            pass
        else:
            check_sql = eval(check_sql)
            t_opt = get_opt(sys.argv[1:])
            g_config = get_global_config(t_opt.get("env"))
            selectdata = selectDataForAPItest(g_config, check_sql)
            print("数据库查询返回的字典:", selectdata)
            for key in selectdata.keys():
                # 从数据库中查到的值
                value1 = selectdata[key]
                # value2是从接口的返回值拿到的指定键的值
                value2 = get_value_from_json(key, res.json(), [])[0]
                self.assertEqual(value2, value1, "返回结果错误，实际结果是%s" % value1)

        #当响应时间大于5s，就会抛错
        self.assertGreater(float(19),res.elapsed.total_seconds(),f"服务器大哥，快点吧，我等的花儿都谢了~~~，响应时间：{res.elapsed.total_seconds()}s")

def selectDataForAPItest(g_config, check_sql_s):
    '''
    通过sql从数据库查询数据,并以字典形式返回
    :param g_config:
    :param check_sql_s:
    :return:
    '''
    db = pymysql.Connect(
        host=g_config.get("qa_host"), port=3306, user=g_config.get("qa_mysqluser"),
        passwd=g_config.get("qa_mysqlpasswd"), db=g_config.get("qa_dbname"), charset='utf8')
    # 创建一个游标对象，执行数据操作
    cursor = db.cursor()
    selectdata = {}
    for key in check_sql_s.keys():
        print(key + ':' + check_sql_s[key])
        cursor.execute(check_sql_s[key])
        data = cursor.fetchone()
        key_value = data[0]
        selectdata[key] = key_value
    print(selectdata)
    db.close()
    return selectdata

def sendEmail():
    '''
    邮件发送
    :return:
    '''
    # 服务协议
    smtpserver = "smtp.exmail.qq.com"

    #发送的账号信息
    user = str(base64.b64decode(b'eWFuLnpodXBpbmdAY3RndG1vLmNvbQ=='.decode("utf-8")),encoding='utf-8')
    password = str(base64.b64decode(b'WXpwMTk5MzA0MjI='.decode("utf-8")),encoding='utf-8')

    #发送=>接收者
    sender = user
    receives = [user]

    #报告路径，读取报告内容
    file_path = os.path.join(get_root_path(), 'test_report', 'testResultSummary.html')
    send_file = open(file_path, "rb").read()

    #邮件标题、正文
    subject = 'jenkins_test_result'
    content = f'''
    <html>    
    <h1 style="color:red">结果详见附件</h1>
    <html>
    '''

    #创建一个带附件的实例
    msgRoot = MIMEMultipart()
    msgRoot['From'] = sender
    msgRoot['To'] = ','.join(receives)
    msgRoot['Subject'] = subject

    #邮件正文内容
    msgRoot.attach(MIMEText(content, 'html', 'utf-8'))

    #构造附件1
    att = MIMEText(send_file, 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = "attachment;filename='testResultSummary.html'"
    msgRoot.attach(att)

    #可以构建附件2
    #......

    #发送
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(user,password)
    print("Start send email...")
    smtp.sendmail(sender, receives, msgRoot.as_string())
    smtp.quit()
    print("Send email end!")

def set_global(set_global_vars, response_json):
    '''
    抽取接口返回的值存储到全局变量字典中
    [{'name':'query'},{'name2':'query2'}]
    :param set_global_vars: 设置的需要抽取值的名称，以及在接口中查询该值的语句
    :param response_json: 接口返回值
    :return:
    '''
    if set_global_vars and isinstance(set_global_vars, list):
        for set_global_var in set_global_vars:
            if isinstance(set_global_var, dict):
                name = list(set_global_var.keys())[0]
                query = list(set_global_var.values())[0]
                value = dict_get(response_json, query)
                if value is None or value == '':
                    continue
                else:
                    global_vals[name] = value

def dict_get(dic, locators, default=None):
    '''
    获取多层嵌套的字典中的某个值（接口响应数据一般都是多层嵌套的字典）
    :param dic: 输入需要在其中取值的原始字典 <dict>,即接口响应数据
    :param locators: 输入取值定位器, 如:['result', 'msg', '-1', 'status'] <list>
    :param default: 进行取值中报错时所返回的默认值 (default: None)
    :return: 返回根据参数locators找出的值
    '''
    #如果接口响应数据非字典且定位取值器非列表，则直接返回默认值None
    if not isinstance(dic, dict) or not isinstance(locators, list):
        return default

    value = None

    for locator in locators:
        #如果value非字典、列表，且定位器是不能转化为整数的字符串
        if not type(value) in [dict, list] and isinstance(locator, str) and not can_convert_to_int(locator):
            try:
                #从返回值取出定位器对应的值
                value = dic[locator]
            except KeyError:
                return default
            continue
        #如果取出的值是字典，则根据定位器继续取值
        if isinstance(value, dict):
            try:
                value = dict_get(value, [locator])
            except KeyError:
                return default
            continue
        if isinstance(value, list) and can_convert_to_int(locator):
            try:
                value = value[int(locator)]
            except IndexError:
                return default
            continue
    return value

def can_convert_to_int(input):
    try:
        int(input)
        return True
    except BaseException:
        return False

def getValueFromComplexDict(dic, json_key):
    '''
    通过指定的键获取接口返回值（多重嵌套的字典）中对应的值
    ！！！貌似不太准
    :param dic: 接口返回值
    :param json_key: 需要查询的键
    :return:
    '''
    temp_value_r = None
    if isinstance(dic, dict):
        for key in dic.keys():
            temp_value = dic[key]
            if key == json_key:
                temp_value_r = temp_value
                break
            else:
                temp_value_r=getValueFromComplexDict(temp_value, json_key)
        return temp_value_r
    elif isinstance(dic, list):
        for list_value in dic:
            temp_value_r=getValueFromComplexDict(list_value, json_key)
    elif isinstance(dic, (str, int)):
        pass
    return temp_value_r

def get_value_from_json(key, tdict, tem_list):
    """
    从Json中获取key值:
    新建两个函数A和B，函数 A处理字典数据，被调用后，判断传递的参数，如果参数为字典，则调用自身；
    如果是列表或者元组，则调用列表处理函数B；
    函数 B处理列表，被调用后，判断传递的参数，如果参数为列表或者元组，则调用自身；
    如果是字典，则调用字典处理函数A；
    :param key:
    :param tdict:
    :param tem_list:
    :return:
    """
    if not isinstance(tdict, dict):
        return tdict , "is not dict"
    elif key in tdict.keys():
        tem_list.append(tdict[key])
    else:
        for value in tdict.values():
            if isinstance(value, dict):
                get_value_from_json(key, value, tem_list)
            elif isinstance(value, (list, tuple)):
                _get_value(key, value, tem_list)
    return tem_list

def _get_value(key, tdict, tem_list):
    """
    :param key:
    :param tdict:
    :param tem_list:
    :return:
    """
    for value in tdict:
        if isinstance(value, (list, tuple)):
            _get_value(key, value, tem_list)
        elif isinstance(value, dict):
            get_value_from_json(key, value, tem_list)

def Get_Target_Value(key, dic, tmp_list):
    """
    目标键名称,嵌套数据,储存变量
    :param key:目标key值
    :param dic:JSON数据
    :param tmp_list:储存获取的数据
    :return: list
    """
    # 非字典类型(列表、元组)输入，进剥层处理
    if isinstance(dic, (list, tuple)):
        # 非字典类型，则遍历元素深入查找
        for v in dic:
            Get_Target_Value(key, v, tmp_list)

    # 字典类型输入，进行遍历查找处理
    elif isinstance(dic, dict):
        # 查找本层字典
        if key in dic.keys():
            tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list

        # 在本层字典的值中查找
        for value in dic.values():
            Get_Target_Value(key, value, tmp_list)
    return tmp_list

if __name__ == '__main__':
    sendEmail()