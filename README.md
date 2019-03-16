# Ethereum-Trading-sms

##Description
This is an app that uses the twilio and coinbase api to check the current Ethereum price, buy/sell ones ethereum, recieve ethereum price updates all via sms. Was a personal project to learn how to use the twilio and coinbase REST APIs.

### Port forward using iptables
```bash
#will forward all port 80 traffic to port 8080(flask server is on port 8080)
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

### Start flask app
```bash
cd Ethereum-Trading-sms

#start virtual environment
source EthBot_environment/bin/activate

#source environment variables that the flask app needs
source bot_env_variables.env

#use setsid to run in background
setsid python EthBot_flask.py
```

### Start celery server in separate terminal
```bash
cd Ethereum-Trading-sms
source EthBot_environment/bin/activate
source bot_env_variables.env
setsid celery -A EthBot_flask.celery worker
```
When exiting both terminals the celery and flask server will continue to run.
