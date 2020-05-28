import requests
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
    raw_html = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_info(dept):

    page = requests.get('https://www.boliviasegura.gob.bo/')
    soup = BeautifulSoup(page.content, 'html.parser')

    fecha = cleanhtml(soup.find_all('h5')[0])

    nacional_hoy = cleanhtml(soup.find_all('h4')[0]).split('HOY: ')[1]

    nacional_total = cleanhtml(soup.find_all('td')[:3][0])
    nacional_decesos = cleanhtml(soup.find_all('td')[:3][1])
    nacional_recuperados = cleanhtml(soup.find_all('td')[:3][2])

    nacional =['Nacional', nacional_hoy, nacional_total, nacional_decesos, nacional_recuperados]

    ls = []
    for element in soup.find_all('td')[3:48]:
        ls.append(cleanhtml(element))

    departamentos = ls[0::5]

    step=0
    for dep in departamentos:
        exec(str(dep.lower().replace(' ','_'))+f'={ls[step:5+step]}')
        step+=5

    value = dept.lower().replace(" ", "_")
    return fecha, eval(value)
