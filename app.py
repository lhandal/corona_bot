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

    if 'hi' in incoming_msg or 'hola' in incoming_msg or 'holi' in incoming_msg or 'menu' in incoming_msg:
        text = f'*Hola!* 👋🏼\nSoy Juan, el robot mas 🔝 de esta cuarentena!\n\nA tus ordenes!'
        msg = msg.body(text)
        responded = True

    if 'la paz' in incoming_msg:
        text = str(get_info('la paz'))
        msg = msg.body(text)
        responded = True

    if responded == False:
        msg.body('I only know about corona, sorry!')

    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)