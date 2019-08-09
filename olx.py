import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path

domain = 'https://www.olx.com.ar/autos-cat-378'
marcas = []
y = 0
index = 1

response = requests.get(domain)

soup = BeautifulSoup(response.text, "html.parser")

#obtengo el link de la siguiente pagina

for z in range(234,235):
        tag2 = soup.findAll('a')[z]
        next_page = tag2['href']
        next_page_link = 'https:' + next_page

#obtengo las imagenes y sus descripciones

for i in range(3,33):
        one_a_tag = soup.findAll('img')[i]
        link = one_a_tag['src']
        desc = one_a_tag['alt']
        desc2 = desc.split(' ',33)
        marca = desc2[y]
        marcas += [marca]
        marcas = sorted(set(marcas)) #elimino duplicados y ordeno la lista de marcas

        path = './download/olx/' + desc2[y].lower().replace(' ', '-') + '/'

        if not os.path.exists(path):
            os.makedirs(path)
            urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(desc2[y]).lower() + '-carID=' + str(i-1) + '.jpg')
            print("Descargada la foto",i-2, "de la pagina", index)
        else:
            urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(desc2[y]).lower() + '-carID=' + str(i-1) + '.jpg')
            print("Descargada la foto",i-2, "de la pagina", index)