from faker import Faker
import pymysql

def getName(number):
    '''
    生成姓名
    :param number:
    :return:
    '''
    fake = Faker(["zh_CN"])
    data=[]
    for i in range(99999999999):
        generatedData = fake.name()
        if generatedData not in data:
            data.append(generatedData)
            if len(data) == number:
                break
    print(len(data))
    print(data)
    return data

def getIDCardNo(number):
    '''
    生成身份证号码
    :param number:
    :return:
    '''
    fake = Faker(["zh_CN"])
    data=[]
    for i in range(99999999999):
        generatedData = fake.ssn()
        if generatedData not in data:
            data.append(generatedData)
            if len(data) == number:
                break
    print(len(data))
    print(data)
    return data

def getBankCardNo(number):
    '''
    生成银行卡账号
    :param number:
    :return:
    '''
    fake = Faker(["zh_CN"])
    data = []
    for i in range(9999999999):
        generatedData = fake.credit_card_number(card_type=None)
        if generatedData not in data and len(generatedData)>=16:
            data.append(generatedData)
            if len(data) == number:
                break
    print(len(data))
    print(data)
    return data

def getMobilePhoneNo(number):
    '''
    生成电话号码
    :param number:
    :return:
    '''
    fake = Faker(["zh_CN"])
    data = []
    for i in range(9999999999):
        generatedData = fake.phone_number()
        if generatedData not in data and len(generatedData) == 11:
            data.append(generatedData)
            if len(data) == number:
                break
    print(len(data))
    print(data)
    return data

def getAccumulationFundNo(number):
    '''
    生成公积金账号
    :param number:
    :return:
    '''
    data = []
    for i in range(10000000, 99999999):
        generatedData = '0' + str(i) + '205'
        if generatedData not in data:
            data.append(generatedData)
            if len(data) == number:
                break
    print(len(data))
    print(data)
    return data

def getEmNo(number):
    '''
    生成员工编号
    :param number:
    :return:
    '''
    data = []
    for i in range(10000000, 99999999):
        generatedData = 'Test' + str(i)
        if generatedData not in data:
            data.append(generatedData)
            if len(data) == number:
                break
    print(len(data))
    print(data)
    return data

def inserIntoMysql(table, field, number, func):
    '''
    将生成的数据插入数据库中
    :param table:
    :param field:
    :param number:
    :param func:
    :return:
    '''
    data = func(number)
    # print(data)
    db = pymysql.Connect(
            host='47.101.52.155',
            port=3306, user='tester',
            passwd='autester', db='automation',
            charset='utf8')

    cursor = db.cursor()
    for i in range(len(data)):
        cursor.execute("insert into %s(%s) values('%s')" % (table, field, data[i]))
    db.commit()
    db.close()

def run(order,*args):
    if order == 'id_card':
        number = args[0]
        getIDCardNo(number)
    if order == 'bank_card':
        number = args[0]
        getBankCardNo(number)

if __name__ == '__main__':
    # getName(10)
    # getIDCardNo(1)
    getBankCardNo(20)
    # getMobilePhoneNo(1)
    # getEmNo(1)
    # getAccumulationFundNo(1)
    # inserIntoMysql('accumulation', 'accFund',1, getName)
    # run('bank_card', 1)