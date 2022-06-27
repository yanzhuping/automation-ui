from mimesis import Person
from mimesis.schema import Schema
import re

def testing():
    return {
        'email': '',
        'password':'',
        'firstname': '',
        'lastname': '',
        'is_subscribed':True
    }

def get_register_data(num):
    schema = Schema(schema=testing)
    print(schema.create(num))

def find_all_data(data, LB='', RB=''):
    '''
    LB,RB为左右边界
    :param data:
    :param LB:
    :param RB:
    :return:
    '''
    rule = LB + r'(.+?)' + RB
    data_list = re.findall(rule, data)
    return data_list


if __name__ == '__main__':
    get_register_data(2)
