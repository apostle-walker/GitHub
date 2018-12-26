import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import json

baseurl='https://movie.douban.com/top250?'

def get_one_page(start):
	params={
	'start':start,
	'filter':''
	}
	headers={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
	}
	url=baseurl+urlencode(params)
	try:
		response=requests.get(url,headers=headers)
		if response.status_code==200:
			return response.text
	except response.ConnectionError as e:
		print('Error:',e.args)

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
		douban['District']=info[5].strip()
		douban['URL']=div.a.get('href')
		douban['IMG']=div.img.get('src')
		douban['score']=div.find(class_='rating_num').string
		douban['quantity']=div.find(property='v:best').find_next().string[:-3]
		# print(info)
		yield douban
	

def main():
	with open('douban.json','w+',encoding='utf-8') as f:
		for i in range(10):
			start=i*25
			html=get_one_page(start)
			results=parse_one_page(html)
			for result in results:
				# print(json.dumps(result,indent=2,ensure_ascii=False))
				f.write(json.dumps(result,indent=2,ensure_ascii=False))
			# break


if __name__=='__main__':
	main()