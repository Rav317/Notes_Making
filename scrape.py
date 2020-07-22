from googlesearch import search 
import requests 
from bs4 import BeautifulSoup 
import csv

from urllib.request import urlopen
from bs4 import BeautifulSoup

from summarize import summarize_htmlpage
# specify the url
# url = "https://www.geeksforgeeks.org/data-structures/linked-list/"

# Connect to the website and return the html to the variable ‘page’
def scrapingfn(url):
	try:
		page = urlopen(url)
	except:
		print("Error opening the URL")
		return	

	# parse the html using beautiful soup and store in variable `soup`
	soup = BeautifulSoup(page, 'html.parser')

	# Take out the <div> of name and get its value
	content = soup.find_all('p')



	article = ''
	for i in content:
		article = article + ' ' +  i.text
	print(article)

	# Saving the scraped text
	with open('scraped_text.txt', 'a') as file:
		file.write(article)

# scrapingfn(url)

# filepath = 'words.txt'
def generate_scraped_content(filepath):
	with open(filepath) as fp:
		for line in enumerate(fp):
	       
	       	# query
			query = line[1].split().pop()
			query = "".join(query)
	       
			print("--------")
			
			for link in search(query, tld="co.in", num=1000, start=0, stop=1, pause=5): 
				print(link)
				# print("Scraped content : \n")
				# scrapingfn(link)
				print("Summarization of page : \n")
				summarize_htmlpage(link)
				#scraping part
				# URL = link

				# r = requests.get(URL) 
				# soup = BeautifulSoup(r.content, 'html5lib')

				# main_content = soup.findAll('p')

				# for i in main_content:
				# 	print(i)

if __name__ == "__main__":
	generate_scraped_content("words.txt")
