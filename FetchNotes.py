from googlesearch import search 
import requests 
from bs4 import BeautifulSoup 
import csv
from scraping import scrapingfn


filepath = 'words.txt'
with open(filepath) as fp:
	for line in enumerate(fp):
       
       	# query
		query = line[1].split().pop()
		query = "".join(query)
       
		print("dd")
		
		for link in search(query, tld="co.in", num=1000, start=0, stop=3, pause=5): 
			
			print(link)
			scrapingfn(link)

			#scraping part
			# URL = link

			# r = requests.get(URL) 
			# soup = BeautifulSoup(r.content, 'html5lib')

			# main_content = soup.findAll('p')

			# for i in main_content:
			# 	print(i)