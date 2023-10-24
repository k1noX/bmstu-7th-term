import sqlite3
conn = sqlite3.connect('db/data.sqlite')
cursor = conn.cursor()
cursor.execute('CREATE TABLE users(ID INTEGER PRIMARY KEY ASC, name TEXT UNIQUE, pass TEXT)')
cursor.execute('INSERT INTO users (name, pass) VALUES ("name", "pass")')
conn.commit()
conn.close()