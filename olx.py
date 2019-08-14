import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path

domain = 'https://www.olx.com.ar/autos-cat-378' #-p-1476
flag = True
marcas = []
y = 0
index = 1 #nro de pagina

response = requests.get(domain)

soup = BeautifulSoup(response.text, "html.parser")

#obtengo el link de la siguiente pagina

for z in range(234,235):
        tag2 = soup.findAll('a')[z]
        tag22 = str(tag2)
        if 'rel' in tag22:
            rel = tag2['rel']
            print("EXISTE REL")
            if rel == ['next']:
                print("ES NEXT")
                next_page = tag2['href']
                next_page_link = 'https:' + next_page
            else:
                print("NO ES NEXT")
                print("LAST PAGE")
                flag = False
        else:
            flag = False
            print("NO EXISTE REL")
            print("LAST PAGE")

#obtengo las imagenes y sus descripciones

for i in range(3,33):
        tag = soup.findAll('img')[i]
        link = tag['src']
        desc = tag['alt']
        desc2 = desc.split(' ',33)
        marca = desc2[y]
        marcas += [marca]
        marcas = sorted(set(marcas)) #elimino duplicados y ordeno la lista de marcas

        #¿eliminar vacios?

        path = './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(i-1) + "-" + str(index) + '/'

        if not os.path.exists(path):
            os.makedirs(path)
            #urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(desc2[y]).lower() + '-carID=' + str(i-1) + '.jpg')
            urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(i-1) + "-" + str(index) + '/' + str(desc2[y]).lower() + '.jpg')
            print("Descargada la foto",i-2, "de la pagina", index)
        else:
            urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(i-1) + "-" + str(index) + '/' + str(desc2[y]).lower() + '.jpg')
            print("Descargada la foto",i-2, "de la pagina", index)