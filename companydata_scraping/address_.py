# ライブラリのインポート
import re

# 住所　→ 都道府県、市区郡、番地、建物以下に振り分ける関数
def address_classificaation(address):
	try:
		todoufuken = ''
		juusyo = ''
		banti = ''
		#念のため半角に変換する
		address.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).replace(',','').replace('ー','-')
		
		if re.compile('東京都|北海道|(?:京都|大阪)府|.{2,3}県').search(address):
			todoufuken = re.search('東京都|北海道|(?:京都|大阪)府|.{2,3}県' , address).group()
			address = address.replace(todoufuken,'')
		# print(todoufuken)
		for i in range(0,len(address)):
			if address[i] in ['1','１','2','２','3','３','4','４','5','５','6','６','7','７','8','８','9','９','0','０']:
				break
			else:
				juusyo += address[i]
		# print(juusyo)

		address_2 = juusyo.replace(todoufuken,'')
		# print(address_2)
		shikugun = ''
    
		if re.compile('市川市|野々市市|四日市市|廿日市市|今市市|八日市場市|八日市市').search(address_2):
			shikugun = re.search('(市川市|野々市市|四日市市|廿日市市|今市市|八日市場市|八日市市)',address_2).group()
			# print(shikugun)

		elif '区' in address_2:
			for i in range(0,len(address_2)):
				if address_2[i] in '区':
					shikugun += '区'
					break
				else:
					shikugun += address_2[i]
		elif '市' in address_2:
			for i in range(0,len(address_2)):
				if address_2[i] in '市':
					shikugun += '市'
					break
				else:
					shikugun += address_2[i]
		elif '郡' in address_2:
			for i in range(0,len(address_2)):
				if address_2[i] in '郡':
					shikugun += '郡'
					break
				else:
					shikugun += address_2[i]

		address_3 = address_2.replace(shikugun,'')
		# print(juusyo)
		address = address.replace(juusyo,'')
		
		# print(address)
		for i in range(0,len(address)):
			if not address[i] in ['1','１','2','２','3','３','4','４','5','５','6','６','7','７','8','８','9','９','0','０','丁','目','−','-','ー','号','番','地','F','Ｆ']:
				if banti[-1]=='-' or banti[-1]=='ー':
					banti+=address[i]
				break
			else:
				banti += address[i]
		address = address.replace(banti,'')

		address_banti = address_3 + banti.replace('ー','-')
		tatemono = address.strip().replace('-','ー')

		return todoufuken.strip(), shikugun.strip(), address_banti.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).strip(), tatemono.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).strip()
	except UnicodeDecodeError:
		todoufuken = address
		shikugun = ''
		address_banti = ''
		tatemono = ''
		print('address_classificaation error')
		return todoufuken.strip(), shikugun.strip(), address_banti.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).strip(), tatemono.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).strip()

def address_clean(address):
    if re.compile('〒\d{7}|\d{7}|〒\d{3}-\d{4}|〒\d{3}ー\d{4}|^\d{3}-\d{4}').search(address):
            address = address.replace(re.search('〒\d{7}|\d{7}|〒\d{3}-\d{4}|〒\d{3}ー\d{4}|^\d{3}-\d{4}',address).group(),'')
    if re.compile('東京都|北海道|(?:京都|大阪)府|.{2,3}県').search(address):
        ad1,ad2,ad3,ad4 = address_classificaation(address)
        stutas = 'success'
    else:
        ad1,ad2,ad3,ad4 = address_classificaation(address)
        stutas = '都道府県抜け'
    return stutas,ad1,ad2,ad3,ad4

# 文字列を半角に変換し余分な（）の文章等を削除する
def clean(str):
    str = str.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    str = str.replace('\n','').replace('\t','').replace('\r','').replace('販売業者','').encode('cp932',errors='ignore').decode('cp932').replace('\u3000','').replace('（株）','株式会社').replace('㈱','株式会社').replace('㈲','有限会社').replace('(株)','株式会社').replace('（有）','有限会社').replace('(有)','有限会社').replace('法人名','').replace('株式会社 ','株式会社').replace('有限会社 ','有限会社').strip()
    if re.compile('\(.+?\)|（.+?）').search(str):
      str = str.replace(re.search('\(.+?\)|（.+?）',str).group(),'')
    return str.strip()