import mysql.connector

maria_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mariaDB'
)

mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='user_info'
)

maria_cursor = maria_conn.cursor()
maria_cursor.execute("SHOW TABLES FROM mariaDB")
tables = maria_cursor.fetchall()

for table in tables:
    table_name = table[0]
    try:
        maria_cursor.execute(f"SELECT * FROM mariaDB.{table_name}")
        data = maria_cursor.fetchall()
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute(f"CREATE TABLE  {table_name} LIKE mariaDB.{table_name}")
    except Exception as e:
        print(f"Table with {table_name} is already exists")
    try:
        for row in data:
            insert_query = f"INSERT IGNORE INTO {table_name} VALUES ({','.join(['%s'] * len(row))})"
            mysql_cursor.execute(insert_query, row)
    except Exception as e:
         print(f"Error occurred while migrating table '{table_name}': {str(e)}")

    mysql_conn.commit()
print("Data Migration is completed")
mysql_conn.close()
maria_conn.close()

 