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

filename = "amazon.html"
HtmlFile = open(filename, 'r', encoding='utf-8')
source_code = HtmlFile.read() 
soup = bs(source_code, 'html.parser')

#while(True):
    #URL = filename
    #headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    #page = requests.get(URL, headers=headers)
in_stock_string = ''

title = soup.find(id="productTitle").get_text()
in_stock = title = soup.find(id="availability").get_text()

if 'stock' or 'Available' in in_stock:
    in_stock_string = 'In Stock'
else:
    in_stock_string = 'Not In Stock'

print(in_stock_string)

image = soup.find('img', attrs={"id": "landingImage"})
image_source = image['data-old-hires']+'\n'
fixed_title = title.strip()

    #time.sleep(60*60*24)

print(title.strip())
print(image['data-old-hires']+'\n')


app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('data'),
])
app.jinja_loader = my_loader

pp = PrettyPrinter(indent=4)

################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    context = {
        'img_src' : image_source,
        'title' : fixed_title,
        'in_stock' : in_stock_string

    }

    return render_template('index.html', **context) 

if __name__ == '__main__':
    app.run(debug=True)