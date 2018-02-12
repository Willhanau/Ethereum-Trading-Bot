#!/bin/bash

#install required packages
sudo easy_install pip virtualenv

#create virtual python environment
if [ ! -f "./bot_environment" ]; then
  virtualenv ./bot_environment
fi

#enter virtualenv
source bot_environment/bin/activate

#install required python packages
pip install twilio coinbase flask
