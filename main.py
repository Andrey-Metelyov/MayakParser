import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url


def get_last_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pagination = soup.find('ul', class_='pagination')
    # print(pagination)
    lis = pagination.find_all('li')
    # print(lis)
    return int(lis[-1].find('a').text)


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
        res.append(Product(name_text, price, link))
    # print(url + ": found " + str(len(res)) + " cards")
    return res


# url = "https://chita.magazinmayak.ru/catalog/komplekti-postelnogo-belya"
# url = "https://chita.magazinmayak.ru/catalog/podushki-i-navolochki"
url = "https://chita.magazinmayak.ru/catalog/postelnie-prinadlegnosti"

last_page = get_last_page(url)
print("found " + str(last_page) + " pages")

products = []

products.extend(get_products(url))

for page in range(2, last_page):
    print('Parsing page: ' + str(page))
    products.extend(get_products(url + "/page=" + str(page) + ";/"))

file_name = 'res.csv';
print('Saving to file: ' + file_name)
file = open(file_name, 'w')

for product in products:
    file.write(
        '"' + product.name + '"' + "," + '"' + product.price + '","https://chita.magazinmayak.ru' + product.url + '"\n')
file.close()
print('Done')
