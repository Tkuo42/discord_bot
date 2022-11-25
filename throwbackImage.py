import mysql.connector

from main import token, password, database

newDb = mysql.connector.connect(
    host="localhost",
    user='root',
    password=password,
    database=database
)

cursor = newDb.cursor(buffered=True)


def addThrowback(name, photo, date, context):
    cursor.execute(
        'INSERT INTO throwback (name, photo, date, context) VALUES (%s, %s, %s, %s)', (name, photo, date, context))
    newDb.commit()
    cursor.reset()


def showThrowbacks():
    cursor.execute('SELECT * FROM throwback')
    throwbacks = cursor.fetchall()
    cursor.reset()
    return throwbacks


def deleteThrowback(id):
    cursor.execute('DELETE FROM throwback WHERE id = %s', (id,))
    newDb.commit()
    cursor.reset()
