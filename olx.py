import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
import re

domain = 'https://www.olx.com.ar/autos-cat-378'
links_paginas = []
k = 2
y = 0
lista = []

response = requests.get(domain)

soup = BeautifulSoup(response.text, "html.parser")

for i in range (0,1): #for para obtener el numero de la ultima pagina
    tag = soup.findAll('p')[i]
    tag = str(tag)
    tag = tag.replace('.','')
    lista = re.findall('\d+', tag)

while k<=int(lista[1]): #while para crear el array con los links de todas las páginas siguientes
    links_paginas += ['https://www.olx.com.ar/autos-cat-378-p-' + str(k)]
    k = k + 1

#entrar a cada item y descargar todas las fotos, id

for i in range(89,400):
        tag2 = soup.findAll('a')[i]
        tag22 = str(tag2)
        if 'data-id' in tag22:
            id = tag2['data-id']
            print(id,y)
            y += 1


'''for z in range(234,235):
        tag2 = soup.findAll('a')[z]
        tag22 = str(tag2)
        if 'rel' in tag22:
            rel = tag2['rel']
            print("EXISTE REL")
            if rel == ['next']:
                print("ES NEXT")
                next_page = tag2['href']
                next_page_link = 'https:' + next_page
                paginas += [next_page_link]
            else:
                print("NO ES NEXT")
                print("LAST PAGE")
                flag = False
        else:
            flag = False
            print("NO EXISTE REL")
            print("LAST PAGE")'''

'''for i in range(3,33):
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
            print("Descargada la foto",i-2, "de la pagina", index)'''