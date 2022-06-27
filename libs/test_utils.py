import configparser
import getopt
import xlrd
import xlwt
from xlutils.copy import copy
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import shutil
import pymysql
import datetime
from libs.global_vars import executeTime
# import win32clipboard
# import win32con
# from libs.global_vars import clipboardList
import base64
import logging
import time
import colorlog

#测试用例的字段结构
excel_option = ["id", "desc", "keywords", "selector", "val", "level"]
#存储配置参数
common_config = ['test_db', 'qa_db']

def read_excel(file_path, option_key=None, json_type=None):
    '''
    读取test_case文件夹内的excel文件中的内容并存储到字典中以备后用
    获取test_case文件夹内的文件列表
    :param file_path:
    :param option_key:
    :param json_type:
    :return:
    '''
    if option_key is None:
        # excel要取的列以及对应的关键字
        option_key = ["id", "desc", "keywords", "selector", "val", "level"]
    data_list = []
    json_data = {}
    work_book = xlrd.open_workbook(file_path)
    data_sheet = work_book.sheets()[0]
    #读取行
    row_num = data_sheet.nrows
    #读取列
    col_num = data_sheet.ncols
    for i in range(row_num):
        col_data = {}
        for j in range(col_num):
            if j < len(option_key):
                if json_type is True:
                    #如果json_type标记为true，则读取实际的元素定位
                    if i > 0 and j == 0:
                        json_data[data_sheet.cell_value(
                            i, 0)] = data_sheet.cell_value(i, 1)
                else:
                    col_data[option_key[j]] = data_sheet.cell_value(i, j)
        # 去掉excel第一行是注释
        if i > 0:
            data_list.append(col_data)
    # print(data_list)
    return json_data if json_type is True else data_list

def get_root_path():
    '''
    获取项目的根路径
    :return:
    '''
    return os.path.dirname(os.path.dirname(__file__))

def load_ele_selector(ele_key):
    '''
    加载元素总表excel中的选择器key对应的实际选择器表达式
    :param ele_key:
    :return:
    '''
    if ele_key == "" or ele_key is None:
        return ""
    file_path = os.path.join(get_root_path(), "element_selector")
    # print(file_path)
    dir_names = ele_key.split(".")
    # print(dir_names)
    dir_names_len = len(dir_names)
    # print(dir_names_len)
    if dir_names_len <= 1:
        return ""
    # 比如：public.common_button.username,public是目录名，common_button是excel文件名，username是key
    for index, name in enumerate(dir_names):
        # print(index,name)
        if index != dir_names_len - 1:
            if index == dir_names_len - 2:
                # print(index, name)
                name = name + ".xls"
            file_path = os.path.join(file_path, name)
            # print("a",file_path)
    json_data = ""
    try:
        json_data = read_excel(file_path,["key", "selector"], True)
    except:
        pass
    # print(json_data)
    return json_data

def get_selector_val(mainhandler, case):
    '''
    获取元素的表达式
    :param mainhandler:
    :param case:
    :return:
    '''
    selector = case.get("selector")
    if selector != "" and selector is not None and selector.find(".") > -1:
        index = selector.rindex(".")
        store_key = selector[0:index]
        selector_json_key = selector[index + 1:]
        json_data = mainhandler.ele_selector_store.get(store_key)
        if json_data is None:
            # 重新加载json数据
            json_data = load_ele_selector(selector)
        if json_data is not None and json_data != "":
            selector_json_val = json_data.get(selector_json_key)
            mainhandler.ele_selector_store[store_key] = json_data
            if selector_json_val != "" and selector_json_val is not None:
                case["selector"] = selector_json_val

def get_execute_dir(file_path=None):
    '''
    获取执行用例的目录
    :param file_path:
    :return:
    '''
    if file_path is None:
        file_path = "execute"
    return os.path.join(get_root_path(), "test_case", file_path)

