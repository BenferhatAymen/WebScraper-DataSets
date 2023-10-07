import requests
from lxml import html
import json
from random import randint
baseUrl = "https://catalog.data.gov/dataset?q=natural+disasters&sort=views_recent+desc&ext_location=&ext_bbox=&ext_prev_extent="
siteUrl = "https://catalog.data.gov"

def pageLinks(page=1):
  page = requests.get(baseUrl+"&page="+str(page))
  tree = html.fromstring(page.text)
  link = tree.xpath('//h3[@class="dataset-heading"]/a/@href')
  name= tree.xpath('//h3[@class="dataset-heading"]/a/text()')
  
  return name,link
test = "https://catalog.data.gov/dataset/fruit-and-vegetable-prices"
def getPageData(url):
  page = requests.get(url)
  tree = html.fromstring(page.text)
  authorImage=tree.xpath('//div[@class="image"]/a/img/@src')
  authorTitle=tree.xpath('//h1[@class="heading"]/text()')
  title = tree.xpath('//h1[@itemprop="name"]/text()')[0].strip()
  description = tree.xpath('//div[@itemprop="description"]/p/text()')[0]
  datasetsLinks = tree.xpath('//a[@itemprop="contentUrl"]/@href')
  dateModified =  tree.xpath('//span[@itemprop="dateModified"]/a/text()')
  fullDataLinks=[]
  for link in datasetsLinks : 
      fullDataLinks.append(siteUrl+link)
  
  datasetsDescription = tree.xpath('//a[@itemprop="contentUrl"]/@title')


  
  return  title , description, fullDataLinks, datasetsDescription,authorImage[0],authorTitle[0].strip(),dateModified
for j in range(1,6):
    print(f"starting page {j} ...")
    PAGE=j
    l= pageLinks(PAGE)[1]
    print("got page")

    dictFull ={"articles":[]}
    dict={}
    for i in l:
        try:
        
            res  = getPageData(siteUrl+i)
            dict["title"]=res[0]
            dict["description"]=res[1]
            dict["dataLinks"]=res[2]
            dict["datasetsDescription"]= res[3]
            dict["authorImage"]= res[4]
            dict["authorTitle"]= res[5]
            dict["dateModified"]=res[6]
            dict["filesNumber"]=len(res[2])

            dictFull["articles"].append(dict)
            
            dict={}
        except Exception as e :
            print(e)
    with open(f"data{str(PAGE)}.json", "w",encoding="utf-8") as outfile:
        json.dump(dictFull, outfile)
    print(f"page {i} done ")

print("all done")