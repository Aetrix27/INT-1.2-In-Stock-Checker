from requests_html import HTMLSession
import jinja2
import os
import time

from pprint import PrettyPrinter
from flask import Flask, request, render_template

graphicsCardUrls = ['https://www.amazon.com/EVGA-08G-P5-3767-KR-GeForce-Technology-Backplate/dp/B08L8L9TCZ/ref=sr_1_1?dchild=1&keywords=3070&qid=1610223381&s=electronics&sr=1-1',
                    'https://www.amazon.com/MSI-GeForce-Tri-Frozr-Architecture-Graphics/dp/B08HR7SV3M/ref=sr_1_3?crid=1Y1DLX8V0GXII&dchild=1&keywords=3080&qid=1610406031&s=electronics&sprefix=3080%2Celectronics%2C280&sr=1-3']

urlPs5 = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp'

def getItemInfo(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render()

    product = {
        'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
        'availability' : r.html.xpath('//*[@id="availability"]', first=True).text,
    }

    about = r.html.find('#landingImage')[0]
    img = about.xpath('//img')[0]
    product['image'] = img.attrs['src']
        
    if 'Currently unavailable' in product['availability']:
        product['stock'] = 'Out of Stock'
      
    else:
        product['stock'] = 'In Stock'
     

    #   'price': 'item unavailable',

    return product

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

def addDictValues(context, product, loopNum):
    productImage = 'img' + str(loopNum+1) 
    productTitle = 'title' + str(loopNum+1)
    productStock = 'stock' + str(loopNum+1)

    context[productImage] = product['image']
    context[productTitle] = product['title']
    context[productStock] = product['stock']

    return context

productArr = [getItemInfo(graphicsCardUrls[0]), getItemInfo(graphicsCardUrls[1])]
product3 = getItemInfo(urlPs5)

@app.route('/')
def home():
    context = {

    }

    for url in range(len(graphicsCardUrls)):
        newContext = addDictValues(context, productArr[url], url)
        context.update(newContext)

    context['imgSrcPs5'] = product3['image']
    context['titlePs5'] = product3['title']
    context['inStockPs5'] = product3['stock']
    print(context)

    return render_template('index.html', **context) 

if __name__ == '__main__':
    app.run(debug=True)