def get_filterFile(file_path, fileName_list=None):
    '''
    获取需要过滤的文件列表
    :param file_path:
    :param file_list:
    :return:
    '''
    filterList = []
    if fileName_list is None or fileName_list == '':
        return filterList
    else:
        for file in fileName_list:
            filePath = os.path.join(file_path, file)
            filterList.append(filePath)
        return filterList

def list_dir(file_path, file_list=None, fileName_list=None):
    '''
    获取指定路径下面的所有文件目录
    :param file_path:
    :param file_list:
    :return:
    '''
    if file_list is None:
        file_list = []
    # 文件直接返回
    if os.path.isfile(file_path):
        file_list.append(file_path)
        # print("这是一个文件",file_list)
        return file_list
    #如果是目录，则获取该目录下的所有文件路径
    dir_list = os.listdir(file_path)
    for cur_file in dir_list:
        # 获取文件的绝对路径
        path = os.path.join(file_path, cur_file)
        if os.path.isfile(path):  # 判断是否是文件还是目录需要用绝对路径
            file_list.append(path)
        if os.path.isdir(path):
            list_dir(path, file_list)  # 目录下面又是目录，则递归子目录
    # print("这是一个文件夹，如下是文件夹内的所有文件",file_list)
    filterList = get_filterFile(file_path, fileName_list)
    if filterList == []:
        pass
    else:
        for filterList_1 in filterList:
            file_list.remove(filterList_1)

    return file_list

def get_global_config(env=None, file_path=None):
    '''
    获取配置文件中的配置项
    :param env:
    :param file_path:
    :return:
    '''
    if env is None:
        env = "qa-trdp-yzp"
    if file_path is None:
        file_path = "config.ini"
    cf = configparser.ConfigParser()
    cf.read(os.path.join(get_root_path(),file_path), 'utf-8')
    g_config = {}
    common_config.append(env)
    for config_name in common_config:
        for item in cf.items(config_name):
            g_config[item[0]] = item[1]
    # print("读取的配置项",g_config)
    return g_config

def get_opt(argv):
    '''
    获取命令行输入的参数，存入字典中,等待调用
    :param argv:
    env:环境参数
    test_case:测试用例的路径或者测试用例所在的文件夹的路径
    level:等级参数，设置不同的级别，用例只执行与传输的参数级别一致的用例
    func:功能参数，如”从数据维护添加一条数据“
    pattern：接口测试所需的参数
    view：视觉参数，支持无头模式或图像模式，yes/no
    customer:客户参数，如，上海自动化测试有限公司
    filter：忽略文件参数，当test_case参数传输的是文件夹路径，此处传入具体文件名称，会忽略不执行
    :return:
    '''
    t_opt = {}
    opts, argv = getopt.getopt(argv, "", [
        "env=", "test_case=", "level=", "func=", "pattern=", "view=", "customer=", "filter="
    ])
    for opt, arg in opts:
        t_opt[opt[2:]] = arg
    # print(t_opt)
    return t_opt

def switch_to_cur_win(driver, exec_fun=None):
    try:
        if exec_fun is not None:
            exec_fun()
        all_win = driver.window_handles

        all_win_num = len(all_win)
        driver.switch_to.window(all_win[all_win_num - 1])
    except Exception as e:
        print('切换窗口异常:', e)

def switch_to_cur_win_ifchange(driver, exec_fun=None):
    '''
    点击过程中出现了打开了新的标签页
    则需要将窗口句柄切换至新的窗口才能进行下一步操作
    :param driver:
    :param exec_fun:
    :return:
    '''
    pre_win_num = len(driver.window_handles)
    if exec_fun is not None:
        exec_fun()
    all_win = driver.window_handles
    cur_win_num = len(all_win)
    if cur_win_num != pre_win_num:
        # print('all_win',all_win)
        driver.switch_to.window(all_win[cur_win_num - 1])

