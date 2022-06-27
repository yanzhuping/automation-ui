from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from small_tools.getJenkinsResult import *

def my_job(id='my_job'):
    print(id, '-->', datetime.datetime.now())
    url = r'D:\WorkCode\automation\test_report\testResultSummary.html'
    projectNames = [
        ['Test_API', 'API', '接口测试'],
        ['StaffManagement', 'UI', '员工管理'],
        ['SalaryCalculation', 'UI', '薪资计算'],
        ['SalaryServiceConfiguration', 'UI', '薪资业务配置'],
        ['CommonServiceConfiguration', 'UI', '公共业务配置'],
        ['CommonSystemConfiguration', 'UI', '公共系统配置'],
        ['SalaryCalculationProcess', 'UI', '薪资计算流程'],
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

jobstores = {'default': MemoryJobStore()}

executors = {'default': ThreadPoolExecutor(20),'processpool': ProcessPoolExecutor(10)}

job_defaults = {'coalesce': False,'max_instances': 3}

scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

# scheduler.add_job(my_job, args=['job_interval', ], id='job_interval', trigger='interval', seconds=5,replace_existing=True)

scheduler.add_job(my_job, args=['job_cron', ], id='job_cron', trigger='cron', day_of_week='0-4', hour=8, minute=50)

try:
    scheduler.start()
except SystemExit:
    print('exit')
    exit()
