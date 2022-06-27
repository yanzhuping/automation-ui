import datetime
from libs.test_utils import *
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from libs.global_vars import *
import traceback
import random
from libs.interface_fun import createSession
import sys,platform

def input_handler(mainhandler, case=None):
    '''
    输入类型的关键字
    :param mainhandler:
    :param case:
    :return:
    '''
    g_config = mainhandler.g_config
    val = str(case.get("val"))
    id = case.get("id")
    driver = mainhandler.driver
    input_val = format_digit_str(val)
    print(input_val, type(input_val))
    selector = case.get("selector")
    desc =case.get("desc")
    # 姓名
    if selector in ["//label[text()='姓名']/following-sibling::div/div/input",
                    "//span[text()='姓名']/../following-sibling::div/div/input",]:
        if input_val is not None or input_val != '':
            pass
        if input_val == '' or input_val is None:
            input_val = readDataFromMySQL(g_config, 'tablename1', 'name')
            print('输入的姓名是：',input_val)
            deleteDataFromMySQL(g_config, 'tablename1', 'name')
            temporaryDick['name'] = input_val
    # 证件号码
    if selector in ["//label[text()='证件号码']/following-sibling::div/div/input",
                    "//span[text()='证件号码']/../following-sibling::div/div/input",
                    "//label[text()='社保账号']/following-sibling::div/div/input",]:
        if input_val == '123456789' or input_val == '340826199404222611':
            pass
        else:
            input_val = readDataFromMySQL(g_config, 'tablename2', 'idNumber')
            deleteDataFromMySQL(g_config, 'tablename2', 'idNumber')
    # 银行卡号
    if selector == "(//label[text()='开户银行账号']/../../../../div[2]/div/div/div/input)[1]":
        if input_val == '123456789' or input_val == 'a严，./':
            pass
        else:
            input_val = readDataFromMySQL(g_config, 'tablename3', 'bankCardNo')
            deleteDataFromMySQL(g_config, 'tablename3', 'bankCardNo')
    #电话号码
    if selector == "//label[text()='手机号']/following-sibling::div/div/div[2]/input":
        if input_val == '1234' or input_val == '13245678909' or input_val == '13012345678':
            pass
        else:
            input_val = readDataFromMySQL(g_config, 'tablename4', 'phoneNo')
            deleteDataFromMySQL(g_config, 'tablename4', 'phoneNo')
    #员工企业编号
    if selector == "//label[text()='员工企业编号']/following-sibling::div/div/input":
        input_val = readDataFromMySQL(g_config, 'tablename5', 'emNo')
        deleteDataFromMySQL(g_config, 'tablename5', 'emNo')
    #住房公积金账号
    if selector == "//label[text()='公积金账号']/following-sibling::div/div/input":
        input_val = readDataFromMySQL(g_config, 'tablename6', 'accFund')
        deleteDataFromMySQL(g_config, 'tablename6', 'accFund')
    #导入文件
    if selector in ['#my-excel-upload-input',
                    '#excel-upload-input',
                    "(//input[@id='excel-upload-input'])[2]",
                    "(//input[@id='excel-upload-input'])[1]",
                    "#excel-upload-input0",
                    "#file-upload-input999",
                    "(//input[@name='file'])[2]",
                    "//input[@class='el-upload__input']",
                    ]:
        if input_val.find(":")>-1:
            dir = input_val.split(":")[0]
            fileName = input_val.split(":")[1]
            input_val = getTestData(dir, fileName)
            print(input_val)
        else:
            raise Exception(f"{desc} 操作值格式异常")
    #员工申报时从全局变量字典获取姓名
    if val == 'global_name1':
        input_val = nameDick[val.split('_')[1]]
    #自主入职的员工姓名
    if val in ['自主入职职员','员工信息添加职员','员工数据维护添加职员']:
        input_val = temporaryDick['name']
    #人事业务配置-组织管理配置，创建组织时的命名
    if val in ['测试父组织','测试子组织','测试孙组织','csfzz','cszzz','csszz']:
        nowTime = datetime.datetime.now()
        input_val = val + str(nowTime.year) + str(nowTime.month) + str(nowTime.day) + str(random.randint(0,99999))
    get_element(driver, selector).send_keys(input_val)
    check_loading_is_hide(driver)

def click_handler(mainhandler, case=None):
    '''
    点击类型的关键字，如果有浮层会等待浮层消失才会进行下一步
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    switch_to_cur_win_ifchange(
        driver,
        lambda: get_element(mainhandler.driver, case.get("selector")).click())
    check_loading_is_hide(driver)

def clickNoWait_handler(mainhandler, case=None):
    '''
    点击类型的关键字，点击后不等待，需要捕捉alert提示语
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    switch_to_cur_win_ifchange(
        driver,
        lambda: get_element(mainhandler.driver, case.get("selector")).click())

def doubleClick_handler(mainhandler, case=None):
    '''
    双击
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    ActionChains(driver).double_click(get_element(driver, case.get("selector"))).perform()

def clear_handler(mainhandler, case=None):
    '''
    清除input输入框中存在的内容
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    get_element(driver, case.get("selector")).clear()

def refresh_handler(mainhandler, case):
    '''
    刷新当前页面
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    driver.refresh()
    sleep(2)

def clearPlus_handler(mainhandler, case):
    '''
    万能删除，本系统的有些输入框无法理解，用clear()无法彻底删除
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    selector = case.get('selector')
    ele = get_element(driver, selector)
    driver.execute_script("arguments[0].value = '';", ele)
    # driver.execute_script('document.querySelector("css选择器").value=""') #通过css选择器选取元素再把value清空
    # driver.find_element_by_id("id").send_keys(keys.CONTROL,"a")
    # driver.find_element_by_id("id").send_keys(keys.DELETE)
    # driver.find_element_by_id("id").send_keys(keys.BACKSPACE)
    # ActionChains(driver).double_click(ele).perform() #通过双击全选

def login_handler(mainhandler, case=None):
    '''
    登录乾薪通关键字
    :param mainhandler:
    :param case:
    :return:
    '''
    login(mainhandler.driver, mainhandler.g_config, case)

def login(driver, g_config, case=None):
    '''
    登录乾薪通
    :param driver:
    :param g_config:
    :param case:
    :return:
    '''
    username = ""
    password = ""
    val = ''
    if case is not None:
        val = str(case.get("val"))
    if val != "":
        val = eval(val)
        username = val.get("username")
        password = val.get("password")
    try:
        driver.get(g_config.get("url"))
        sleep(1)
        driver.maximize_window()
        driver.find_element_by_css_selector('[name="username"][class="el-input__inner"]').send_keys(
            username if username != "" else g_config.get("username"))
        driver.find_element_by_css_selector('[name="password"][class="el-input__inner"]').send_keys(
            password if password != "" else g_config.get("password"))
        driver.find_element_by_css_selector('[placeholder="请输入图形验证码"]').send_keys("1234")
        driver.find_element_by_xpath('(//span[@class="el-checkbox__inner"])[1]').click()
        driver.find_element_by_xpath('(//span[@class="el-checkbox__inner"])[2]').click()
        # sleep(10)
        driver.find_element_by_css_selector(
            '[type="button"][class="el-button el-button--primary el-button--medium"]').click()
        sleep(1)
    except:
        print("登录失败，请检查登录功能")
        pass

def login1_handler(mainhandler, case=None):
    '''
    登录乾薪通关键字
    :param mainhandler:
    :param case:
    :return:
    '''
    login_1(mainhandler.driver, mainhandler.g_config,mainhandler.t_opt, case)

def login_1(driver, g_config, t_opt, case=None):
    '''
    登录乾薪通
    :param driver:
    :param g_config:
    :param case:
    :return:
    '''
    username = ""
    password = ""
    val = ''
    if case is not None:
        val = str(case.get("val"))
    if val != "":
        val = eval(val)
        username = val.get("username")
        password = val.get("password")
    try:
        driver.get(g_config.get("url"))
        sleep(1)
        driver.maximize_window()
        driver.find_element_by_css_selector('[name="username"][class="el-input__inner"]').send_keys(
            username if username != "" else g_config.get("username"))
        driver.find_element_by_css_selector('[name="password"][class="el-input__inner"]').send_keys(
            password if password != "" else g_config.get("password"))
        driver.find_element_by_css_selector('[placeholder="请输入图形验证码"]').send_keys("1234")
        driver.find_element_by_xpath('(//span[@class="el-checkbox__inner"])[1]').click()
        driver.find_element_by_xpath('(//span[@class="el-checkbox__inner"])[2]').click()
        driver.find_element_by_css_selector(
            '[type="button"][class="el-button el-button--primary el-button--medium"]').click()
        sleep(1)
        try:
            driver.find_element_by_css_selector('[placeholder="客户名称"]').click()
            sleep(1)
            tar = "//span[text()='%s']" % t_opt.get('customer')
            driver.find_element_by_xpath(tar).click()
        except:
            pass
    except:
        print("登录失败，请检查登录功能")
        pass

def logout_handler(mainhandler, case=None):
    '''
    登出关键字
    :param mainhandler:
    :param case:
    :return:
    '''
    logout(mainhandler.driver, mainhandler.g_config, case)

def logout(driver, g_config, case=None):
    '''
    登出功能
    :param driver:
    :param g_config:
    :param case:
    :return:
    '''
    username = ''
    password = ''
    val = ''
    if case is not None:
        val = str(case.get("val"))
    if val != "":
        val = eval(val)
        username = val.get("username")
        password = val.get("password")
    try:
        driver.find_element_by_xpath('//div[@class="right-menu"]/div[3]/div[1]').click()
        driver.find_element_by_xpath('//div[@class="right-menu"]/div[3]/div[2]/div[2]/p[text()="退出"]').click()
        ##########
        sleep(1.5)
        driver.find_element_by_css_selector('[name="username"][class="el-input__inner"]').click()
        driver.find_element_by_xpath('//span/span/i').click()
        driver.find_element_by_css_selector('[name="username"][class="el-input__inner"]').send_keys(
            username if username != "" else g_config.get("username"))
        ########
        driver.find_element_by_css_selector('[name="password"][class="el-input__inner"]').send_keys(
            password if password != "" else g_config.get("password"))
        driver.find_element_by_css_selector('[placeholder="请输入图形验证码"]').send_keys("1234")
        # sleep(10)
        driver.find_element_by_css_selector(
            '[type="button"][class="el-button el-button--primary el-button--medium"]').click()
    except:
        print("登录失败，请检查登录功能")
        pass

def sleep_handler(mainhandler, case=None):
    '''
    睡眠关键字
    :return:
    '''
    val = case.get("val")
    num = val if val is not None and val != "" else 1
    sleep(num)

def select_handler(mianhandler, case=None):
    '''
    选择下拉框元素关键字
    :param mianhandler:
    :param case:
    :return:
    '''
    driver = mianhandler.driver
    selector = case.get("selector")
    val = format_digit_str(case.get("val"))
    get_element(driver, selector).click()
    sleep(2)
    tar = "//span[text()='%s']" % val
    driver.find_element_by_xpath(tar).click()

def get_IndeInfoConfig_url(driver):
    '''
    获取自主入职信息配置的链接地址
    :param driver:
    :return:
    '''
    sel = '//div[text()="开工啦！！！"]/../../preceding-sibling::div/div'
    linkURL = driver.find_element_by_xpath(sel).get_attribute("title")
    print(linkURL)
    return linkURL

def openURL_handler(mainhandler, case=None):
    '''
    打开自定义的网页
    :param mainhandler:
    :param case:
    :return:
    '''
    val = case.get('val')
    if val == '模板链接':
        val = get_IndeInfoConfig_url(mainhandler.driver)
    open_url(mainhandler.driver, val, mainhandler.g_config)

