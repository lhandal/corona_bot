from flask import Flask, request
import requests
import os
import json
import datetime
import emoji
from twilio.twiml.messaging_response import MessagingResponse
from scraper import *
from helper_functions import normalize_text

app = Flask(__name__)


@app.route('/', methods=['POST'])


def bot():
    incoming_msg = normalize_text(request.values.get('Body'))
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    departamentos = ['Bolivia', 'Nacional', 'Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosí','Santa Cruz','Tarija']

    if 'hi' in incoming_msg or 'hola' in incoming_msg or 'holi' in incoming_msg or 'menu' in incoming_msg:
        text = f'''*Hola!* 👋🏼\nSoy Corona Bot 👑🤖, el robot mas 🔝 de esta cuarentena!\n\nA tus ordenes!\n
¿Quieres saber las estadisticas de coronavirus en Bolivia 🇧🇴? \n
🦠️ Envia el *nombre del departamento* o la palabra *nacional* para datos de todo el pais. \n
🦠️ Envia *sintomas* para información acerca de los síntomas y recomendaciones.️\n
🦠 Envia *evaluacion* para ir a una autoevaluacion de COVID-19.\n
🦠 Envia *ayudar* para informarte como puedes ayudar.\n
🦠 Envia *comunicado* para recibir el ultimo comunicado oficial.\n
🦠 Envia *mundo* para recibir una noticia sobre COVID-19 en el mundo.\n


*#QuedateEnCasa*
'''
        msg = msg.body(text)
        responded = True

    if any(dep.lower().replace(' ', '_') in incoming_msg.replace(' ', '_') for dep in departamentos):
        fecha, info = get_info(incoming_msg)
        text = f"""
*{info[0]}*
Al día {fecha} 
Nuevos casos: {info[1]}
Total casos: {info[2]}
Decesos: {info[3]}
Recuperados: {info[4]}

    """
        msg = msg.body(text)
        responded = True

    if 'sintoma' in incoming_msg:
        text = '''Si tienes los uno de estos síntomas y tuviste contacto cercano con algún caso positivo o sospechoso de COVID-19, o estuviste en alguna región de Bolivia o el exterior con casos positivos ponte en contacto con las líneas gratuitas.
\n 📞 800 10 1104
\n 📞 800 10 1106'''
        img_address = 'https://www.boliviasegura.gob.bo/images/covid2.jpg'
        msg.body(text)
        msg.media(img_address)
        responded = True

    if 'evaluacion' in incoming_msg:
        text = '''*¿Te sientes enfermo?* 🤒 \n
Evalúa tu estado de salud en línea, registra tus síntomas, recibe instrucciones y recomendaciones sobre el Coronavirus COVID-19 de acuerdo los protocolos establecidos por la Organización Mundial de la Salud y el Gobierno del Estado Plurinacional de Bolivia.
\n\nautoevaluacioncovid19.agetic.gob.bo'''
        msg.body(text)
        responded = True

    if 'ayuda' in incoming_msg:
        text = '''*¿Quieres ayudar?* \n
En los siguientes links entontraras informacion de formas para donar a la gente que mas lo necesita:

*_COVID BOLIVIA_*
❤️ www.covid-bolivia.com/donaciones

*_Una Mano Para Mamá_*
❤️ gf.me/u/xycj2f'''
        msg.body(text)
        responded = True

    if 'comunicado' in incoming_msg:
        text, img_address = get_comm()
        msg.body(text)
        msg.media(img_address)
        responded = True

    if 'plague' in incoming_msg or 'mundo' in incoming_msg:
        text = '😬'
        img_address = plague()
        msg.body(text)
        msg.media(img_address)
        responded = True

    if responded == False:
        msg.body('''Lo siento, no tengo implementada esa opción aún...\n
Para mas informacion visita: 
boliviasegura.gob.bo''')
    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
