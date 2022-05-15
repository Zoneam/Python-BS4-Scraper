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
        inner_data = {}
        for i, item in enumerate(soup.findAll("div", {"class": "product-listing-price"})):
            buy_button = ""
            price = p.findall(item.text.strip())
            buy_button = item.find_next_sibling("button").text
            if buy_button != 'Notify': # Filtering only in stock items
                title = item.find_previous_sibling("h2").text
                inner_data[page[1] + 'ammo' + '_' + str(i)] = ({'title': title, 'price': price, 'in_stock': buy_button})
        if inner_data:
            data.append(inner_data)
    pprint.PrettyPrinter(depth = 5).pprint(data)  


scrape_pages()



