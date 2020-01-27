#!/usr/bin/python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

# if has Chinese, apply decode()
html = urlopen("http://app.wuli.wiki/posts").read().decode('utf-8')
soup = bs(html, "html.parser")                #make BeautifulSoup
prettyHTML = soup.prettify()   #prettify the html

text_file = open("followers.html", "w")
text_file.write(prettyHTML)
text_file.close()
