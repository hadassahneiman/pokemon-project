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


def find_owners(name):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT distinct o.name from owner o join pokemon p join owner_pokemon op ON o.id = op.owner_id and p.id = op.pokemon_id WHERE p.name = \"{name}\""
            cursor.execute(query)
            res = cursor.fetchall()
            return [x['name'] for x in res]

    except:
        print("DB error")


if __name__ == '__main__':
    print(find_owners("gengar"))