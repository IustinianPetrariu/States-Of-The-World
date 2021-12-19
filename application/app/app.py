from flask import Flask,request,jsonify 
app = Flask(__name__) 

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post("/database")
def create_database():
    pass
    
    


