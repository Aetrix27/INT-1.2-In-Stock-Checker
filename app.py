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

    return product

class Product:
    def __init__(self, name):
        self.imgArr = []
        self.titleArr = []
        self.stockArr = []
        self.urlArr = []
        self.name = name
        self.image = ''
        self.title = ''
        self.stock = ''
        self.url = ''

def addDictValues(product, itemInfo):
    itemInfo.imgArr.append(product['image'])
    itemInfo.titleArr.append(product['title'])
    itemInfo.stockArr.append(product['stock'])
    itemInfo.urlArr.append(product['url'])

    return itemInfo

def updateContext(totalItemArr, totalDict):
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
        for ind in range(len(productName.imgArr)):
            totalDict['totalImgArr'].append(productName.imgArr[ind])
            totalDict['totalTitleArr'].append(productName.titleArr[ind])
            totalDict['totalStockArr'].append(productName.stockArr[ind])
            totalDict['totalUrlArr'].append(productName.urlArr[ind])
    
    return totalDict

productArr = [getItemInfo(graphicsCardUrls[0])]
product3 = getItemInfo(urlPs5)
xboxItemArr = [getItemInfo(xboxUrls[0]), getItemInfo(xboxUrls[1])]

@app.route('/')
def home():
    totalDict = {}
    graphicsCardInfo = Product('graphicsCardInfo')
    xboxInfo = Product('xboxInfo')

    context = {
        'graphicsCardInfo' : graphicsCardInfo,
        'xboxInfo' : xboxInfo,
        'totalDict' : totalDict

    }

    totalItemArr = [graphicsCardInfo, xboxInfo]

    for url in range(len(graphicsCardUrls)):
        graphicsCardInfo = addDictValues(productArr[url], graphicsCardInfo)

    for url in range(len(xboxUrls)):
        xboxInfo = addDictValues(xboxItemArr[url], xboxInfo)

    updatedTotalDict = updateContext(totalItemArr, totalDict)
    totalDict.update(updatedTotalDict) 
    
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

    totalDict = {}
    graphicsCardInfo = Product('graphicsCardInfo')
    xboxInfo = Product('xboxInfo')

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
        graphicsCardInfo = addDictValues(productArr[url], graphicsCardInfo)

    for url in range(len(xboxUrls)):
        xboxInfo = addDictValues(xboxItemArr[url], xboxInfo)

    updatedTotalDict = updateContext(totalItemArr, totalDict)
    totalDict.update(updatedTotalDict) 
    
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