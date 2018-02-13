# Ethereum-Trading-Bot

#start virtual environment
cd Ethereum-Trading-Bot
source EthBot_environment/bin/activate

#source env variables
source bot_env_variables.env

#start celery server
celery -A EthBot_flask.celery worker

#run flask app in seperate console
python EthBot_flask.py
