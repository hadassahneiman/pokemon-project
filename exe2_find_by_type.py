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


def find_by_type(type_name):
    try:
        with connection.cursor() as cursor:
            query = f"select p.name from pokemon p join type t on p.type_id = t.id where t.name=\'{type_name}\'"
            cursor.execute(query)
            res = cursor.fetchall()
            return [x['name'] for x in res]
            
    except:
        print("DB error")


if __name__ == '__main__':
    print(find_by_type("grass"))