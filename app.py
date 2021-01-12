from requests_html import HTMLSession
import jinja2
import os
import time

from pprint import PrettyPrinter
from flask import Flask, request, render_template, send_file

graphicsCardUrls = ['https://www.amazon.com/EVGA-08G-P5-3767-KR-GeForce-Technology-Backplate/dp/B08L8L9TCZ/ref=sr_1_1?dchild=1&keywords=3070&qid=1610223381&s=electronics&sr=1-1',
                    'https://www.amazon.com/MSI-GeForce-Tri-Frozr-Architecture-Graphics/dp/B08HR7SV3M/ref=sr_1_3?crid=1Y1DLX8V0GXII&dchild=1&keywords=3080&qid=1610406031&s=electronics&sprefix=3080%2Celectronics%2C280&sr=1-3',
                    'https://www.amazon.com/MSI-GeForce-Architecture-Overclocked-Graphics/dp/B08CLV8CKP/ref=sr_1_1?dchild=1&keywords=2080&qid=1610047787&s=electronics&sr=1-1',
                    'https://www.amazon.com/MSI-RTX-2070-Super-Architecture/dp/B0856BVRFL/ref=pd_di_sccai_3/140-1216297-8899404?_encoding=UTF8&pd_rd_i=B0856BVRFL&pd_rd_r=b3eb018f-0a42-48fb-8cb6-ca8ed796a4fc&pd_rd_w=YQ1vP&pd_rd_wg=epyd0&pf_rd_p=c9443270-b914-4430-a90b-72e3e7e784e0&pf_rd_r=QYD5HM1P1RN7W9K1RNZV&psc=1&refRID=QYD5HM1P1RN7W9K1RNZV']

urlPs5 = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp'
urlXboxSX = 'https://www.amazon.com/Xbox-X/dp/B08H75RTZ8/ref=sr_1_13?dchild=1&keywords=xbox+series+x&qid=1610417662&sr=8-13'

def getItemInfo(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)

    product = {
        'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
        'availability' : r.html.xpath('//*[@id="availability"]', first=True).text,
    }

    about = r.html.find('#landingImage')[0]
    img = about.xpath('//img')[0]
    product['image'] = img.attrs['src']
        
    if 'Currently unavailable' in product['availability']:
        product['stock'] = 'Out of Stock'
    elif 'sellers' in product['availability']:
        product['stock'] = 'In Stock (By Limited Sellers)'
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

def addDictValues(context, product, loopNum, itemInfo, name):
    productImage = 'img' + str(loopNum+1) 
    productTitle = 'title' + str(loopNum+1)
    productStock = 'stock' + str(loopNum+1)

    context['imgName'] = productImage
    context['titleName'] = productTitle
    context['stock'] = productStock

    context[name]['imgArr'].append(product['image'])
    context[name]['titleArr'].append(product['title'])
    context[name]['stockArr'].append(product['stock'])
    print(context[name]['stockArr'])

    context[productImage] = product['image']
    context[productTitle] = product['title']
    context[productStock] = product['stock']

    return context, itemInfo

productArr = [getItemInfo(graphicsCardUrls[0]), getItemInfo(graphicsCardUrls[1]), getItemInfo(graphicsCardUrls[2]), getItemInfo(graphicsCardUrls[3])]
product3 = getItemInfo(urlPs5)
xboxSX = getItemInfo(urlXboxSX)

@app.route('/')
def home():
    context = {

    }

    return render_template('index.html', **context) 


@app.route('/itemData')
def itemData():
    ps5Chosen = False
    xboxSXChosen = False
    graphicsCardsChosen = False
    allChosen = False
    imgArr = []
    titleArr = []
    stockArr = []
    totalImgArr = []
    totalTitleArr = []
    totalStockArr = []

    select = request.args.get('choice')
    print(select)

    if select == "Graphics":
        graphicsCardsChosen = True

    elif select == "XboxSX":
        xboxSXChosen = True

    elif select == "Ps5":
        ps5Chosen = True
    
    elif select == "All":
        allChosen = True

    name = 'graphicsCardInfo'
    graphicsCardInfo = {
        'name' : name,
        'imgArr' : imgArr,
        'titleArr' : titleArr,
        'stockArr' : stockArr

    }

    context = {
        'ps5Chosen' : ps5Chosen,
        'xboxSXChosen' : xboxSXChosen,
        'graphicsCardsChosen' : graphicsCardsChosen,
        'allChosen' : allChosen,
        'graphicsCardInfo' : graphicsCardInfo,
        'totalImgArr' : totalImgArr,
        'totalStockArr' : totalStockArr,
        'totalTitleArr' : totalTitleArr

    }

    for url in range(len(graphicsCardUrls)):
        newContext, newGraphicsCardInfo = addDictValues(context, productArr[url], url, graphicsCardInfo, name)
        graphicsCardInfo.update(newGraphicsCardInfo)
        context.update(newContext)
    
    print(context['graphicsCardInfo']['stockArr'][0])

    for ind in range(len(context['graphicsCardInfo']['imgArr'])):
        totalImgArr.append(context['graphicsCardInfo']['imgArr'][ind])
        totalTitleArr.append(context['graphicsCardInfo']['titleArr'][ind])
        totalStockArr.append(context['graphicsCardInfo']['stockArr'][ind])

    
    context['imgSrcPs5'] = product3['image']
    context['titlePs5'] = product3['title']
    context['inStockPs5'] = product3['stock']

    totalImgArr.append(product3['image'])
    totalTitleArr.append(product3['title'])
    totalStockArr.append(product3['stock'])

    context['imgSrcXboxSX'] = xboxSX['image']
    context['titleXboxSX'] = xboxSX['title']
    context['inStockXboxSX'] = xboxSX['stock']

    totalImgArr.append(xboxSX['image'])
    totalTitleArr.append(xboxSX['title'])
    totalStockArr.append(xboxSX['stock'])

    return render_template('itemData.html', **context) 

if __name__ == '__main__':
    app.run(debug=True)