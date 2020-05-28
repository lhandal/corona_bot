from flask import Flask, request
import requests
import os
import json
import datetime
import emoji
from twilio.twiml.messaging_response import MessagingResponse
from scraper import *

app = Flask(__name__)


@app.route('/', methods=['POST'])


def bot():
    incoming_msg = request.values.get('Body').lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    departamentos = ['Nacional', 'Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosí','Santa Cruz','Tarija']

    if 'hi' in incoming_msg or 'hola' in incoming_msg or 'holi' in incoming_msg or 'menu' in incoming_msg:
        text = f'''*Hola!* 👋🏼\nSoy Corona Bot, el robot mas 🔝 de esta cuarentena!\n\nA tus ordenes!\n
¿Quieres saber las estadisticas de coronavirus en algun departamento de Bolivia 🇧🇴? \n\n Puedes mandarme el nombre del departamento o la palabra "nacional" para datos de todo el pais!'''
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

    if 'todo' in incoming_msg:
        for i in departamentos:

            fecha, info = get_info(i)
            part = f"""
            *{info[0]}*
            Al día {fecha} 
            Nuevos casos: {info[1]}
            Total casos: {info[2]}
            Decesos: {info[3]}
            Recuperados: {info[4]}

            """
            text += part + '\n'
        msg = msg.body(text)
        responded = True

    if responded == False:
        msg.body('Lo siento, no tengo implementada esa opción aún...')

    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)