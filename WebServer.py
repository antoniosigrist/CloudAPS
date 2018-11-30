from flask import Flask,request,render_template, Response
import requests
#import request as req


dic = {}

primarykey = len(dic)


def adicionaTarefa(tarefa):

	global dic
	global primarykey

	dic[str(primarykey)] = tarefa
	primarykey += 1


app = Flask(__name__)


@app.route("/", methods=['GET'])

def index():  
    return "200"

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

			return dic.text

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
