from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World! Available services: /Put"

@app.route("/Put", methods = ["POST", "PUT"])
def putResource():
	if request.method == "POST":
		print("Received POST data:" + request.get_data().decode("utf-8"))
		return("OK")
	if request.method == "PUT":
		print("Received PUT data:" + request.get_data().decode("utf-8"))
		return("OK")
