import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
import re
import json

domain = 'https://www.olx.com.ar/autos-cat-378'
headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/50.0.2661.102 Safari/537.36'}

response = requests.get(domain, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# for para obtener el numero de la ultima pagina

lista = []

for i in range(0, 1):
    tag2 = soup.findAll('p')[i]
    tag2 = str(tag2)
    tag2 = tag2.replace('.', '')
    lista = re.findall('\d+', tag2)

# while para crear el array con los links de todas las páginas

k = 2
links_paginas = []

while k <= int(lista[1]):
    links_paginas += ['https://www.olx.com.ar/autos-cat-378-p-' + str(k)]
    k = k + 1

links_paginas.reverse()
links_paginas.append("https://www.olx.com.ar/autos-cat-378")
links_paginas.reverse()

# for para recorrer todas las paginas de autos

j = 0

for j in range(0, len(links_paginas)):
    url = links_paginas[j]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # obtengo los links de las publaciones que hay por cada pagina

    links_publicaciones = []

    for i in range(108, 227):
        tag = soup.findAll('a')[i]
        href = tag['href']
        if 'iid' in href:
            href2 = 'https:' + href
            links_publicaciones += [href2]

    links_per_page = []

    for i in links_publicaciones:
        if i not in links_per_page:
            links_per_page.append(i)

    # for para recorrer todas las publicaciones dentro de una pagina

    u = 0

    for u in range(0, len(links_per_page)):
        url_public = links_per_page[u]
        print(url_public)
        response = requests.get(url_public, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # obtengo el ID de la publicacion en la que me encuentro

        url_public_str = str(url_public)
        ides = re.findall('\d+', url_public_str)
        ides = list(map(int, ides))
        ID = max(ides)

        # obtengo los datos del vehiculo, obtengo la marca y luego creo el json

        datos_vehiculo = {}
        campos = []

        for li_tag in soup.findAll('ul', {'class': 'item_partials_optionals_view compact'}):
            for span_tag in li_tag.find_all('li'):
                value = span_tag.find('span').text
                field = span_tag.find('strong').text
                campos += [field]
                datos_vehiculo[field] = value

        if 'Marca / Modelo:' in campos:
            marca = datos_vehiculo['Marca / Modelo:'].split(' ', 1)[0]
        elif 'Marca:' in campos:
            marca = datos_vehiculo['Marca:']
        else:
            marca = "unknown"

        path = './download/olx/' + str(marca).lower().replace(' ', '-') + '/' + str(ID) + '/'

        if not os.path.exists(path):
            os.makedirs(path)

        # creo el archivo .json con las características del vehiculo

        with open('./download/olx/' + str(marca).lower().replace(' ', '-') + '/' + str(ID) + '/meta.json', 'w') as fp:
            json.dump(datos_vehiculo, fp)

        print("Creado meta.json")

        # obtengo los links de las imagenes de la publicacion en la que me encuentro

        q = 0
        images2 = []
        images = []

        for i in range(0, len(soup.findAll('a'))):
            tag = soup.findAll('a')[i]
            href = tag['href']
            if 'image;p=full' in href:
                q = q + 1
                images += [href]

        if len(images) == 0:
            for i in range(0, len(soup.findAll('img'))):
                tag = soup.findAll('img')[i]
                source = tag['src']
                if 'image;p=full' in source:
                    q = 1
                    images2 += [source]

        for i in images2:
            if i not in images:
                images.append(i)

        y = 0

        while y < q:
            urllib.request.urlretrieve(images[y], './download/olx/' + str(marca).lower().replace(' ', '-') + '/' + str(ID) + '/' + str(marca).lower() + '_' + str(ID) + '_' + str(y + 1) + '.jpg')
            print("Descargada la imagen", y + 1, "de la publicacion", u + 1, "de la pagina", j + 1)
            y = y + 1

print("End")