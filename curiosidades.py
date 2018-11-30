from flask import Flask,request,render_template, Response
import requests
import json
import sys
import os


app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

	if request.method == 'POST':

		try:

			json = request.get_json()
			res = requests.post(server_addr, json=json)

			return res.text

		except:

		 	print("POST ERROR")

	else:

		try:

			r = requests.get(server_addr)
			return r.text
			
		except:
			
			print("GET ERROR")

			return "ERROR GET /Tarefa"

if __name__ == '__main__':

	server_addr = os.environ.get('DB_HOST')

	print(server_addr)

	server_addr = "http://"+server_addr+":5000/Tarefa/"
	app.run(host='0.0.0.0')




	

# def adicionaLista(loadbalancer):

# 	response = ec2_.instances.filter(Filters=[{
# 	'Name': "instance-state-name",
# 	'Values': ['running']
# 	}])


	# for instance in response:

	# 	for tag in instance.tags:

	# 		if "Owner" in tag['Key']:

	# 			if instance.instance_id not in ip_dic:

	# 				ip_dic[instance.instance_id] = instance.public_ip_address
	# 				loadbalancer.append(instance.instance_id)
	# 				loadbalancer.append(instance.public_ip_address)

	# 		elif "Owner2" in tag['Key']:
	# 			if instance.instance_id not in ip_dic:

	# 				print("Adicionou owner 2")
	# 				ip_dic[instance.instance_id] = instance.public_ip_address

	# 	return loadbalancer






"""#!/bin/bash
	cd home
	cd ubuntu
	sudo rm /var/lib/dpkg/lock
	sudo dpkg --configure -a
	sudo rm /var/lib/apt/lists/lock
	sudo rm /var/cache/apt/archives/lock
	sudo apt-get -y update
	sudo apt install -y python-pip 
	git clone https://github.com/antoniosigrist/CloudAPS.git
	pip install boto3
	pip install Flask
	pip install requests
	cd CloudAPS/
	export FLASK_APP=curiosidades.py {}
	python -m flask run"""