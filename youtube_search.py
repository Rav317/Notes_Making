import urllib.request
from bs4 import BeautifulSoup
import re
from summarize import summarize_caption


def make_para(i):
    f = open(i+".txt", "r")
    f2 = open(i+"_n.txt", "a")
    for line in f:
        line = line.rstrip("\n")+" "
        f2.write(line)


def generate_transcripts_for_youtube(filepath):

	with open(filepath) as fp:
		for line in enumerate(fp):
	       
	       	# query
			query = line[1].split().pop()
			query = "".join(query)
	       
			print("-------->>>>")


			# from youtube_vid_transcript import transcript_youtube_gen

			textToSearch = query
			query = urllib.parse.quote(textToSearch)
			url = "https://www.youtube.com/results?search_query=" + query
			response = urllib.request.urlopen(url)
			html = response.read()
			soup = BeautifulSoup(html, 'html.parser')
			url_list=[]
			for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
			    # print('https://www.youtube.com' + vid['href'])
			    url_list.append('https://www.youtube.com' + vid['href'])
			# print(url_list)

			# for i in url_list:
			# 	transcript_youtube_gen(i)
			for i in url_list:
				try:
					match = re.search(r"youtube\.com/.*v=([^&]*)", i)
					if match:
							result = match.group(1)
					else:
							result = ""
					# print(result)
					from youtube_transcript_api import YouTubeTranscriptApi

					text_dict=YouTubeTranscriptApi.get_transcript(result)

					art=''
					for i in text_dict:
						art+=i['text']

					with open('temphold.txt','w') as file:
						file.write(art)

					# print("My article stuff : ", article)

					make_para('temphold')
					summarize_caption('temphold_n.txt')
					with open('youtube_text.txt', 'a') as file:
							file.write(art)

				except:
					pass

if __name__ == '__main__':
	generate_transcripts_for_youtube("words.txt")



