def open_url(driver, url, g_config=None):
    '''
    打开url
    :return:
    '''
    if url is not None:
        if url in ('qthl_url'):
            url = g_config.get(url)
        switch_to_cur_win_ifchange(driver,lambda: driver.execute_script("window.open('{}')".format(url)))

def close_tab(driver, num=0):
    '''
    关闭指定数量的标签页
    :param driver:
    :param num:
    :return:
    '''
    for i in range(num):
        try:
            driver.close()
            switch_to_cur_win(driver)
        except Exception as e:
            print("窗口关闭异常：",e)

def closeTab_handler(mainhandler, case):
    '''
    关闭指定数量的浏览器标签页
    :param mainhandler:
    :param case:
    :return:
    '''
    val = case.get('val')
    num = 1
    if val != '' and (isinstance(val, float) or isinstance(val, str)):
        num = int(val)
    close_tab(mainhandler.driver, num)

def closeTabKeepOneWin_handler(mainhandler, case):
    '''
    关闭所有打开的标签页，仅留最开始的一个标签页
    :param mainhandler:
    :param case:
    :return:
    '''
    all_win_num = len(mainhandler.driver.window_handles)
    close_tab(mainhandler.driver,all_win_num-1)

def switchToOtherPage_handler(mainhandler, case):
    '''
    切换到其它页面，如：iframe，alert，窗口
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    val = case.get('val')
    if val == 'iframe':
        driver.switch_to.frame(get_element(driver, case.get('selector')))
    if val == 'alert':
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except:
            print('未找到alert')
    if val is not None and "win" in val:
        change_num = val.split(":")[1]
        val = -1 if change_num is None or change_num == "" else int(change_num)
        switch_to_win(driver, val)

def switchToMainframe_handler(mainhandler, case):
    '''
    切换到主页面
    :param mainhandler:
    :param case:
    :return:
    '''
    mainhandler.driver.switch_to.default_content()

def assert_handler(mainhandler, case):
    '''
    校验
    :param mainhandler:
    :param case:
    :return:
    '''
    val = case.get("val")
    selector = case.get("selector")
    desc = case.get("desc")
    if val == 'text:最低小时工资:请输入数字，最多两位小数':
        assert_key = 'text'
        assert_val = '最低小时工资:请输入数字，最多两位小数'
    else:
        assert_key, assert_val = val.split(":")
    if assert_val in ['True', 'False']:
        assert_val = True if assert_val == 'True' else False
    if assert_val in ['自主入职职员','员工信息添加职员','员工数据维护添加职员']:
        assert_val = temporaryDick['name']
    globals().get(f"assert_{assert_key}_handler")(
        mainhandler.driver, selector, assert_val, desc)

def assert_isAlert_handler(driver, selector, assert_val, desc):
    '''
    校验alert弹窗是否存在,（带“确定”按钮的那种）
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    # alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = EC.alert_is_present()(driver)
    if alert and assert_val == True:
        print(f"{desc}{assert_val}校验成功")
    else:
        raise Exception(f"{desc}{assert_val}校验失败")

def assert_text_handler(driver, selector, assert_val, desc):
    '''
    断言元素的文本
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    text = get_element(driver, selector).text
    if text != assert_val:
        print("lll",text)
        raise Exception(f"{desc} {selector} 校验失败")
    elif text == assert_val:
        print(f"{desc} {selector} 校验成功")

def assert_text1_handler(driver, selector, assert_val, desc):
    '''
    断言元素的文本,采用get_attribute()方法
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    text = get_element(driver, selector).get_attribute('textContent')
    if text != assert_val:
        print("lll",text)
        raise Exception(f"{desc} {selector} 校验失败")
    elif text == assert_val:
        print(f"{desc} {selector} 校验成功")

def assert_ele_count_handler(driver, selector, assert_val, desc):
    '''
    断言元素的个数
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    try:
        ele_list = driver.find_elements_by_css_selector(selector)
    except:
        ele_list = driver.find_elements_by_xpath(selector)
    if len(ele_list) != str(assert_val):
        raise Exception(f"{desc} {selector} 校验失败")
    else:
        print(f"{desc} {selector} 校验成功")

def assert_ele_exist_handler(driver, selector, assert_val, desc):
    '''
    校验元素是否存在
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    try:
        ele = get_element(driver, selector)
        if ele and ele.is_displayed() != False and assert_val == False:
            # sleep(2)
            raise Exception(f"{desc} {selector} 校验失败")
        else:
            print(f"{desc} {selector} 校验成功")
    except TimeoutException:
        if assert_val == True:
            # sleep(2)
            raise Exception(f"{desc} {selector} 校验失败")
        else:
            print(f"{desc} {selector} 校验成功")

def assert_ele_enabled_handler(driver, selector, assert_val, desc):
    '''
    校验元素是否可编辑、点击
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    ele = get_element(driver, selector)
    if ele and ele.is_enabled() != False and assert_val == False:
        raise Exception(f"{desc} {selector} 校验失败")
    else:
        print(f"{desc} {selector} 校验成功")

def get_input_val(driver, selector):
    value = ""
    try:
        ele = get_element(driver, selector)
        value = ele.get_attribute("value")
        # print(value)
    except:
        pass
    return value

def assert_input_val_handler(driver, selector, assert_val, desc):
    '''
    校验input输入框的值
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    value = get_input_val(driver, selector)
    print("assert_value", assert_val)
    print("value:", value)
    if value != assert_val:
        raise Exception(f"{desc} {selector} 校验失败")
    elif value == assert_val:
        print(f"{desc} {selector} 校验成功")

def assert_table_header_handler(driver, selector, assert_val, desc):
    '''
    校验表头的字段
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    try:
        eles = driver.find_elements_by_css_selector(selector)
    except:
        eles = driver.find_elements_by_xpath(selector)
    if len(eles) == len(assert_val) + 1:
        tableHead = []
        for i in range(len(eles) - 1):
            if selector.startswith("/"):
                sel = selector + f"[{i + 2}]/div"
            else:
                sel = selector + f":nth-child({i + 2})>div"
            tex = get_element(driver, sel).get_attribute('textContent')
            tableHead.append(tex)
        # print(tableHead)
        if assert_val == tableHead:
            print(f"{desc} {selector} 校验成功")
        else:
            raise Exception(f"{desc} {selector} 校验失败")
    else:
        raise Exception(f"{desc} {selector} 校验失败")

def assert_dropDownBox_handler(driver, selector, assert_val, desc):
    '''
    校验下拉框的内容
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    print(assert_val)
    print(selector)
    # print(len(assert_val))
    try:
        eles = driver.find_elements_by_css_selector(selector)
    except:
        eles = driver.find_elements_by_xpath(selector)
    # print(eles)
    print('长长长度：', len(eles))
    if len(eles) == len(assert_val):
        dropDownList = []
        for i in range(len(eles)):
            if selector.endswith("div"):
                if selector.startswith("/") or selector.startswith("("):
                    sel = selector + f"[{i + 1}]/label/span[2]"
                else:
                    sel = selector + f":nth-child({i + 1})>label>span:nth-child(2)"
            else:
                if selector.startswith("/") or selector.startswith("("):
                    sel = selector + f"[{i + 1}]/span"
                else:
                    sel = selector + f":nth-child({i + 1})>span"
            tex = get_element(driver, sel).get_attribute('textContent')
            dropDownList.append(tex)
        # print("下拉项汇总",dropDownList)
        # print(len(dropDownList))

        if assert_val == dropDownList:
            print(f"{desc} {selector} 校验成功")
        else:
            raise Exception(f"{desc} {selector} 校验失败")
    else:
        raise Exception(f"{desc} {selector} 校验失败")

def assert_index_count_handler(driver, selector, assert_val, desc):
    '''
    校验员工数据维护-表格第一行的数据的名字
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    if assert_val == None or assert_val == "":
        assert_val = temporaryDick.get('name')
    else:
        assert_val = assert_val
    print(assert_val)
    sel = '//*[@id="table"]/div[3]/table/tbody/tr[1]/td[2]//p[1]/span[1]'
    tex = get_element(driver, sel).get_attribute('textContent')
    print(tex)
    if assert_val == tex:
        print(f"{desc} {sel} 校验成功")
    else:
        raise Exception(f"{desc} {sel} 校验失败")

def assert_accuratePayrollCycle_handler(driver, selector, assert_val, desc):
    '''
    校验薪资业务配置-薪资周期精确搜索
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    sel = '//*[@id="table"]/div[3]/table/tbody/tr'
    eles = driver.find_elements_by_xpath(sel)
    print(eles)
    print('长长长度：', len(eles))
    set1 = set()
    for i in range(len(eles)):
        sel_1 = f"{sel}[{i + 1}]/td[2]/div/span"  # 姓名定位
        tex = get_element(driver, sel_1).get_attribute('textContent')
        set1.add(tex)
    setToList = list(set1)
    if len(setToList) > 1 or len(setToList) == 0:
        raise Exception(f"{desc} {sel} 校验失败")
    if len(setToList) == 1:
        if setToList == assert_val:
            print(f"{desc} {sel} 校验成功")
        else:
            raise Exception(f"{desc} {sel} 校验失败")

def assert_FuzzyPayrollCycle_handler(driver, selector, assert_val, desc):
    '''
    校验薪资业务配置-薪资周期模糊搜索
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    sel = '//*[@id="table"]/div[3]/table/tbody/tr'
    eles = driver.find_elements_by_xpath(sel)
    print(eles)
    print('长长长度：', len(eles))
    set1 = set()
    if len(eles) == 0:
        raise Exception(f"{desc} {sel} 校验失败")
    else:
        for i in range(len(eles)):
            sel_1 = f"{sel}[{i + 1}]/td[2]/div/span"  # 姓名定位
            tex = get_element(driver, sel_1).get_attribute('textContent')
            set1.add(tex)
        setToList = list(set1)
        # print(setToList)
        # print(assert_val)
        for data in setToList:
            # print(data)
            if data.find(assert_val[0]) > -1:
                pass
            else:
                raise Exception(f"{desc} {sel} 校验失败")
        print(f"{desc} {sel} 校验成功")

def assert_accurateSearch_handler(driver, selector, assert_val, desc):
    '''
    校验员工数据维护-精确搜索出来的数据的相关属性，属性需要列表中展示的属性
    姓名、编号、职位、部门、证件类型、用工性质、员工类型、员工状态
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    print(assert_val)
    # print(len(assert_val))
    sel = '//*[@id="table"]/div[3]/table/tbody/tr'
    eles = driver.find_elements_by_xpath(sel)
    print(eles)
    print('长长长度：', len(eles))
    set1 = set()
    for i in range(len(eles)):

        sel_1 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[1]/span[1]"  # 姓名定位
        sel_2 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[1]/span[2]"  # 编号定位
        sel_3 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[2]/span[1]"  # 职位名称定位
        sel_4 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[2]/span[2]"  # 部门名称定位
        sel_5 = f"{sel}[{i + 1}]/td[3]/div/span"  # 证件类型定位
        sel_6 = f"{sel}[{i + 1}]/td[5]/div/span"  # 用工性质列对应的属性
        sel_7 = f"{sel}[{i + 1}]/td[6]/div/span"  # 员工类型列对应的属性
        sel_8 = f"{sel}/td[7]/div/span"  # 员工状态列对应的属性
        tex = ''
        if assert_val[0] == '姓名':
            tex = get_element(driver, sel_1).get_attribute('textContent')
        if assert_val[0] == '编号':
            tex = get_element(driver, sel_2).get_attribute('textContent')
        if assert_val[0] == '职位' or assert_val[0] == '岗位':
            tex = get_element(driver, sel_3).get_attribute('textContent')
        if assert_val[0] == '部门':
            tex = get_element(driver, sel_4).get_attribute('textContent')
        if assert_val[0] == '证件类型':
            tex = get_element(driver, sel_5).get_attribute('textContent')
        if assert_val[0] == '用工性质':
            tex = get_element(driver, sel_6).get_attribute('textContent')
        if assert_val[0] == '员工类型' or assert_val[0] == '薪资组':
            tex = get_element(driver, sel_7).get_attribute('textContent')
        if assert_val[0] == '员工状态':
            tex = get_element(driver, sel_8).get_attribute('textContent')
        set1.add(tex)
    setToList = list(set1)
    if len(setToList) > 1:
        raise Exception(f"{desc} {sel} 校验失败")
    if len(setToList) == 1 or len(setToList) == 0:
        if setToList[0] == assert_val[1]:
            print(f"{desc} {sel} 校验成功")
        else:
            raise Exception(f"{desc} {sel} 校验失败")

