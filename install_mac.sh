#!/bin/bash

#install required packages
sudo easy_install pip virtualenv

#install homebrew
#/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

#brew install redis

#create virtual python environment
if [ ! -f "EthBot_environment" ]; then
  virtualenv EthBot_environment
fi

#enter virtualenv
source EthBot_environment/bin/activate

#install required python packages
pip install -r requirements_python.txt
