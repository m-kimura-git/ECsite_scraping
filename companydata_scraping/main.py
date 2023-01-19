# ライブラリのインポート
from address_ import *
from scraping import *

def main():

    # ↓ここに　特定商取引ページURLのリストのCSVファイルの名前を入れて実行すること！
    print('特定商取引ページURLのCSVファイル名を入力してください。')
    filename = input()

    scraping_list = []
    with open(filename,encoding="utf-8") as f:
        for url in f:
            company,administrator,tel,ad_num,address = scraping(url)
            ad1 = ''
            ad2 = ''
            ad3 = ''
            ad4 = ''
            stutas=''
            if company !='' and address!='' and tel!='':
                stutas,ad1,ad2,ad3,ad4 = address_clean(address)
                print(stutas)
            elif company == '' and administrator=='' and tel=='' and ad_num=='' and address=='':
                continue
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
    df = pd.DataFrame(scraping_list,index=False)
    df.to_csv( re.search('(.*?).csv',filename).group(1) +'_result.csv')


if __name__ == "__main__":
    main()