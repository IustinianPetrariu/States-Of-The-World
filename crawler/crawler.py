### crawler for wikipedia - list of countries 
import os
import shutil
import requests
import sys
import csv 
import re
from bs4 import BeautifulSoup 

# main URL -states of the world 
URL = 'https://ro.wikipedia.org/wiki/Lista_statelor_lumii'
base_URL = 'https://ro.wikipedia.org'
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
    header = ['name', 'capital', 'surface', 'neighbors','timezone','density','population','languages','governance']
    with open(csv_file, 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f,delimiter = '|')
        # write the header
        writer.writerow(header)


def write_in_csv(row):
    with open(csv_file, 'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f,delimiter = '|')
        writer.writerow(row)

def sanitaze_data(content):
  clean_content = content.strip()
  clean_content = re.sub(r"\[.+?\]","",clean_content)
  clean_content = re.sub (r"(,){1,}",", ",clean_content)
  return clean_content

def deal_with_big_numbers(content):
    if  "." in content and "," in content :
       print("here1")
       content = re.sub(r"(\.| )","", content)
       content = re.sub(r"(,)",".", content)
       return content
    else:
       return content

def go_spider_scrapping(row, href):
  
    link_crawl = base_URL + href
    # link_crawl = 'https://ro.wikipedia.org/wiki/Albania'
    print(link_crawl)
    r = re.compile("(([0-9]+[\.|,| ])+[0-9]+)|[0-9]+")
    page = requests.get(link_crawl)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table",{"class":"infocaseta"})

    # 3. surface 
    surface = 0
    surface = table.find(lambda tag:tag.name=="th" and "Geografie" in tag.text).parent.find_next_sibling('tr').find_next_sibling('tr')
    result = r.search(surface.td.text) 
    print(surface.td.text)
    if result:
        surface = result.group(0)
        surface = re.sub(r"(,| |\.)", "", surface)
    row.append(surface)
    print(surface)

    # 4. neighbours 
    store_neighbours = "Unknown"
    neighbors = table.find(lambda tag:tag.name=="th" and "Vecini" in tag.text)
    if neighbors:
        store_neighbours = ""
        neighbors = neighbors.find_next_sibling('td')
        for neighbor in neighbors.find_all('a'):
            store_neighbours += neighbor.text + " "
            print(neighbor.text)
    row.append(sanitaze_data(store_neighbours))

    # 5. time zone
    time_zone = 'Unknown'
    time_zone = table.find(lambda tag:tag.name=="th" and "Fus orar" in tag.text).find_next_sibling('td').text
    row.append(sanitaze_data(time_zone))
    print(time_zone)

 # 6. density 
    result_density = 0
    density = table.find(lambda tag:tag.name=="th" and "Densitate" in tag.text)
    if density: 
      density = density.find_next_sibling('td')
      text = density.text 
      text = re.sub(r"\(.+?\)","",text) 
      result = r.search(text) 
      print(result.group(0))
      result_density = result.group(0)
      result_density = deal_with_big_numbers(result_density)
      result_density = re.sub(r"(,| )", ".", result_density)
    row.append(result_density)

    # 7. population
    #first, we search for estimation
    population = 0
    estimation = table.find_all(lambda tag:tag.name=="th" and "Estimare" in tag.text)
    if estimation:
      estimation = estimation[-1].find_next_sibling('td')
      result = r.search(estimation.text)
      print(estimation.text)
      population = result.group(0) 
      population = re.sub(r"(,| |\.)", "", population)
    else:
      population_search = table.find(lambda tag:tag.name=="th" and "Recensământ" in tag.text)
      if population_search:
        population_search = population_search.find_next_sibling('td')
        result = r.search(population_search.text)
        if result:
           population = result.group(0)
           population = re.sub(r"(,| |\.)", "", population)
    print(population)
    row.append(population)

     #  8. Languages 
    result_languages = 'Unknown'
    language = table.find(lambda tag:tag.name=="th" and "Limbi oficiale" in tag.text)
    if language:
      language = language.find_next_sibling('td')
      languages = language.find_all('a') 
      if languages:
        result_languages = languages[0].text
        for lang in languages[1:]:
         result_languages += ', ' + lang.text
      else:
        result_languages = language.text
        
    print(result_languages)
    row.append(result_languages)

    # 9. governance
    result_governance = 'Unknown'
    governance = table.find(lambda tag:tag.name=="th" and "Sistem politic" in tag.text)
    if governance:
      result_governance = governance.find_next_sibling('td').text
    print(result_governance)
    row.append(result_governance)

    write_in_csv(row)


def crawler():
  page = requests.get(URL)  
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find(id ='mw-content-text')
  table_elements = results.find("table") 
  trs = table_elements.find_all("tr") 
  for tr in trs[1:]:
      row = []
      tds = tr.find_all("td")
      link = tds[0].find("b").a
      # get the href of the countries to search for further information
      href = link.get('href')
      print('->>>',link.text)
      # 1. get the name of the country
      row.append(link.text)
      # 2. get the capital of the country
      get_capital = "Unknown"
      capital = tds[4].find("i")
      if capital != None:
          capital = tds[4].find("i").findNext('a')
          print(capital.text)
          get_capital = capital.text

      row.append(get_capital)
      go_spider_scrapping(row,href)


def main():
    deleteFiles() 
    makeFiles()
    crawler()
    # go_spider_scrapping()
    

if __name__ == "__main__":
    main()














































