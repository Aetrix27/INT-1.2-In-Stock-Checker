import requests
import re
from bs4 import BeautifulSoup as bs

# Load the webpage content
r = requests.get("")

# Convert to a beautiful soup object
soup = bs(r.content, features="html.parser")

# Pretty prints out our html
print(soup.prettify())

links = soup.select("a")
