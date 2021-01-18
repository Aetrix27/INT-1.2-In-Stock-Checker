from requests_html import HTMLSession
import jinja2
import os
import time

from flask import Flask, request, render_template, send_file

app = Flask(__name__)

graphicsCardUrls = ['https://www.amazon.com/EVGA-08G-P5-3767-KR-GeForce-Technology-Backplate/dp/B08L8L9TCZ/ref=sr_1_1?dchild=1&keywords=3070&qid=1610223381&s=electronics&sr=1-1',
                    'https://www.amazon.com/MSI-GeForce-Tri-Frozr-Architecture-Graphics/dp/B08HR7SV3M/ref=sr_1_3?crid=1Y1DLX8V0GXII&dchild=1&keywords=3080&qid=1610406031&s=electronics&sprefix=3080%2Celectronics%2C280&sr=1-3']

urlPs5 = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp'
xboxUrls = ['https://www.amazon.com/Xbox-X/dp/B08H75RTZ8/ref=sr_1_13?dchild=1&keywords=xbox+series+x&qid=1610417662&sr=8-13',
            'https://www.amazon.com/Xbox-X/dp/B08G9J44ZN/ref=sr_1_13?dchild=1&keywords=xbox%2Bseries%2Bx&qid=1610417662&sr=8-13&th=1']

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
    elif 'sellers' in product['availability']:
        product['stock'] = 'In Stock (By Limited Sellers)'
    else:
        product['stock'] = 'In Stock'
    
    product['url'] = url

    #   'price': 'item unavailable',

    return product

def addDictValues(context, product, loopNum, itemInfo, name):
    productImage = 'img' + str(loopNum+1) 
    productTitle = 'title' + str(loopNum+1)
    productStock = 'stock' + str(loopNum+1)
    productUrl = 'url' + str(loopNum+1)

    context['imgName'] = productImage
    context['titleName'] = productTitle
    context['stock'] = productStock
    context['url'] = productUrl

    context[name]['imgArr'].append(product['image'])
    context[name]['titleArr'].append(product['title'])
    context[name]['stockArr'].append(product['stock'])
    context[name]['urlArr'].append(product['url'])

    context[productImage] = product['image']
    context[productTitle] = product['title']
    context[productStock] = product['stock']
    context[productUrl] = product['url']

    return context, itemInfo

productArr = [getItemInfo(graphicsCardUrls[0]), getItemInfo(graphicsCardUrls[1])]
product3 = getItemInfo(urlPs5)
xboxItemArr = [getItemInfo(xboxUrls[0]), getItemInfo(xboxUrls[1])]

@app.route('/')
def home():
    imgArr = []
    titleArr = []
    stockArr = []
    urlArr = []
    imgArr2 = []
    titleArr2 = []
    stockArr2 = []
    urlArr2 = []
    totalImgArr = []
    totalTitleArr = []
    totalStockArr = []
    totalUrlArr = []

    name = 'graphicsCardInfo'
    name2 = 'xboxInfo'

    graphicsCardInfo = {
        'name' : name,
        'imgArr' : imgArr,
        'titleArr' : titleArr,
        'stockArr' : stockArr,
        'urlArr' : urlArr

    }

    xboxInfo = {
        'name' : name2,
        'imgArr' : imgArr2,
        'titleArr' : titleArr2,
        'stockArr' : stockArr2,
        'urlArr' : urlArr2

    }

    context = {
        'graphicsCardInfo' : graphicsCardInfo,
        'totalImgArr' : totalImgArr,
        'totalStockArr' : totalStockArr,
        'totalTitleArr' : totalTitleArr,
        'totalUrlArr' : totalUrlArr,
        'xboxInfo' : xboxInfo


    }

    for url in range(len(graphicsCardUrls)):
        newContext, newGraphicsCardInfo = addDictValues(context, productArr[url], url, graphicsCardInfo, name)
        graphicsCardInfo.update(newGraphicsCardInfo)
        context.update(newContext)
    
    for ind in range(len(context['graphicsCardInfo']['imgArr'])):
        totalImgArr.append(context['graphicsCardInfo']['imgArr'][ind])
        totalTitleArr.append(context['graphicsCardInfo']['titleArr'][ind])
        totalStockArr.append(context['graphicsCardInfo']['stockArr'][ind])
        totalUrlArr.append(context['graphicsCardInfo']['urlArr'][ind])

    for url in range(len(xboxUrls)):
        newContext2, newXboxInfo = addDictValues(context, xboxItemArr[url], url, xboxInfo, name2)
        xboxInfo.update(newXboxInfo)
        context.update(newContext2)
    
    for ind in range(len(context['xboxInfo']['imgArr'])):
        totalImgArr.append(context['xboxInfo']['imgArr'][ind])
        totalTitleArr.append(context['xboxInfo']['titleArr'][ind])
        totalStockArr.append(context['xboxInfo']['stockArr'][ind])
        totalUrlArr.append(context['xboxInfo']['urlArr'][ind])

    
    context['imgSrcPs5'] = product3['image']
    context['titlePs5'] = product3['title']
    context['inStockPs5'] = product3['stock']
    context['urlPs5'] = product3['url']

    totalImgArr.append(product3['image'])
    totalTitleArr.append(product3['title'])
    totalStockArr.append(product3['stock'])
    totalUrlArr.append(product3['url'])

    return render_template('index.html', **context) 

