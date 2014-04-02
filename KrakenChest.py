import urllib2
import json
from BeautifulSoup import BeautifulSoup
import sys
__author__ = 'Jordan'

url = 'http://www.senscritique.com/'
file

def getPages(pseudo):
    global url
    global file
    url = url+pseudo+'/collection/wish/films'
    file = open(pseudo+'.json','w+')
    file.close()
    first_page = urllib2.urlopen(url+pseudo+'/collection/wish/films').read()
    soup = BeautifulSoup(first_page)
    for page in soup.findAll("li",{"class":"eipa-page"}):
        nb_page = page.text
    nb_page = int(nb_page[3:])
    return nb_page

def getWishes(pseudo):
    file = open(pseudo+'.html','w+')
    file.write('<html><body>')
    for i in range(1,getPages(pseudo)+1):
        page = urllib2.urlopen(url+'/page-'+str(i)).read()
        soup = BeautifulSoup(page)
        soup.prettify()
        for wish in soup.findAll("li",{"class" : "elco-collection-item"}):
            wish_json = '<li>'
            for element_title in wish.findAll("div",{"class" : "elco-collection-content"}):
                exist = False
                for title_original in element_title.findAll('span',{'class':'elco-original-title'}):
                    link = getLink(title_original.text.encode('utf-8'))
                    wish_json = wish_json + '<a href="' + str(link) + '">' + title_original.text.encode('utf-8') + '</a></li>'
                    file.write(wish_json)
                    exist = True
                for title in element_title.findAll('a',{"class": "elco-anchor"}):
                    if exist is False:
                        link = getLink(title.text.encode('utf-8'))
                        wish_json = wish_json + '<a href="' + str(link) + '">' + title.text.encode('utf-8') + '</a></li>'
                        file.write(wish_json)
    file.write('</body></html>')
    file.close()

def getLink(title):
    print(title)
    title = title.replace(" ", "%20")
    url = 'http://www.thepiratebay.se/search/'+title+'/0/7/0'
    print(url)
    try:
        searched_page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(searched_page)
        soup.prettify()
        index = 0
        for tr in soup.findAll('div',{"id" : "main-content"}):
            if index == 0:
                for td in tr.findAll("td"):
                    for a in td.findAll("a"):
                        if "magnet" in a["href"]:
                            return a["href"]
            index += 1
    except urllib2.HTTPError:
        return ""

if __name__ == '__main__':
    getWishes(sys.argv[1])