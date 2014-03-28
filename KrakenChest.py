import urllib2
from BeautifulSoup import BeautifulSoup
__author__ = 'Jordan'



first_page = urllib2.urlopen('http://www.senscritique.com/DIG/collection/wish/films').read()
soup = BeautifulSoup(first_page)
# nb_page = 0
for page in soup.findAll("li",{"class":"eipa-page"}):
    nb_page = page.text
nb_page = int(nb_page[3:])

for i in range(1,nb_page+1):
    print(i)
    page = urllib2.urlopen('http://www.senscritique.com/DIG/collection/wish/films/page-'+str(i)).read()
    soup = BeautifulSoup(page)
    soup.prettify()
    for wish in soup.findAll("li",{"class" : "elco-collection-item"}):
        print("-----NEW FILM----")
        for element_title in wish.findAll("div",{"class" : "elco-collection-content"}):
            exist = False
            for title_original in element_title.findAll('span',{'class':'elco-original-title'}):
                print(title_original.text)
                exist = True
            for title in element_title.findAll('a',{"class": "elco-anchor"}):
                if exist is False :
                    print(title.text)
        print("-----------------\n")
