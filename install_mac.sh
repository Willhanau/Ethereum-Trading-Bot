#!/bin/bash

#install required packages
sudo easy_install pip virtualenv

#install homebrew
#/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

#brew install redis

#create virtual python environment
if [ ! -f "./bot_environment" ]; then
  virtualenv ./bot_environment
fi

#enter virtualenv
source bot_environment/bin/activate

#install required python packages
pip install twilio coinbase flask celery[redis] schedule
