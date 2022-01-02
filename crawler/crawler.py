# crawler for wikipedia - list of countries
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
# define where to store information
director = f"{os.path.dirname(__file__)}/Content"
csv_file = f"{os.path.dirname(__file__)}/Content/data.csv"
r = re.compile("(([0-9]+[\.|,| ])+[0-9]+)|[0-9]+")


def deleteFiles():
    """
    used to create the path where to store the information taken by crawler

    """
    if os.path.exists(director):
        shutil.rmtree(director)
    if os.path.exists(csv_file):
        os.remove(csv_file)


def makeFiles():
    """
        Used to create the csv file and write the header
    """
    os.mkdir(director)
    header = ['name', 'capital', 'surface', 'neighbors', 'timezone', 'density', 'population', 'languages', 'governance']
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        # write the header
        writer.writerow(header)


def write_in_csv(row):
    """
        Used to write information scrapped in a csv file

        :param row: information to write in csv file
    """
    with open(csv_file, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(row)


def sanitaze_data(content):
    """
        Used for sanitaze content received

        :param content: string to be cleared
        :return: clean data
    """
    clean_content = content.strip()
    clean_content = re.sub(r"\[.+?\]", "", clean_content)
    clean_content = re.sub(r" {2,}", "", clean_content)
    clean_content = re.sub(r"(, )+", ",", clean_content)
    clean_content = re.sub(r",+$|, $", "", clean_content)
    # clean_content = re.sub(r"\[.*$","",clean_content)
    # clean_content = re.sub(r", ,",",",clean_content)
    # clean_content = re.sub(r",$|, $","",clean_content)
    # clean_content = re.sub (r"(,){1,}",", ",clean_content)
    return clean_content


def deal_with_big_numbers(content):
    """
    deal with different format for numbers

    :return: a correct number
    """

    content = re.sub(r"(\.| )", "", content)
    content = re.sub(r"(,)", ".", content)
    return content


def scrap_surface(table, row):
    """
        used for scrapping surface informations

        :param table: html table from website
        :row: list with information already taken
    """
    surface = 0
    surface = table.find(lambda tag: tag.name == "th" and "Geografie" in tag.text).parent.find_next_sibling(
        'tr').find_next_sibling('tr')
    result = r.search(surface.td.text)
    print(surface.td.text)
    if result:
        surface = result.group(0)
        if "." in surface and "," in surface:
            surface = deal_with_big_numbers(surface)
        else:
            surface = re.sub(r"(,| |\.)", "", surface)
    row.append(surface)
    return row


def scrap_neighbours(table, row):
    """ 
        used for scrapping neighbours informations

        :param table: html table from website
        :row: list with information already taken
    """
    store_neighbours = "Unknown"
    neighbors = table.find(lambda tag: tag.name == "th" and "Vecini" in tag.text)
    if neighbors:
        store_neighbours = ""
        neighbors = neighbors.find_next_sibling('td')
        for neighbor in neighbors.find_all('a'):
            store_neighbours += neighbor.text + ", "
            print(neighbor.text)
    print(store_neighbours)
    row.append(sanitaze_data(store_neighbours))
    return row


def sanitaze_timezone(content):
    """ 
        used for sanitaze timezone informations

        :param content: string to be cleared
        :return: clean content
    """
    clean_content = re.sub(r"\[.*$", "", content)
    clean_content = re.sub(r" {2,}", "", clean_content)
    return clean_content


def scrap_timezone(table, row):
    """
        used for scrapping timezone informations

        :param table: html table from website
        :row: list with information already taken
    """
    time_zone = 'Unknown'
    time_zone = table.find(lambda tag: tag.name == "th" and "Fus orar" in tag.text).find_next_sibling('td').text
    # row.append(sanitaze_data(time_zone))
    row.append(sanitaze_timezone(time_zone))
    print(time_zone)
    return row


def scrap_density(table, row):
    """
        used for scrapping density informations

        :param table: html table from website
        :row: list with information already taken
    """
    result_density = 0
    density = table.find(lambda tag: tag.name == "th" and "Densitate" in tag.text)
    if density:
        density = density.find_next_sibling('td')
        text = density.text
        text = re.sub(r"\(.+?\)", "", text)
        result = r.search(text)
        print(result.group(0))
        result_density = result.group(0)
        if "." in result_density and "," in result_density:
            result_density = deal_with_big_numbers(result_density)
        else:
            result_density = re.sub(r"(,| )", ".", result_density)
    row.append(result_density)
    return row


def scrap_population(table, row):
    """
        used for scrapping population informations

        :param table: html table from website
        :row: list with information already taken
    """
    # first, we search for estimation
    population = 0
    estimation = table.find_all(lambda tag: tag.name == "th" and "Estimare" in tag.text)
    if estimation:
        estimation = estimation[-1].find_next_sibling('td')
        result = r.search(estimation.text)
        print(estimation.text)
        population = result.group(0)
        population = re.sub(r"(,| |\.)", "", population)
    else:
        population_search = table.find(lambda tag: tag.name == "th" and "Recensământ" in tag.text)
        if population_search:
            population_search = population_search.find_next_sibling('td')
            result = r.search(population_search.text)
            if result:
                population = result.group(0)
                population = re.sub(r"(,| |\.)", "", population)
    print(population)
    row.append(population)
    return row


def scrap_languages(table, row):
    """
        used for scrapping languages informations

        :param table: html table from website
        :row: list with information already taken
    """
    result_languages = 'Unknown'
    language = table.find(lambda tag: tag.name == "th" and "Limbi oficiale" in tag.text)
    if language:
        language = language.find_next_sibling('td')
        languages = language.find_all('a')
        if languages:
            result_languages = languages[0].text
            for lang in languages[1:]:
                result_languages += ', ' + lang.text
        else:
            result_languages = language.text
    # print("afisez limbile")
    # print(result_languages)
    print(sanitaze_data(str(result_languages)))
    row.append(sanitaze_data(result_languages))
    return row


def scrap_governance(table, row):
    """
        used for scrapping governance informations

        :param table: html table from website
        :row: list with information already taken
    """
    result_governance = 'Unknown'
    governance = table.find(lambda tag: tag.name == "th" and "Sistem politic" in tag.text)
    if governance:
        result_governance = governance.find_next_sibling('td').text
    print(result_governance)
    row.append(sanitaze_data(result_governance))
    return row


def go_spider_scrapping(row, href):
    """
        Function used for crawl a specific url and get data

        :param row: list with information already taken
        :param href: link where to crawl to
    """

    link_crawl = base_URL + href
    # link_crawl = 'https://ro.wikipedia.org/wiki/Albania'
    print(link_crawl)

    page = requests.get(link_crawl)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", {"class": "infocaseta"})
    # 3. surface
    row = scrap_surface(table, row)
    # 4. neighbours
    row = scrap_neighbours(table, row)
    # 5. time zone
    row = scrap_timezone(table, row)
    # 6. density
    row = scrap_density(table, row)
    # 7. population
    row = scrap_population(table, row)
    #  8. Languages
    row = scrap_languages(table, row)
    # 9. governance
    row = scrap_governance(table, row)

    write_in_csv(row)


def crawler():
    """
        main function for crawler to scrap data from website
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mw-content-text')
    table_elements = results.find("table")
    trs = table_elements.find_all("tr")
    for tr in trs[1:]:
        row = []
        tds = tr.find_all("td")
        link = tds[0].find("b").a
        # get the href of the countries to search for further information
        href = link.get('href')
        print('->>>', link.text)
        # 1. get the name of the country
        row.append(link.text)
        # 2. get the capital of the country
        get_capital = "Unknown"
        capital = tds[4].find("i")
        if capital is not None:
            capital = tds[4].find("i").findNext('a')
            print(capital.text)
            get_capital = capital.text

        row.append(get_capital)
        go_spider_scrapping(row, href)


def main():
    """
        Main file to manage the crawler for delete and create new files
    """
    deleteFiles()
    makeFiles()
    crawler()
    # go_spider_scrapping()


if __name__ == "__main__":
    main()