def assert_FuzzySearch_handler(driver, selector, assert_val, desc):
    '''
    校验员工数据维护-模糊搜索出来的数据的相关属性，属性需要列表中展示的属性
    姓名、编号、职位、部门、证件类型、用工性质、员工类型、员工状态
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    print(assert_val)
    # print(len(assert_val))
    sel = '//*[@id="table"]/div[3]/table/tbody/tr'
    eles = driver.find_elements_by_xpath(sel)
    print(eles)
    print('长长长度：', len(eles))
    set1 = set()
    if len(eles) == 0:
        raise Exception(f"{desc} {sel} 校验失败")
    else:
        for i in range(len(eles)):

            sel_1 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[1]/span[1]"  # 姓名定位
            sel_2 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[1]/span[2]"  # 编号定位
            sel_3 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[2]/span[1]"  # 职位名称定位
            sel_4 = f"{sel}[{i + 1}]/td[2]/div/div/div[2]/p[2]/span[2]"  # 部门名称定位
            sel_5 = f"{sel}[{i + 1}]/td[3]/div/span"  # 证件类型定位
            sel_6 = f"{sel}[{i + 1}]/td[5]/div/span"  # 用工性质列对应的属性
            sel_7 = f"{sel}[{i + 1}]/td[6]/div/span"  # 员工类型列对应的属性
            sel_8 = f"{sel}/td[7]/div/span"  # 员工状态列对应的属性
            tex = ''
            if assert_val[0] == '姓名':
                tex = get_element(driver, sel_1).get_attribute('textContent')
            if assert_val[0] == '编号':
                tex = get_element(driver, sel_2).get_attribute('textContent')
            if assert_val[0] == '职位' or assert_val[0] == '岗位':
                tex = get_element(driver, sel_3).get_attribute('textContent')
            if assert_val[0] == '部门':
                tex = get_element(driver, sel_4).get_attribute('textContent')
            if assert_val[0] == '证件类型':
                tex = get_element(driver, sel_5).get_attribute('textContent')
            if assert_val[0] == '用工性质':
                tex = get_element(driver, sel_6).get_attribute('textContent')
            if assert_val[0] == '员工类型':
                tex = get_element(driver, sel_7).get_attribute('textContent')
            if assert_val[0] == '员工状态':
                tex = get_element(driver, sel_8).get_attribute('textContent')
            set1.add(tex)
        setToList = list(set1)
        for data in setToList:
            if data.find(f"{assert_val[1]}") > -1:
                pass
            else:
                raise Exception(f"{desc} {sel} 校验失败")
        print(f"{desc} {sel} 校验成功")

def assert_deleteStaff_handler(driver, selector, assert_val, desc):
    '''
    删除勾选的员工数据并检验成功删除,选择前两条数据删除
    :param driver:
    :return:
    '''
    sel5 = '//*[@id="table"]/div[3]/table/tbody/tr[1]/td[2]/div/div/div[2]/p[1]/span[1]'
    sel6 = '//*[@id="table"]/div[3]/table/tbody/tr[2]/td[2]/div/div/div[2]/p[1]/span[1]'
    tex1 = get_element(driver, sel5).get_attribute('textContent')
    tex2 = get_element(driver, sel6).get_attribute('textContent')
    print('未删除前的前两条数据是：',tex1, tex2)

    sel1 = '//*[@id="table"]/div[3]/table/tbody/tr[1]/td[1]/div/div/span'
    sel2 = '//*[@id="table"]/div[4]/div[2]/table/tbody/tr[1]/td[1]/div/div/label/span/span'
    sel3 = '//*[@id="table"]/div[3]/table/tbody/tr[2]/td[1]/div/div/span'
    sel4 = '//*[@id="table"]/div[4]/div[2]/table/tbody/tr[2]/td[1]/div/div/label/span/span'

    switch_to_cur_win_ifchange(
        driver,
        lambda: ActionChains(driver).move_to_element(
            get_element(driver, sel1)).perform())
    driver.find_element_by_xpath(sel2).click()
    switch_to_cur_win_ifchange(
        driver,
        lambda: ActionChains(driver).move_to_element(
            get_element(driver, sel3)).perform())
    driver.find_element_by_xpath(sel4).click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="excel-upload-input"]/../div[3]/span').click()
    sleep(1)
    driver.find_element_by_xpath(
        "//ul[starts-with(@id,'dropdown-menu')]/li[2][text()=' 勾选删除 ']").click()
    sleep(1)
    driver.find_element_by_xpath("//div[@class='el-message-box__btns']/button[2]/span").click()
    sleep(1)
    tex3 = get_element(driver, sel5).get_attribute('textContent')
    tex4 = get_element(driver, sel6).get_attribute('textContent')
    print('删除后的前两条数据是：', tex3, tex4)
    if tex1 == tex3 and tex2 == tex4:
        raise Exception(f"{desc} 校验失败")
    else:
        print(f"{desc} 校验成功")

def assert_calendarName_handler(driver, selector, assert_val, desc):
    '''
    校验薪资业务配置-年度日历配置：卡片的名称与期望名称一致
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    assert_val = set(assert_val)
    # sel = "//div[@class='calender-list']/div"
    sel = selector
    eles = driver.find_elements_by_xpath(sel)
    NameList = []
    if eles is None:
        if NameList != assert_val:
            raise Exception(f"{desc} 校验失败")
        else:
            print(f"{desc} 校验成功")
    else:
        for i in range(len(eles)):
            sel1 = f"{sel}{[i + 1]}/div/div/div/span"  # 日历名称定位
            tex = get_element(driver, sel1).get_attribute('textContent')
            print(tex)
            NameList.append(tex)
        if set(NameList) != assert_val:
            raise Exception(f"{desc} 校验失败")
        else:
            print(f"{desc} 校验成功")

def assert_salaryGroupName_handler(driver, selector, assert_val, desc):
    '''
    校验薪资业务配置-薪资组配置：卡片的名称与期望名称一致
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    assert_val = set(assert_val)
    # sel = "//div[@class='calender-list']/div"
    sel = selector
    eles = driver.find_elements_by_xpath(sel)
    NameList = []
    if eles is None:
        if NameList != assert_val:
            raise Exception(f"{desc} 校验失败")
        else:
            print(f"{desc} 校验成功")
    else:
        for i in range(len(eles)):
            sel1 = f"{sel}{[i + 1]}/div[2]/div[2]/div[2]"  # 日历名称定位
            tex = get_element(driver, sel1).get_attribute('textContent')
            print(tex)
            NameList.append(tex)
        if set(NameList) != assert_val:
            raise Exception(f"{desc} 校验失败")
        else:
            print(f"{desc} 校验成功")

def assert_PaidPersonnelName_handler(driver, selector, assert_val, desc):
    '''
    校验薪资业务配置-计薪人员组：卡片的名称与期望名称一致
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    assert_val = set(assert_val)
    # sel = "//div[@class='calender-list']/div"
    sel = selector
    eles = driver.find_elements_by_xpath(sel)
    NameList = []
    if eles is None:
        if NameList != assert_val:
            raise Exception(f"{desc} 校验失败")
        else:
            print(f"{desc} 校验成功")
    else:
        for i in range(len(eles)):
            sel1 = f"{sel}{[i + 1]}/div[1]/div/span"  # 日历名称定位
            tex = get_element(driver, sel1).get_attribute('textContent')
            print(tex)
            NameList.append(tex)
        if set(NameList) != assert_val:
            raise Exception(f"{desc} 校验失败")
        else:
            print(f"{desc} 校验成功")

def assert_courseName_handler(driver, selector, assert_val, desc):
    '''
    校验薪资组配置-详细信息-科目名称
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    print(assert_val)
    sel = '//ul[@class="dialog-m-ul"]/li'
    eles = driver.find_elements_by_xpath(sel)
    print('长长长度：', len(eles))
    if len(eles) == len(assert_val):
        CourseList = []
        for i in range(len(eles)):
            sel1 =  sel + f"[{i + 1}]/span"
            tex = get_element(driver, sel1).get_attribute('textContent')
            CourseList.append(tex)
        print(CourseList)
        if assert_val == CourseList:
            print(f"{desc}校验成功")
        else:
            raise Exception(f"{desc}校验失败")
    else:
        raise Exception(f"{desc}校验失败")

def assert_reference_handler(driver, selector, assert_val, desc):
    '''
    校验薪资业务配置-薪资公式配置-引用项目/科目名称/函数
    :return:
    '''
    assert_val = eval(assert_val)
    sel1 = selector
    eles = driver.find_elements_by_xpath(sel1)
    datalist = []
    for i in range(len(eles)):
        sel2 = f"{sel1}[{i+1}]/td[3]/div/span"
        tex = get_element(driver, sel2).get_attribute('textContent')
        datalist.append(tex)
    print(datalist)
    if set(datalist) == set(assert_val):
        print(f"{desc}校验成功")
    else:
        print(set(datalist) ^ set(assert_val))
        raise Exception(f"{desc}校验失败")

def assert_importFile_handler(driver, selector, assert_val, desc):
    '''
    校验出勤数据导入，各输入框的校验
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    sel =  '//tr[@class="elx-body--row"]/td'
    sel1 = '//tr[@class="elx-body--row"]/td[@data-colid="col_7"]'   #实际工作小时数，从col_7开始，至col_68结束，共62个
    sel2 = '//tr[@class="elx-body--row"]/td[@data-colid="col_5"]'   #证件号码
    sel3 = '//tr[@class="elx-body--row"]/td[@data-colid="col_6"]'   #姓名
    data = ['实际工作小时数','计件数量','病假天数','病假小时','医疗期','事假天数','事假小时','产前假天数','产前假小时',
            '产假天数','陪产假天数','陪产假小时','哺乳假天数','哺乳假小时','旷工天数','旷工小时','不扣薪假天数','不扣薪假小时',
            '年假剩余天数','年假剩余小时','法定离退休实际月数','病假扣款调整','事假扣款调整','产前假扣款调整','哺乳假扣款调整',
            '旷工扣款调整','年假折现调整','转正前应勤天数','转正前实际工作天数','试用中实际工作天数','试用中应勤天数',
            '迟到分钟','迟到次数','早退分钟','早退次数','工作日加班天数','工作日加班小时','假日加班天数','假日加班小时',
            '节日加班天数','节日加班小时','特殊加班天数','特殊加班小时','支援次数','支援天数','支援小时数','早班次数','中班次数',
            '晚班次数','夜间次数','工作日加班工资调整','假日加班工资调整','节日加班工资调整','特殊加班工资调整',
            '工作日加班转调休小时数','工作日加班转调休天数','假日加班转调休小时数','假日加班转调休天数','工作日加班转调休金额',
            '假日加班转调休金额','迟到扣款标准','早退扣款标准']
    errData = []
    for i in range(62):
        sel4 = f"{sel}[@data-colid='col_{i+7}']/div/div/p[contains(@class,'item pointer')]"
        print(sel4)
        sel5 = f'//span[text()="{data[i]}"]' #表头元素
        print(sel5)
        try:
            if i<=1:
                pass
            else:
                js = f'document.getElementsByClassName("elx-table--body-wrapper body--wrapper")[0].scrollLeft={360*(i // 2)+80}'
                driver.execute_script(js)
                sleep(1)
            desc1 = f"{data[i]}字段内容为红色"
            assert_ele_exist_handler(driver, sel4, 'True', desc1)
            switch_to_cur_win_ifchange(
                driver,
                lambda: ActionChains(driver).move_to_element(
                    get_element(driver, sel4)).perform())
            sleep(1)
            assert_val = data[i]+'请输入数值，最多保留三位小数'
            desc2 = f"悬浮至{data[i]}出现提示语句:{assert_val}"
            assert_text_handler(driver, '(//div[@role="tooltip"])[last()]', assert_val, desc2)
        except:
            errdata = f'{data[i]}校验错误'
            print(errdata)
            errData.append(data[i])
    if errData == []:
        print("校验成功")
    else:
        print(errData)
        raise Exception('校验失败！！！')

