import requests
from bs4 import BeautifulSoup


def get_products(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all('div', class_='card-product')
    res = []

    for card in cards:
        product = card.find("div", "card-product__body")
        name = product.find("a")
        name_text = name.text
        link = name.get('href')
        price = str(product.find("div", "card-product__price").find("div").text)
        price = price.replace(" ", "")
        # print(name, price)
        res.append((name_text, price, link))
    return res


url = "https://chita.magazinmayak.ru/catalog/komplekti-postelnogo-belya"

products = []

products.extend(get_products(url))

for page in range(2, 18):
    products.extend(get_products(url + "/page=" + str(page) + ";/"))

for product in products:
    print('"' + product[0] + '"' + "," + product[1] + ",https://chita.magazinmayak.ru/" + product[2])
