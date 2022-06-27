# 参数解释：
## 必填参数
* env：在config.ini文件中配置的用户参数
* test_case: 运行的测试用例，可以是具体的文件路径或是需要执行的文件夹路径
## 非必填参数
* level：根据设置不同的level运行测试用例,等级可以用:1，2，3
* view：是否展示视图模式，yes/no
* filter：忽略文件参数，当test_case参数传输的是文件夹路径，此处传入具体文件名称，会忽略不执行,格式:[],注意，部署到linux环境，list内的元素，引号需要转义”\“
* func:功能参数，如:员工管理添加一条数据/人事管理添加一条数据
* pattern：接口测试所需的参数，具体的接口测试用例名称或者所有接口测试用例,如：test_EveryDay_1.py/test*.py
* customer:客户参数，如：上海自动化测试有限公司、上海家花化妆品有限公司

# 命令写法如下：
* 运行单个文件，路径写到具体的文件名
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/SalaryGroup.xls
> 
> python main.py --env=auto --view=yes --test_case=fuc/EveryDayTest.xls
* 运行整个文件夹中的用例，则路径只需要写到execute下面的具体文件夹
> python main.py --env=auto --view=yes --test_case=execute/CommonServiceConfiguration
> 
> python main.py --env=auto --view=yes --test_case=execute/CommonSystemConfiguration
> 
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration
> 
> python main.py --env=auto --view=yes --test_case=execute/SalaryCalculation
> 
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration
> 
> python main.py --env=auto --view=yes --test_case=execute/SocialSecurityServiceApplication
> 
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration
> 
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement
> 
# 备份数据
* 在本地的D盘（会自动创建文件夹）备份element_selector、test_case、test_data三个文件夹的内容
> python backupCopy.py
# API自动化测试
* 运行api_case文件夹内的所有接口用例
> python API_Main.py --pattern=test*.py --env=qa-trdp-yzp --customer=上海自动化测试有限公司
* 每日校验接口测试-租户
> python API_Main.py --pattern=test_EveryDay_1.py
* 每日校验接口测试-单立户
> python API_Main.py --pattern=test_EveryDay_2.py
* 政策查询
> python API_Main.py --pattern=test_PolicyQuery.py

# UI自动化测试
## 相关功能
* 获取jenkins集成测试结果，输出报告testResultSummary.html
> python ./small_tools/getJenkinsResult.py
* 每日校验
> python main.py --env=auto --view=yes --test_case=fuc/EveryDayTest.xls
* 增加1条员工数据：
> python main.py --env=auto --view=yes --test_case=fuc/AddStaffData.xls
* 删除2条员工数据：
> python main.py --env=auto --view=yes --test_case=fuc/DeleteStaffData.xls
* 薪资计算的一个完整流程：启动-计算（计算中-待审批）-审批-拒绝-计算-审批-通过-关账
> python main.py --env=qa-trdp-yzp --view=yes --test_case=fuc/SalaryCalculationProcess.xls
* 一个申报的成功流程： 
  
  HR提交
  
  前道客服审核(社保、公积金)
  
  后道客服审核通过(社保、公积金)
> python main.py --env=auto --view=yes --test_case=fuc/DeclarationProcessSuccessful.xls
* 一个申报的失败后再次重新申请的完整流程：
  
  HR提交-前道客服审核(社保、公积金)-后道客服审核(社保拒绝、公积金拒绝)
  
  HR再次提交-前道客服审核(社保、公积金)-后道客服审核(社保失败、公积金成功)
  
  HR再次提交-前道客服审核(社保、公积金)-后道客服审核(社保通过、公积金通过)
