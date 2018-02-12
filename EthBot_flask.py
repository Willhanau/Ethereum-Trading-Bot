#!/usr/bin/env python

from os import environ
from time import sleep
from twilio.rest import Client as twilio_Client
from twilio.twiml.messaging_response import MessagingResponse
from coinbase.wallet.client import Client as coinbase_Client
from flask import Flask, request, redirect

#figure out way to source file variables in python script
#manual way: source bot_env_variables.env

#twilio variables
USER_NUMBER = environ.get("USER_NUMBER")
TWILIO_NUMBER = environ.get("TWILIO_NUMBER")
ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN")

#coinbase variables
COINBASE_READ_API_KEY = environ.get("COINBASE_READ_API_KEY")
COINBASE_READ_SECRET_KEY = environ.get("COINBASE_READ_SECRET_KEY")

#create connections to client APIs
twilio_client = twilio_Client(ACCOUNT_SID, AUTH_TOKEN)
coinbase_client = coinbase_Client(COINBASE_READ_API_KEY, COINBASE_READ_SECRET_KEY)

#App variables
eth_price_updates = True

def get_eth_price():
    buy_price = coinbase_client.get_buy_price(currency_pair = 'ETH-USD')
    sell_price = coinbase_client.get_sell_price(currency_pair = 'ETH-USD')
    return "Ethereum:\nBuy Price: ${}\nSell Price: ${}".format(buy_price.amount, sell_price.amount)

def send_twilio_message(message):
    twilio_message = twilio_client.messages.create(to = USER_NUMBER, from_ = TWILIO_NUMBER, body = message,)
    print(twilio_message.sid)

def eth_price_update(time):
    while(True):
        eth_price = get_eth_price()
        send_twilio_message(eth_price)
        sleep(time)

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def incoming_sms_response():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    # Start our TwiML response
    resp = MessagingResponse()
    if body == 'u':
        resp.message(get_eth_price)
    elif body == 'b':
        resp.message("1 Ethereum Bought!")
    elif body == 's':
        resp.message("1 Ethereum Sold!")
    elif body == "stop updates":
        resp.message("Ethereum Price Updates Have Stopped.")
        eth_price_updates = False
    elif body == "start updates":
        resp.message("Ethereum Price Updates Have Resumed!")
        eth_price_updates = True
        eth_price_update(3600)
    return str(resp)

if __name__ == '__main__':
    #eth_price_update(3600)
    app.run()
