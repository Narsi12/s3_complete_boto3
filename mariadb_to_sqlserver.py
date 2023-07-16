import pyodbc
import mysql.connector

# Connect to MariaDB
maria_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='students'
)

# Connect to MSSQL
mssql_conn = pyodbc.connect(
    Trusted_Connection='Yes',
    driver='{SQL Server}',
    # driver='ODBC Driver 17 for SQL Server',
    server="172.17.10.45",
    database="MT_TRAINING"
)

maria_cursor = maria_conn.cursor()

maria_cursor.execute("SHOW TABLES FROM students")
tables = maria_cursor.fetchall()


for table in tables:
    table_name = table[0]
    try:
        maria_cursor.execute(f"SELECT * FROM students.{table_name}")
        rows = maria_cursor.fetchall()
        mssql_cursor = mssql_conn.cursor()
        mssql_cursor.execute(f"CREATE TABLE  {table_name} LIKE students.{table_name}")
    except Exception as e:
        print(f"Table with {table_name} is already exists")
    try:    
        for row in rows:
            insert_query = f"INSERT IGNORE INTO {table_name} VALUES ({','.join(['%s'] * len(row))})"
            mssql_cursor.execute(insert_query, row)
    except Exception as e:
         print(f"Error occurred while migrating table '{table_name}': {str(e)}")
    
    mssql_conn.commit()
    mssql_cursor.close()
print("Data Migration is completed")
maria_cursor.close()
maria_conn.close()
mssql_conn.close()
