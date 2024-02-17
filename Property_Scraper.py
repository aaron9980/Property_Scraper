from bs4 import BeautifulSoup
import requests


def num_pages(soup):# get the max number of pages for a location and range
    butt_list = [
    ]
    for i in range(0, len(soup)):
        try:
            if "page" in soup[i]["aria-label"]:
                # print(buttons[i].text)
                # print(i)
                if "..." in soup[i].text:

                    butt_list.append(soup[i].text.replace("...", ""))
                else:

                    butt_list.append(soup[i].text)
        except:
            pass

    pages = int(max(butt_list))
    return pages

def get_ids(soup):# get all the property ids in the location and range
    list_id=[]
    for item in soup:
        try:
            if  item["href"].startswith("/buy/"):
                #print(item["href"].removeprefix("/buy/"))
                list_id.append(int(item["href"].removeprefix("/buy/")))
        except:
            pass
    return list_id


def getArea(soup):#get all the living area of the properties
    area = []
    for item in soup:
        try:
            if item["title"]:
                area.append(int(item.text.replace("m²", "")))
        except:
            pass
    return area


def getPrice(soup):#get all the prices of the properties
    price = []
    for item in soup:

        try:

            if "CHF" in item.text:
                price.append(int(item.text[5:-3].replace(",", "")))
        except:
            pass
    return price


def cityScraper(city, rangee):#main function that scrapes property ids,price and living area for city and range given
    ids = []
    area = []
    price = []
    url = "https://www.immoscout24.ch/en/house/buy/city-" + city + "/?r=" + str(rangee) + "&map=1"
    x = requests.get(url)

    soup = BeautifulSoup(x.text, 'html.parser')
    page = soup.findAll('a')
    pages = num_pages(page)
    for i in range(pages):
        x = requests.get(url)
        soup = BeautifulSoup(x.text, 'html.parser')
        buttons = soup.findAll('a')
        ids = ids + get_ids(buttons)
        areas = soup.findAll('strong')
        area += getArea(areas)
        prices = soup.findAll('span')

        price += getPrice(prices)
        url = "https://www.immoscout24.ch/en/house/buy/city-" + city + "/?pn=" + str(i) + "&r=" + str(
            rangee) + "&map=true"
    return ids, area, price

