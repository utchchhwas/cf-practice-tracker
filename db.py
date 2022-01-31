from sqlite3 import Cursor
import cx_Oracle

# Establish the database connection
connection = cx_Oracle.connect(user="c##cf", password='cf',
                               dsn="localhost/orcl")

print('Successfully connected to the database')

cur = connection.cursor()