def assert_importFileSalary_handler(driver, selector, assert_val, desc):
    '''
    校验薪资数据导入，各输入框的校验
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    dir = assert_val[0]
    file_name = assert_val[1]
    sel =  '//tr[@class="elx-body--row"]/td'
    ##津贴薪金数据类
    file_path = getTestData(dir,file_name)
    data = getTemplate(file_path)
    # print(data)
    data.remove('证件号码')
    data.remove('姓名')
    errData = []
    for i in range(len(data)):
        sel4 = f"{sel}[@data-colid='col_{i+7}']/div/div/p[contains(@class,'item pointer')]"
        print(sel4)
        sel5 = f'//span[text()="{data[i]}"]' #表头元素
        print(sel5)
        try:
            if i<=1:
                pass
            else:
                js = f'document.getElementsByClassName("elx-table--body-wrapper body--wrapper")[0].scrollLeft={360*(i // 2)+80}'
                driver.execute_script(js)
                sleep(1)
            desc1 = f"{data[i]}字段内容为红色"
            assert_ele_exist_handler(driver, sel4, 'True', desc1)
            switch_to_cur_win_ifchange(
                driver,
                lambda: ActionChains(driver).move_to_element(
                    get_element(driver, sel4)).perform())
            sleep(1)
            assert_val = data[i]+'请输入数值，最多保留三位小数'
            desc2 = f"悬浮至{data[i]}出现提示语句:{assert_val}"
            assert_text_handler(driver, '(//div[@role="tooltip"])[last()]', assert_val, desc2)
        except:
            errdata = f'{data[i]}校验错误'
            print(errdata)
            errData.append(data[i])
    if errData == []:
        print("校验成功")
    else:
        print(errData)
        raise Exception('校验失败！！！')

def assert_allowanceEntryRules_handler(driver, selector, assert_val, desc):
    '''
    校验薪资数据维护-详情-各输入框的输入规则
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    ##津贴薪金数据类
    data1=['车辆补贴','交通补贴','餐费补贴','通讯补贴','职位补贴','岗位补贴','节日礼金','年会奖品',
          '停车费','探亲假路费','高温津贴','保健食品费','住房津贴','出差津贴','现场津贴','调动津贴',
          '生活成本津贴','医疗津贴','采暖津贴','职工困难补贴','销售提成','救济费','早班津贴','早班津贴调整',
          '中班津贴','中班津贴调整','晚班津贴','晚班津贴调整','夜间津贴','夜间津贴调整','支援津贴','支援津贴调整',
          '中班餐费津贴','晚班餐费津贴','夜间餐费津贴','绩效奖金','计件奖金','综合奖金','突破奖金','季度奖金',
          '年中奖金']
    ##绩效工资类
    data2 = ['绩效工资额度', '个人考核系数（%）', '公司效益系数（%）',
             '绩效工资']
    ##专向附加扣除
    data3 = ['累计子女教育_专项扣除', '累计继续教育_专项扣除', '累计住房贷款_专项扣除',
             '累计住房租金_专项扣除','累计赡养老人_专项扣除']
    ##社会保险类
    data4 = ['个人养老基数', '个人医疗基数', '个人大病医疗基数', '个人失业基数', '企业养老基数', '企业医疗基数',
             '企业大病医疗基数', '企业失业基数', '企业工伤基数', '企业生育基数','企业残保金基数', '企业采暖费基数',
             '个人养老比例（%）', '个人医疗比例（%）', '个人大病医疗比例（%）', '个人失业比例（%）', '企业养老比例（%）', '企业医疗比例（%）',
             '企业大病医疗比例（%）', '企业失业比例（%）', '企业工伤比例（%）', '企业生育比例（%）', '企业残保金比例（%）', '企业采暖费比例（%）',
             '个人养老', '个人养老补缴', '个人养老补差', '个人养老退费', '个人医疗', '个人医疗补缴',
             '个人医疗补差', '个人医疗退费', '个人大病医疗', '个人大病医疗补缴', '个人大病医疗补差', '个人大病医疗退费',
             '个人失业', '个人失业补缴', '个人失业补差', '个人失业退费', '个人偶发性费用', '个人偶发性费用补缴',
             '个人偶发性费用补差', '个人偶发性费用退费', '企业养老', '企业养老补缴', '企业养老补差', '企业养老退费',
             '企业医疗', '企业医疗补缴', '企业医疗补差', '企业医疗退费', '企业大病医疗', '企业大病医疗补缴',
             '企业大病医疗补差', '企业大病医疗退费', '企业失业', '企业失业补缴', '企业失业补差', '企业失业退费',
             '企业工伤', '企业工伤补缴', '企业工伤补差','企业工伤退费', '企业生育',
             '企业生育补缴', '企业生育补差', '企业生育退费', '企业残保金', '企业残保金补缴',
             '企业残保金补差', '企业残保金退费', '企业采暖费', '企业采暖费补缴', '企业采暖费补差',
             '企业采暖费退费', '企业偶发性费用', '企业偶发性费用补缴', '企业偶发性费用补差', '企业偶发性费用退费', '个人养老汇缴调整值',
             '个人养老补缴调整值', '个人养老补差调整值', '个人医疗汇缴调整值', '个人医疗补缴调整值', '个人医疗补差调整值', '个人大病医疗汇缴调整值',
             '个人大病医疗补缴调整值', '个人大病医疗补差调整值', '个人失业汇缴调整值', '个人失业补缴调整值', '个人失业补差调整值',
             '个人偶发性费用汇缴调整值', '个人偶发性费用补缴调整值', '个人偶发性费用补差调整值', '企业养老汇缴调整值',
             '企业养老补缴调整值', '企业养老补差调整值', '企业医疗汇缴调整值', '企业医疗补缴调整值', '企业医疗补差调整值', '企业大病医疗汇缴调整值',
             '企业大病医疗补缴调整值', '企业大病医疗补差调整值', '企业失业汇缴调整值', '企业失业补缴调整值', '企业失业补差调整值', '企业工伤汇缴调整值',
             '企业工伤补缴调整值', '企业工伤补差调整值', '企业生育汇缴调整值', '企业生育补缴调整值', '企业生育补差调整值',
             '企业残保金汇缴调整值', '企业残保金补缴调整值', '企业残保金补差调整值', '企业采暖费汇缴调整值', '企业采暖费补缴调整值',
             '企业采暖费补差调整值', '企业偶发性汇缴调整值', '企业偶发性补缴调整值', '企业偶发性补差调整值', '个人社保合计调整值', '企业社保合计调整值']
    ##住房公积金类
    data5 = ['个人公积金基数', '个人公积金比例（%）', '个人补充公积金基数', '个人补充公积金比例（%）', '企业公积金基数', '企业公积金比例（%）',
             '企业补充公积金基数', '企业补充公积金比例（%）', '个人公积金', '个人公积金补缴', '个人公积金补差',
             '个人公积金退费', '企业公积金', '企业公积金补缴', '企业公积金补差', '企业公积金退费', '个人补充公积金',
             '个人补充公积金补缴','个人补充公积金补差', '个人补充公积金退费', '企业补充公积金', '企业补充公积金补缴', '企业补充公积金补差',
             '企业补充公积金退费', '个人公积金汇缴调整值', '个人公积金补缴调整值', '个人公积金补差调整值', '个人公积金小计', '企业公积金汇缴调整值',
             '企业公积金补缴调整值', '企业公积金补差调整值', '企业公积金小计', '个人补充公积金汇缴调整值', '个人补充公积金补缴调整值', '个人补充公积金补差调整值',
             '个人补充公积金小计', '企业补充公积金汇缴调整值', '企业补充公积金补缴调整值', '企业补充公积金补差调整值', '企业补充公积金小计', '个人公积金合计调整值',
             '个人补充公积金合计调整值', '企业公积金合计调整值', '企业补充公积金合计调整值']
    ##个人所得税
    data6 = ['工资薪金所得税', '奖金税', '劳务报酬所得税', '劳务报酬所得税_保证其他', '离职补偿金税', '股票期权税',
             '利息、股息、红利所得税', '偶然所得税', '稿酬所得税', '特许权使用费所得税', '财产租赁所得税', '财产转让所得税',
             '提前退休一次性补贴收入税', '工资薪金所得税调整', '奖金税调整', '劳务报酬所得税调整', '劳务报酬所得税_保证其他调整', '离职补偿金税调整',
             '股票期权税调整', '利息_股息_红利所得税调整', '偶然所得税调整', '稿酬所得税调整', '特许权使用费所得税调整', '财产租赁所得税调整',
             '财产转让所得税调整', '提前退休一次性补贴收入税调整', '个人所得税合计调整']
    ##计税不发薪类
    data7 = ['捐款', '税延养老保险税前抵扣', '商业健康险', '企业年金_免税', '公积金超额纳税金额',
             '残疾人免税额', '生育津贴标准']
    ##其它税前加项类
    data8 = ['其它税前加项', '其它税前调整', '工资不足抵扣_税前', '股票期权', '利息、股息、红利所得', '偶然所得',
             '代通知金', '离职补偿金', '稿酬所得', '特许权使用费所得',  '财产原值',
             '其它合理费用', '财产租赁所得', '财产转让所得', '企业年金_月度税', '企业年金_综合税', '提前退休一次性补贴收入',
             '内退一次性补偿收入']
    ##其它税前减项类
    data9 = ['其它税前减项', '其它税前调整_减项',
             '上月工资不足抵扣返回_税前']
    ##其它税后加项类
    data10 = ['报销', '体检费', '独生子女费', '其它税后加项', '其它税后调整',
              '企业年金_税后', '工资不足抵扣_税后']
    ##其它税后减项类
    data11 = ['其它税后减项', '其它税后调整_减项',
              '上月工资不足抵扣返回_税后']
    ##其它类
    data12 = ['工会经费', '招聘费', '教育经费',
              '培训费', '服务费', '增值税率']
    ##年终奖数据类
    data13 = ['13薪', '年终奖', '年度销售奖金', '特殊奖金',
              '录用奖金', '留用奖金', '一次性奖金', '忠诚奖金']
    ##外籍人免税类
    data14 = ['外籍人免税额', '语言训练费_外籍', '住房补贴_外籍', '子女教育费_外籍',
              '伙食补贴_外籍', '搬迁费_外籍', '洗衣费_外籍', '出差补贴_外籍', '探亲费_外籍'
]
    assert_val = eval(assert_val)
    salaryType = assert_val[0]
    # print(salaryType)
    inputType = assert_val[1]
    # print(inputType)
    if salaryType == '津贴资金数据类':
        salaryType = data1
    if salaryType == '绩效工资类':
        salaryType = data2
    if salaryType == '专项附加扣除类':
        salaryType = data3
    if salaryType == '社会保险类':
        salaryType = data4
    if salaryType == '住房公积金类':
        salaryType = data5
    if salaryType == '个人所得税类':
        salaryType = data6
    if salaryType == '计税不发薪类':
        salaryType = data7
    if salaryType == '其它税前加项类':
        salaryType = data8
    if salaryType == '其它税前减项类':
        salaryType = data9
    if salaryType == '其它税后加项类':
        salaryType = data10
    if salaryType == '其它税后减项类':
        salaryType = data11
    if salaryType == '其它类':
        salaryType = data12
    if salaryType == '年终奖数据类':
        salaryType = data13
    if salaryType == '外籍人免税类':
        salaryType = data14
    errData = []
    for i in range(len(salaryType)):
        sel = f"//label[text()='{salaryType[i]}']/following-sibling::div/div/input"
        if inputType == '特殊字符':
            driver.find_element_by_xpath(sel).send_keys(',./abC你好')
            value = get_input_val(driver, sel)
            if salaryType[i] == '是否是个人按市场价出租居民住房':
                selec = "//label[text()='是否是个人按市场价出租居民住房']/following-sibling::div/div[2]"
                delsel = "//label[text()='是否是个人按市场价出租居民住房']/following-sibling::div/div/span/span/i"
                tex = driver.find_element_by_xpath(selec).get_attribute('textContent')
                if tex != "请输入文本类型" and value != "abC你好":
                    errData.append(salaryType[i])
                driver.find_element_by_xpath(sel).click()
                driver.find_element_by_xpath(delsel).click()
            else:
                if value != "":
                    errData.append(salaryType[i])
        if inputType == '小数保留位数':
            driver.find_element_by_xpath(sel).send_keys(str(999.9999))
            value = get_input_val(driver, sel)
            if salaryType[i].find("（%）")>-1:
                if value != "100":
                    errData.append(salaryType[i])
            if salaryType[i] == '是否是个人按市场价出租居民住房':
                if value != "9999999":
                    errData.append(salaryType[i])
            if salaryType[i] != '是否是个人按市场价出租居民住房' and salaryType[i].find("（%）") == -1:
                if value != str(999.999):
                    errData.append(salaryType[i])
    if errData == []:
        print(assert_val[0],assert_val[1],'校验成功')
    else:
        print('校验失败的输入项：',errData)
        raise Exception(assert_val[0],assert_val[1],'校验失败')

