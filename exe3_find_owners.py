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
    with connection.cursor() as cursor:
        query = f"SELECT distinct op.owner_name from pokemon p join owner_pokemon op ON p.id = op.pokemon_id WHERE p.name = \"{name}\""
        cursor.execute(query)
        res = cursor.fetchall()
        return [x['owner_name'] for x in res]



if __name__ == '__main__':
    print(find_owners("gengar"))