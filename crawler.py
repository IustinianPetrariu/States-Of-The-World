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
#define where to store information 
director = f"{os.path.dirname(__file__)}/Content"


def deleteFiles():
    if os.path.exists(director):
        shutil.rmtree(director)


def makeDirectory():
    os.mkdir(director)


def crawler():
   page = requests.get(URL) 
   soup = BeautifulSoup(page.content, 'html.parser')
   


def main():
    # deleteFiles() 
    # makeDirectory()
    crawler()
    

if __name__ == "__main__":
    main()


















































