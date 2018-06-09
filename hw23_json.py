import json
from pprint import pprint
import chardet
#import xml
#import xml.etree.ElementTree as ET

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


# читает json файл в заданной кодировке, возвращает частосту слов:
def read_json(file_name, codePage):
    with open(file_name, encoding=codePage) as f:
        try:
            text = json.load(f)
        except UnicodeError:
            print('Не могу прочитать файл "{}" в кодировке {}'.format(file_name, codePage))
            return

        list_news = text['rss']['channel']['items']
        data = ''

        for new in list_news:
            data += new['description']

    frequency = det_frequency(data)
    i = 0
    req = sorted(list(frequency.values()), reverse=True)
    print('Часто встречающиеся слова в файле "{}":'.format(file_name))
    while i < min(6, len(req)):
        print('{} - {} раз'.format(getKeys(frequency, req[i]), req[i]))
        i += 1


# читает xml-файл
def read_xml(file_name):
    pass
    #tree = ET.parse(file_name)


list_files = ['newsafr.json', 'newsfr.json', 'newscy.json', 'newsit.json']
#'newsfr.xml', 'newsit.xml', 'newsafr.xml', 'newscy.xml', 'newscy.xm'

for news_file in list_files:
    tmpstr = news_file.split('.')
    extent = tmpstr[len(tmpstr) - 1]

    if extent == 'json':
        # предварительно определяем кодироку текста:
        with open(news_file, 'rb') as f:
            data = f.read()
            result = chardet.detect(data)
            codePage = result['encoding']

        read_json(news_file, codePage)
    elif extent == 'xml':
        read_xml(news_file)
    else:
        print('Не умею читать файлы с расширением "{}"'.format(extent))