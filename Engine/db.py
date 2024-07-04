import csv
import sqlite3

con=sqlite3.connect("Porcupine.db")
cursor=con.cursor()

#System Commands
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#Web Commands
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

#Contacts
query="CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)"
cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/'), (null,'chat gpt','https://chatgpt.com/'),(null,'canva','https://www.canva.com/')"
# cursor.execute(query)
# con.commit()

# query = "INSERT INTO sys_command VALUES (null,'Visual Studio', 'C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\\IDE\\devenv.exe')"
# cursor.execute(query)
# con.commit()
