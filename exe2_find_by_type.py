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
            query = f"select p.name from pokemon p join pokemon_type pt on pt.pokemon_id = p.id where pt.type_name=\'{type_name}\'"
            cursor.execute(query)
            res = cursor.fetchall()
            return [x['name'] for x in res]
            
    except Exception as e:
        print("DB error", e)


if __name__ == '__main__':
    print(find_by_type("grass"))