from flask import Flask,request,render_template, Response
from aps1 import *
import requests
#import request as req

import os.path


def root_dir():  

    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename): 

    try:

        src = os.path.join(root_dir(), filename)

        return open(src).read()

    except IOError as exc:

        return str(exc)


app = Flask(__name__)


@app.route("/", methods=['GET'])

def index():  

    content = get_file('home.html')
    return Response(content, mimetype="text/html")

@app.route("/Tarefa/", methods=['POST','GET'])
def tarefas():

	print(request.method)

	if request.method == 'POST':

		try:

			data = request.get_json()
			
			value = data.split(":")[1]

			adicionaTarefa(value)

			print (dic)

			return "Rodou POST /Tarefa/"

		except:

		 	print("POST ERROR")

	else:

		try:
			dic_list = []

			for k,v in dic.items():
				
				dic_list.append(v)

			print (dic_list)

			return "Rodou GET /Tarefa/"

		except:

			print("GET ERROR")

			return "ERROR GET /Tarefa"

@app.route("/Tarefa/<int:id_>",methods=['GET', 'PUT','DELETE'])
def arruma(id_):

	print(request.method)

	if request.method == 'GET':
		print((dic[str(id_)]))
		return  "Rodou GET /TAREFA/ID"

	elif request.method == 'PUT':

		value = str(request.get_data())

		print(value)

		value = value.split("=")[1]

		dic[str(id_)] = value

		print (dic)

		return  "Rodou PUT /TAREFA/ID"


	elif request.method == 'DELETE':
		del dic[str(id_)]
		print (dic)
		return  "Rodou DELETE /TAREFA/ID"

@app.route("/healthcheck/")
def healthcheck():
	print("Rodou")
	return "200"

# if __name__ == '__main__':
#    app.run(host='0.0.0.0')