def assert_homeDirectory_handler(driver, selector, assert_val, desc):
    '''
    校验主目录
    首页：//div[@class="menu-scrollbar-item"]/div/a/span[text()="首页"]
    员工管理：//div[@class="menu-scrollbar-item"]/div/span[text()="员工管理"]
    员工数据维护：//div[@class="menu-left-sidebar-block"]/a/span[text()='员工数据维护']
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    directory = []
    sel1 = '//div[@class="menu-scrollbar-item"]/div/a/span[text()="首页"]'
    sel2 = '//div[@class="menu-scrollbar-item"]/div/span'

    eles1 = driver.find_elements_by_xpath(sel1)
    if eles1 == []:
        pass
    else:
        directory.append('首页')
    eles2 = driver.find_elements_by_xpath(sel2)
    if eles2 == []:
        pass
    else:
        for ele in eles2:
            tex = ele.get_attribute('textContent')
            directory.append(tex)
    if assert_val == directory:
        print(f"{desc}校验成功")
    else:
        raise Exception(f"{desc}校验失败")

def assert_secondaryDirectory_handler(driver, selector, assert_val, desc):
    '''
    校验第二级目录
    员工数据维护：//div[@class="menu-left-sidebar-block"]/a/span[text()='员工数据维护']
    :param driver:
    :param selector:
    :param assert_val:
    :param desc:
    :return:
    '''
    assert_val = eval(assert_val)
    directory = []
    sel = '//div[@class="menu-left-sidebar-block"]/a/span'
    eles = driver.find_elements_by_xpath(sel)
    if eles == []:
        pass
    else:
       for ele in eles:
            tex = ele.get_attribute('textContent')
            directory.append(tex)
    if assert_val == directory:
        print(f"{desc}校验成功")
    else:
        raise Exception(f"{desc}校验失败")

def get_xiangmu_handler(mainhandler, case):
    '''
    获取薪资数据维护-详情页面的所有选项，输出字典
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel = '//div[@class="staff-data-salary-r-con"]'
    dic = {}
    for i in range(14):
        sel1 = f'({sel})[{i+1}]/div'
        eles = driver.find_elements_by_xpath(sel1)
        data = []
        for n in range(len(eles)):
            sel2 = f'{sel1}[{n+1}]/form/div/label'
            tex = driver.find_element_by_xpath(sel2).get_attribute('textContent')
            data.append(tex)
        dic[f"data{i+1}"] = data
    print(dic)

def dragLeftAngRight_handler(mainhandler, case):
    '''
    自定义拖动页面,左右拖动
    :param mainhandler:
    :param case:
    :return:
    '''
    val = case.get('val')
    driver = mainhandler.driver
    js = f'document.getElementsByClassName("elx-table--body-wrapper body--wrapper")[0].scrollLeft={val}'
    driver.execute_script(js)
    sleep(2)

def drag_handler(mainhandler, case):
    '''
    自定义拖动页面,上下拖动
    :param mainhandler:
    :param case:
    :return:
    '''
    val = case.get('val')
    driver = mainhandler.driver
    js = f"window.scrollTo(0,{val});"
    driver.execute_script(js)
    sleep(4)

# 将当前页面拖到最底部
def dragPageEnd_handler(mainhandler, case):
    driver = mainhandler.driver
    js = "var action=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    sleep(1)


# 将页面拖动到最顶部
def dragPageTop_handler(mainhandler, case):
    driver = mainhandler.driver
    js = "var action=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    sleep(1)

def dragToTarEle_handler(mainhandler, case):
    '''
    向上或者向下滚动到目标元素处
    :param mainhandler:
    :param case:
    :return:
    '''
    selector = case.get('selector')
    driver = mainhandler.driver
    ele = get_element(driver, selector)
    try:
        driver.execute_script("arguments[0].scrollIntoView();", ele)
        sleep(1)
        driver.execute_script("window.scrollBy(0, -40)")
    except:
        driver.execute_script("arguments[0].scrollIntoView(false);", ele)
        sleep(1)
        driver.execute_script("window.scrollBy(0, 40)")

def clickInvisibleTarEle_handler(mainhandler, case=None):
    '''
    直接点击不可见的目标元素
    :param mainhandler:
    :param case:
    :return:
    '''
    selector = case.get('selector')
    driver = mainhandler.driver
    ele = get_element(driver, selector)
    driver.execute_script("arguments[0].click();", ele)

def moveToElement_handler(mainhandler, case=None):
    '''
    悬浮鼠标在元素上,使目标元素出现
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    switch_to_cur_win_ifchange(
        driver,
        lambda: ActionChains(driver).move_to_element(
            get_element(mainhandler.driver, case.get("selector"))).perform())
    sleep(1)
    print('鼠标悬浮成功', case.get("desc"), case.get("keywords"), case.get("keyexpression"))

def clearCalendarCards_handler(mainhandler, case=None):
    '''
    清除薪资业务配置-年度日历配置页面的脏数据，只保留：测试-禁用日历、下月年度日历、上月年度日历、本月年度日历
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel = "//div[@class='calender-list']/div"
    eles = driver.find_elements_by_xpath(sel)
    sel3 = "(//ul[starts-with(@id,'dropdown-menu')]/li[2])[last()]"  # 删除按钮
    standList = ['测试-禁用日历', '下月年度日历', '上月年度日历', '本月年度日历','严测试日历3']
    delNameList = []
    for i in range(len(eles)):
        sel1 = f"{sel}{[i+1]}/div/div/div[1]/span"  #日历名称定位
        tex = get_element(driver, sel1).get_attribute('textContent')
        print(tex)
        if tex not in standList:
            delNameList.append(tex)
    print(delNameList)
    if delNameList is None:
        pass
    else:
        for name in delNameList:
            sel2 = f"//span[text()='{name}']/../following-sibling::div/div/span/i"
            driver.find_element_by_xpath(sel2).click()
            sleep(1)
            driver.find_element_by_xpath(sel3).click()
            try:
                driver.find_element_by_xpath("//span[text()='提示']/../../following-sibling::div[2]/button[2]/span").click()
            except:
                pass
            driver.refresh()
            sleep(1.5)

def clearSalaryGroups_handler(mainhandler, case=None):
    '''
    清除薪资业务配置-薪资组配置页面的脏数据，只保留：测试-严测试薪资组、上月薪资组、本月薪资组、下月薪资组
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel = "//div[@class='calender-list clearfix']/div"
    eles = driver.find_elements_by_xpath(sel)
    sel3 = "(//ul[starts-with(@id,'dropdown-menu')]/li[2])[last()]"  # 删除按钮
    standList_1 = ['禁用-严测试薪资组', '上月薪资组', '本月薪资组', '下月薪资组', '测试薪资组','报税薪资组']
    delNameList = []
    for i in range(len(eles)):
        sel1 = f"{sel}{[i+1]}/div[2]/div[2]/div[2]"  #日历名称定位或者薪资组名称定位
        tex = get_element(driver, sel1).get_attribute('textContent')
        print(tex)
        if tex not in standList_1:
            delNameList.append(tex)
    print(delNameList)
    if delNameList is None:
        pass
    else:
        for name in delNameList:
            sel2 = f"//div[text()='{name}']/../../preceding-sibling::div/div/div/span/i"
            driver.find_element_by_xpath(sel2).click()
            sleep(1)
            driver.find_element_by_xpath(sel3).click()
            try:
                driver.find_element_by_xpath("//span[text()='提示']/../../following-sibling::div[2]/button[2]/span").click()
            except:
                pass
            driver.refresh()
            sleep(1.5)

def clearPaidPersonner_handler(mainhandler, case=None):
    '''
    清除薪资业务配置-计薪人员组的脏数据，只保留：['禁用计薪人员', '上月计薪人员', '下月计薪人员', '本月计薪人员']
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel = "//div[@class='pay-salary-group']/div"
    eles = driver.find_elements_by_xpath(sel)
    sel3 = "(//ul[starts-with(@id,'dropdown-menu')]/li[2])[last()]"  # 删除按钮
    standList= ['禁用计薪人员', '上月计薪人员', '下月计薪人员', '本月计薪人员']
    delNameList = []
    for i in range(len(eles)):
        sel1 = f"{sel}{[i+1]}/div[1]/div/span"  #日历名称定位或者薪资组名称定位
        tex = get_element(driver, sel1).get_attribute('textContent')
        print(tex)
        if tex not in standList:
            delNameList.append(tex)
    print(delNameList)
    if delNameList is None or delNameList == []:
        pass
    else:
        for name in delNameList:
            sel2 = f"//span[text()='{name}']/following-sibling::div[1]/div[2]/div/span/i"
            driver.find_element_by_xpath(sel2).click()
            sleep(1)
            driver.find_element_by_xpath(sel3).click()
            try:
                driver.find_element_by_xpath("//span[text()='提示']/../../following-sibling::div[2]/button[2]/span").click()
            except:
                pass
            sleep(1.5)
    driver.refresh()
    sleep(1.5)

