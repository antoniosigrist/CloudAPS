#!/usr/bin/env
# -*- coding: utf-8 -*-

import boto3
import sys
from random import randint
from flask import Flask,request,render_template, Response
import requests
import json
from pprint import pprint



s3 = boto3.resource('s3')
ec2_ = boto3.resource('ec2',region_name='us-east-1')#,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ec2 = boto3.client('ec2',region_name='us-east-1')#,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY) 
client = ec2
lista_ips = []
ip_dic = {}
loadbalancer = []
lista_ids = []

def escolheIp(lista_ips):

	ip = None

	while ip == None:

		n = int(randint(0,len(lista_ips)-1))
		ip = lista_ips[n]

		return ip


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
		                    'Value': 'Antonio'
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


user_data = '''#!/bin/bash
			sudo apt-get -y update
			sudo apt install snapd
			sudo apt install -y python3-pip 
			sudo apt-get install -y python-pip git awscli
			git clone https://github.com/antoniosigrist/CloudAPS.git
			pip install boto3
			pip install Flask
			pip install requests
			cd ..
			cd ..
			cd CloudAPS/
			export FLASK_APP=s3.py
			python -m flask run
			'''

criarInstancia(user_data,1,"Owner")

for i in ip_dic:

	loadbalancer.append(i)
	loadbalancer.append(ip_dic[i])

def adicionaLista(loadbalancer):

	response = ec2_.instances.filter(Filters=[{
	'Name': "instance-state-name",
	'Values': ['running']
	}])


	for instance in response:

		for tag in instance.tags:

			if "Owner" in tag['Key']:

				if instance.instance_id not in ip_dic:

					ip_dic[instance.instance_id] = instance.public_ip_address
					loadbalancer.append(instance.instance_id)
					loadbalancer.append(instance.public_ip_address)

			elif "Owner2" in tag['Key']:
				if instance.instance_id not in ip_dic:

					print("Adicionou owner 2")
					ip_dic[instance.instance_id] = instance.public_ip_address

		return loadbalancer


#loadbalancer = adicionaLista(loadbalancer)

user_data = '''#!/bin/bash
			sudo apt-get -y update
			sudo apt install snapd
			sudo apt-get -y install python
			sudo apt-get --assume-yes install python-pip
			pip install boto3
			pip install Flask
			git clone https://github.com/antoniosigrist/CloudAPS.git
			pip install requests
			cd ..
			cd ..
			cd CloudAPS
			export FLASK_APP=WebServer.py
			python -m flask run --host=0.0.0.0
			'''
		
criarInstancia(user_data,1,"Owner2")


#loadbalancer = adicionaLista(loadbalancer)

print("IP LB: "+ loadbalancer[1])

random_number = randint(0,len(ip_dic)-1)

for i in ip_dic:

	lista_ips.append(ip_dic[i])

random_ip = lista_ips[random_number]

print("IP DIC")
print(ip_dic)

while random_ip == loadbalancer[1]:

	random_number = randint(0,len(ip_dic)-1)
	random_ip = lista_ips[random_number]
	#print("Random IP: "+random_ip)


server_addr = "http://"+random_ip+":5000/Tarefa/"

print ("Endereco randomico: "+ server_addr)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

	if request.method == 'POST':

		try:

			json = request.get_json()
			res = requests.post(server_addr, json=json)

		except:

		 	print("POST ERROR")

	else:

		try:	
			r = requests.get(server_addr)
			return r
		except:
			print("GET ERROR")

			return "ERROR GET /Tarefa"

if __name__ == '__main__':
   app.run(host='0.0.0.0')



