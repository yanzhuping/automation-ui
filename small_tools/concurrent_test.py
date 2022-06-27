import requests, time, json, threading, random
from time import ctime
import logging
import re

class Presstest(object):

    def __init__(self, press_url, account="yanry4548", password="333333"):
        self.press_url = press_url
        self.account = account
        self.password = password
        self.session = requests.session()
        self.header= {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

    def login(self):
        logging.captureWarnings(True)
        base_url = 'https://opm-cas.sh-sit.eainc.com:8443/cas/login?service=https://opm-cas.sh-sit.eainc.com:8443/OPM/shiro-cas'
        r = self.session.get(base_url, headers=self.header, verify=False)

        strr = r.text
        pat1 = r'= {execution: "(.*?)", _eventId:'
        execution = re.findall(pat1, strr)
        par1 = {'username': self.account, 'password': self.password, 'execution': '%s' % execution[0], '_eventId': 'submit',
                'oginType': '0'}
        r1 = self.session.post(base_url, headers=self.header, data=par1, allow_redirects=False, verify=False)

        location = r1.headers['Location']
        r2 = self.session.get(location, headers=self.header, allow_redirects=False, verify=False)

        r3 = self.session.get(location, headers=self.header, allow_redirects=False, verify=False)

        url = "https://opm-cas.sh-sit.eainc.com:8443/OPM/login/validatelogin"
        data = {}
        re4 = self.session.post(url, headers=self.header, data=data, verify=False)
        
    def testinterface(self):
        '''压测接口'''
        data = {"accountType": 3,"crmOrgCode": "H201012070002",
                             "accountName": "接口测试普通助理%s"%ctime()}
        global ERROR_NUM  #出错数
        try:
            html = self.session.post(self.press_url, data=data,headers=self.header,verify=False)
            print(html.text)
            if html.json().get('msg') != '成功':
                print(html.json())
                ERROR_NUM += 1
        except Exception as e:
            print(e)
            ERROR_NUM += 1

    def testonework(self):
        '''一次并发处理单个任务'''
        i = 0
        while i < ONE_WORKER_NUM:  #每个线程的循环次数
            i += 1
            self.testinterface()
        time.sleep(LOOP_SLEEP)  #每次请求的时间间隔

    def run(self):
        '''使用多线程进程并发测试'''
        t1 = time.time()
        Threads = []

        for i in range(THREAD_NUM): #线程数
            print("开始线程:",i,ctime())
            t = threading.Thread(target=self.testonework, name="T" + str(i))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()
        t2 = time.time()

        print("===============压测结果===================")
        print("URL:", self.press_url)
        print("任务数量:", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM * ONE_WORKER_NUM)
        print("总耗时(秒):", t2 - t1)
        print("每次请求耗时(秒):", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("每秒承载请求数:", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("错误数量:", ERROR_NUM)


if __name__ == '__main__':
    press_url = 'https://opm-cas.sh-sit.eainc.com:8443/OPM/assistant/addAssistant'
    account = "yanry4548"
    password = "333333"

    THREAD_NUM = 10  # 并发线程总数
    ONE_WORKER_NUM = 5  # 每个线程的循环次数
    LOOP_SLEEP = 1 # 每次请求时间间隔(秒)
    ERROR_NUM = 0  # 出错数

    obj = Presstest(press_url=press_url, account=account, password=password)
    obj.login()
    obj.run()