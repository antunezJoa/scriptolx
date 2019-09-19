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


def downloadlinks():
    response = requests.get(domain, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    path = './download/olx/'

    if not os.path.exists(path):
        os.makedirs(path)

    links = {}
    c = 0

    # for para obtener el numero de la ultima pagina

    list_nums = []

    for i in range(0, 1):
        tag2 = soup.findAll('p')[i]
        tag2 = str(tag2)
        tag2 = tag2.replace('.', '')
        list_nums = re.findall('\d+', tag2)

    # while para crear el array con los links de todas las páginas

    k = 2
    links_pages = []

    while k <= int(list_nums[1]):
        links_pages += ['https://www.olx.com.ar/autos-cat-378-p-' + str(k)]
        k = k + 1

    links_pages.reverse()
    links_pages.append("https://www.olx.com.ar/autos-cat-378")
    links_pages.reverse()

    # for para recorrer todas las paginas de autos

    for j in range(0, len(links_pages)):
        url = links_pages[j]
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # obtengo los links de las publaciones que hay por cada pagina

        links_public = []

        for i in range(108, 227):
            tag = soup.findAll('a')[i]
            href = tag['href']
            if 'iid' in href:
                href2 = 'https:' + href
                links_public += [href2]

        links_per_page = []

        for i in links_public:
            if i not in links_per_page:
                links_per_page.append(i)

        for i in range(0, len(links_per_page)):
            links['url' + str(c)] = links_per_page[i]
            with open(path + "item_links.json", "w") as file:
                json.dump(links, file)
            print("Saved", links['url' + str(c)], "number of links saved:", c)
            c += 1
    print("End")


path = './download/olx/item_links.json'

if not os.path.exists(path):
    downloadlinks()
else:
    with open('./download/olx/item_links.json', 'r') as f:
        domains = f.read()

doms = json.loads(domains)

count = 0  # count es el contador que indica en cual link arranca la descarga de imagenes

links_number = 100  # aca va el numero de links guardados en el json

while count <= links_number:
    url_public = doms['url' + str(count)]
    print(url_public, count)

    response = requests.get(url_public, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # obtengo el ID de la publicacion en la que me encuentro

    url_public_str = str(url_public)
    ides = re.findall('\d+', url_public_str)
    ides = list(map(int, ides))
    ID = max(ides)

    # obtengo los datos del vehiculo, obtengo la marca y luego creo el json

    data_vehicle = {}
    fields = []

    for li_tag in soup.findAll('ul', {'class': 'item_partials_optionals_view compact'}):
        for span_tag in li_tag.find_all('li'):
            value = span_tag.find('span').text
            field = span_tag.find('strong').text
            fields += [field]
            data_vehicle[field] = value

    if 'Marca / Modelo:' in fields:
        brand = data_vehicle['Marca / Modelo:'].split(' ', 1)[0]

    elif 'Marca:' in fields:
        brand = data_vehicle['Marca:']
    else:
        brand = "unknown"

    path = './download/olx/' + str(brand).lower().replace(' ', '-') + '/' + str(ID) + '/'

    if not os.path.exists(path):
        os.makedirs(path)

    # creo el archivo .json con las características del vehiculo

    with open(path + 'meta.json', 'w') as fp:
        json.dump(data_vehicle, fp)

    print("Created meta.json")

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
        urllib.request.urlretrieve(images[y], './download/olx/' + str(brand).lower().replace(' ', '-') + '/' + str(ID) + '/' + str(brand).lower() + '_' + str(ID) + '_' + str(y + 1) + '.jpg')
        print("Downloaded image", y + 1, "/", brand)
        y = y + 1

    count = count + 1

print("End")
