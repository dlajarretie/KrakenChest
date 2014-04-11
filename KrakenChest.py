import urllib2
import json
from BeautifulSoup import BeautifulSoup
import sys
__author__ = 'Jordan'

url = 'http://www.senscritique.com/'
file

# Use this opener to avoid following redirections and getting a false 200

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

opener = urllib2.build_opener(NoRedirectHandler())

def getPages(pseudo):
    global url
    global file
    url = url+pseudo+'/collection/wish/films'
    file = open(pseudo+'.json','w+')
    file.close()
    response = opener.open(url+pseudo+'/collection/wish/films')
    if 300 <= response.getcode() < 400:
        print "Oops, this user does not exit :("
        return 0
    elif response.getcode() >= 400:
        print "An http error occured :("
        return 0
    first_page = response.read()
    soup = BeautifulSoup(first_page)
    for page in soup.findAll("li",{"class":"eipa-page"}):
        nb_page = page.text
    try:
        nb_page
    except NameError:
        return 1

    return int(nb_page)

def getWishes(pseudo):
    lines = []
    pages = getPages(pseudo)
    if pages == 0:
        return
    for i in range(1,pages+1):
        page = urllib2.urlopen(url+'/page-'+str(i)).read()
        soup = BeautifulSoup(page)
        soup.prettify()
        for empty in soup.findAll("li",{"class" : "elco-collection-item-empty d-emptyMessage"}):
            print "Aborting : there isn't a single movie in your wishlist yet :("
            return
        for wish in soup.findAll("li",{"class" : "elco-collection-item"}):
            wish_json = '<li>'
            for element_title in wish.findAll("div",{"class" : "elco-collection-content"}):
                exist = False
                for title_original in element_title.findAll('span',{'class':'elco-original-title'}):
                    link = getLink(title_original.text.encode('utf-8'))
                    wish_json = wish_json + '<a href="' + str(link) + '">' + title_original.text.encode('utf-8') + '</a></li>'
                    lines.append(wish_json)
                    exist = True
                for title in element_title.findAll('a',{"class": "elco-anchor"}):
                    if exist is False:
                        link = getLink(title.text.encode('utf-8'))
                        wish_json = wish_json + '<a href="' + str(link) + '">' + title.text.encode('utf-8') + '</a></li>'
                        lines.append(wish_json)

    file = open(pseudo+'.html','w+')
    file.write('<html><body>')
    for line in lines:
        file.write(line)
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