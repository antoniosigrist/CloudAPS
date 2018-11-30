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

