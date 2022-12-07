import sqlite3

conn = sqlite3.connect('project_db.sqlite')
cur = conn.cursor()

query1 = '''CREATE TABLE IF NOT EXISTS users ( 
id INTEGER, 
username TEXT,
hash TEXT,
PRIMARY KEY(id))'''


cur.execute(query1)
conn.commit()

query2 ='''CREATE TABLE IF NOT EXISTS vehicles (
id INTEGER,
ak TEXT,
type TEXT,
brand TEXT,
model TEXT,
displacement INTEGER,
userid INTEGER,
FOREIGN KEY (userid) REFERENCES users (id),
PRIMARY KEY(id))'''

cur.execute(query2)
conn.commit()

query3 = '''CREATE TABLE IF NOT EXISTS customers (
id INTEGER,
firstname TEXT,
lastname TEXT,
address1 TEXT,
address2 TEXT,
phonenum1 TEXT,
phonenum2 TEXT,
licence TEXT,
id_passport TEXT,
userid INTEGER,
FOREIGN KEY (userid) REFERENCES users(id),
PRIMARY KEY (id))'''

cur.execute(query3)
conn.commit()

query4 = '''CREATE TABLE IF NOT EXISTS contracts (customer	INTEGER, 
vehicle INTEGER,
rentday TEXT,
returnday TEXT,
chargepd NUMERIC,
payinad NUMERIC,
totalcharge NUMERIC,
reminder NUMERIC,
userid INTEGER,
id	INTEGER,
FOREIGN KEY(userid) REFERENCES users (id),
FOREIGN KEY(customer) REFERENCES customers (id),
FOREIGN KEY(vehicle) REFERENCES vehicles (id),
PRIMARY KEY(id))'''

cur.execute(query4)
conn.commit()

conn.close()