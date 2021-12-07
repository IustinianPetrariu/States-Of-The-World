from flask import Flask,request,jsonify 

app = Flask(__name__) 

@app.route('/')
def hello_world():
    return 'Hello, World!'

# @app.get("/countries")
# def get_countries():
#     return jsonify(countries)


