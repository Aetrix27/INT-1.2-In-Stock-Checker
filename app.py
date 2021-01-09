import requests
import re
from bs4 import BeautifulSoup as bs
import jinja2
import os
import time

from pprint import PrettyPrinter
from flask import Flask, request, render_template

################################################################################
## SETUP
################################################################################

app = Flask(__name__)

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('data'),
])
app.jinja_loader = my_loader

pp = PrettyPrinter(indent=4)

################################################################################
## ROUTES
################################################################################


def getTitle(filename):
    #HtmlFile = open(filename, 'r', encoding='utf-8')
    #source_code = HtmlFile.read() 

    URL = filename
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = bs(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    fixed_title = title.strip()

    return fixed_title, soup

def getImage(filename):
    title, soup = getTitle(filename)
    image = soup.find('img', attrs={"id": "landingImage"})
    image_source = image['data-old-hires']+'\n'
    #fixed_title = title.strip()

    print(image_source)
    return image_source

def in_stock(filename):
    title, soup = getTitle(filename)
    in_stock = soup.find(id="availability").get_text()

    if 'stock' or 'Available' in in_stock:
        in_stock_string = 'In Stock'
    else:
        in_stock_string = 'Not In Stock'

    print(in_stock_string)

    return in_stock_string

@app.route('/')
def home():
    while(True):
        #filename1 = "amazon.html"
        global fixed_title
        global in_stock_string
        global image_source
        filename1 = "https://www.amazon.com/EVGA-08G-P5-3767-KR-GeForce-Technology-Backplate/dp/B08L8L9TCZ/ref=sr_1_1?dchild=1&keywords=3070&qid=1610223381&s=electronics&sr=1-1"
        fixed_title, soup = getTitle(filename1)
        print(soup.prettify())

        in_stock_string = in_stock(filename1)
        image_source = getImage(filename1)
        time.sleep(60*60)

    context = {
        'img_src' : image_source,
        'title' : fixed_title,
        'in_stock' : in_stock_string

    }

    return render_template('index.html', **context) 

if __name__ == '__main__':
    app.run(debug=True)