import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def delete_by_owner(owner_name, pokemon_name):
    with connection.cursor() as cursor:
        query = f"delete from owner_pokemon where owner_name = \"{owner_name}\" and pokemon_id = (select id from pokemon where name = \"{pokemon_name}\");"
        cursor.execute(query)
        connection.commit()