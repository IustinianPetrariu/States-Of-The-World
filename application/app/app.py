from flask import Flask,request,jsonify 
from flask.helpers import make_response
from setup.configuration import config
import psycopg2 

app = Flask(__name__) 

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/top-10-countries/<value>",methods = ['GET'])
def top_response(value):
    # check if the user input is correct 
    if not value in ['density', 'population','surface']:
       return make_response(jsonify({"error":"Your input is not correct, information missing.."}), 400)
    response = []
    connection = None 
    try: 
        #read connection parameters from configuration file
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        #create a cursor 
        cursor = connection.cursor()
        # execute a statement
        query = f'''SELECT ID,NAME,{value} FROM COUNTRIES ORDER BY {value} DESC limit 10; '''
        cursor.execute(query)
        rows = cursor.fetchall() 
        #close the cursor
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return make_response(jsonify({"message":error}), 500)
    finally:
        if connection is not None:
            connection.close()
    # prepare the response for user 
    for row in rows:
        dictionary = {'id' : int(row[0]), 'name':row[1], value :float(row[2])} 
        response.append(dictionary)
    return make_response(jsonify(response),200)
    

@app.route("/countries/<category>/<value>",methods = ['GET'])
def response(category,value):
     # check if the user input is correct 
    if not category in ['timezone', 'languages','governance']:
       return make_response(jsonify({"error":"Your input is not correct, information missing.."}), 400)
    response = []
    connection = None 
    try: 
        #read connection parameters from configuration file
        params = config()
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        #create a cursor 
        cursor = connection.cursor()
        # execute a statement
        query = f'''SELECT ID,NAME,{category} FROM COUNTRIES WHERE {category} LIKE '%{value}%' '''
        print(query,(category,category,value))
        cursor.execute(query)
        rows = cursor.fetchall() 
        #close the cursor
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return make_response(jsonify({"message":error}), 500)
    finally:
        if connection is not None:
            connection.close()
    # prepare the response for user 
    for row in rows:
        dictionary = {'id' : int(row[0]), 'name':row[1], category:row[2]} 
        response.append(dictionary)
    return make_response(jsonify(response),200)



















