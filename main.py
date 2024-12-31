import os

# Get the current working directory
CURRENT_PATH = os.getcwd()
BKP_PATH = os.path.join(CURRENT_PATH,"bkp")
# create bkp file if not exists
if not os.path.exists(BKP_PATH):
    os.makedirs(BKP_PATH)

import argparse

# parse db connection args
parser = argparse.ArgumentParser(description='Database connection arguments')
parser.add_argument('--host',default='localhost',help="database host")
parser.add_argument('-p','--port',default='3306',help="database port")
parser.add_argument('-u','--username',default='root',help="database username")
parser.add_argument('-pwd','--password',default='admin',help="database password")
parser.add_argument('-db','--db_name',default='ecom_db',help="database name")
parser.add_argument('-d','--destination',default=r'D:\test\github\db-backup-utility\main.py',help="destination folder for backup files")
args = parser.parse_args()


# get params/cred for db_backup
host =args.host
port =args.port
username =args.username
password =args.password
db_name =args.db_name
destination =args.destination


# connect to db

from myconnection import connect_to_mysql

config = {
    "host": host,
    "user": username,
    "password": password,
    "database": db_name,
}


def connect_to_db():

    cnx = connect_to_mysql(config, attempts=3)

    if cnx and cnx.is_connected():

        with cnx.cursor() as cursor:


            fetch_tables(cursor)
            
            # result = cursor.execute("SELECT * FROM product_dtl")
            
        cnx.close()

    else:

        print("Could not connect")

# get list of all tables

def fetch_tables(cursor):
    result = cursor.execute("SHOW TABLES;")

    all_tables = cursor.fetchall()

    for table_name in all_tables:

        table_name = table_name[0]

        table_qry = f"SELECT * FROM {table_name};"
        
        cursor.execute(table_qry)
        
        columns = [column[0] for column in cursor.description]

        # Fetch all rows from the table
        rows = cursor.fetchall()

        # Generate INSERT statements for each row
        insert_statements = []
        for row in rows:
            values = ', '.join(f"'{str(value).replace('\'', '\\\'')}'" if value is not None else 'NULL' for value in row)
            insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});")

        print('insert_statements',insert_statements)
        
        table_desc_qry = f"SHOW CREATE TABLE {table_name}"
        cursor.execute(table_desc_qry)
        create_table_query = cursor.fetchall()
        
        # write_to_file(table_name,table_data)


def write_to_file(table_name,table_data):
    pass

connect_to_db()
# get data of each table and write to file
# check for ways to write it to a file

# use gzip to zip file into smaller size.

# v2

# use pandas to read csv file and write to db
