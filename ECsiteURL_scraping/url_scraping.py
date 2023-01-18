# ライブラリのインポート
import time
from selenium import webdriver
import chromedriver_binary   
from selenium.webdriver.common.by import By
import csv
import random
import re
import pandas as pd

#####################################################
######現状ショップサーブ抽出用のコードになっている##########
#####################################################
def url_scraping():
    #googleで検索する文字
    print('検索キーワードを入力してください。')
    print('例："html/ordercontract.html"')
    search_string = input()

    #   print('何件データ抽出を行いますか。')
    #   num = input()
    print('URLを保存するファイル名を入力してください。')
    filename = input()
    num=10

    #Seleniumを使うための設定とgoogleの画面への遷移
    INTERVAL = 5
    URL = "https://www.google.com/"
    driver_path = "/Users/manayakimura/Library/Mobile Documents/com~apple~CloudDocs/WebScraping/chromedriver_109ver/chromedriver"
    driver = webdriver.Chrome()
    driver.maximize_window()
    time.sleep(INTERVAL)
    driver.get(URL)
    time.sleep(INTERVAL)

    #検索を実行
    #driver.find_element(By.CSS_SELECTOR, ".rr4y5c").click() 
    element = driver.find_element(By.NAME,"q")
    element.send_keys(search_string)
    element.submit()
    time.sleep(INTERVAL)

    #検索結果の一覧を取得する
    results = []
    output = []
    flag = False
    while True:
        g_ary = driver.find_elements(By.CLASS_NAME,'g')
        for g in g_ary:
            result = {}
            url = g.find_element(By.CSS_SELECTOR,'div.yuRUbf > a').get_attribute('href')
            if re.compile('hpgen/HPB/shop/business.html').search(url):
                result['特定商'] = url
                result['URL'] = url.replace('hpgen/HPB/shop/business.html','')
                result['TITLE'] = g.find_element(By.TAG_NAME,'h3').text
                results.append(result)
            else:
                break
            if len(results) >= num: #抽出する件数を指定
                flag = True
                break
        if flag:
            break
        try:
            # 次へ　のボタンがあればクリック
            driver.find_element(By.ID,'pnnext').click()
            time.sleep(INTERVAL + random.uniform(0,5))
        except:
            break
    driver.close()
    print(len(results))
    df = pd.DataFrame(results)
    df.to_csv(filename+'_result.csv',index=False)

url_scraping()
