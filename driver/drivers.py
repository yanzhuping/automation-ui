from selenium import webdriver
from msedge.selenium_tools import Edge,EdgeOptions
import threading
from time import sleep
from libs.test_utils import get_root_path
import os

def setBrowser(br):
    '''
    定义一个浏览器，设置浏览器的启动属性
    :name:浏览器名称
    :return:
    '''
    try:
        if br == 'chrome':
            print('start browser name is chrome')
            option = setAttribute(br)
            driver = webdriver.Chrome(chrome_options=option)
            driver.get('https://www.baidu.com')
            sleep(10)
            return driver
        elif br == 'firefox':
            print('start browser name is firefox')
            option = setAttribute(br)
            driver = webdriver.Firefox(firefox_options=option)
            driver.get('https://www.baidu.com')
            sleep(10)
            return driver
        elif br == 'edge':
            print('start browser name is edge')
            option = setAttribute(br)
            driver = Edge(options=option)
            return driver
    except:
        print('没有发现参数中的浏览器(chrome,firefox,edge)，请检查设备')

def setAttribute(br):
    '''
    设置浏览器的相关属性、功能
    :return:
    '''
    option = ''
    if br == 'chrome':
        option = webdriver.ChromeOptions()
    elif br == 'firefox':
        option = webdriver.FirefoxOptions()
    elif br == 'edge':
        option = EdgeOptions()
        option.use_chromium = True
    option.add_argument('--window-size=1920,1080')
    # option.add_argument('--headless')
    return option

def browser(name):
    for br in name:
        print(br)
        threads = []
        t1 = threading.Thread(target=setBrowser, args=(br,))
        threads.append(t1)
        for t2 in threads:
            t2.start()
            t2.join()#注释掉，则会同时运行

if __name__ == '__main__':
    name = ['chrome','firefox']
    browser(name)