import database as database
import os
import csv

csv_file = '../../crawler/Content/data.csv'


def check_files():
    """
    verify if files where crawler store data exists.

    """
    if os.path.exists(csv_file):
        print("csv file ready")
    else:
        print("csv file doesn't exists")
        quit()


def create_table(db):
    """
    Used to drop existing tables and create new ones to store data.
    
    :param db: used for communication with database
    """
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
    except Exception as error:
        print(error)


def insert_data(db, csv_file):
    """
    Read the file where data is stored and then write information in database.

    :param db : used to communicate with database
    :param csv_file: where information collected by crawler is stored.
    """
    try:
        cursor = db.cursor()
        with open(csv_file, encoding='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            next(csv_reader)  # Skip the header row.
            for row in csv_reader:
                cursor.execute(
                    "INSERT INTO countries (name,capital,surface,neighbours, timezone, density, population, languages,"
                    "governance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    row
                )
        # close communication with the PostgreSQL database server
        cursor.close()
        # commit the changes
        db.commit()
    except (Exception) as error:
        print(error)


def import_to_database(csv_file):
    """
    Insert data collected by crawler in the database.
    Clear all created tables and create new ones.

    :param csv_file: used to collect data from a
    specif folder where crawler write data.
    """
    db = database.get_connection()
    if db:
        print("Connected to database!")
    else:
        print("database is not working!")
    create_table(db)
    insert_data(db, csv_file)
    db.close()


def main():
    """
    Main function used to check for files and import data

    """
    check_files()
    import_to_database(csv_file)


if __name__ == "__main__":
    main()
