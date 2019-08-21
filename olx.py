import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
import re
import json

domain = 'https://www.olx.com.ar/autos-cat-378'

response = requests.get(domain)
soup = BeautifulSoup(response.text, "html.parser")

'''for para obtener el numero de la ultima pagina'''

lista = []

for i in range(0, 1):
    tag2 = soup.findAll('p')[i]
    tag2 = str(tag2)
    tag2 = tag2.replace('.', '')
    lista = re.findall('\d+', tag2)

'''while para crear el array con los links de todas las páginas'''

k = 2
links_paginas = []

while k <= int(lista[1]):
    links_paginas += ['https://www.olx.com.ar/autos-cat-378-p-' + str(k)]
    k = k + 1

links_paginas.reverse()
links_paginas.append("https://www.olx.com.ar/autos-cat-378")
links_paginas.reverse()

'''for para recorrer todas las paginas de autos'''

j = 0

for j in range(0, len(links_paginas)):
    url = links_paginas[j]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    '''obtengo los links de las publaciones que hay por cada pagina'''

    lista2 = []

    for i in range(108, 227):
        tag = soup.findAll('a')[i]
        href = tag['href']
        href2 = 'https:' + href
        lista2 += [href2]

    links_per_page = []

    for i in lista2:
        if i not in links_per_page:
            links_per_page.append(i)
    links_per_page.remove('https:')

    '''for para recorrer todas las publicaciones dentro de una pagina'''

    u = 0

    for u in range(0, len(links_per_page)):
        url2 = links_per_page[u]
        response = requests.get(url2)
        soup = BeautifulSoup(response.text, "html.parser")

        '''obtengo el ID de la publicacion en la que me encuentro'''

        url3 = str(url2)
        ides = re.findall('\d+', url3)
        ides = list(map(int, ides))
        ID = max(ides)

        '''obtengo la marca del auto de la publicacion en la que me encuentro'''

        marca2 = []

        for i in range(31, 32):
            tag = soup.findAll('span')[i]
            marca = tag.string
            marca2 = marca.split(' ', 1)
            marca22 = marca2[0]

        '''obtengo los elementos a guardar en el archivo .json'''

        data_list = []

        for i in range(27, 34):
            tag = soup.findAll('span')[i]
            data = tag.string
            data2 = data.split(' ', 1)
            data_list += [data2]

        for i in range(0, len(data_list)):
            if len(data_list[i]) >= 2:
                data_list[i] = "-".join(data_list[i])

        '''datos del json'''

        datos = {}
        datos['año/condicion'] = ''.join(data_list[0])
        datos['transmision'] = ''.join(data_list[1])
        datos['vendedor'] = ''.join(data_list[2])
        datos['kilometraje'] = ''.join(data_list[3])
        datos['marca/modelo'] = ''.join(data_list[4])
        datos['combustible'] = ''.join(data_list[5])
        datos['color'] = ''.join(data_list[6])

        path = './download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(ID) + '/'
        if not os.path.exists(path):
            os.makedirs(path)

        '''funcion para crear archivos json'''

        def writeToJSONFile(path, data):
            filePathNameWExt = path + 'meta.json'
            with open(filePathNameWExt, 'w') as fp:
                json.dump(data, fp)

        '''creo el archivo .json con las características del vehiculo'''

        writeToJSONFile('./download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(ID) + '/', datos)

        '''obtengo los links de las imagenes de la publicacion en la que me encuentro'''

        q = 0
        images = []

        for i in range(0, len(soup.findAll('a'))):
            tag = soup.findAll('a')[i]
            href = tag['href']
            if 'full' in href:
                q = q + 1
                images += [href]

        y = 0

        while y < q:
            path = './download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(ID) + '/'

            if not os.path.exists(path):
                os.makedirs(path)
            urllib.request.urlretrieve(images[y], './download/olx/' + str(marca2[0]).lower().replace(' ', '-') + '/' + str(ID) + '/' + str(marca2[0]).lower() + str(y) + '.jpg')
            print("Descargada la imagen", y + 1, "de la publicacion", u + 1, "de la pagina", j + 1)
            y = y + 1

print("The end")
