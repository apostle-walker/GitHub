import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import json

baseurl='https://movie.douban.com/top250?'

def get_page_url(start):
	params={
	'start':start,
	'filter':''
	}
	return baseurl+urlencode(params)

def get_one_page(url):	
	headers={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
	}

	try:
		response=requests.get(url,headers=headers)
		if response.status_code==200:
			return response.text
	except response.ConnectionError as e:
		print('Error:',e.args)

def get_one_page_urls(url_list,html):
	soup=BeautifulSoup(html,'lxml')
	for div in soup.find_all(attrs={'class':'item'}):
		url_list.append(div.a.get('href'))
	return url_list

def parse_one_page(html_2nd):
	soup=BeautifulSoup(html_2nd,'lxml')
	# print(soup)
	d=soup.find(attrs={'type':"application/ld+json"}).string
	# print(d)
	d=json.loads(d,encoding='utf-8',strict=False) # 忽视字符串的控制或者提前替换掉回车符、换行符
	print(soup.find( class_="top250-no").string)
	douban={}
	douban['index']=soup.find( class_="top250-no").string[3:]
	douban['name']=d['name']
	douban['director']=[item['name'] for item in d['director']][0]
	douban['author']='/'.join([item['name'] for item in d['author']])
	douban['actor']='/'.join([item['name'] for item in d['actor']])
	douban['datePublished']=d['datePublished']
	douban['description']=d['description']
	douban['duration']=d['duration']
	douban['genre']=d['genre']
	douban['District']=re.search('制片国家/地区:</span> (.+?)<br/>',str(soup))[1]
	douban['URL']=d['url']
	douban['IMG']=d['image']
	douban['ratingValue']=d["aggregateRating"]['ratingValue']
	douban['ratingCount']=d["aggregateRating"]['ratingCount']
	yield douban 

def main():
	with open('douban.json','w+',encoding='utf-8') as f:
		f.write('['+'\n')
		d={}
		url_list=[]
		for i in range(10):
			start=i*25
			url=get_page_url(start)
			html=get_one_page(url)
			url_list=get_one_page_urls(url_list,html)
		for url_2nd in url_list:
			html_2nd=get_one_page(url_2nd)
			print(type(html_2nd))
			results=parse_one_page(html_2nd)
			print(requests)
			#以下部分作用-------
			#保存json为list，判断末尾，适时写入分隔符
			while True:
				print('--')
				if not d:
					d=next(results)
					print('---')
					continue
				else:
					f.write(json.dumps(d,indent=2,ensure_ascii=False))
					try:
						d=next(results)
						f.write(','+'\n')
					except StopIteration as e:
						if i<9:
							f.write(','+'\n')
						else:
							f.write('\n')
						break
		f.write(']')


if __name__=='__main__':
	main()
