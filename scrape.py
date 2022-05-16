from bs4 import BeautifulSoup as bs4
import requests
import re
import pprint


p = re.compile('\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})') #matching price string


pages = [
    ['https://www.targetsportsusa.com/handgun-ammo-c-26.aspx','handgun'],
    ['https://www.targetsportsusa.com/rifle-ammo-c-27.aspx', 'rifle'],
    ['https://www.targetsportsusa.com/rimfire-ammo-c-196.aspx', 'rimfire'],
    ['https://www.targetsportsusa.com/shotgun-ammo-c-28.aspx','shotgun'],
    ['https://www.targetsportsusa.com/combination-ammo-c-972.aspx','combination'],
    ]


def scrape_pages():
    data = []
    for idx, page in enumerate(pages):
        soup = bs4(requests.get(page[0]).text, 'html.parser')
        inner_data = []
        for i, item in enumerate(soup.findAll("div", {"class": "product-listing-price"})):
            in_stock = ""
            price = p.findall(item.text.strip())
            in_stock = True if item.find_next_sibling("button").text ==  'Add To Cart' else False
            title = item.find_previous_sibling("h2").text
            if in_stock != 'not in stock': # Filtering only in stock items
                inner_data.append({'title': title, 'price': price, 'in_stock': in_stock})
        if inner_data:
            data.append({page[1]:inner_data})
    pprint.PrettyPrinter(depth = 5).pprint(data[3]['shotgun'])  


scrape_pages()



