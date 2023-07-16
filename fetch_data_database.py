import mysql.connector
import pyodbc

maria_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='students'
)

mssql_conn = pyodbc.connect(
    driver='{ODBC Driver 17 for SQL Server}',
    server="172.16.10.45",
    database="MT_TRAINING",
    trusted_connection='yes'
)
maria_cursor = maria_conn.cursor()
maria_cursor.execute("SHOW TABLES FROM students")
tables = maria_cursor.fetchall()

for table in tables:
    table_name = table[0]
    maria_cursor.execute(f"SELECT * FROM students.{table_name}")
    data = maria_cursor.fetchall()
     



 