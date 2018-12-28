import pandas as pd
from bs4 import BeautifulSoup
import re

# df=pd.read_json('douban.json',orient='record',encoding='utf-8')
# # df1=df[:8]
# # print(df1)
# # i=0
# # for a in df['time']:
# # 	print(a.isdigit())
# # 	print(type(a),a)
# # 	print(df1['index'][i])



def parse_one_page(html):
	soup=BeautifulSoup(html,'lxml')
	for div in soup.find_all(attrs={'class':'item'}):
		douban={}
		douban['index']=div.em.string
		film=""
		film_name=div.div.find_next_sibling().div.a.children
		for f in film_name:
			# print(f.string)
			film+=f.string
		douban['title']=re.sub('\xa0|\n| ','',film)		
		info=re.sub('导演: |主演: |主|/\xa0|\n','|',div.find(class_='bd').p.text).split('|')
		douban['director']=info[2].strip()
		douban['actor']=info[3].strip()
		douban['time']=info[4].strip()
		# # 		# -------------------------------
		# if douban['time'].isdigit()!=True:
		# 	print(div)
		# 	break

		# # # ------------------------------------
		douban['District']=info[5].strip()
		douban['URL']=div.a.get('href')
		douban['IMG']=div.img.get('src')
		douban['score']=div.find(class_='rating_num').string
		douban['quantity']=div.find(property='v:best').find_next().string[:-3]
		# print(info)
		yield douban
with open('test.txt',encoding='utf-8') as f:
	data=f.read()
	results=parse_one_page(data)
	for result in results:
		print(result)