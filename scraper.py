import requests
from bs4 import BeautifulSoup
import re
from facebook_scraper import get_posts

def cleanhtml(raw_html):
    raw_html = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_info(dept):
    page = requests.get('https://www.boliviasegura.gob.bo/datos.php')
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        fecha = re.search(r'Reporte Epidemiológico al (.*?)\n', soup.text).group(1)
    except:
        fecha = cleanhtml(soup.find_all('h1')[1]).split('Reporte Epidemiológico al ')[1]

    try:
        nacional_hoy = cleanhtml(soup.find_all('h4')[0]).split('CONFIRMADOS HOY: ')[1]
    except IndexError:
        nacional_hoy = cleanhtml(soup.find_all('h4')[1]).split('CONFIRMADOS HOY: ')[1]

    nacional_total = cleanhtml(soup.find_all('td')[0])
    nacional_decesos = cleanhtml(soup.find_all('td')[1])
    nacional_recuperados = cleanhtml(soup.find_all('td')[2])

    nacional =['Bolivia', nacional_hoy, nacional_total, nacional_decesos, nacional_recuperados]
    bolivia = ['Bolivia', nacional_hoy, nacional_total, nacional_decesos, nacional_recuperados]

    ls = []
    for element in soup.find_all('td')[3:48]:
        ls.append(cleanhtml(element))
    # ls = ls[4:]
    departamentos = ls[0::5]
    print(ls)

    step=0
    for dep in departamentos:
        exec(str(dep.lower().replace(' ','_'))+f'={ls[step:5+step]}')
        step+=5

    value = dept.lower().replace(" ", "_")
    return fecha, eval(value)


def get_comm():
    x = requests.get(f'https://www.boliviasegura.gob.bo/comunicados.php').text.find('COMUNICADO ')
    text = requests.get(f'https://www.boliviasegura.gob.bo/comunicados.php').text[x:].split('><img')[0]
    num = text.split('?Seleccion=')[1][:-1]
    jpg = f"https://www.boliviasegura.gob.bo/archivos/noticia{num}.jpg"
    header = text.split('</a>')[0]

    return header, jpg

def plague():
    for post in get_posts('GlobalNewsCovid19', pages=1):
        jpg = post['image']
        break
    return jpg
