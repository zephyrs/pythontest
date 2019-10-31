import datetime
import random
import sqlite3

conn = sqlite3.connect('d:\\dump\\sc.db')
c = conn.cursor()
print("OPEN database successfully")

counter = 0
while counter < 100000:
    d1 = random.random()
    d2 = random.random()
    d3 = random.random()
    t = datetime.datetime.now()
    c.execute("insert into diameter(d1, d2, sum, time) values(?, ?, ?, ?)",
              (d1, d2, d3, t))

    c.execute("insert into pre_length(l1, l2, time) values(?, ?, ?)",
              (d1, d2, t))

    c.execute(
        "insert into slope(x1, y1, z1, x2, y2, z2, time) values(?, ?, ?, ?, ?, ?, ?)",
        (d1, d2, d3, d1, d2, d3, t))

    counter += 1

conn.commit()
c.close()
conn.close()
