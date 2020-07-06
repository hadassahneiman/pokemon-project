import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def update_pokemon_owner(owner_name, pokemon_id, new_id):
    with connection.cursor() as cursor:
        query = f"update owner_pokemon set pokemon_id = {new_id} where owner_name = \'{owner_name}\' and pokemon_id = {pokemon_id};"
        cursor.execute(query)
        connection.commit()