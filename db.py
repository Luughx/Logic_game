import mysql.connector as connector
import datetime

con = connector.connect(
    host="localhost",
    password="admin",
    user="root",
    database="logic_game"
)

def createTable():
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE Players(
                Id INTEGER AUTO_INCREMENT PRIMARY KEY,
                Nombre VARCHAR(20),
                Puntos INTEGER,
                Tiempo INTEGER,
                Fecha DATE
        )

    """)

    con.commit()
    cur.close()

def insertUser(name, points, time):
    cur = con.cursor()
    sql = "INSERT INTO players(Nombre, Puntos, Tiempo, Fecha) VALUES (%s, %s, %s, %s)"
    data = (name, points, time, datetime.datetime.now())
    cur.execute(sql, data)

    con.commit()
    cur.close()

def insertUser(name, points, time):

    if points < 0:
        return

    name = name.strip()
    if len(name) > 20 or name == "":
        name = "Lughx"

    cur = con.cursor()
    sql = "INSERT INTO players(Nombre, Puntos, Tiempo, Fecha) VALUES (%s, %s, %s, %s)"
    data = (name, points, time, datetime.datetime.now())
    cur.execute(sql, data)
    print("guarda")
    con.commit()
    cur.close()

def getUsers():
    cur = con.cursor()
    sql = "SELECT * FROM players ORDER BY puntos DESC LIMIT 0, 50 "
    cur.execute(sql)
    users = []
    for row in cur:
        users.append(row)
    con.commit()
    cur.close()
    return users
