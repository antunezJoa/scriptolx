import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os.path

domain = 'https://www.olx.com.ar/autos-cat-378'

response = requests.get(domain)

soup = BeautifulSoup(response.text, "html.parser")

#next page link url

for z in range(234,235):
        tag2 = soup.findAll('a')[z]
        next_page = tag2['href']
        next_page_link = 'https:' + next_page

marcas = []
y=0

for i in range(3,33):
        #if 'alt' in one_a_tag:
        one_a_tag = soup.findAll('img')[i]
        link = one_a_tag['src']
        desc = one_a_tag['alt']
        desc2 = desc.split(' ',33)
        marca = desc2[y]
        marcas += [marca]
        marcas_ord = sorted(set(marcas)) #elimino duplicados y ordeno la lista de marcas

        #como descargar las imagenes?
        # urllib.request.urlretrieve(link, './download/olx/' + #marcaDelAuto + / )


        #creacion directorios

        #for x in range(0, len(marcas_ord)):
        #        path = './download/olx/' + marcas_ord[x].lower().replace(' ', '-')
        #        if not os.path.exists(path):
        #                os.makedirs(path)