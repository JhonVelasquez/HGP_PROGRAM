import sqlite3


conn = sqlite3.connect('.\db\hgp_dev.db')

c = conn.cursor()

c.execute("SELECT * FROM Cliente")
records = c.fetchall()
print(records)

conn.commit()

conn.close()

