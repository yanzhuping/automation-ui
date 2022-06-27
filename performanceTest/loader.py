import csv
from typing import Text

def load_csv_file(csv_file: Text):
    csv_content_list = []
    with open(csv_file, encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            csv_content_list.append(row)
    print(csv_content_list)

    return csv_content_list

if __name__ == '__main__':
    load_csv_file('./data/user.csv')
