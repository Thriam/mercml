"""
Docstring for ML.employee
"""


import psycopg2


conn= psycopg2.connect(host="localhost",
                      user="postgres",
                      password="postgres",
                      database="mb",port=5432)
cursor= conn.cursor()

cursor.execute("create table employee(id int primary key,name varchar(40))")

cursor.execute("insert into employee values(102,'test1')")
cursor.execute("select * from employee")

for row in cursor.fetchall():
    print(row)
