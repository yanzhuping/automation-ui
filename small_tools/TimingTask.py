import time
from pytz import utc
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from small_tools.getJenkinsResult import outPutResult
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pymongo import MongoClient

def job():
    url = r'D:\WorkCode\automation\test_report\testResultSummary.html'
    projectNames = [
        ['Test_API', 'API', '接口测试'],
        ['StaffManagement', 'UI', '员工管理'],
        ['SalaryCalculation', 'UI', '薪资计算'],
        ['SalaryServiceConfiguration', 'UI', '薪资业务配置'],
        ['CommonServiceConfiguration', 'UI', '公共业务配置'],
        ['CommonSystemConfiguration', 'UI', '公共系统配置'],
        ['SalaryCalProcess', 'UI', '薪资计算流程'],
        ['DeclarationProcessFull', 'UI', '员工信息申报完整流程'],
        ['DeclarationProcessSuccessful', 'UI', '员工信息申报仅成功流程'],
        ['InServiceProcessFail', 'UI', '在职服务申请完整流程'],
        ['InServiceProcessSuc', 'UI', '在职服务申请成功流程'],
        ['PersonnelServiceConfiguration', 'UI', '人事业务配置'],
        ['SocialSecurityServiceApplication', 'UI', '社保业务申请'],
        ['SocialSecuritySystemConfiguration', 'UI', '社保系统配置'],
        ['EmployeeOnboardingProcess', 'UI', '自主入职流程'],
        ['PermissionsValidation', 'UI', '各种账号的权限校验'],
    ]
    outPutResult(projectNames, url)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


host = '127.0.0.1'
port = 27017
client = MongoClient(host, port)

jobstores = {
    'mongo': MongoDBJobStore(collection='job', database='test', client=client),
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')
scheduler.add_job(job, 'cron', day_of_week='mon-fri', hour=11, minute=34)

try:
    scheduler.start()
except SystemExit:
    client.close()