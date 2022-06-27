# -*- coding:UTF-8 -*-
import sys
from libs.keywords_trans import *
from driver.driver import *
import traceback
import datetime
import webbrowser

class MainHandler:
    def __init__(self):
        # 读取命令行参数
        self.t_opt = get_opt(sys.argv[1:])
        # 根据参数读取配置
        self.g_config = get_global_config(self.t_opt.get("env"))
        #调用设置的浏览器
        self.driver = browser(self.t_opt.get("view"))
        # 存储用例,结构如下：{"login1":[{'id': 'login01', 'desc': '登录网站', },{},{},]}
        self.case_store = {}
        # 存储用例执行过程的变量
        self.case_variable = {}
        # 用例执行结果
        self.case_result = {'total': set(), 'failed': set()}
        # 存储元素选择器json
        self.ele_selector_store = {}

    def do_execute(self):
        # 读取所有的用例
        start = datetime.datetime.now()
        print(start)
        filterList = get_filterFile(get_execute_dir(self.t_opt.get("test_case")),
                                    fileName_list=eval(str(self.t_opt.get("filter"))))
        file_list = list_dir(get_execute_dir(self.t_opt.get("test_case")),fileName_list=filterList)
        # 命令行读取到的level
        # 如果level字段为空，则默认给一个-1
        opt_level = str(self.t_opt.get("level",'-1'))
        for file_path in file_list:
            '''
            读取excel中具体的用例,返回一个数据列表，格式如：
            [{'id': 'login01', 'desc': '登录网站', 'keywords': 'login_qthl', 
            'selector': '','val': '', 'level': ''},{},{},]
            '''
            print(file_path)
            case_list = read_excel(file_path)
            errorLines = []
            case_id = ''
            # index(下标)从0开始，case是读取的excel每一行的数据，类型是字典
            for index, case in enumerate(case_list):
                # print("index:",index)
                # print("case:",case)
                #在读取的case后面增加一个字段，增加后：{"":"",……,"keyexpression":"public.common_button.customerName"}
                case['keyexpression'] = case.get('selector')
                # print("修改过后的case",case)
                case_id = case.get("id")
                #如果一个用例中没有任何的失败抛出，就把这条用例从该字典中删除
                if len(self.case_store) != 0:
                    #第一个循环不走这一步
                    # print("case_store:")
                    # print(self.case_store)
                    # print("++++++++++++++++++++++++++++++++")
                    #获取用例存储字典中所有的key
                    case_store_keys = list(self.case_store.keys())
                    # 取最后一个key
                    pre_caseid = case_store_keys[-1]
                    # 执行一个新的caseId（新用例）时，如果上个用例没有失败就在case_store删除保存的用例
                    if case_id not in case_store_keys and pre_caseid not in self.case_result.get(
                            "failed"):
                        self.case_store.pop(pre_caseid)

                keywords = case.get("keywords")
                # 根据key从json文件获取选择器,拿到最终的元素定位
                get_selector_val(self, case)
                # 将用例中的level项格式化，如2.0变成2
                case_level = format_digit_str(case.get("level"))
                # 关键词存在并且用例的level和命令行指定的level一致（命令行没有指定level则运行所有的用例）
                if keywords is not None and keywords != "" and (
                        opt_level == '-1' or opt_level == case_level):
                    try:
                        if self.case_store.get(case.get('id')) is None:
                            self.case_store[case.get('id')] = []  #{”login“：[]}
                        if case_id is not None and case_id != "":
                            #total:用例总数，self.case_result.get("total")=》set()
                            #将用例数目添加进集合，id一样会自动去重
                            self.case_result.get("total").add(case_id)
                        # 根据keywords触发相应的函数
                        globals().get(case.get("keywords") + "_handler")(
                            self, case)
                        try:
                            insert_img(
                                self.driver, case_id, "{}_{}.png".format(
                                    case_id,len(self.case_store.get(case_id))))
                        except:
                            pass

                        # 保存相应的用例后面校验用  根据用例Id动态生成变量
                        self.case_store[case.get('id')].append(case)
                        successful_desc = "用例Id：{id},步骤描述：{desc}，关键字：{keywords}，元素" \
                                          "关键字：{keyexpression}，选择器：{selector},操作值：{val}".format(
                            **case)  # **case通过字典设置参数
                        print("第",index+2,"行成功！",successful_desc)
                    except:
                        insert_img(
                            self.driver, case_id, "{}_{}.png".format(
                                case_id, len(self.case_store.get(case_id))))
                        failed_desc = "用例Id：{id},步骤描述：{desc}，关键字：{keywords}，元素" \
                                      "关键字：{keyexpression}，选择器：{selector},操作值：{val}".format(
                            **case)  # **case通过字典设置参数
                        traceback_info = traceback.format_exc()
                        print("第",index+2,"行失败！",failed_desc)
                        errorLines.append(int(index+1))
                        print(traceback_info)
                        #将失败的用例添加进集合
                        self.case_result.get("failed").add(case_id)
                        #在失败的case后面添加一个字段{"id","",……,"keyexpression":"","traceback":"抛出的报错信息"}
                        case["traceback"] = traceback_info
                        self.case_store[case.get('id')].append(case)
            #当1个用例执行完毕，关闭浏览器，并再次打开，执行第二条用例
            ## 将错误的行数标记成设置的背景色#################
            print(errorLines)
            try:
                markErrorLines(errorLines, case_id, file_path)
            except:
                # print(traceback.format_exc())
                pass
            #############################################
            self.driver.quit()
            self.driver = browser(self.t_opt.get("view"))
        #处理测试用例的结果
        end = datetime.datetime.now()
        executeTime.append(start)
        executeTime.append(end)
        # print(executeTime)
        handle_case_result(self.case_result, self.case_store)
        print("------------------------全部执行结束--------------------------------")
        self.driver.quit()
        print("程序运行时间：",end - start)
        if self.case_result.get('failed') != set():
            print("OH~NO/(ㄒoㄒ)/~~运行有报错，请查看异常测试报告")
            print('完整测试报告：',os.path.join(get_root_path(), 'test_report', "report.html"))
            print('异常测试报告：',os.path.join(get_root_path(), 'test_report', "error_report.html"))
            webbrowser.open(os.path.join(get_root_path(), 'test_report', "error_report.html"), new=2)
        else:
            print("NICE(*￣▽￣*)，运行正常，无报错")


if __name__ == "__main__":
    main_handler = MainHandler()
    main_handler.do_execute()