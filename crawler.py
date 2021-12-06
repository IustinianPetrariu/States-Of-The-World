### crawler for wikipedia - list of countries 
import os
import shutil
import requests
import sys
import csv 
from bs4 import BeautifulSoup 

# main URL -states of the world 
URL = 'https://ro.wikipedia.org/wiki/Lista_statelor_lumii'
base_URL = 'https://ro.wikipedia.org/wiki'
URLS = []
file_ = ""
#define where to store information 
director = f"{os.path.dirname(__file__)}/Content"
csv_file = f"{os.path.dirname(__file__)}/Content/data.csv"


def deleteFiles():
    if os.path.exists(director):
        shutil.rmtree(director)
    if os.path.exists(csv_file):
        os.remove(csv_file)


def makeFiles():
    os.mkdir(director)
    header = ['Name', 'Capital', 'Population', 'Language']
    with open(csv_file, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)


def spider():
    pass


def crawler():
   page = requests.get(URL) 
   soup = BeautifulSoup(page.content, 'html.parser')
   results = soup.find(id ='mw-content-text')
   table_elements = results.find("table") 
   trs = table_elements.find_all("tr") 
   for tr in trs[1:]:
       row = []
       tds = tr.find_all("td")
       link = tds[0].find("a")
       # get the href of the countries to search for further information
       href = link.get('href')
       # get the name of the country
       row.append(link.text)
       # get the capital of the country
       capital = "None"
       capital = tds[4].find("i")
       if capital != None:
           capital = tds[4].find("i").findNext('a')
           print(capital.text)
       row.append(capital)


def main():
    deleteFiles() 
    makeFiles()
    crawler()
    

if __name__ == "__main__":
    main()


















































