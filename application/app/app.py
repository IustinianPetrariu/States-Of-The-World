from flask import Flask,request,jsonify 
from flask.helpers import make_response
from setup.configuration import config
import psycopg2 

app = Flask(__name__) 

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/top-10-countries-density",methods = ['GET'])
def create_database():
    
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
        query = 'SELECT ID,NAME,DENSITY FROM COUNTRIES ORDER BY DENSITY DESC limit 10;'
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
        dictionary = {'id' : int(row[0]), 'name':row[1], 'density:':float(row[2])} 
        response.append(dictionary)
    return make_response(jsonify(response),200)
    