def switch_to_win(driver, change_num):
    '''
    从当前窗口切换到指定窗口，change_num 负数表示前第几个窗口，正数表示后第几个窗口
    :param driver:
    :param change_num:
    :return:
    '''
    all_win = driver.window_handles
    cur_win = driver.current_window_handle
    index = all_win.index(cur_win)
    driver.switch_to.window(all_win[index+change_num])

def get_element(driver, selector, is_immedite=None):
    '''
    通过不同的定位方式获取页面元素，如css.selector,xpath
    :param driver:
    :param selector:
    :param is_immedite:
    :return:
    '''
    wait = WebDriverWait(driver, 2, 0.5)
    text = None
    # 支持选择器中带文本 比如：div>span[text]=病例 正常选择器中是没有这种写法的
    if selector.find("[text]=") > -1:
        selector, text = selector.split("[text]=")
    if selector.startswith("/") or  selector.startswith("(") or selector.find("following-sibling::")  > -1:
        if is_immedite:
            elements = driver.find_elements_by_xpath(selector)
        else:
            elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, selector)))
    else:
        if is_immedite:
            elements = driver.find_elements_by_css_selector(selector)
        else:
            elements = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, selector)))
    if len(elements) > 0 and text is not None:
        for ele in elements:
            if ele.text == text:
                return ele
        return None
    return elements[0] if elements is not None and len(elements) > 0 else None

def format_digit_str(val):
    '''
    格式化数字字符串，如，在excel中输入的2，可能在程序读取的时候变成2.0
    :param val:
    :return:
    '''
    if val is None:
        return val
    if val == '610730198506195543':
        return val
    try:
        if isinstance(val, str):
            pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
            if pattern.match(val) is None:
                return val
            else:
                try:
                    if int(val) > 1000000000000000000:
                        return str(val)
                except:
                    val = float(val)
        return [str(val), str(int(val))][int(val) == val]
    except:
        return val

