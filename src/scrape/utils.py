import json
import requests
from bs4 import BeautifulSoup


# articul_example = '71875051'

BASE_URL_DATA = 'https://www.wildberries.ru/catalog/{}/detail.aspx'
BASE_URL_SELLER = 'https://wbx-content-v2.wbstatic.net/sellers/{}.json'


def price_to_int(price: str):
    clean_price = price.strip().rstrip('₽')
    arr = clean_price.split()
    price_str = ''.join(arr)
    return int(price_str)


def get_supplier(articul: str):
    text = requests.get(BASE_URL_SELLER.format(articul)).text
    json_data = json.loads(text)
    return json_data['supplierName']


def get_all_good_info(articul: str):
    articul_clean = articul.strip()
    src = requests.get(BASE_URL_DATA.format(articul_clean)).text
    soup = BeautifulSoup(src, 'lxml')

    header = soup.find('h1', class_='same-part-kt__header')
    prices = soup.find('p', class_='price-block__price-wrap')

    if not header or not prices:
        return {}

    spans = [span.text for span in header.find_all('span')]
    brand = spans[0]
    goods_name = spans[1]

    price_with_discount = prices.find('span', class_='price-block__final-price').text
    price_without_discount = prices.find('del').text
    price_with_discount = price_to_int(price_with_discount)
    price_without_discount = price_to_int(price_without_discount)

    supplier = get_supplier(articul_clean)

    return {
        'articul': int(articul_clean),
        'goods_name': goods_name,
        'price_without_discount': price_without_discount,
        'price_with_discount': price_with_discount,
        'brand': brand,
        'supplier': supplier
    }


# TESTING ZONE

# info = get_all_good_info(articul_example)

