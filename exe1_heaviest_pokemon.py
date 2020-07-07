import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")


def find_heaviest():
    try:
        with connection.cursor() as cursor:
            query = "select name from pokemon where weight = (select max(weight) from pokemon)"
            cursor.execute(query)
            return cursor.fetchone()['name']
    except Exception as e:
        print('DB error', e)


if __name__ == '__main__':
    print(find_heaviest())
