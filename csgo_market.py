#!/usr/bin/env python
# coding: utf-8

# ## Формирование csv-файла по данным из excel-файла с предметами на торговой площадке Steam

# In[ ]:


# импорт библиотек
import json
import time
import os
import re
import bs4
import requests
import pandas as pd
from openpyxl import Workbook, load_workbook
from bs4 import BeautifulSoup
from datetime import datetime


# In[ ]:


# загрузка данных из excel-файла
items = pd.read_excel('items.xlsx')


# In[ ]:


# steam id игры
game_id = 730

# cookie steamLoginSecure только для авторизированных пользователей на сайте Steam
steam_login_secure = 'Your steam_login_secure'

# url, к которому будем обращаться
items['url'] = f'https://steamcommunity.com/market/listings/{game_id}/' + items['name']


# In[ ]:


# создадим функцию для поиска определённого класса в HTML-коде
def parse_html(html, class_):
    # Используем библиотеку beautiful soup для анализа HTML-кода
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Используем re.search для поиска классов по тегу 'class_'
    text = soup.find(class_=class_)

    return text


# In[ ]:


# создадим словарь с заголовками для GET-запроса
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
           'Accept-Language': 'ru-RU',
           'Content-Type': 'application/json'}
cookies = {'steamLoginSecure': steam_login_secure}


# In[ ]:


# выполним запрос к торговой площадке Steam
items['response_text'] = items.apply(lambda row: (time.sleep(12),
                                                  requests.get(row['url'],
                                                               headers=headers,
                                                               cookies=cookies).text)[1],
                                     axis=1)


# In[ ]:


# найдём в HTML коде строки с продажами для каждого предмета
items['sells_text'] = items.apply(lambda row: re.search(r'var line1=(.+);',
                                                        row['response_text']),
                                  axis=1)


# In[ ]:


# найдём в HTML коде строки с url изображения для каждого предмета
items['image_text'] = items.apply(lambda row: re.search(r'src="(.*?)"',
                                                        str(parse_html(row['response_text'],
                                                                       'market_listing_largeimage'))),
                                  axis=1)


# In[ ]:


# преобразуем полученный HTML-код в строку
items['sells'] = items.apply(lambda row: row['sells_text'].group(1), axis=1)
items['image_url'] = items.apply(lambda row: row['image_text'].group(1), axis=1)


# In[ ]:


items['sells'] = items.apply(lambda row: eval(row['sells']), axis=1) # преобразование строки в список списков
items = items.explode('sells') # разделение списков на отдельные строки


# In[ ]:


# создадим новые столбцы и удалим ненужные
items[['date_sold_item', 'median_price_sold_item', 'count_sold_item']] = pd.DataFrame(items['sells'].tolist(),
                                                                                      index=items.index)

items.drop(['url',
            'response_text',
            'sells_text',
            'sells',
            'image_text'],
           axis=1,
           inplace=True)


# In[ ]:


# преобразуем типы данных
items = items.astype({'count_sold_item': 'int64'})


# In[ ]:


# создадим словарь с месяцами
months = {'Jan': '01',
          'Feb': '02', 
          'Mar': '03',
          'Apr': '04', 
          'May': '05', 
          'Jun': '06',
          'Jul': '07',
          'Aug': '08',
          'Sep': '09',
          'Oct': '10', 
          'Nov': '11', 
          'Dec': '12'}


# In[ ]:


# заменим текстовое обозначение месяцев на числовое
for key in months.keys():
    items['date_sold_item'] = items['date_sold_item'].str.replace(key, months[key])


# In[ ]:


# удалим значения времени в конце строки
items['date_sold_item'] = items['date_sold_item'].apply(lambda row: row[:-7])
# приведём строку с датой к формату 'datetime'
items['date_sold_item'] = items['date_sold_item'].apply(lambda row: pd.to_datetime(row, format='%m %d %Y'))


# In[ ]:


# сбросим индекс
items = items.reset_index(drop=True)


# In[ ]:


# сгруппируем датафрейм
items = items.groupby(['name',
                       'category',
                       'image_url',
                       'date_sold_item']).agg({'median_price_sold_item': 'median',
                                               'count_sold_item': 'sum'}).reset_index()


# In[ ]:


# выгрузим данные в формате csv
items.to_csv('items.csv', header=True, index=False)

