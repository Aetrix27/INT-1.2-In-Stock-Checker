import requests
import re
from bs4 import BeautifulSoup as bs

URL = "https://www.amazon.com/MSI-GeForce-Architecture-Overclocked-Graphics/dp/B08CLV8CKP/ref=sr_1_1?dchild=1&keywords=2080&qid=1610047787&s=electronics&sr=1-1"

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = bs(page.content, 'html.parser')

title = soup.find(id="productTitle").get_text()
print(title.strip())

images = soup.find('img', attrs={"id": "landingImage"})

print(images['data-old-hires']+'\n')