
import csv
from dataclasses import field
from bs4 import BeautifulSoup
import sys

import requests

def main3():
    sys.setrecursionlimit(15000)
    filename = 'places2022_06_30_14_38_42 - Copy.csv'
    # read all data in file
    with  open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        
    print(len(data))
    for entry in data[0:3]:
        category, name, link = entry

        # request the link and parse it with BeautifulSoup
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        page_content = soup.find('div', {'id': 'page_content'})
        div_box = page_content.find('div', {'class': 'box'})
        p_el = div_box.find('p')
        ret = {}
        info =p_el.text
        ret['info'] = info
        split_info = info.split('\n')
        ret['first'] = split_info[0]
        for line in split_info:
            if ':' in line:
                fieldData = line.split(':')
                fieldName = fieldData[0].strip()
                fieldValue = fieldData[1].strip()
                ret[fieldName] = fieldValue
        pass
if __name__ == '__main__':
    main3()
