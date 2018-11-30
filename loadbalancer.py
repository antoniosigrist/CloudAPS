#!/usr/bin/env
# -*- coding: utf-8 -*-

import boto3
import sys
from random import randint
from flask import Flask,request,render_template, Response
import requests
import json
from pprint import pprint
import threading



s3 = boto3.resource('s3')
ec2_ = boto3.resource('ec2',region_name='us-east-1')#,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ec2 = boto3.client('ec2',region_name='us-east-1')#,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY) 
client = ec2
lista_ips = []
ip_dic = {}
loadbalancer = []
agregadora = []
lista_ids = []

def escolheIp(lista_ips):

	ip = None

	while ip == None:

		n = int(randint(0,len(lista_ips)-1))
		ip = lista_ips[n]

		return ip


app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

	if request.method == 'POST':

		try:

			json = request.get_json()
			res = requests.post(server_addr, json=json)

			return res

		except:

		 	print("POST ERROR")

	else:

		try:	
			r = requests.get(server_addr)
			return r
		except:

			print("GET ERROR")

			return "ERROR GET /Tarefa"
### Apagando uma key pair

try: 

	response = ec2.delete_key_pair(
    KeyName = 'antonio2',
    DryRun = False
	)

except Exception as e:
    print(e)
    print("Chave nao existe")

# ### Criando uma key pair

try:

	file = open('antonio2.pub','r')

	response = ec2.import_key_pair(
    KeyName = 'antonio2',
    DryRun = False,
    PublicKeyMaterial=file.read()
	)
	file.close()

except Exception as e:

	print ("Erro ao importar chave")
	print(e)

	response = client.describe_key_pairs(
	    
	    KeyNames=[

	        'antonio2',
	    ],
	    DryRun=False
	)

### Apagando um security grup

try:

	response = client.delete_security_group(
	    GroupName='APS',
	    GroupId='sg-0e7c5c438430609d2',
	    DryRun=False
	)

except Exception as e:
	print("Erro ao apagar grupo de seguranca")
	print(e)


### Criando um security grup


try:

	response = client.create_security_group(
    Description='APS Criacao',
    GroupName='APS',
    VpcId='vpc-219b565b',
    DryRun=False
	)

	ec2.authorize_security_group_ingress(
	GroupId=response['GroupId'],
	IpProtocol="tcp",
	CidrIp="0.0.0.0/0",
	FromPort=22,
	ToPort=22
	)

	ec2.authorize_security_group_ingress(
	GroupId=response['GroupId'],
	IpProtocol="tcp",
	CidrIp="0.0.0.0/0",
	FromPort=5000,
	ToPort=5000
	)
	ec2.authorize_security_group_ingress(
	GroupId=response['GroupId'],
	IpProtocol="tcp",
	CidrIp="0.0.0.0/0",
	FromPort=80,
	ToPort=80
	)
	


except Exception as e:

	print("Erro ao criar grupo de seguranca")
	print(e)


## Criando uma instancia Ubuntu 18
def criarInstancia(user_data,numero,tag):

	for i in range (0,numero):

		try:


			instance = ec2_.create_instances(
			#sudo apt-get install -y <package-name>
			    ImageId='ami-0ac019f4fcb7cb7e6',
			    MinCount=1,
			    MaxCount=1,
			    KeyName='antonio2',
			    InstanceType='t2.micro',
			    UserData=user_data,
			    TagSpecifications=[
		        {
		            'ResourceType': 'instance',
		            'Tags': [
		                {
		                    'Key': tag,
		                    'Value': "Antonio"
		                },
		            ]
		        },
		    ],
			    SecurityGroupIds=[response['GroupId']])

			id_ = str(instance[0].id)

			lista_ids.append(id_)

			# Wait for the instance to enter the running state

			print("Esperando rodar")

			instance = instance[0]

			instance.wait_until_running()

			# Reload the instance attributes
			instance.load()

			try:

				ip_dic[instance.instance_id] = instance.public_ip_address

			except:

				print("Não deu para inserir no dic")

		except Exception as e:

			print("Erro para criar uma instancia")
			print(e)


user_data_load = '''#!/bin/bash
sudo apt-get -y update
sudo apt install snapd
sudo apt install -y python-pip 
sudo apt-get install -y python-pip git awscli
git clone https://github.com/antoniosigrist/CloudAPS.git
pip install boto3
pip install Flask
pip install requests
cd ..
cd ..
cd CloudAPS/
export FLASK_APP=loadbalancer.py
python -m flask run
'''
user_data_agreg = '''#!/bin/bash
sudo apt-get -y update
sudo apt install snapd
sudo apt install -y python-pip 
sudo apt-get install -y python-pip git awscli
git clone https://github.com/antoniosigrist/CloudAPS.git
pip install boto3
pip install Flask
pip install requests
cd ..
cd ..
cd CloudAPS/
export FLASK_APP=WebServer.py
python -m flask run
'''

criarInstancia(user_data_load,1,"Owner")

for i in ip_dic:

	loadbalancer.append(i)
	loadbalancer.append(ip_dic[i])

criarInstancia(user_data_agreg,1,"Agregadora")

for i in ip_dic:

	if i != loadbalancer[0]:
		agregadora.append(i)
		agregadora.append(ip_dic[i])

print("IP Agregadora: "+agregadora[1])



def checkhealth(ip_dic,agregadora):

	user_data = """#!/bin/bash
	sudo apt-get -y update
	sudo apt install snapd
	sudo apt install -y python-pip 
	sudo apt-get install -y python-pip git awscli
	git clone https://github.com/antoniosigrist/CloudAPS.git
	pip install boto3
	pip install Flask
	pip install requests
	cd ..
	cd ..
	cd CloudAPS/
	export FLASK_APP=curiosidades.py {}
	python -m flask run
	""".format(agregadora[1])

	lista_ips_excluidos = []

	while(1):

		ipsativos = -2
		lista_ips = []
		

		for instance in ec2_.instances.all():

			if instance.instance_id in ip_dic and instance.state['Name'] != 'running':

				print ("IP Excluido "+str(instance.public_ip_address))

				lista_ips_excluidos.append(instance.public_ip_address)

				ip_dic[instance] = False

				print ("ip_dic pos none")

				print (ip_dic)

			if instance.state['Name'] == 'running':

				ipsativos += 1


		while ipsativos < 1:

			criarInstancia(user_data,1, "Owner2")
			ipsativos += 1

		random_number = randint(0,len(ip_dic)-1)
		print ("ip_dic fora")
		print (ip_dic)

		for i in ip_dic:

			if ip_dic[i] != False:

				lista_ips.append(ip_dic[i])

		for i in lista_ips:

			if i in lista_ips_excluidos:

				lista_ips.delete(i)

		random_number = randint(0,len(lista_ips)-1)
		random_ip = lista_ips[random_number]

		print("Lista de Ips disponiveis: ")
		print(lista_ips)


		while random_ip == loadbalancer[1] or random_ip == agregadora[1]:

			random_number = randint(0,len(lista_ips)-1)
			random_ip = lista_ips[random_number]



		server_addr = "http://"+random_ip+":5000/Tarefa/"

		print ("Endereco randomico: "+ server_addr)


threading.Thread(target=checkhealth,args = [ip_dic,agregadora]).start()

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)


# https://gist.github.com/ableasdale/8cb7a61cad3202e09bab3e11c4639133





