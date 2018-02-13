# Ethereum-Trading-Bot

### Start flask app
```bash
cd Ethereum-Trading-Bot
#start virtual environment
source EthBot_environment/bin/activate
#source environment variables that the flask app needs
source bot_env_variables.env
#use setsid to run in background
setsid python EthBot_flask.py
```

### Start celery server in separate terminal
```bash
cd Ethereum-Trading-Bot
source EthBot_environment/bin/activate
source bot_env_variables.env
setsid celery -A EthBot_flask.celery worker
```
When exiting both terminals the celery and flask server will continue to run.
