from requests_html import HTMLSession
import jinja2

from flask import Flask, request, render_template

app = Flask(__name__)

graphicsCardUrls = ['https://www.amazon.com/EVGA-08G-P5-3767-KR-GeForce-Technology-Backplate/dp/B08L8L9TCZ/ref=sr_1_1?dchild=1&keywords=3070&qid=1610223381&s=electronics&sr=1-1']

urlPs5 = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp'
xboxUrls = ['https://www.amazon.com/Xbox-X/dp/B08H75RTZ8/ref=sr_1_13?dchild=1&keywords=xbox+series+x&qid=1610417662&sr=8-13',
            'https://www.amazon.com/Xbox-X/dp/B08G9J44ZN/ref=sr_1_13?dchild=1&keywords=xbox%2Bseries%2Bx&qid=1610417662&sr=8-13&th=1']

s = HTMLSession()

def getItemInfo(url):
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

def updateContext(context, totalItemArr, totalDict):
    totalImgArr = []
    totalTitleArr = []
    totalStockArr = []
    totalUrlArr = []

    totalDict = {
        'totalImgArr' : totalImgArr,
        'totalTitleArr' : totalTitleArr,
        'totalStockArr' : totalStockArr,
        'totalUrlArr' : totalUrlArr
      
    }

    for productName in totalItemArr: 
        for ind in range(len(context[productName['name']]['imgArr'])):
            print(context[productName['name']]['imgArr'][ind])
            totalDict['totalImgArr'].append(context[productName['name']]['imgArr'][ind])
            totalDict['totalTitleArr'].append(context[productName['name']]['titleArr'][ind])
            totalDict['totalStockArr'].append(context[productName['name']]['stockArr'][ind])
            totalDict['totalUrlArr'].append(context[productName['name']]['urlArr'][ind])
    
    return context, totalDict


productArr = [getItemInfo(graphicsCardUrls[0])]
product3 = getItemInfo(urlPs5)
xboxItemArr = [getItemInfo(xboxUrls[0]), getItemInfo(xboxUrls[1])]

class Product:
    def __init__(self, image, title, stock, url):
        self.image = image
        self.title = title
        self.stock = stock
        self.url = url


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
    totalDict = {}

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
        'xboxInfo' : xboxInfo,
        'totalDict' : totalDict

    }

    totalItemArr = [graphicsCardInfo, xboxInfo]

    for url in range(len(graphicsCardUrls)):
        newContext, newGraphicsCardInfo = addDictValues(context, productArr[url], url, graphicsCardInfo, name)
        graphicsCardInfo.update(newGraphicsCardInfo)
        context.update(newContext)

    for url in range(len(xboxUrls)):
        newContext2, newXboxInfo = addDictValues(context, xboxItemArr[url], url, xboxInfo, name2)
        xboxInfo.update(newXboxInfo)
        context.update(newContext2)

    updatedContext, updatedTotalDict = updateContext(context, totalItemArr, totalDict)
    totalDict.update(updatedTotalDict) 
    context.update(updatedContext)
    
    context['imgSrcPs5'] = product3['image']
    context['titlePs5'] = product3['title']
    context['inStockPs5'] = product3['stock']
    context['urlPs5'] = product3['url']

    totalDict['totalImgArr'].append(product3['image'])
    totalDict['totalTitleArr'].append(product3['title'])
    totalDict['totalStockArr'].append(product3['stock'])
    totalDict['totalUrlArr'].append(product3['url'])

    return render_template('index.html', **context) 

@app.route('/itemData')
def itemData():
    ps5Chosen = False
    xboxChosen = False
    graphicsCardsChosen = False
    allChosen = False

    select = request.args.get('choice')

    if select == "Graphics":
        graphicsCardsChosen = True
    elif select == "Xbox SX/S":
        xboxChosen = True
    elif select == "Ps5":
        ps5Chosen = True
    elif select == "All":
        allChosen = True

    imgArr = []
    titleArr = []
    stockArr = []
    urlArr = []
    imgArr2 = []
    titleArr2 = []
    stockArr2 = []
    urlArr2 = []
    totalDict = {}

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
        'xboxInfo' : xboxInfo,
        'totalDict' : totalDict,
        'xboxChosen' : xboxChosen,
        'ps5Chosen' : ps5Chosen,
        'graphicsCardsChosen' : graphicsCardsChosen,
        'allChosen' : allChosen

    }

    totalItemArr = [graphicsCardInfo, xboxInfo]

    for url in range(len(graphicsCardUrls)):
        newContext, newGraphicsCardInfo = addDictValues(context, productArr[url], url, graphicsCardInfo, name)
        graphicsCardInfo.update(newGraphicsCardInfo)
        context.update(newContext)

    for url in range(len(xboxUrls)):
        newContext2, newXboxInfo = addDictValues(context, xboxItemArr[url], url, xboxInfo, name2)
        xboxInfo.update(newXboxInfo)
        context.update(newContext2)

    updatedContext, updatedTotalDict = updateContext(context, totalItemArr, totalDict)
    totalDict.update(updatedTotalDict) 
    context.update(updatedContext)
    
    context['imgSrcPs5'] = product3['image']
    context['titlePs5'] = product3['title']
    context['inStockPs5'] = product3['stock']
    context['urlPs5'] = product3['url']

    totalDict['totalImgArr'].append(product3['image'])
    totalDict['totalTitleArr'].append(product3['title'])
    totalDict['totalStockArr'].append(product3['stock'])
    totalDict['totalUrlArr'].append(product3['url'])

    return render_template('itemData.html', **context) 



if __name__ == '__main__':
    app.run(debug=True)