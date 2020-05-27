from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# msg.body('this is the response text')
# msg.media('https://example.com/path/image.jpg')

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'hola' in incoming_msg :
        text = f'Hola bola!'
        msg.body(text)
        responded = True

    return str(resp)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)