def insert_img(driver,dir_name,filename):
    '''
    页面截图，并将图片保存到指定的文件夹
    :param driver:
    :param dir_name:
    :param filename:
    :return:
    '''
    dir_path = os.path.join(get_root_path(),"test_report","screenshot",dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    driver.get_screenshot_as_file(os.path.join(dir_path,filename))

def handle_case_result(case_result, case_store):
    '''
    处理测试结果
    :return:
    '''
    failed_case_id = case_result.get("failed")
    generate_test_report(case_result, case_store)
    generate_test_errorReport_1(case_result, case_store) #html中的图片信息采用base64编码
    generate_test_errorReport_2(case_result, case_store) #html中的图片信息引用外部链接
    for case_id in case_result.get("total"):
        # 删除成功的截图,只保留有失败case的截图
        if case_id not in failed_case_id:
            del_file(
                os.path.join(get_root_path(), "test_report", "screenshot",
                             case_id))
    # del_report()

def del_file(filepath):
    '''
    删除文件
    :param filepath:
    :return:
    '''
    if os.path.exists(filepath):
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
        if os.path.isfile(filepath):
            os.remove(filepath)

def generate_test_report(case_result, case_store):
    # now = strftime("%Y-%m-%d %H_%M_%S")
    # final_path = os.path.join(
        # get_root_path(), "test_report", "%s_report.html"%now)
    final_path = os.path.join(get_root_path(), "test_report", "report.html")
    origin_path = os.path.join(get_root_path(), "test_report",
                               "report_temp.html")
    table_str = ""
    for (key, case_list) in case_store.items():
        if key in case_result.get("failed"):
            for index, case in enumerate(case_list):
                flag = '成功' if case.get("traceback") is None else '失败'
                info = case.get('traceback', "").replace(f"\n", "<br>")
                img_src = "screenshot/{}/{}_{}.png".format(
                    case.get("id"), case.get("id"), index)
                table_str += f""" <tr>
                    <td>{index+2}</td>
                    <td {'class="red"' if flag=='失败' else ''}>{flag}</td>
                    <td>{case.get("id")}</td>
                    <td>{case.get('desc')}</td>
                    <td>{case.get('keywords')}</td>
                    <td>{case.get('keyexpression')}</td>
                    <td>{case.get('selector')}</td>
                    <td>{case.get('val')}</td>
                    <td>{info}</td>
                    <td class="screenshot_img">
                        <img src="{img_src}" />
                    </td>
                </tr>"""
    with open(origin_path, 'r', encoding="utf-8") as temp:
        with open(final_path, "w", encoding="utf-8") as final_f:
            for line in temp:
                line = line.replace("__total_result__",
                                    str(len(case_result.get("total"))))
                line = line.replace("__failed_result__",
                                    str(len(case_result.get("failed"))))
                #######
                line = line.replace("start", str(executeTime[0]))
                line = line.replace("ElapsedTime", str(executeTime[1] - executeTime[0]))
                ######
                line = line.replace("__result_table_info__", table_str)
                final_f.write(line)

def generate_test_errorReport_1(case_result, case_store):
    final_path = os.path.join(get_root_path(), "test_report", "new_error_report.html")
    origin_path = os.path.join(get_root_path(), "test_report",
                               "report_temp_1.html")
    table_str = ""
    for (key, case_list) in case_store.items():
        if key in case_result.get("failed"):
            for index, case in enumerate(case_list):
                flag = '成功' if case.get("traceback") is None else '失败'
                if flag == '失败':
                    info = case.get('traceback', "").replace(f"\n", "<br>")
                    img_src = "screenshot/{}/{}_{}.png".format(
                        case.get("id"), case.get("id"), index)
                    img_src = photoToBase64(img_src)
                    table_str += f""" <tr>
                        <td>{index+2}</td>
                        <td {'class="red"' if flag=='失败' else ''}>{flag}</td>
                        <td>{case.get("id")}</td>
                        <td>{case.get('desc')}</td>
                        <td>{case.get('keywords')}</td>
                        <td>{case.get('keyexpression')}</td>
                        <td>{case.get('selector')}</td>
                        <td>{case.get('val')}</td>
                        <td>{info}</td>
                        <td class="screenshot_img">
                            <img src="data:image/png;base64,{img_src}" />
                        </td>
                    </tr>"""
    with open(origin_path, 'r', encoding="utf-8") as temp:
        with open(final_path, "w", encoding="utf-8") as final_f:
            for line in temp:
                line = line.replace("__total_result__",
                                    str(len(case_result.get("total"))))
                line = line.replace("__failed_result__",
                                    str(len(case_result.get("failed"))))
                #######
                line = line.replace("start",str(executeTime[0]))
                line = line.replace("ElapsedTime",str(executeTime[1]-executeTime[0]))
                ######
                line = line.replace("__result_table_info__", table_str)
                final_f.write(line)

def generate_test_errorReport_2(case_result, case_store):
    final_path = os.path.join(get_root_path(), "test_report", "error_report.html")
    origin_path = os.path.join(get_root_path(), "test_report",
                               "report_temp_1.html")
    table_str = ""
    for (key, case_list) in case_store.items():
        if key in case_result.get("failed"):
            for index, case in enumerate(case_list):
                flag = '成功' if case.get("traceback") is None else '失败'
                if flag == '失败':
                    info = case.get('traceback', "").replace(f"\n", "<br>")
                    img_src = "screenshot/{}/{}_{}.png".format(
                        case.get("id"), case.get("id"), index)
                    table_str += f""" <tr>
                        <td>{index+2}</td>
                        <td {'class="red"' if flag=='失败' else ''}>{flag}</td>
                        <td>{case.get("id")}</td>
                        <td>{case.get('desc')}</td>
                        <td>{case.get('keywords')}</td>
                        <td>{case.get('keyexpression')}</td>
                        <td>{case.get('selector')}</td>
                        <td>{case.get('val')}</td>
                        <td>{info}</td>
                        <td class="screenshot_img">
                            <img src="{img_src}" />
                        </td>
                    </tr>"""
    with open(origin_path, 'r', encoding="utf-8") as temp:
        with open(final_path, "w", encoding="utf-8") as final_f:
            for line in temp:
                line = line.replace("__total_result__",
                                    str(len(case_result.get("total"))))
                line = line.replace("__failed_result__",
                                    str(len(case_result.get("failed"))))
                #######
                line = line.replace("start",str(executeTime[0]))
                line = line.replace("ElapsedTime",str(executeTime[1]-executeTime[0]))
                ######
                line = line.replace("__result_table_info__", table_str)
                final_f.write(line)

def photoToBase64(filePath):
    '''
    将图片转换为base64
    :param filePath:
    :return:
    '''
    file = os.path.join(get_root_path(), "test_report",filePath)
    with open(file, "rb") as f:  # 转为二进制格式
        base64_data = str(base64.b64encode(f.read()),'utf-8')  # 使用base64进行加密
    return base64_data

def del_report():
    '''
    删除多余的测试报告，只保留9份最新的报告
    :return:
    '''
    tar = []
    file_list = list_dir(os.path.join(get_root_path(),"test_report"))
    for file_name in file_list:
        # print("file_name:",file_name)
        if file_name.find("2021") > -1:
            tar.append(file_name)
    # print(tar)
    if len(tar) <= 9:
        pass
    else:
        for i in range(len(tar)-9):
            # print(tar[i])
            os.remove(tar[i])

def del_logs():
    '''
    删除多余的logs文件，只保留9份最新的报告
    :return:
    '''
    tar = []
    file_list = list_dir(os.path.join(get_root_path(), "logs"))
    for file_name in file_list:
        # print("file_name:",file_name)
        if file_name.find("_log.txt") > -1:
            tar.append(file_name)
    # print(tar)
    if len(tar) <= 9:
        pass
    else:
        for i in range(len(tar) - 9):
            # print(tar[i])
            os.remove(tar[i])

def create_cursor(g_config):
    '''
    连接数据库
    :param g_config:
    :return:
    '''
    db = pymysql.Connect(host=g_config.get("host"),
                         port=3306,
                         user=g_config.get("mysqluser"),
                         passwd=g_config.get("mysqlpasswd"),
                         db=g_config.get("dbname"),
                         charset='utf8')

    return db

def readDataFromMySQL(g_config, table, field):
    '''
    从数据库拿取数据
    :param g_config:
    :return:
    '''
    db = create_cursor(g_config)
    cursor = db.cursor()
    sql = "select %s from %s order by id asc limit 1" % (field,
        g_config.get(table))
    cursor.execute(sql)
    input_db = cursor.fetchone()
    db.close()
    return input_db[0]

def deleteDataFromMySQL(g_config, table, field):
    '''
    从数据库中删除已经读取的数据
    :param g_config:
    :return:
    '''
    db = create_cursor(g_config)
    cursor = db.cursor()
    sql = "delete from %s where %s='%s'" % (
        g_config.get(table), field, readDataFromMySQL(g_config, table, field))
    cursor.execute(sql)
    db.commit()

def getTestData(dir, fileName):
    return os.path.join(get_root_path(), 'test_data', dir, fileName)

def getTemplate(file_path):
    '''
    获取导入数据模板的表头
    :return: list
    '''

    data_list = []
    work_book = xlrd.open_workbook(file_path)
    data_sheet = work_book.sheets()[0]
    #读取行
    row_num = data_sheet.nrows
    print(row_num)
    #读取列
    col_num = data_sheet.ncols
    print(col_num)
    for i in range(row_num):
        for j in range(col_num):
            data = data_sheet.cell_value(i, j)
            data_list.append(data)
    # print(data_list)
    return data_list

def getTestCaseRows():
    '''
    获取test_case文件夹内的所有用例的行数
    :return:
    '''
    docList = list_dir(os.path.join(get_root_path(),'test_case'))
    # print(docList)
    print('共有测试用例文件数量：',len(docList))
    sum = 0
    for file_path in docList:
        work_book = xlrd.open_workbook(file_path)
        data_sheet = work_book.sheets()[0]
        row_num = data_sheet.nrows
        # print(row_num)
        sum = sum + (row_num-1)
    print('测试用例行数：',sum)
    return sum

def getEleLocationRows():
    '''
    获取element_selector文件夹内的所有元素定位的行数
    :return:
    '''
    docList = list_dir(os.path.join(get_root_path(),'element_selector'))
    # print(docList)
    print('共有元素定位文件数量：',len(docList))
    sum = 0
    for file_path in docList:
        work_book = xlrd.open_workbook(file_path)
        data_sheet = work_book.sheets()[0]
        row_num = data_sheet.nrows
        # print(row_num)
        sum = sum + (row_num-1)
    print('元素定位行数：',sum)
    return sum

def getCodeRowNum():
    '''
    获取该项目下的代码行数
    :return:
    '''
    newDocList = [] #py文件数量
    sum = 0 #总行数，包含代码、空行、注释
    blankLine = 0 #空行数
    annotationLine = 0 #注释行数

    docList = list_dir(get_root_path())

    for fileName in docList:
        if fileName.split('.')[1] == 'py':
            newDocList.append(fileName)

    for file in newDocList:
        content = open(file,encoding='utf-8').readlines()
        t = len(content)
        sum = sum + t
        for line in content:
            line = line.strip()
            if line == '':
                blankLine = blankLine + 1
            if line.startswith('#'):
                annotationLine = annotationLine + 1
    print('总代码行数：',sum)
    # print('空行数：',blankLine)
    # print('注释行数：',annotationLine)
    # print('纯代码行数：',sum - blankLine - annotationLine)
    return sum

# def clipboardContents():
#     '''
#     获取剪贴板内容
#     :return:
#     '''
#     win32clipboard.OpenClipboard()
#     # content = win32clipboard.GetClipboardData(win32con.CF_TEXT)
#     content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
#     print(content)
#     win32clipboard.CloseClipboard()
#     clipboardList.append(content)
#     return content
#
# def clearclipboardContents():
#     '''
#     清空剪贴板内容
#     :return:
#     '''
#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.CloseClipboard()

def markErrorLines(errorLines, case_id, file_name):
    '''
    标记单元格的样式
    :param file_name:
    :return:
    '''
    # style = xlwt.easyxf('pattern: pattern solid, fore_colour red; font: name 宋体, height 220')  # 红色
    style = set_Style('宋体', 11, 0x08, 1, 0x0A)
    style1 = set_Style('宋体', 11, 0x08, 1, 0x7FFF)
    rb = xlrd.open_workbook(file_name,formatting_info=True)  # 打开t.xls文件
    ro = rb.sheets()[0]  # 读取表单0
    row_num = ro.nrows
    wb = copy(rb)  # 利用xlutils.copy下的copy函数复制
    ws = wb.get_sheet(0)  # 获取表单0
    col = 0  # 指定修改的列
    for i in range(1,row_num-1):
        ws.write(i, col, ro.cell(i, col).value, style1)
    for i in errorLines:  # 循环所有的行
        result = ro.cell(i, col).value
        if result == case_id:  # 判断是否等于当前id
            ws.write(i, col, ro.cell(i, col).value, style)
    wb.save(file_name)

def set_Style(name,size,color,borders_size,color_fore,blod=False):
    '''
    :param name: 字体名称
    :param size: 字号
    :param color: 字体颜色
    :param borders_size: 边框尺寸
    :param color_fore: 背景颜色
    :param blod: 是否加粗
    :return:
    '''
    style = xlwt.XFStyle()  # 初始化样式
    # 字体
    font = xlwt.Font()
    font.name = name
    font.height = 20 * size  # 字号
    font.bold = blod  # 加粗
    font.colour_index = color  # 默认：0x7FFF 黑色：0x08
    style.font = font
    # 居中
    alignment = xlwt.Alignment()  # 居中
    # alignment.horz = xlwt.Alignment.HORZ_CENTER   #水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  #垂直剧中
    style.alignment=alignment
    # 边框
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = borders_size  # 自定义：1：细线；2：中细线；3：虚线；4：点线
    style.borders = borders
    # 背景颜色
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置背景颜色的模式(NO_PATTERN; SOLID_PATTERN)
    pattern.pattern_fore_colour = color_fore  # 默认：无色：0x7FFF；黄色：0x0D；蓝色：0x0C
    style.pattern = pattern

    return style


def getlogger():
    '''
    日志级别：critical > error > warning > info > debug
    说明:
    DEBUG：详细的信息,通常只出现在诊断问题上
    INFO：确认一切按预期运行
    WARNING：一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”)。这个软件还能按预期工作。
    ERROR：更严重的问题,软件没能执行一些功能
    CRITICAL：一个严重的错误,这表明程序本身可能无法继续运行
    :return:
    '''
    log_colors_config = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }
    logger = logging.getLogger("logger")
    # 判断是否有处理器，避免重复执行
    if not logger.handlers:
        # 日志输出的默认级别为warning及以上级别，设置输出info级别
        logger.setLevel(logging.DEBUG)
        # 创建一个处理器handler  StreamHandler()控制台实现日志输出
        sh = logging.StreamHandler()
        # 创建一个格式器formatter  （日志内容：当前时间，文件，日志级别，日志描述信息）
        # formatter = logging.Formatter(fmt="当前时间是%(asctime)s,文件是%(filename)s,行号是%(lineno)d，日志级别是%(levelname)s，"
        #                                   "描述信息是%(message)s", datefmt="%Y/%m/%d %H:%M:%S")

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
            log_colors=log_colors_config)

        # 创建一个文件处理器，文件写入日志
        fh = logging.FileHandler(
            filename="{}/{}_log.txt".format(os.path.join(get_root_path(), 'logs'),
                                            time.strftime("%Y_%m_%d %H_%M_%S", time.localtime())),
            encoding="utf8")
        # 创建一个文件格式器f_formatter
        f_formatter = logging.Formatter(fmt="当前时间是%(asctime)s,文件是%(filename)s,行号是%(lineno)d，日志级别是%(levelname)s，"
                                            "描述信息是%(message)s", datefmt="%Y/%m/%d %H:%M:%S")

        # 关联控制台日志器—处理器—格式器
        logger.addHandler(sh)
        sh.setFormatter(formatter)
        # 设置处理器输出级别
        sh.setLevel(logging.INFO)

        # 关联文件日志器-处理器-格式器
        logger.addHandler(fh)
        fh.setFormatter(f_formatter)
        # 设置处理器输出级别
        fh.setLevel(logging.DEBUG)

    return logger

if __name__ == '__main__':

    # filepath = r'D:\WorkCode\automation\test_data\人事管理之员工信息\上海自动化测试有限公司创建数据模板.xlsx'
    # readAndWeiteXLSX(filepath,'残障人士证书号','1212121212')
    # print(format_digit_str("2"))
    # print(type(format_digit_str("2")))
    # getTemplate(r'D:\WorkCode\automation\test_data\薪资数据导入\薪资数据导入模板.xlsx')
    # list_dir(r"D:\WorkCode\automation\test_report")
    # list_dir(r"D:\WorkCode\automation\test_case\execute\phase1")
    # get_global_config()
    # load_ele_selector("public.common_button.username")
    # del_report()
    # getTestCaseRows()
    # getEleLocationRows()
    # getCodeRowNum()
    # file_name= r'C:\Users\admin\Desktop\DeleteStaffData.xls'
    # file_name= r'C:\Users\admin\Desktop\AddStaffData.xls'
    # markErrorLines(2,'yanzhuping',file_name)
    # color_execl(file_name)
    del_logs()