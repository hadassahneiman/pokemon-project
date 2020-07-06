import pymysql;
import json;

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


def open_file(file):
    try:
        with open("pokemon_data.json") as file:
            pokemon_data = json.load(file)
            return pokemon_data
    except:
        print("error in opening file")


def is_owner(name):
    with connection.cursor() as cursor:
        query = f"select name from owner where name=\"{name}\""
        cursor.execute(query)
        result = cursor.fetchone()
        return True if result else False


# def is_owner_pokemon(trainer, id):
#     with connection.cursor() as cursor:
#         query = f"select * from owner_pokemon where owner_name=\"{trainer}\" and pokemon_id = {id}"
#         cursor.execute(query)
#         result = cursor.fetchone()
#         return True if result else False


def get_pokemon_id(name):
    with connection.cursor() as cursor:
        query = f"select id from pokemon where name=\"{name}\""
        cursor.execute(query)
        result = cursor.fetchone()
        return result['id'] if result else None


def add_owner(name, town):
    with connection.cursor() as cursor:
        query = f"insert into owner values (\"{name}\", \"{town}\")"
        cursor.execute(query)
        connection.commit()


def insert_owner_pokemon(owner_name, pokemon_id):
     with connection.cursor() as cursor:
        query = f"insert into owner_pokemon values (\'{owner_name}\', {pokemon_id})"
        cursor.execute(query)
        connection.commit()


def insert_owners(pokemon_id, owners):
    for owner in owners:
        if not is_owner(owner['name']):
            add_owner(owner['name'], owner['town'])

        insert_owner_pokemon(owner['name'], pokemon_id)


def insert_type(pokemon_id, type_name):
    with connection.cursor() as cursor:
        query = f'insert into pokemon_type values ({pokemon_id}, \'{type_name}\')'
        cursor.execute(query)
        connection.commit()


def add_pokemon(pokemon):
    with connection.cursor() as cursor:
        query = f'insert into pokemon values ({pokemon["id"]}, \"{pokemon["name"]}\", {pokemon["height"]}, {pokemon["weight"]})'
        cursor.execute(query)
        connection.commit()


def insert_data():
    pokemon_data = open_file("pokemon_data.json")

    for pokemon in pokemon_data:
        add_pokemon(pokemon)
        insert_type(pokemon['id'], pokemon['type'])
        insert_owners(pokemon['id'], pokemon['ownedBy'])
        

if __name__ == '__main__':
    insert_data()