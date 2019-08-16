import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
import re

domain = 'https://mardelplata.olx.com.ar/citroen-aircross-iid-1058334945'

response = requests.get(domain)
soup = BeautifulSoup(response.text, "html.parser")

for i in range(0, len(soup.findAll('a'))):
    tag = soup.findAll('a')[i]
    href = tag['href']
    if 'full' in str(href):
        image = href