@app.route('/itemData')
def itemData():
    ps5Chosen = False
    xboxChosen = False
    graphicsCardsChosen = False
    allChosen = False
    imgArr = []
    titleArr = []
    stockArr = []
    urlArr = []
    imgArr2 = []
    titleArr2 = []
    stockArr2 = []
    urlArr2 = []
    totalImgArr = []
    totalTitleArr = []
    totalStockArr = []
    totalUrlArr = []


    select = request.args.get('choice')
    print(select)

    if select == "Graphics":
        graphicsCardsChosen = True
    elif select == "Xbox SX/S":
        xboxChosen = True
    elif select == "Ps5":
        ps5Chosen = True
    elif select == "All":
        allChosen = True


    name = 'graphicsCardInfo'
    name2 = 'xboxInfo'

    graphicsCardInfo = {
        'name' : name,
        'imgArr' : imgArr,
        'titleArr' : titleArr,
        'stockArr' : stockArr,
        'urlArr' : urlArr

    }

    xboxInfo = {
        'name' : name2,
        'imgArr' : imgArr2,
        'titleArr' : titleArr2,
        'stockArr' : stockArr2,
        'urlArr' : urlArr2

    }

    context = {
        'graphicsCardInfo' : graphicsCardInfo,
        'totalImgArr' : totalImgArr,
        'totalStockArr' : totalStockArr,
        'totalTitleArr' : totalTitleArr,
        'totalUrlArr' : totalUrlArr,
        'ps5Chosen' : ps5Chosen,
        'xboxChosen' : xboxChosen,
        'graphicsCardsChosen' : graphicsCardsChosen,
        'allChosen' : allChosen,
        'xboxInfo' : xboxInfo
 
    }

    for url in range(len(graphicsCardUrls)):
        newContext, newGraphicsCardInfo = addDictValues(context, productArr[url], url, graphicsCardInfo, name)
        graphicsCardInfo.update(newGraphicsCardInfo)
        context.update(newContext)
    
    for ind in range(len(context['graphicsCardInfo']['imgArr'])):
        totalImgArr.append(context['graphicsCardInfo']['imgArr'][ind])
        totalTitleArr.append(context['graphicsCardInfo']['titleArr'][ind])
        totalStockArr.append(context['graphicsCardInfo']['stockArr'][ind])
        totalUrlArr.append(context['graphicsCardInfo']['urlArr'][ind])

    for url in range(len(xboxUrls)):
        newContext2, newXboxInfo = addDictValues(context, xboxItemArr[url], url, xboxInfo, name2)
        xboxInfo.update(newXboxInfo)
        context.update(newContext2)
    
    for ind in range(len(context['xboxInfo']['imgArr'])):
        totalImgArr.append(context['xboxInfo']['imgArr'][ind])
        totalTitleArr.append(context['xboxInfo']['titleArr'][ind])
        totalStockArr.append(context['xboxInfo']['stockArr'][ind])
        totalUrlArr.append(context['xboxInfo']['urlArr'][ind])

    
    context['imgSrcPs5'] = product3['image']
    context['titlePs5'] = product3['title']
    context['inStockPs5'] = product3['stock']
    context['urlPs5'] = product3['url']

    totalImgArr.append(product3['image'])
    totalTitleArr.append(product3['title'])
    totalStockArr.append(product3['stock'])
    totalUrlArr.append(product3['url'])

    return render_template('itemData.html', **context) 

if __name__ == '__main__':
    app.run(debug=True)