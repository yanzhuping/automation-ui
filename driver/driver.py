from selenium import webdriver
from libs.test_utils import get_root_path
import os

def browser(view='No'):
    '''
    定义一个浏览器，设置浏览器的启动属性
    :return:
    '''
    #配置chrome启动时的属性
    chrome_options = webdriver.ChromeOptions()
    # 无头模式
    if view == "No" or view == '' or view == None:
        chrome_options.add_argument('--headless')

    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    #部分网址打开提示有安全问题
    chrome_options.add_argument('--ignore-certificate-errors')
    # 无头模式打印日志级别 INFO = 0,WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3 default is 0
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--no-sandbox')
    #大量渲染时写入/tmp(到磁盘)不写入/dev/shm(文件系统级共享内存)中
    chrome_options.add_argument('--disable-dev-shm-usage')
    #限制网速
    # driver.set_network_conditions(offline=False, latency=5, throughput=4000)
    # Selenium中禁用Chrome实验性选项same-site-by-default-cookies和cookies-without-same-site-must-be-secure
    # 实现登陆后的自动跳转
    experimentalFlags = [
        "same-site-by-default-cookies@2",
        "cookies-without-same-site-must-be-secure@2",
    ]
    chromeLocalStatePrefs = {
        "browser.enabled_labs_experiments": experimentalFlags
    }
    chrome_options.add_experimental_option("localState", chromeLocalStatePrefs)
    #设定下载文件的目录
    prefs = {"download.default_directory":os.path.join(get_root_path(), "test_data", "downLoadDoc")}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(2)
    driver.maximize_window()

    return driver