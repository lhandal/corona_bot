from scraper import *
from datetime import date, time, datetime
import base64
import time
from twilio.rest import Client
from random import randint

date_dict = {'Enero':1, 'Febrero':2, 'Marzo':3, 'Abril':4, 'Mayo':5, 'Junio':6, 'Julio':7, 'Agosto':8, 'Septiembre':9, 'Octubre':10, 'Noviembre':11, 'Diciembre':12}
contacts = ['+34695686937']
enc_sid = b'QTZDNDY5NmE3ZGY0YmNhYWNkM2M3NTJlNWM0OGJiNzU4ZmM2YTA3NWJjMGE5OTU1YWE5YWM1MGRmYjM3MjE3Ng=='
departamentos = ['Bolivia', 'Beni', 'Chuquisaca', 'Cochabamba', 'La Paz', 'Oruro', 'Pando', 'Potosí', 'Santa Cruz', 'Tarija']

def get_fecha():
    page = requests.get('https://www.boliviasegura.gob.bo/')
    soup = BeautifulSoup(page.content, 'html.parser')
    fecha = cleanhtml(soup.find_all('h5')[0])
    return fecha

def parse_date(fecha):
    dia = int(fecha.split()[1])
    año = int(fecha.split()[-1])
    mes = int(date_dict[fecha.split()[3]])
    parsed = date(año, mes, dia)
    return parsed

def get_date():
    page = requests.get('https://www.boliviasegura.gob.bo/')
    soup = BeautifulSoup(page.content, 'html.parser')
    fecha = cleanhtml(soup.find_all('h5')[0])
    date = parse_date(fecha)
    return date

def get_info(dept):

    page = requests.get('https://www.boliviasegura.gob.bo/')
    soup = BeautifulSoup(page.content, 'html.parser')

    fecha = cleanhtml(soup.find_all('h5')[0])

    nacional_hoy = cleanhtml(soup.find_all('h4')[0]).split('HOY: ')[1]

    nacional_total = cleanhtml(soup.find_all('td')[:3][0])
    nacional_decesos = cleanhtml(soup.find_all('td')[:3][1])
    nacional_recuperados = cleanhtml(soup.find_all('td')[:3][2])

    nacional =['Bolivia', nacional_hoy, nacional_total, nacional_decesos, nacional_recuperados]
    bolivia = ['Bolivia', nacional_hoy, nacional_total, nacional_decesos, nacional_recuperados]

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

def send_message(enc_sid, text, contacts):
    sid_token = base64.b64decode(enc_sid.decode("utf-8")).decode("utf-8")
    client = Client(sid_token[::2]+'6a', sid_token[1::2])
    for contact in contacts:
        message = client.messages.create(
                                  body=text,
                                  from_='whatsapp:+14155238886',
                                  to=f'whatsapp:{contact}'
                              )

    print(message.sid)

def reporte(departamentos=departamentos):
    fecha = get_fecha()
    big = f'*Reporte diario:*\n*{fecha}*\n\n'
    for dep in departamentos:
        fecha, info = get_info(dep)
        text = f"""
    *{info[0]}*
    Nuevos casos: {info[1]}
    Total casos: {info[2]}
    Decesos: {info[3]}
    Recuperados: {info[4]}\n\n
    """
        big += text
    return big

fecha = get_fecha()
last_check = datetime.now()
x=0

print('Script running!')

while True:
    if fecha != get_fecha():
        print(f'[{datetime.now():%H:%M:%S}]: Sending update!')
        send_message(enc_sid, reporte(), contacts)
        print(f'[{datetime.now():%H:%M:%S}]: Update sent to:')
        print(f'{contacts}')
        fecha = get_fecha()
        x=0
    else:
        x+=1
        if x >=6:
            x=0
            print(f'[{datetime.now():%H:%M:%S}]: running...')
            pass
    time.sleep(300)

