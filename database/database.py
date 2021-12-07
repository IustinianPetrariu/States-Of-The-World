import psycopg2 
from setup.configuration import config

def connect():
    """Connect to the PostgreSQL database server"""

    connection = None 
    try: 
        #read connection parameters from configuration file
        params = config()

        #connect to the PostgreSQl server 
        print("Connecting to the PostgreSQL database...") 
        connection = psycopg2.connect(**params)

        #create a cursor 
        cursor = connection.cursor()

        print('PostgreSQL database version:')
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)

        #close the cursor
        cursor.close()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
       

def get_connection():
    connection = None
    try: 
        #read connection parameters from configuration file
        params = config()

        #connect to the PostgreSQl server 
        print("Connecting to the PostgreSQL database...") 
        connection = psycopg2.connect(**params) 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            print("Succesfully")
            return connection


if __name__ == '__main__':
    connect()








