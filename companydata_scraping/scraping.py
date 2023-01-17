# ライブラリのインポート
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import re

url = 'https://www.ajisho.jp/hpgen/HPB/shop/business.html'


try:
    url = url.replace('\n','').replace('\t','').replace('\r','')
    r = requests.get(url)
    sleep(1)
    _soup = BeautifulSoup(r.text)
    _word_list = _soup.text.split('\n')
    # print(_word_list)
    
except Exception as e:
  url = url