def clearRemindEvents_handler(mainhandler, case=None):
    '''
    清除事件提醒中的脏数据，防止对后续测试造成干扰
    :param mainhandler:
    :param case:
    :return:
    '''
    sleep(1.5)
    driver = mainhandler.driver
    sel1 = '//div[text()="事件提醒配置"]/following-sibling::div[1]/div[1]/div'
    sel4 = '//div[text()="事件提醒配置"]/following-sibling::div[1]/div[2]/div'
    for i in range(10):
        sel2 = f'{sel1}[{i+1}]/label'
        sel3 = f'{sel1}[{i+1}]/label/span[2]'
        if get_element(driver, sel2).get_attribute('class') == 'el-checkbox is-checked':
            driver.find_element_by_xpath(sel3).click()
    eles = driver.find_elements_by_xpath(sel4)
    if len(eles) == 1:
        pass
    else:
        for i in range(len(eles)-1):
            sel5 = f'{sel4}[{i+1}]/i'
            driver.find_element_by_xpath(sel5).click()
            driver.find_element_by_xpath("//div[@aria-label='提示']/div/div[3]/button[2]").click()
            sleep(0.5)
    sel6 = '//span[text()="批量配置"]/following-sibling::span'
    if get_element(driver, sel6).get_attribute('class') == 'iconfont iconduihao-01 is-checked':
        driver.find_element_by_xpath(sel6).click()
    sleep(2)

def getCalendarHeader(driver):
    '''
    获取当前的时间以及日历本的头部信息
    :param driver:
    :return:
    '''
    sel1 = "//div[@class='el-row']/div[1]/p"
    sel2 = "//div[@class='el-row']/div[2]/p"
    sel3 = "//div[@class='el-row']/div[3]/p"
    tex1 = get_element(driver, sel1).get_attribute('textContent').split(" ")
    tex2 = get_element(driver, sel2).get_attribute('textContent').split(" ")
    tex3 = get_element(driver, sel3).get_attribute('textContent').split(" ")
    return tex1,tex2,tex3

def getCurrentMonthWorkAndRest(driver):
    '''
    获取当前月份的作息时间并返回
    :param driver:
    :return:
    '''
    blackWorkDay = []
    yellowHoliday = []
    redLegalHoliday = []
    sel1 = "//div[@class='el-row']/div[2]/ul[2]/li[@class='date-view']"
    eles = driver.find_elements_by_xpath(sel1)
    for i in range(len(eles)):
        sel2 = f"{sel1}[{i+1}]/span[1]"
        tex = get_element(driver, sel2).get_attribute('textContent')
        color = get_element(driver, sel2).get_attribute('class').split(" ")
        if color == ['date-day']:
            blackWorkDay.append(tex)
        if len(color) == 2:
            color = color[1].split("-")[1]
            if color == 'yellow':
                yellowHoliday.append(tex)
            if color == "red":
                redLegalHoliday.append(tex)
    return blackWorkDay,yellowHoliday,redLegalHoliday

def changeDayColor(driver, sel1, sel2, colors):
    '''
    改变当前日期月三种日期类型的颜色并做校验
    :param driver:
    :param sel1: 日期定位
    :param sel2: 更改的类型1
    :param colors: 预期的颜色
    :return:
    '''
    # 点击当前日期
    driver.find_element_by_xpath(sel1).click()
    # 点击日期属性勾选圈圈
    driver.find_element_by_xpath(sel2).click()
    #获取当前日期的颜色
    color = get_element(driver, sel1).get_attribute('class').split(" ")
    #校验日期颜色与预期一致
    if len(color) == 2 and color[1].split("-")[1] == colors:
        print("日期属性转换成功")
    else:
        raise Exception("日期属性转换失败")

def calendarPage_handler(mainhandler, case=None):
    '''
    校验年度日历配置-日历卡片-详情（年度日历配置）
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    #获取当前的事件
    currentYear = datetime.datetime.now().year
    currentMonth = datetime.datetime.now().month
    a = currentMonth - 1
    b = currentMonth + 1
    c = currentYear
    d = currentYear
    if currentMonth == 12:
        a = currentMonth - 1
        b = 1
        c = c + 1
    if currentMonth == 1:
        a = 12
        b = currentMonth + 1
        d = d - 1
    #校验日历本默认展示：当前月-1，当前月，当前月+1
    datalist = getCalendarHeader(driver)
    if datalist[0] == [
        f"{d}年",f"{a}月"] and datalist[1] == [
        f"{currentYear}年",f"{currentMonth}月"] and datalist[2] == [
        f"{c}年",f"{b}月"]:
        print("默认展示的日历本正确")
    else:
        raise Exception('默认展示的日历本异常')

    #校验自定义的选择日期
    #点击年份下拉框、选择当前年
    driver.find_element_by_xpath("//div[@class='calen-header el-row']/div/div/div/div/input").click()
    driver.find_element_by_xpath(f"//span[text()='{currentYear}']")
    #点击月份下拉框，选择3月
    driver.find_element_by_xpath("//div[@class='calen-header el-row']/div/div[2]/div/div/input").click()
    sleep(1)
    driver.find_element_by_xpath('(//li/span[text()="3"]/..)[last()]').click()
    sleep(2)
    datalist = getCalendarHeader(driver)
    if datalist[0] == [
        f"{currentYear}年",f"{2}月"] and datalist[1] == [
        f"{currentYear}年",f"{3}月"] and datalist[2] == [
        f"{currentYear}年",f"{4}月"]:
        print("调整后的日历本展示正确")
    else:
        raise Exception('调整后的展示的日历本异常')

    #校验左箭头、右箭头、今天按钮
    sel4 = "//div[@class='calen-header el-row']/div/div[3]/div/button[1]/i"
    sel5 = "//div[@class='calen-header el-row']/div/div[3]/div/button[2]/span/i"
    sel6 = "//div[@class='calen-header el-row']/div/div[3]/button/span"
    driver.find_element_by_xpath(sel4).click()
    sleep(2)
    datalist = getCalendarHeader(driver)
    if datalist[0] == [
        f"{currentYear}年", f"{1}月"] and datalist[1] == [
        f"{currentYear}年", f"{2}月"] and datalist[2] == [
        f"{currentYear}年", f"{3}月"]:
        print("调整后的日历本展示正确")
    else:
        raise Exception('调整后的展示的日历本异常')

    driver.find_element_by_xpath(sel5).click()
    sleep(2)
    datalist = getCalendarHeader(driver)
    if datalist[0] == [
        f"{currentYear}年", f"{2}月"] and datalist[1] == [
        f"{currentYear}年", f"{3}月"] and datalist[2] == [
        f"{currentYear}年", f"{4}月"]:
        print("调整后的日历本展示正确")
    else:
        raise Exception('调整后的展示的日历本异常')

    driver.find_element_by_xpath(sel6).click()
    sleep(2)
    datalist = getCalendarHeader(driver)
    if datalist[0] == [
        f"{d}年", f"{a}月"] and datalist[1] == [
        f"{currentYear}年", f"{currentMonth}月"] and datalist[2] == [
        f"{c}年", f"{b}月"]:
        print("点击”今天“展示的日历本正常")
    else:
        raise Exception('点击”今天“展示的日历本异常')

def calendarDayColor_handler(mainhandler, case=None):
    '''
    校验当前月工作日、假日、节日的颜色
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    # 工作日、假日、节日勾选
    sel4 = '//div[@class="el-radio-group"]/label[1]/span[1]'
    sel5 = '//div[@class="el-radio-group"]/label[2]/span[1]'
    sel6 = '//div[@class="el-radio-group"]/label[3]/span[1]'
    ####校验三种类型的日期转换导致的字体颜色变化
    data = getCurrentMonthWorkAndRest(driver)
    anyBlackDay = data[0][0]
    print("选择的工作日是：",anyBlackDay)
    anyYllowDay = data[1][0]
    print("选择的假日是：", anyYllowDay)

    # 任意的工作日具体日期
    sel3 = f"//div[@class='el-row']/div[2]/ul[2]/li[@class='date-view']/span[1][text()='{anyBlackDay}']"
    # 任意的假日具体日期
    sel7 = f"//div[@class='el-row']/div[2]/ul[2]/li[@class='date-view']/span[1][text()='{anyYllowDay}']"
    ###选择任意的一个工作日将其改变为假日、节日
    changeDayColor(driver, sel3, sel5, 'yellow')
    sleep(2)
    changeDayColor(driver, sel3, sel6, 'red')
    sleep(2)

    ###选择任意的一个假日，将其改变为工作日、节日
    changeDayColor(driver, sel7, sel4, 'green')
    sleep(2)
    changeDayColor(driver, sel7, sel6, 'red')
    sleep(2)

    ###选择任意的一个节日，将其改变为工作日、假日
    if data[2] == [] or data[2] == "" or data[2] is None:
        pass
    else:
        # 任意的节日具体日期
        anyRedDay = data[2][0]
        sel8 = f"//div[@class='el-row']/div[2]/ul[2]/li[@class='date-view']/span[1][text()='{anyRedDay}']"
        print("选择的节日是：", anyRedDay)
        changeDayColor(driver, sel8, sel4, 'green')
        sleep(2)
        changeDayColor(driver, sel8, sel5, 'yellow')
        sleep(2)

def gethhhhh_handler(mainhandler, case):
    '''
    为了调试的时候获取某些元素的值
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    selector = case.get('selector')
    tex = get_element(driver, selector).get_attribute('textContent')
    print('tex:',tex)

def initSalaryGroupCard_handler(mainhandler, case):
    '''
    操作薪资组卡片开关锁，初始化薪资计算
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    value = case.get('value')
    sel1 = '//span[text()="本月薪资组"]/following-sibling::div/span[@class="list-dom-lock is-disabled"]/i'
    sel2 = '//span[text()="本月薪资组"]/following-sibling::div/span[@class="list-dom-lock is-lock"]/i'
    ele = get_element(driver,sel1)
    if ele:
        driver.find_element_by_xpath(sel1).click()
        sleep(2)
        ele1 = get_element(driver,sel2)
        if ele1:
            driver.find_element_by_xpath(sel2).click()
        else:
            driver.find_element_by_xpath(sel1).click()
            sleep(2)
            driver.find_element_by_xpath(sel2).click()
    else:
        driver.find_element_by_xpath(sel2).click()
    sleep(1)

