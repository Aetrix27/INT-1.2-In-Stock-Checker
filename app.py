from requests_html import HTMLSession
import pandas as pd

url = 'https://www.amazon.com/EVGA-08G-P5-3767-KR-GeForce-Technology-Backplate/dp/B08L8L9TCZ/ref=sr_1_1?dchild=1&keywords=3070&qid=1610223381&s=electronics&sr=1-1'

def getItemInfo(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)

    product = {
        'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
        'availability' : r.html.xpath('//*[@id="availability"]', first=True).text,
    }

    if 'stock' or 'Available' in product['availability']:
        print("In Stock")
        product['stock'] = 'In Stock'
    else:
        print("Out of Stock")
        product['stock'] = 'Out of Stock'

    #   'price': 'item unavailable',

    print(product)
    print(product['stock'])


    return product

getItemInfo(url)
