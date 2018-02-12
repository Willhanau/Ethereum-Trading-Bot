#!/bin/bash

#install required packages
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python2.7 python-pip virtualenv redis

#create virtual python environment
if [ ! -f "bot_environment" ]; then
  virtualenv ./bot_environment
fi

#enter virtualenv
source bot_environment/bin/activate

#install required python packages
pip install -r requirements.txt