def clearCalculateData_handler(mainhandler, case):
    '''
    清除计算流程中的脏数据，将计算状态会退至待计算
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/span[text()="薪资计算"]').click()
    sleep(2)
    sel1 = "//span[text()='计算薪资组']/../following-sibling::div/span"
    tex= get_element(driver, sel1).get_attribute('textContent')
    if tex == '待计算':
        pass
    if tex == '待审批':
        driver.find_element_by_xpath("//span[text()='计算薪资组']/../following-sibling::div/div/div/span/i").click()
        sleep(0.5)
        driver.find_element_by_xpath("(//ul/li[text()='状态退回'])[last()]").click()
        sleep(1)
        driver.find_element_by_xpath('//div[@aria-label="状态退回"]/div[3]/span/button[2]').click()
    if tex == '审批中':
        driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/a/span[text()="首页"]').click()
        sleep(1.5)
        driver.find_element_by_xpath('(//span[@class="pan-task-span"])[1]').click()
        sleep(1.5)
        sel1 = "(//tbody/tr[1]/td[3]/div/span[text()='计算薪资组']/../../..)[last()]/td[10]/div/div/button[1]/span[text()='审批']"
        sel2 = "(//tbody/tr[1]/td[3]/div/span[text()='计算薪资组']/../../..)[last()]/td[10]/div/div/button[2]/span[text()='撤回']"
        driver.find_element_by_xpath(sel2).click()
        sleep(1)
        driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
        sleep(1)
        driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/span[text()="薪资计算"]').click()
        sleep(1)
        driver.find_element_by_xpath("//span[text()='计算薪资组']/../following-sibling::div/div/div/span/i").click()
        driver.find_element_by_xpath("(//ul/li[text()='状态退回'])[last()]").click()
        driver.find_element_by_xpath('//div[@aria-label="状态退回"]/div[3]/span/button[2]').click()

def clearTestSalaryGroup_handler(mainhandler, case=None):
    '''
    清除薪资业务配置-薪资组配置页面测试薪资组
    :param mainhandler:
    :param case:
    :return:
    '''

    driver = mainhandler.driver
    driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/span[text()="薪资计算"]').click()
    sleep(2)
    sel1 = "//span[text()='测试薪资组 ']/../following-sibling::div/span"
    try:
        tex = get_element(driver, sel1).get_attribute('textContent')
        if tex in ['初始化', '待计算', '已关账']:
            salaryLock(driver)
        if tex == '待审批':
            driver.find_element_by_xpath("//span[text()='测试薪资组 ']/../following-sibling::div/div/div/span/i").click()
            sleep(0.5)
            driver.find_element_by_xpath("(//ul/li[text()='状态退回'])[last()]").click()
            sleep(1)
            driver.find_element_by_xpath('//div[@aria-label="状态退回"]/div[3]/span/button[2]').click()
            sleep(1)
            salaryLock(driver)
        if tex == '审批中':
            driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/a/span[text()="首页"]').click()
            sleep(1.5)
            driver.find_element_by_xpath("//div[text()='待办任务']/following-sibling::div[1]/ul/li[2]/div[1]").click()
            driver.find_element_by_xpath("//ul/li[1]/div/span[text()='薪资审批']").click()
            sleep(3)
            # sel2 = "(//tbody/tr[1]/td[3]/div/span[text()='测试薪资组']/../../..)[last()]/td[10]/div/div/button[2]/span[text()='撤回']"
            sel2 = "(//tbody/tr[1]/td[3]/div/span[text()='测试薪资组']/../../..)[1]/td[10]/div/div/button[2]/span[text()='撤回']"
            # sel2 = "(//tbody/tr[1])[last()]/td/div/div/button[2]/span"
            driver.find_element_by_xpath(sel2).click()
            sleep(1)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(6)
            driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/span[text()="薪资计算"]').click()
            sleep(1)
            driver.find_element_by_xpath("//span[text()='测试薪资组 ']/../following-sibling::div/div/div/span/i").click()
            sleep(1)
            driver.find_element_by_xpath("(//ul/li[text()='状态退回'])[last()]").click()
            print("haha")
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="状态退回"]/div[3]/span/button[2]').click()
            print("hehe")
            sleep(1)
            salaryLock(driver)
        if tex == '待关账':
            # driver.find_element_by_xpath("//span[contains(@class,'salary-span-name') and text()='测试薪资组 ']").click()
            sleep(1)
            driver.find_element_by_xpath("//span[text()='测试薪资组']/../../following-sibling::div[4]/button/span").click()
            sleep(0.5)
            salaryLock(driver)
    except:
        pass

def salaryLock(driver):
    driver.find_element_by_xpath('//div[@class="menu-scrollbar-item"]/div/span[text()="薪资业务配置"]').click()
    sleep(2)
    driver.find_element_by_xpath('//div[@class="menu-left-sidebar-block"]/a/span[text()="薪资组配置"]').click()
    sleep(4)
    # driver.find_element_by_xpath("//div[text()='测试薪资组']/../preceding-sibling::div/div[2]/span/i").click()
    # sleep(1)
    # driver.find_element_by_xpath("//div[text()='测试薪资组']/../preceding-sibling::div/div[2]/span/i").click()
    # sleep(1)
    # driver.find_element_by_xpath("//div[text()='测试薪资组']/../preceding-sibling::div/div[2]/div/span/i").click()
    driver.find_element_by_xpath("//div[text()='测试薪资组']/../../preceding-sibling::div/div/span/i").click()
    sleep(5)
    driver.find_element_by_xpath("//div[text()='测试薪资组']/../../preceding-sibling::div/div/span/i").click()
    sleep(5)
    driver.find_element_by_xpath("//div[text()='测试薪资组']/../../preceding-sibling::div/div/div/span/i").click()
    sleep(1)
    driver.find_element_by_xpath("(//ul[starts-with(@id,'dropdown-menu')]/li[2])[last()]").click()
    sleep(1)
    driver.find_element_by_xpath("//span[text()='提示']/../../following-sibling::div[2]/button[2]/span").click()
    sleep(1)

def waitEle_handler(mainhandler, case):
    '''
    等待某个元素出现，如做出一些操作后要过一会才能出现的元素
    eg:点击计算，要过一会才会出现计算完成的按钮
    :param mainhandler:
    :param case:
    :return:
    '''
    selector = case.get("selector")
    val = str(case.get("val"))
    is_hidden = None
    is_need_refresh = None
    if val != "":
        val = eval(val)
        is_hidden = val.get("hidden")
        is_need_refresh = val.get("refresh")
    driver = mainhandler.driver
    wait_for_ele(driver, selector, is_need_refresh, is_hidden)

def wait_for_ele(driver, selector, is_need_refresh=None, is_hidden=None):
    '''
    等待元素出现或者消失  val="hidden"时是等待元素消失
    print("等待 {} 元素{}".format(selector, "消失" if is_hidden else "出现"))
    :param driver:
    :param selector:
    :param is_need_refresh:
    :param is_hidden:
    :return:
    '''
    wait = WebDriverWait(driver, 150, 3)
    if is_hidden:
        wait.until(
            EC.invisibility_of_element(get_element(driver, selector, True)))
    else:
        global wait_to_get_selector_opt
        wait_to_get_selector_opt["is_need_refresh"] = is_need_refresh
        wait_to_get_selector_opt["selector"] = selector
        wait.until(do_get_ele)

def do_get_ele(driver):
    '''
    刷新并且获取元素
    :param driver:
    :return:
    '''
    driver.implicitly_wait(0)
    if wait_to_get_selector_opt.get("is_need_refresh"):
        driver.refresh()
        sleep(2)
    ele = get_element(driver, wait_to_get_selector_opt.get("selector"), True)
    if ele:
        driver.implicitly_wait(10)
    return ele

def check_loading(driver):
    '''
    检查有没有loading层覆盖，有的话等待loading消失
    eg：点击保存后出现的等待小圈圈，转啊转,等它消失了再执行下一步
    :param driver:
    :return:
    '''
    try:
        wait = WebDriverWait(driver, 30, 0.5)
        loading_ele = driver.execute_script(
            "return document.querySelector('#icon-loading')")
        loading_ele1 = driver.execute_script(
            "return document.querySelector('#iconLoading')")
        if loading_ele is not None:
            wait.until(EC.invisibility_of_element(loading_ele))
        if loading_ele1 is not None:
            wait.until(EC.invisibility_of_element(loading_ele1))
        sleep(1)
    except:
        traceback_info = traceback.format_exc()
        print(traceback_info)

def clearSocialSecurityRulesData_handler(mainhandler, case):
    '''
    删除社保规则配置中的多条数据（平台）
    删除公积金规则配置中的多条数据（平台）
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    val = case.get('val')
    sel1 = f'//div[@class="el-table__fixed"]/div[2]/table/tbody/tr/td[2]/div/span[contains(text(),"{val}")]/../../preceding-sibling::td/div/div/span'
    sel2 = f'//div[@class="el-table__fixed"]/div[2]/table/tbody/tr/td[2]/div/span[contains(text(),"{val}")]/../../preceding-sibling::td/div/div/div/label/span/span'
    sel5 = '//*[@id="excel-upload-input"]/../button[2]'
    sel6 = '//div[@aria-label="提示"]/div/div[3]/button[2]'
    print('sel1', sel1)
    print('sel2', sel2)
    eles = driver.find_elements_by_xpath(sel1)
    if eles == []:
        pass
    else:
        for i in range(len(eles)):
            sel3 = f'({sel1})[{i+1}]'
            sel4 = f'({sel2})[{i+1}]'
            print(sel4)
            ActionChains(driver).move_to_element(
                get_element(driver, sel3)).perform()
            driver.find_element_by_xpath(sel4).click()

        driver.find_element_by_xpath(sel5).click()
        driver.find_element_by_xpath(sel6).click()
        sleep(2)

def clearInServiceConfig_handler(mainhandler, case):
    '''
    删除在职服务配置中的多条数据（平台）
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    val = case.get('val')
    sel1 = f'//div[@class="el-table__fixed"]/div[2]/table/tbody/tr/td[2]/div/div[contains(text(),"{val}")]/../../preceding-sibling::td/div/div/span'
    sel2 = f'//div[@class="el-table__fixed"]/div[2]/table/tbody/tr/td[2]/div/div[contains(text(),"{val}")]/../../preceding-sibling::td/div/div/div/label/span/span'
    sel5 = '//*[@id="excel-upload-input"]/../button[2]'
    sel6 = '//div[@aria-label="提示"]/div/div[3]/button[2]'
    print('sel1', sel1)
    print('sel2', sel2)
    eles = driver.find_elements_by_xpath(sel1)
    if eles == []:
        pass
    else:
        for i in range(len(eles)):
            sel3 = f'({sel1})[{i+1}]'
            sel4 = f'({sel2})[{i+1}]'
            print(sel4)
            ActionChains(driver).move_to_element(
                get_element(driver, sel3)).perform()
            driver.find_element_by_xpath(sel4).click()

        driver.find_element_by_xpath(sel5).click()
        driver.find_element_by_xpath(sel6).click()
        sleep(2)

def getStaffNameTonameDick_handler(mainhandler, case):
    '''
    测试申报流程的时候获取申报的数据的名称存储到一个全局变量字典中，后面的步骤需要用
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    selector = case.get('selector')
    tex = get_element(driver, selector).get_attribute('textContent')
    print('tex:', tex)
    nameDick['name1'] = tex
    print(nameDick)

def clearUserManageDirtyData_handler(mainhandler, case):
    '''
    清除公共系统配置-用户管理的测试脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = "(//span[text()='trdp-new'])[2]/../../../td[1]/div/div/label/span/span"
    sel2 = "(//span[text()='trdp-test'])[2]/../../../td[1]/div/div/label/span/span"
    ele1 = driver.find_elements_by_xpath(sel1)
    ele2 = driver.find_elements_by_xpath(sel2)
    if ele1 == [] and ele2 == []:
        pass
    else:
        if ele1 == [] and ele2 != []:
            driver.find_element_by_xpath(sel2).click()
        if ele1 != [] and ele2 == []:
            driver.find_element_by_xpath(sel1).click()
            sleep(1)
        driver.find_element_by_xpath("//span[text()='删除']").click()
        sleep(0.5)
        driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
        sleep(1)

def clearCustomerManageDirtyData_handler(mainhandler, case):
    '''
    清除公共系统配置-客户管理的测试脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = "(//span[text()='魔都超级NB有限公司'])[2]/../../../td[1]/div/div/label/span/span"
    ele1 = driver.find_elements_by_xpath(sel1)
    if ele1 == []:
        pass
    else:
        tex = driver.find_element_by_xpath(
            "(//span[text()='魔都超级NB有限公司']/../../../td[6]/div/span)[1]").get_attribute('textContent')
        if tex == '0':
            driver.find_element_by_xpath(sel1).click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
        else:
            # driver.find_element_by_xpath(
            #     "(//span[text()='魔都超级NB有限公司']/../../../td[8]/div/div/button/span[text()='详情'])[last()]").click()
            driver.find_element_by_xpath(
                "(//span[text()='魔都超级NB有限公司']/../../../td[2])[1]").click()
            sleep(1)
            driver.find_element_by_xpath("//div/span[text()='法人实体']").click()
            sleep(0.5)
            # driver.find_element_by_xpath('(//div[@class="cell"]/div/button/span/i)[last()]').click()
            driver.find_element_by_xpath('(//div[@class="cell"]/div/button/span/i)[1]').click()
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
            driver.find_element_by_xpath('//div[@class="menu-left-sidebar-block"]/a/span[text()="客户管理"]').click()
            sleep(1)
            driver.find_element_by_xpath(sel1).click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)

