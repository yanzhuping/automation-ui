from locust import HttpUser, task
import os
import queue
from performanceTest.loader import load_csv_file



#如果是全局参数，放在任务类之外
def dataxxx():
    pass

# 全局参数化，适合类似于注册业务
# q = queue.Queue()
# csv_list = load_csv_file('./data/user.csv')
# for item in csv_list:
#     q.put(item)

# 创建任务类
class MyTask(HttpUser):
    host = 'https://baike.baidu.com'
    weight = 2  #设置类与类之前的权重
    wait_time = 100  #等待时间，ms
    # wait_time = constant_throughput(1)   #固定吞吐量，一个用户达到的最高吞吐量，在混合场景使用

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.q = queue.Queue()

    def on_start(self):
        csv_list = load_csv_file('./data/user.csv')
        for item in csv_list:
            self.q.put(item)

    @task(2)#设置类内部的权重
    def login(self):
        item =self.q.get()
        data = {'email':item.get('email'), 'password':item.get('password')}
        with self.client.post(url='', data=data, catch_response=True) as response:
            if response.status_code != 200:
                response.failure("失败了！！！")
            else:
                response.success()
        self.q.put(item)  #将取出的数据重新放回队列中,如果不加这一步，当队列中的数据取完，测试就会停止

    @task(1)
    def do_execute(self):
        headers = {}
        params = {}
        with self.client.get("/item/Python/407313?fr=aladdin", catch_response=True, name='python介绍',
                             headers=headers, params=params) as response:
            if response.status_code != 200:
                response.failure("失败了！！！")
            else:
                response.success()

class MyTask1(HttpUser):
    host = 'https://baike.baidu.com'
    weight = 1 #shezhi
    # wait_time = 1

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.q = queue.Queue()

    def on_start(self):
        csv_list = load_csv_file('./data/user.csv')
        for item in csv_list:
            self.q.put(item)

    @task(2)#设置类内部的权重
    def login(self):
        item =self.q.get()
        data = {'email':item.get('email'), 'password':item.get('password')}
        with self.client.post(url='', data=data, catch_response=True) as response:
            if response.status_code != 200:
                response.failure("失败了！！！")
            else:
                response.success()
        self.q.put(item)  #将取出的数据重新放回队列中,如果不加这一步，当队列中的数据取完，测试就会停止


if __name__ == '__main__':
    os.system("locust -f locustfile.py --web-host=127.0.0.1")
