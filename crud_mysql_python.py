import mysql.connector as narsimha

mysql_conn = narsimha.connect(
    host='localhost',
    user='root',
    password='root',
    database='dsa_sheet'
)
my_cursor = mysql_conn.cursor()

#CREATE DATABASE
my_cursor.execute('create database dsa_sheet')
print(my_cursor.execute('show databases'))

#CREATE TABLE
my_cursor.execute("CREATE TABLE leetcode (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(33), email VARCHAR(15))")



#INSERT RECORDS IN TABLE
my_cursor.execute("INSERT INTO leetcode (name,email) VALUES ('narsimha','ch@gmail.com')")
mysql_conn.commit()



# GET RECORSD ALL OR BASED ON WHERE CONDITION
my_cursor.execute('SELECT * FROM leetcode')
my_cursor.execute("SELECT * FROM leetcode WHERE id = 3 ")
x = my_cursor.fetchall()
print(x)


#DROP TABLE 
my_cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(33), email VARCHAR(15))")
my_cursor.execute('DROP TABLE users')



