from bs4 import BeautifulSoup
import requests
from pprint import pprint as pp
import csv
from datetime import datetime

CSV = 'kivano.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/mobilnye-telefony'
HEADERS = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}


def get_html(url, params=''):
    respose = requests.get(URL, headers=HEADERS, params=params, verify=False)
    return respose

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='item product_listbox oh')
    comps = []

    for item in items:
        comps.append({
            'title': item.find('div', class_='listbox_title oh').find('a').get_text(strip=True),
            'link': HOST + item.find('div', class_='listbox_img pull-left').find('img').get('src'),
            'price': item.find('div', class_='listbox_price text-center').find(strip=True)
        })

    return comps

def save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link']])

def parser():
    PAGENATOR = input('введите номер страницы:  ')
    PAGENATOR = int(PAGENATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, PAGENATOR):
            print(f"Страница №{page}готова")
            html = get_html(URL, params={'page':page})
            new_list.extend(get_content(html.text))
        save(new_list, CSV)
        print('готов к работе')
    else:
        print('Error')

parser()