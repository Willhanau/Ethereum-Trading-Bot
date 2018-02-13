#!/usr/bin/env python

from os import environ
from time import sleep
from twilio.rest import Client as twilio_Client
from twilio.twiml.messaging_response import MessagingResponse
from coinbase.wallet.client import Client as coinbase_Client
from flask import Flask, request, redirect
from celery_flask import make_celery

#figure out way to source file variables in python script
#manual way: source bot_env_variables.env

#twilio variables
USER_NUMBER = environ.get("USER_NUMBER")
TWILIO_NUMBER = environ.get("TWILIO_NUMBER")
TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN")

#coinbase variables
COINBASE_READ_API_KEY = environ.get("COINBASE_READ_API_KEY")
COINBASE_READ_SECRET_KEY = environ.get("COINBASE_READ_SECRET_KEY")

#create connections to client APIs
twilio_client = twilio_Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
coinbase_client = coinbase_Client(COINBASE_READ_API_KEY, COINBASE_READ_SECRET_KEY)

#App variables
price_updates = {"enabled": False, "celery_task": None}

def get_eth_price():
    buy_price = coinbase_client.get_buy_price(currency_pair = 'ETH-USD')
    sell_price = coinbase_client.get_sell_price(currency_pair = 'ETH-USD')
    return "Ethereum:\nBuy Price: ${}\nSell Price: ${}".format(buy_price.amount, sell_price.amount)

def send_twilio_message(message):
    twilio_message = twilio_client.messages.create(to = USER_NUMBER, from_ = TWILIO_NUMBER, body = message,)
    print(twilio_message.sid)

def eth_price_update(time):
    while(eth_price_updates_enabled):
        eth_price = get_eth_price()
        send_twilio_message(eth_price)
        sleep(time)

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task(name='EthBot_flask.periodic_price_update')
def periodic_price_update(time):
    while(1):
        eth_price = get_eth_price()
        send_twilio_message(eth_price)
        sleep(time)

@app.route('/')
def Test():
    return "Testing: Flask app is running!"

@app.route('/sms', methods=['POST'])
def incoming_sms_response():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body').lower().strip()
    from_num = request.values.get('From')
    # Start our TwiML response
    resp = MessagingResponse()
    if from_num == USER_NUMBER:
        if body == 'u':
            resp.message(get_eth_price())

        elif body == 'b':
            resp.message("1 Ethereum Bought!")

        elif body == 's':
            resp.message("1 Ethereum Sold!")

        elif body == "stop updates":
            if price_updates["enabled"]:
                resp.message("Ethereum price updates have stopped.")
                price_updates["enabled"] = False
                price_updates["celery_task"].revoke(terminate=True)
            else:
                resp.message("Ethereum price updates are already disabled!")

        elif body == "start updates":
            if price_updates["enabled"]:
                resp.message("Ethereum price updates are already in effect!")
            else:
                resp.message("Ethereum price updates have resumed!")
                price_updates["enabled"] = True
                price_updates["celery_task"] = periodic_price_update.delay(3600)

        else:
            resp.message("Text Options:\n U: Get current Ethereum coinbase price.\n B: Buy 1 Ethereum.\n S: Sell 1 Ethereum.\n Stop Updates: Stop automatic Ethereum price updates.\n Start Updates: Start automatic Ethereum price updates.")
    else:
        resp.message("Unauthorized User.")

    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
