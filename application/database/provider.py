import database as database 
import os

import csv


csv_file = '../../crawler/Content/data.csv'

def checkFiles():
    if os.path.exists(csv_file):
        print("csv file ready") 
    else:
        print("csv file doesn't exists")
        quit()
        

def create_table(db):
    # create table in the PostgreSQL database 
    commands = (
                """
                 DROP TABLE IF EXISTS countries
                """,
                """  CREATE TABLE countries (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        capital VARCHAR(100) NOT NULL,
                        surface numeric,
                        neighbours text,
                        timezone text,
                        density numeric,
                        population numeric,
                        languages text,
                        governance text
                        )
                """)         
    try:
        cursor = db.cursor()
        for command in commands:
            cursor.execute(command)
            # close communication with the PostgreSQL database server
        cursor.close()
            # commit the changes
        db.commit()
    except (Exception) as error:
        print(error)

#  (row[0],row[1],float(row[2]),row[3],row[4],float(row[5]),float(row[6]),row[7],row[8],row[9])
def insert_data(db, csv_file):
    try:
        cursor = db.cursor()
        with open(csv_file,encoding='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            next(csv_reader) # Skip the header row.
            for row in csv_reader:
                  cursor.execute(
                  "INSERT INTO countries (name,capital,surface,neighbours, timezone, density, population, languages,governance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                   row
                                )
            # close communication with the PostgreSQL database server
        cursor.close()
            # commit the changes
        db.commit()
    except (Exception) as error:
        print(error)


def importToDatabase(csv_file):
    db = database.get_connection()
    if db:
        print("Connected to database!")
    else:
        print("database is not working!")
    create_table(db)
    insert_data(db,csv_file)
    db.close()


def main():
   checkFiles()
   importToDatabase(csv_file)
   


if __name__ == "__main__":
    main()