> python main.py --env=auto --view=yes --test_case=fuc/DeclarationProcessFailure.xls
* 在职服务申请流程-成功
> python main.py --env=auto --view=yes --test_case=fuc/InServiceProcessSuc.xls
* 在职服务申请流程-失败，再次申请，然后成功
> python main.py --env=auto --view=yes --test_case=fuc/InServiceProcessFail.xls
* 自主入职流程
> python main.py --env=auto --view=yes --test_case=fuc/IndependentOrientation.xls
* 每种角色的权限校验
> python main.py --view=yes --test_case=fuc/PermissionsValidation.xls
## 员工管理
* 员工数据维护（各输入框、下拉框属性、必填校验等）
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement/StaffData.xls
* 员工数据导入
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement/ImportStaffData.xls
* 出勤数据维护
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement/AttendanceData.xls
* 出勤数据导入
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement/ImportAttendanceData.xls
* 薪资数据维护
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement/SalaryData.xls
* 薪资数据导入
> python main.py --env=auto --view=yes --test_case=execute/StaffManagement/ImportSalaryData.xls
## 薪资计算
* 薪资计算
> python main.py --env=auto --view=yes --test_case=execute/SalaryCalculation/SalaryCalculation.xls
* 薪资计算导入
> python main.py --env=auto --view=yes --test_case=execute/SalaryCalculation/ImportSalaryCalculation.xls
* 计算结果查询
> python main.py --env=auto --view=yes --test_case=execute/SalaryCalculation/QueryCalculationResult.xls
## 薪资业务配置
* 年度日历配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/AnnualCalendar.xls
* 薪资周期配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/PayrollCycle.xls
* 薪资组配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/SalaryGroup.xls
* 薪资公式配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/SalaryFormula.xls
* 最低工资配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/MinimumWage.xls
* 平均工资配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/AverageSalary.xls
* 计薪人员组配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/PaidPersonnelGroup.xls
* 薪资科目配置
> python main.py --env=auto --view=yes --test_case=execute/SalaryServiceConfiguration/SalaryAccounts.xls
## 社保系统配置（平台）
* 社保规则配置
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration/SocialSecurityRules.xls
* 公积金规则配置
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration/AccumulationFundRules.xls
* 在职服务配置
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration/InServiceConfig.xls
## 政策查询
* 社保规则查询
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration/QuerySocialSecurityRules.xls
* 公积金规则查询
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration/QueryAccumulationFundRules.xls
* 在职服务配置查询
> python main.py --env=auto --view=yes --test_case=execute/SocialSecuritySystemConfiguration/QueryInServiceConfig.xls
## 申报管理（平台）
* 员工信息反馈
> python main.py --env=auto --view=yes --test_case=execute/SocialSecurityServiceApplication/EmInfoFeedback.xls
## 在职服务（平台）
* 在职服务确认
> python main.py --env=auto --view=yes --test_case=execute/SocialSecurityServiceApplication/InServiceConfirm.xls
* 在职服务反馈
> python main.py --env=auto --view=yes --test_case=execute/SocialSecurityServiceApplication/InServiceFeedback.xls
## 公共系统配置(admin)
* 用户管理
> python main.py --env=admin --view=yes --test_case=execute/CommonSystemConfiguration/UserManagement.xls
* 客户管理
> python main.py --env=admin --view=yes --test_case=execute/CommonSystemConfiguration/CustomerManagement.xls
* 服务费配置
> python main.py --env=admin --view=yes --test_case=execute/CommonSystemConfiguration/ServiceFeeConfig.xls
## 公共业务配置
* 用户配置
> python main.py --env=auto --view=yes --test_case=execute/CommonServiceConfiguration/UserConfig.xls
## 人事业务配置
* 自主入职信息配置
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/IndeInfoConfig.xls
* 组织管理配置
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/OriganManageConfig.xls
* 职位管理配置
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/PositionManageConfig.xls
* 岗位管理配置
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/JobsManageConfig.xls
* 职级管理配置
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/RankManageConfig.xls
* 组织、职位、岗位，导入功能
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/ImportPersonnelServiceConfig.xls
## 人事管理
* 异动管理
> python main.py --env=auto --view=yes --test_case=execute/PersonnelServiceConfiguration/Change.xls
## 添加员工不同入口
* 汇总
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess
* H5页面创建，入职时间为当前时间，且员工维护页面的修改不影响员工信息
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess/IndependentOrientation_1.xls
* H5页面创建，入职时间为过去时间
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess/IndependentOrientation_2.xls
* H5页面创建，入职时间为未来时间
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess/IndependentOrientation_3.xls
* 员工信息页面创建，入职时间为当前时间
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess/IndependentOrientation_4.xls
* 员工信息页面创建，入职时间为未来时间
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess/IndependentOrientation_5.xls
* 员工数据维护页面创建，数据不同步至员工信息
> python main.py --env=auto --view=yes --test_case=execute/EmployeeOnboardingProcess/IndependentOrientation_6.xls
## 合同管理
* 合同模板管理
> python main.py --env=auto --view=yes --test_case=execute/ContractManagement/ContractTemplateManagement.xls
* 合同签署
> python main.py --env=auto --view=yes --test_case=execute/ContractManagement/SignedContract.xls