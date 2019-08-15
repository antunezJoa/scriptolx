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
lista2 = []
q = 0
lista_ids = []

response = requests.get(domain)
soup = BeautifulSoup(response.text, "html.parser")

#obtengo los 30 links de las 30 publaciones que hay por cada pagina

for i in range(108,227):
    tag = soup.findAll('a')[i]
    href = tag['href']
    href2 = 'https:' + href
    lista2 += [href2]
lista_nueva = []
for i in lista2:
    if i not in lista_nueva:
        lista_nueva.append(i)
lista_nueva.remove('https:')

#for para obtener el numero de la ultima pagina

for i in range (0,1):
    tag2 = soup.findAll('p')[i]
    tag2 = str(tag2)
    tag2 = tag2.replace('.','')
    lista = re.findall('\d+', tag2)

#while para crear el array con los links de todas las páginas siguientes

while k<=int(lista[1]):
    links_paginas += ['https://www.olx.com.ar/autos-cat-378-p-' + str(k)]
    k = k + 1

links_paginas.reverse()
links_paginas.append("https://www.olx.com.ar/autos-cat-378")
links_paginas.reverse()

#entrar a cada item y descargar todas las fotos,id
##################################################

j = 0
while (j <= len(links_paginas)):
    urls = links_paginas[j]
    response = requests.get(urls)
    soup = BeautifulSoup(response.text, "html.parser")

    for x in range(71, 350):
        tag3 = soup.findAll('a')[x]
        tag33 = str(tag3)
        if 'data-id' in tag33:
            id = tag3['data-id']
            lista_ids += [id]

    for i in range(3,33):
            tag4 = soup.findAll('img')[i]
            link = tag4['src']
            desc = tag4['alt']
            desc2 = desc.split(' ',33)

            path = './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(lista_ids[q]) + '/'

            if not os.path.exists(path):
                os.makedirs(path)
                urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(lista_ids[q]) + '/' + str(desc2[y]).lower() + '.jpg')
                q = q + 1
                print("Descargada imagen numero",i-2,"de la pagina",j+1)
            else:
                urllib.request.urlretrieve(link, './download/olx/' + desc2[y].lower().replace(' ', '-') + '/' + str(lista_ids[q]) + '/' + str(desc2[y]).lower() + '.jpg')
                q = q + 1
                print("Descargada imagen numero",i-2,"de la pagina",j+1)
    j = j + 1




































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