def clearServiceFeeConfigDirtyData_handler(mainhandler, case):
    '''
    清除公共系统配置-服务费配置的测试脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = "(//span[text()='auto001'])[2]/../../../td[1]/div/div/label/span/span"
    ele1 = driver.find_elements_by_xpath(sel1)
    if ele1 == []:
        pass
    else:
        tex = driver.find_element_by_xpath(
            "(//span[text()='auto001']/../../../td[6]/div/span)[1]").get_attribute('textContent')
        if tex == '0':
            driver.find_element_by_xpath(sel1).click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
        else:
            # driver.find_element_by_xpath(
            #     "(//span[text()='auto薪资发放']/../../../td[9]/div/div/button/span[text()='详情'])[last()]").click()
            driver.find_element_by_xpath(
                "(//span[text()='auto薪资发放']/../../../td[2]'])[1]").click()
            sleep(1)
            driver.find_element_by_xpath("//div[text()='关联客户']").click()
            sleep(0.5)
            driver.find_element_by_xpath("(//span[text()='2021060101'])[2]/../../../td[1]/div/div/label/span/span").click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
            driver.find_element_by_xpath("//div[@class='menu-left-sidebar-block']/a/span[text()='服务费配置']").click()
            sleep(1)
            driver.find_element_by_xpath(sel1).click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)

def clearUserConfigDirtyData_handler(mainhandler, case):
    '''
    清除公共业务配置-用户配置的测试脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = "(//span[text()='test-account'])[2]/../../../td[1]/div/div/label/span/span"
    # sel1 = "(//tbody/tr[1])[2]//span/span"
    ele1 = driver.find_elements_by_xpath(sel1)
    if ele1 == []:
        pass
    else:
        driver.find_element_by_xpath(sel1).click()
        driver.find_element_by_xpath("//span[text()='删除']").click()
        sleep(0.5)
        driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
        sleep(1)

def clearOriganManageConfigDirtyData_handler(mainhandler, case):
    '''
    清除人事业务配置-组织管理配置中的脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = "(//span[contains(text(),'测试父组织')])[1]"
    sel2 = "(//span[contains(text(),'测试子组织')])[1]"
    sel3 = "(//span[contains(text(),'测试孙组织')])[1]"
    ele1 = driver.find_elements_by_xpath(sel1)
    print(ele1)
    if ele1 == []:
        pass
    else:
        ele1[0].click()
        driver.find_element_by_xpath("//button/span[contains(text(),'编辑')]/../following-sibling::div/span").click()
        sleep(1)
        driver.find_element_by_xpath("//ul/li[text()='失效']").click()
        driver.find_element_by_xpath("(//button/span[contains(text(),'确定')])[last()]").click()
    sleep(2)
    ele2 = driver.find_elements_by_xpath(sel2)
    if ele2 == []:
        pass
    else:
        ele2[0].click()
        ele3 = driver.find_elements_by_xpath(sel3)
        if ele3 == []:
            pass
        else:
            ele3[0].click()
            driver.find_element_by_xpath("//button/span[contains(text(),'编辑')]/../following-sibling::div/span").click()
            sleep(1)
            driver.find_element_by_xpath("//ul/li[text()='失效']").click()
            driver.find_element_by_xpath("(//button/span[contains(text(),'确定')])[last()]").click()
            sleep(2)
        driver.find_element_by_xpath(sel2).click()
        driver.find_element_by_xpath("//button/span[contains(text(),'编辑')]/../following-sibling::div/span").click()
        sleep(1)
        driver.find_element_by_xpath("//ul/li[text()='失效']").click()
        driver.find_element_by_xpath("(//button/span[contains(text(),'确定')])[last()]").click()
    sleep(1)

def clearRankManageConfigDirtyData_handler(mainhandler, case):
    '''
    清除人事业务配置-职级管理配置的脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = "//ul/li/p[text()='测试线']"
    sel2 = "(//tr/td[2]/div/span[text()='cs001'])[1]"
    sel3 = "(//tr/td[2]/div/span[text()='cs002'])[1]"
    ele1 = driver.find_elements_by_xpath(sel1)
    if ele1 == []:
        pass
    else:
        ele1[0].click()
        ele2 = driver.find_elements_by_xpath(sel2)
        ele3 = driver.find_elements_by_xpath(sel3)
        if ele2 == [] and ele3 == []:
            driver.find_element_by_xpath("//p[text()='测试线']/../div/i[2]").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
        else:
            driver.find_element_by_xpath("(//tr/th[1]/div/div/label/span/span)[2]").click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
            driver.find_element_by_xpath("//p[text()='测试线']/../div/i[2]").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
            sleep(1)
    sleep(1)

def clearPositionManageConfigDirtyData_handler(mainhandler, case):
    '''
    清除人事业务配置-职位管理配置的脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = ["(//span[text()='测试经理'])[2]/../../../../preceding-sibling::td/div/div/label/span/span",
            "(//span[text()='测试经理'])[2]/../../../../../preceding-sibling::td/div/div/label/span/span"]
    sel2 = ["(//span[text()='专家级测试工程师'])[2]/../../../../preceding-sibling::td/div/div/label/span/span",
            "(//span[text()='专家级测试工程师'])[2]/../../../../../preceding-sibling::td/div/div/label/span/span"]
    for sel in sel1:
        ele1 = driver.find_elements_by_xpath(sel)
        if ele1 == []:
            pass
        else:
            ele1[0].click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
    sleep(1)
    for sel_1 in sel2:
        ele2 = driver.find_elements_by_xpath(sel_1)
        if ele2 == []:
            pass
        else:
            ele2[0].click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
    sleep(1)

def clearJobsManageConfigDirtyData_handler(mainhandler, case):
    '''
    清除人事业务配置-岗位管理配置的脏数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    sel1 = ["(//span[text()='事业部总监'])[2]/../../../../preceding-sibling::td/div/div/label/span/span",
            "(//span[text()='事业部总监'])[2]/../../../../../preceding-sibling::td/div/div/label/span/span"]
    for sel in sel1:
        ele1 = driver.find_elements_by_xpath(sel)
        if ele1 == []:
            pass
        else:
            ele1[0].click()
            driver.find_element_by_xpath("//span[text()='删除']").click()
            sleep(0.5)
            driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
    sleep(1)

def check_loading_is_hide(driver):
    '''
    检查有没有loading层覆盖，如果有就等待loading消失
    :param driver:
    :return:
    '''
    try:
        wait = WebDriverWait(driver, 240, 0.5)
        loading_ele1 = driver.execute_script(
            "return document.querySelector('.el-loading-mask.is-fullscreen')")
        loading_ele2 = driver.execute_script(
            "return document.querySelector('.el-loading-spinner')")
        loading_ele3 = driver.execute_script(
            "return document.querySelector('.load-contaior')")
        loading_ele4 = driver.execute_script(
            "return document.querySelector('.el-loading-mask.is-fullscreen.el-loading-fade-leave-active.el-loading-fade-leave-to')")
        loading_ele5 = driver.execute_script(
            "return document.querySelector('.el-loading-mask.is-fullscreen.el-loading-fade-leave-active.el-loading-fade-enter-to')")
        print('loading返回状态：',loading_ele1,loading_ele2,loading_ele3,loading_ele4,loading_ele5)
        if loading_ele1 is None and loading_ele2 is None and loading_ele3 is None and loading_ele4 is None and loading_ele5 is None:
            pass
        else:
            if loading_ele1 is not None:
                print('有浮层1，稍等！！！')
                wait.until(EC.invisibility_of_element_located(loading_ele1))
                print("lading1...............................................")
            if loading_ele2 is not None:
                print('有浮层2，稍等！！！')
                wait.until(EC.invisibility_of_element_located(loading_ele2))
                print("lading2...............................................")
                # sleep(1)
            if loading_ele3 is not None:
                print('有加载页3，稍等！！！')
                wait.until(EC.invisibility_of_element_located(loading_ele3))
                print("lading3...............................................")
            if loading_ele4 is not None:
                print('有浮层4，稍等！！！')
                wait.until(EC.invisibility_of_element_located(loading_ele4))
                print("lading4...............................................")
            if loading_ele5 is not None:
                print('有浮层5，稍等！！！')
                wait.until(EC.invisibility_of_element_located(loading_ele5))
                print("lading5...............................................")
            sleep(0.5)
    except:
        traceback_info = traceback.format_exc()
        print(traceback_info)

def deleteStaffData_handler(mainhandler, case):
    '''
    删除员工数据维护列表中的数据
    :param mainhandler:
    :param case:
    :return:
    '''
    driver = mainhandler.driver
    val = case.get('val')
    driver.find_element_by_css_selector(
        'div.saech-div:nth-child(1)>div>div>div>input').send_keys(val)
    driver.find_element_by_css_selector('div.saech-btn>button:nth-child(2)').click()
    sleep(1)
    if driver.find_elements_by_xpath(f"(//tr/td[2]//p[1]/span[text()='{val}'])[1]") == []:
        pass
    else:
        ActionChains(driver).move_to_element(
            driver.find_element_by_xpath(f"(//span[text()='{val}']/../../../../../preceding-sibling::td//div/span)[last()]")).perform()
        driver.find_element_by_xpath(f"(//span[text()='{val}']/../../../../../preceding-sibling::td)[last()]//label/span/span").click()
        driver.find_element_by_xpath('//*[@id="excel-upload-input"]/../div[3]/span').click()
        sleep(1)
        driver.find_element_by_xpath("(//ul/li[text()=' 勾选删除 '])[last()]").click()
        sleep(0.5)
        driver.find_element_by_xpath('//div[@aria-label="提示"]/div/div[3]/button[2]').click()
    driver.refresh()
    sleep(2)

def deleteStaffData1_handler(mainhandler, case):
    '''
    通过接口删除员工管理-数据维护的数据
    :param mainhandler:
    :param case:
    :return:
    '''
    s = createSession('trdp-yzp1', 'yzp123456', '2021060101')
    url = r'https://qa.tranderpay.com/api/v1/employee/delBylist'
    if platform.system() == 'Windows':
        db = pymysql.Connect(
            host='139.196.136.162', port=3306, user='root',
            passwd='Root@123456', db='cn2021060101', charset='utf8')
    else:
        db = pymysql.Connect(
            host='172.19.116.28', port=3306, user='root',
            passwd='Root@123456', db='cn2021060101', charset='utf8')
    # 创建一个游标对象，执行数据操作
    cursor = db.cursor()
    for name in ['卓奇','姜竹萍']:
        sql = f"SELECT `eid` FROM `employee_master_data` WHERE `ee_name`='{name}' ORDER BY updated DESC LIMIT 1"
        cursor.execute(sql)
        data = cursor.fetchone()
        json = [{"eid":data[0]}]
        try:
            res = s.request(method='post',url=url,json=json,verify=False,timeout=20)
        except:
            pass
    db.close()