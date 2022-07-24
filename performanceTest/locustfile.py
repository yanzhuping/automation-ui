from locust import HttpUser, task,TaskSet,LoadTestShape
import os
import queue
from performanceTest.loader import load_csv_file


###并发设置
from locust import events
from gevent._semaphore import Semaphore
all_locusts_spawned = Semaphore(0)
all_locusts_spawned.acquire()


#如果是全局参数，放在任务类之外
def dataxxx():
    pass

# 全局参数化，适合类似于注册业务
# q = queue.Queue()
# csv_list = load_csv_file('./data/user.csv')
# for item in csv_list:
#     q.put(item)


########################如果要进行并发测试，则需要增加集合点##############
# def on_hatch_complete(**kwargs):
#     #创建钩子方法
#     all_locusts_spawned.release()
#
# #挂载到locust钩子函数（所有的Locust实例产生完成时触发）
# events.hatch_complete += on_hatch_complete
#
#
#
# ##然后在
# class TestTask(TaskSet):
#     def on_start(self):
#         """ on_start is called when a Locust start before any task is scheduled """
#         self.login()
#         all_locusts_spawned.wait() #限制在所有用户准备完成前处于等待状态

######################################################################

#自定义用户增加行为
# class MyCustomShape(LoadTestShape):
#     #在10s中之内增加到10个用户，频率是每秒钟增加5个
#     #在60s中之内增加到20个用户，频率是每秒钟增加5个
#
#     stages = [
#         {"time":10, "users":10, "spawn_rate":5},
#         {"time":60, "users":20, "spawn_rate":5},
#     ]
#
#     def tick(self):
#         run_time = self.get_run_time()
#         print("run_time:", run_time)
#         for stage in self.stages:
#             if run_time < stage['time']:
#                 print('1阶段',stage['time'])
#                 tick_data = (stage['users'], stage['spawn_rate'])
#                 return tick_data
#         return None


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



    ###监控参数，发现问题：用户数、吞吐量、响应时间
    ###通过专业的工具是定位问题：prometheus+exporter+grafans

