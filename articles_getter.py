import requests
from lxml import html
import json

def getParagraphs(url):
  page = requests.get(url)
  tree = html.fromstring(page.text)
  link = tree.xpath('//p/text()')
  
  return link
    
    
f = open('c.json')
data = json.load(f)
    
def remove_non_utf8_symbols(input_string):
   

    cleaned_string = ''.join(char for char in input_string if ord(char) < 190)

    return cleaned_string


for i in data["articles"]:
    paragraphslist=getParagraphs(i["url"])
    
    i["paragraphs"]=paragraphslist
    paragraphs = i['paragraphs']
    cleaned_paragraphs = [remove_non_utf8_symbols(p) for p in paragraphs]
    i['paragraphs'] = cleaned_paragraphs
    
with open("samplez.json", "w",encoding="utf-8") as outfile:
    json.dump(data, outfile)