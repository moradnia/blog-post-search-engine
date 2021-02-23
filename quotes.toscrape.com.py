#!/usr/bin/env python
# coding: utf-8

# In[80]:


import time
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
es= Elasticsearch(HOST="http://localhost",PORT=9200)
es= Elasticsearch()
es.indices.create(index='scrape-quotes', ignore=400)
url = 'https://quotes.toscrape.com/page/'
for i in range(11):
    real_url = url+str(i)
    response = requests.get(real_url)
    soup = BeautifulSoup(response.content,'html.parser')
    box = soup.findAll('div',class_='quote')
    for b in box:
        text = b.find('span',class_='text').text
        auther = b.find('small',class_='author').text
        about_sample = b.select('span a')
        for x in about_sample:
            about=x['href']
        tag_div = b.select('div.tags > a')
        for x in tag_div:
            tag_div=x.text

        doc = {
            'url':text,
            'title':auther,
            'tags':tag_div,
            'date':time.strftime("%Y-%m-%d"),
            'about':'https://quotes.toscrape.com/'+about
        }
        res = es.index(index="scrape-quotes", doc_type="docs", body=doc)
        time.sleep(0.5)
        
        


# In[ ]:





# In[ ]:




