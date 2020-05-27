from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/bot', methods=['POST', 'GET'])
def bot():
    incoming_msg = request.values.get('Body', '')
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'Hi' in incoming_msg or 'Hey' in incoming_msg or 'Heya' in incoming_msg or 'Menu' in incoming_msg:
        text = f'Hello hello'
        msg.body(text)
        responded = True

    if responded == False:
        msg.body('I only know about corona, sorry!')

    return str(resp)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)