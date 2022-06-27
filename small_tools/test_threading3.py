#!/usr/bin/python3

import queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("开启线程：" + self.name)
        process_data(self.name, self.q)
        print ("退出线程：" + self.name)

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)

print(11111)
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
print(22222)
for tName in threadList:
    print('aaaaa')
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
print(3333)
queueLock.acquire()
for word in nameList:
    print('bbbbb')
    workQueue.put(word)
queueLock.release()

# 等待队列清空
print(44444)
while not workQueue.empty():
    # print('ccccc')
    pass

# 通知线程是时候退出
print(55555)
exitFlag = 1

# 等待所有线程完成
print(66666)
for t in threads:
    print('ddddd')
    t.join()
print ("退出主线程")