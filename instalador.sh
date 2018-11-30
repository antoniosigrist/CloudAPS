#!/bin/bash
sudo apt -y update
sudo apt install snapd
sudo apt install -y python-pip 
git clone https://github.com/antoniosigrist/CloudAPS.git
pip install boto3
pip install awscli --upgrade --user
pip install Flask
pip install requests
cd CloudAPS/
aws configure
export FLASK_APP=instalador.py
python -m flask run --host=0.0.0.0