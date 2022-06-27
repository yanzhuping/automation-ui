#psutil:获取系统信息模块，可以获取CPU，内存，磁盘等的使用情况
import psutil
import time
import datetime
#logfile：监测信息写入文件
def MonitorSystem(logfile = None):
    #获取cpu使用情况
    cpuper = psutil.cpu_percent()
    #获取内存使用情况：系统内存大小，使用内存，有效内存，内存使用率
    mem = psutil.virtual_memory()
    #内存使用率
    print(mem)
    memper = mem.percent
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} cpu:{cpuper}%, mem:{memper}%'
    print(line)
    if logfile:
        logfile.write(line)


MonitorSystem(logfile = None)