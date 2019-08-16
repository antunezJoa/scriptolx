import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
import re

domain = 'https://www.olx.com.ar/autos-cat-378'
q = 0

response = requests.get(domain)
soup = BeautifulSoup(response.text, "html.parser")

'''for para obtener el numero de la ultima pagina'''

lista = []

for i in range(0, 1):
    tag2 = soup.findAll('p')[i]
    tag2 = str(tag2)
    tag2 = tag2.replace('.', '')
    lista = re.findall('\d+', tag2)

'''while para crear el array con los links de todas las páginas siguientes'''

k = 2
links_paginas = []

while k <= int(lista[1]):
    links_paginas += ['https://www.olx.com.ar/autos-cat-378-p-' + str(k)]
    k = k + 1

links_paginas.reverse()
links_paginas.append("https://www.olx.com.ar/autos-cat-378")
links_paginas.reverse()

j = 0

while j <= len(links_paginas):
    url = links_paginas[j]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    lista_ids = []

    for x in range(71, 350):
        tag3 = soup.findAll('a')[x]
        tag33 = str(tag3)
        if 'data-id' in tag33:
            ID = tag3['data-id']
            lista_ids += [ID]

    '''obtengo los 30 links de las 30 publaciones que hay por cada pagina'''

    lista2 = []

    for i in range(108, 227):
        tag = soup.findAll('a')[i]
        href = tag['href']
        href2 = 'https:' + href
        lista2 += [href2]

    lista_nueva = []

    for i in lista2:
        if i not in lista_nueva:
            lista_nueva.append(i)
    lista_nueva.remove('https:')

    u = 0
    while u <= len(lista_nueva):
        url2 = lista_nueva[u]
        response = requests.get(url2)
        soup = BeautifulSoup(response.text, "html.parser")

        marca2 = []

        for i in range(31, 32):
            tag = soup.findAll('span')[i]
            marca = tag.string
            marca2 = marca.split(' ', 1)

        image = []

        for i in range(0, len(soup.findAll('img'))):
            tag = soup.findAll('img')[i]
            tagg = str(tag)
            if 'data-modal-image' in tagg:
                image = tag['data-modal-image']
                print(image)

            path = './download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(lista_ids[q]) + '/'

            if not os.path.exists(path):
                os.makedirs(path)
                urllib.request.urlretrieve(image, './download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(lista_ids[q]) + '/' + str(marca2[0]).lower() + '.jpg')
                q = q + 1
                print("Descargada la imagen", i + 1, "de la publicacion", u + 1, "de la pagina", j + 1)
            else:
                urllib.request.urlretrieve(image, './download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(lista_ids[q]) + '/' + str(marca2[0]).lower() + '.jpg')
                q = q + 1
                print("Descargada la imagen", i + 1, "de la publicacion", u + 1, "de la pagina", j + 1)
            u = u + 1
    j = j + 1
