from flask import Flask,request,render_template, Response
import requests
import json



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

if __name__ == '__main__':
   app.run(host='0.0.0.0')





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