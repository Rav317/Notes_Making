from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

html_page = urlopen("https://www.geeksforgeeks.org/data-structures/")
# soup = BeautifulSoup(html_page)
soup = BeautifulSoup(html_page, 'html.parser')
for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    print(link.get('href'))