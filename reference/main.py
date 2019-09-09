import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup, Comment

# tables = soup.findAll("table")

r = requests.get('https://www.rbcgam.com/en/ca/products/mutual-funds/?tab=performance&series=f')
# print(r.text)
soup = BeautifulSoup(r.text)
# Remove particular enemies
# replace with `soup.findAll` if you are using BeautifulSoup3
# for div in soup.find_all("div", {'class':'sidebar'}): 
#     div.decompose()

def _remove_attrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = None
        for attribute in ["class", "id", "name", "style"]:
            del tag[attribute]
    return soup

for tag in soup():
    for attribute in ["class", "id", "name", "style"]:
        del tag[attribute]
clean_soup = _remove_attrs(soup)
[s.extract() for s in soup('script')]
[s.extract() for s in soup('style')]
for script in soup(["script", "style", "img"]): # remove all javascript and stylesheet code
    script.extract()

for tag in soup: 
    tag.attrs = {}

for tag in soup:
    for attribute in ["class", "data-aria"]: # You can also add id,style,etc in the list
        del tag[attribute]
        del tag['class']

for child in soup:
    if isinstance(child, Comment):
        child.extract()

tables = clean_soup.findAll("table")
# print(soup)
for table in tables:
     if table.findParent("table") is None:
         print(str(table.encode('utf-8')))