# 参数解释：
## 必填参数
* env：在config.ini文件中配置的用户参数
* test_case: 运行的测试用例
## 非必填参数
* level：根据设置不同的level运行测试用例

# 生产环境
> python main.py --env=prod_test --view=yes --test_case=prod_execute/******
* 从员工管理-员工数据维护-添加1条数据
> python main.py --env=prod_test --view=yes --test_case=prod_execute/AddStaffData.xls
* 薪资审批流程
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryCalPro.xls
* 基础校验流程
> python main.py --env=prod_test --view=yes --test_case=prod_execute/EveryDayTest.xls
## 人事业务配置
* 自主入职信息配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/PersonnelServiceConfiguration/IndeInfoConfig.xls
* 组织管理配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/PersonnelServiceConfiguration/OriganManageConfig.xls
* 职位管理配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/PersonnelServiceConfiguration/PositionManageConfig.xls
* 岗位管理配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/PersonnelServiceConfiguration/JobsManageConfig.xls
* 职级管理配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/PersonnelServiceConfiguration/RankManageConfig.xls
## 薪资业务配置
* 年度日历配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/AnnualCalendar.xls
* 薪资周期配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/PayrollCycle.xls
* 薪资组配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/SalaryGroup.xls
* 最低工资配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/MinimumWage.xls
* 平均工资配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/AverageSalary.xls
* 计薪人员组配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/PaidPersonnelGroup.xls
* 薪资科目配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SalaryServiceConfiguration/SalaryAccounts.xls
## 各种模块的导入
* 出勤数据导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportAttendanceData.xls
* 平均薪资导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportAverageSalary.xls
* 最低薪资导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportMinimumWage.xls
* 人事业务配置所有导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportPersonnelServiceConfig.xls
* 薪资计算导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportSalaryCalculation.xls
* 薪资数据导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportSalaryData.xls
* 员工数据导入
> python main.py --env=prod_test --view=yes --test_case=prod_execute/Prod_import/ImportStaffData.xls
## 社保系统配置（平台）
* 社保规则配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SocialSecuritySystemConfiguration/SocialSecurityRules.xls
* 公积金规则配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SocialSecuritySystemConfiguration/AccumulationFundRules.xls
* 在职服务配置
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SocialSecuritySystemConfiguration/InServiceConfig.xls
## 政策查询
* 社保规则查询
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SocialSecuritySystemConfiguration/QuerySocialSecurityRules.xls
* 公积金规则查询
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SocialSecuritySystemConfiguration/QueryAccumulationFundRules.xls
* 在职服务配置查询
> python main.py --env=prod_test --view=yes --test_case=prod_execute/SocialSecuritySystemConfiguration/QueryInServiceConfig.xls