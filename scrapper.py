#author: Nicolas Padula - @nvpadula
 
from lxml import html
from lxml.builder import E
import requests
 
def getWebPage(url):
   page = requests.get(url)
   return html.fromstring(page.text) #Generates HtmlElement (subclass of etree.Element)
   #for a given url
 
def serializeList(aList,fileName):
   file=open(fileName,'w+')
   for var in aList:
   file.write(var)
archive = 'http://scriptogr.am/elhumoestaenelfoco/archive' #URL of the desired scriptogr.am blog archive
 
print("Accessing archive...")
pageTree = getWebPage(archive) #obtains archive's tree
#obtains article titles and links
print("Parsing article titles...")
articleTitles = pageTree.xpath('//span[@class="archive-link"]/a/text()')
print("Parsing article links...")
articleLinks = pageTree.xpath('//span[@class="archive-link"]/a/@href')
print("Creating index...")#If you want to find a given article you just ctrl+f in the titles file
serializeList(articleTitles,'titulos.txt')
 
 
count = 0
#iterates through links and gets each post's contents
for article,articleURL in zip(articleTitles,articleLinks):
   print("Scrapping", article.encode('utf-8', 'ignore')) #real sanitizing takes too long
   outputFile = open(article.replace("/","-").replace("¿","").replace("?","") +'.html','w+')
   articleTree = getWebPage(articleURL) #generates tree for each article
   content = articleTree.xpath('//div[@class="articlepost"]',smart_strings=False) #Selects the whole article
   outputPage = E.html(E.head(E.title(article)),E.body(content[0])) #generates html doc to be persisted
   pageStr = html.tostring(outputPage, method="html", pretty_print=False)
   outputFile.write(pageStr.decode('utf-8'))
   outputFile.close()
   count+=1
 
print(count, "articles have been scrapped")
