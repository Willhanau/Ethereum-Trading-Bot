#!/usr/bin/env python
from os import environ
from time import sleep
from twilio.rest import Client as twilio_Client
from coinbase.wallet.client import Client as coinbase_Client

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

def get_eth_price():
    buy_price = coinbase_client.get_buy_price(currency_pair = 'ETH-USD')
    sell_price = coinbase_client.get_sell_price(currency_pair = 'ETH-USD')
    return "Ethereum:\nBuy Price: ${}\nSell Price: ${}".format(buy_price.amount, sell_price.amount)

def send_twilio_message(message):
    twilio_message = twilio_client.messages.create(to = USER_NUMBER, from_ = TWILIO_NUMBER, body = message,)
    print(twilio_message.sid)

def main():
    while(True):
        eth_price = get_eth_price()
        send_twilio_message(eth_price)
        sleep(3600)
    return 0

main()
