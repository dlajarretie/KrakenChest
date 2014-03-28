import urllib2
import json
from BeautifulSoup import BeautifulSoup
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
    file = open(pseudo+'.json','w+')
    for i in range(1,getPages(pseudo)+1):
        page = urllib2.urlopen(url+'/page-'+str(i)).read()
        soup = BeautifulSoup(page)
        soup.prettify()
        for wish in soup.findAll("li",{"class" : "elco-collection-item"}):
            wish_json = '{"wish":'
            for element_title in wish.findAll("div",{"class" : "elco-collection-content"}):
                exist = False
                for title_original in element_title.findAll('span',{'class':'elco-original-title'}):
                    wish_json = wish_json + '{"title":"'+title_original.text.encode('utf-8')+'"}},'
                    file.write(wish_json)
                    exist = True
                for title in element_title.findAll('a',{"class": "elco-anchor"}):
                    if exist is False :
                        wish_json = wish_json + '{"title":"'+title.text.encode('utf-8')+'"}},'
                        file.write(wish_json)
    file.close()



if __name__ == '__main__':
    getWishes("ClaudiaL")