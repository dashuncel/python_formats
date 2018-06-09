# -*- coding: utf-8 -*-
import json
from pprint import pprint
import chardet
import xml.etree.ElementTree as ET

# возвращает ключ по значению из словаря:
def getKeys(dict, val):
    keys = []
    for key, elem in dict.items():
        if val == elem:
           keys.append(key)
    return keys


# возвращает словарь "слово" - частота
def det_frequency(text):
    wordlist = text.lower().split(None)
    frequencies = {}
    for word in wordlist:
        if len(word) < 6:
            continue
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    return frequencies


# вывод на печать топ-6 частов встречающихся слов:
def print_frequency(frequency, file_name):
    i = 0
    req = sorted(list(frequency.values()), reverse=True)
    print('Часто встречающиеся слова в файле "{}":'.format(file_name))
    while i < min(6, len(req)):
        print('{} - {} раз'.format(getKeys(frequency, req[i]), req[i]))
        i += 1

# читает json файл в заданной кодировке, возвращает частосту слов:
def read_json(file_name, codePage):
    with open(file_name, encoding=codePage) as f:
        try:
            text = json.load(f)
        except UnicodeError:
            print('Не могу прочитать файл "{}" в кодировке {}'.format(file_name, codePage))
            return

        try:
            list_news = text['rss']['channel']['items']
        except IndexError:
            print('Неверная структура данных файла {}'.format(file_name))
            return

        data = ''

        for new in list_news:
            data += new['description']

    print_frequency(det_frequency(data), file_name)


# читает xml-файл
def read_xml(file_name, codePage):
    try:
        with open(file_name, encoding=codePage) as f:
            data = f.read()
            tree = ET.fromstring(data)
    except UnicodeError:
        print('Не могу распарсить xml из файла {}!'.format(file_name))
        return

    for child in tree.iter('item'):
        data += child.find('description').text

    print_frequency(det_frequency(data), file_name)


list_files = ['newsafr.json', 'newsfr.json', 'newscy.json', 'newsit.json', 'newsfr.xml', 'newsit.xml', 'newsafr.xml', 'newscy.xml']
#list_files = ['newsfr.xml', 'newsit.xml', 'newsafr.xml', 'newscy.xml']
#list_files = ['newsafr.json', 'newsfr.json', 'newscy.json', 'newsit.json']

for news_file in list_files:
    tmp_str = news_file.split('.')
    extent = tmp_str[len(tmp_str) - 1]

    with open(news_file, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        codePage = result['encoding']

    if extent == 'json':
        read_json(news_file, codePage)
    elif extent == 'xml':
        read_xml(news_file, codePage)
    else:
        print('Не умею читать файлы с расширением "{}"'.format(extent))