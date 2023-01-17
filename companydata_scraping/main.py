# ライブラリのインポート
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import re
from address_ import *

re_company1 = '販売会社：|販売業者：|販売事業者：|販売業者名：|販売事業者名：|運営元：|事業者：|事業者:|販売会社:|販売業者:|販売事業者:|販売業者名:|販売事業者名:|運営元:'
re_company2 = '販売会社|販売業者|販売事業者|販売業者名|販売事業者名|運営元|事業者'
re_administrator = '運営統括責任者名' 
re_mail = '公開メールアドレス|メールアドレス' 
re_ad1 = '住所：|住所:|所在地：|所在地:'
re_ad2 = '住所|所在地|所在地及び連絡先'
re_tel1 = '電話番号：|電話番号:|電話：|電話:|連絡先：|連絡先:|TEL:'
re_tel2 = '電話番号|電話|連絡先|TEL'
re_yubin = '〒\d{7}|\d{7}|〒\d{3}-\d{4}|〒\d{3}ー\d{4}|^\d{3}-\d{4}'
re_tel3 = '\d{2,4}-\d{2,4}-\d{3,4}|\d{10,11}'


def main():  
  # ↓ここに　特定商取引ページURLのリストのCSVファイルの名前を入れて実行すること！
  print('特定商取引ページURLのCSVファイル名を入力してください。')
  filename = input()

  scraping_list = []
  with open(filename,encoding="utf-8") as f:
      for url in f:
          try:
              url = url.replace('\n','').replace('\t','').replace('\r','')
              # url = url+'?mode=sk'
              # print(url)
              r = requests.get(url)
              sleep(1)

              _soup = BeautifulSoup(r.content,'html.parser')
              _word_list = _soup.text.split('\n')
              _word_list = [s.encode('cp932',errors='ignore').decode('cp932').replace('\u3000','') for s in _word_list if '' != s]
              # print(_word_list)
              # print(url)
              i=0
              stutas=''
              company=''
              address=''
              tel =''
              ad1 = ''
              ad2 = ''
              ad3 = ''
              ad4 = ''
              mail =''
              administrator = ''

              for _word in _word_list:
                  #*========*========*会社名の抽出*========*========*
                  if re.compile(re_company1).search(_word):
                      company = clean(_word.replace(re.match(re_company1,_word).group(),''))
                      print(company)
                  else: 
                      if re.compile(re_company2).search(_word):
                          company = clean(_word_list[i+1])
                          print(company)
                  #*========*========*運営統括責任者の抽出*========*========*
                  if re.compile(re_administrator).search(_word):
                      administrator = clean(_word_list[i+1])
                      print(administrator)
                  #*========*========*メールアドレスの抽出*========*========*
                  if re.compile(re_mail).search(_word):
                      mail = _word_list[i+1]
                      print(mail)

                  #*========*========*住所の抽出*========*========*
                  if re.compile(re_ad1).search(_word):
                      address = _word.replace(re.match(re_ad1,_word).group(),'')
                      if re.compile(re_yubin).search(address):
                          address = address.replace(re.search(re_yubin,address).group(),'')
                      print(address)
                  else:
                      if re.compile(re_ad2).search(_word):
                          address = _word_list[i+1]
                          if re.compile(re_yubin).search(address):
                              address = address.replace(re.search(re_yubin,address).group(),'')
                          print(address)

                  #*========*========*電話番号の抽出*========*========*
                  if re.compile(re_tel1).search(_word):
                      tel = clean(_word.replace(re.match(re_tel1,_word).group(),''))
                      if re.compile(re_tel3).search(tel):
                          tel = re.search(re_tel3,tel).group()
                          print(tel)
                      else:
                          tel = ''
                  else:
                      if re.compile(re_tel2).search(_word):
                          if re.compile(re_tel3).search(_word_list[i+1]):
                              tel = re.search(re_tel3,_word_list[i+1]).group()
                              print(tel)
                  if company !='' and address!='' and tel!='':
                      break
                  i+=1
              if company !='' and address!='' and tel!='':
                  stutas,ad1,ad2,ad3,ad4 = address_clean(address)
                  print(stutas)
                  data = {
                          'url':url,
                          'stutas':stutas,
                          'company':company,
                          'tel':tel,
                          'ad1':ad1,
                          'ad2':ad2,
                          'ad3':ad3,
                          'ad4':ad4
                  }
                  scraping_list.append(data)
              else:
                  stutas,ad1,ad2,ad3,ad4 = address_clean(address)
                  stutas = 'scraping error'
                  print(stutas)
                  data = {
                      'url':url,
                      'stutas':stutas,
                      'company':company,
                      'tel':tel,
                      'ad1':ad1,
                      'ad2':ad2,
                      'ad3':ad3,
                      'ad4':ad4
                  }
                  scraping_list.append(data)

          except UnicodeDecodeError:
              print('UnicodeDecode error')
              stutas = 'UnicodeDecode error'

              company=''
              address=''
              tel =''
              ad1 = ''
              ad2 = ''
              ad3 = ''
              ad4 = ''
              data = {
                      'url':url,
                      'stutas':stutas,
                      'company':company,
                      'tel':tel,
                      'ad1':ad1,
                      'ad2':ad2,
                      'ad3':ad3,
                      'ad4':ad4
                  }
              scraping_list.append(data)


          except Exception as e:
              print('Access error')
              stutas = 'Access error'
              company=''
              address=''
              tel =''
              ad1 = ''
              ad2 = ''
              ad3 = ''
              ad4 = ''
              data = {
                      'url':url,
                      'stutas':stutas,
                      'company':company,
                      'tel':tel,
                      'ad1':ad1,
                      'ad2':ad2,
                      'ad3':ad3,
                      'ad4':ad4
                  }
              scraping_list.append(data)

  df = pd.DataFrame(scraping_list)
  df.to_csv( re.search('(.*?).csv',filename).group(1) +'_result.csv')


if __name__ == "__main__":
  main()