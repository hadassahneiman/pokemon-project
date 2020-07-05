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


def find_id_type(type_name):
    id = None
    with connection.cursor() as cursor:
        query = f"select id from type where name=\"{type_name}\""
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            id = result.get('id')
    return id


def open_file(file):
    try:
        with open("pokemon_data.json") as file:
            pokemon_data = json.load(file)
            return pokemon_data
    except:
        print("error in opening file")


def get_owner_id(name, town):
    with connection.cursor() as cursor:
        query = f"select id from owner where name=\"{name}\" and town=\"{town}\""
        cursor.execute(query)
        result = cursor.fetchone()
        return result['id'] if result else None


def add_owner(name, town):
    with connection.cursor() as cursor:
        query = f"insert into owner values (null, \"{name}\", \"{town}\")"
        cursor.execute(query)
        connection.commit()


def insert_owner_pokemon(owner_id, pokemon_id):
     with connection.cursor() as cursor:
        query = f"insert into owner_pokemon values ({owner_id}, {pokemon_id})"
        cursor.execute(query)
        connection.commit()


def insert_owners(pokemon_id, owners):
    for owner in owners:
        id = get_owner_id(owner['name'], owner['town'])

        if not id:
            add_owner(owner['name'], owner['town'])

        insert_owner_pokemon(get_owner_id(owner['name'], owner['town']), pokemon_id)


def insert_data():
    pokemon_data = open_file("pokemon_data.json")

    for pokemon in pokemon_data:
        type_id = find_id_type(pokemon['type'])
        if type_id:
            with connection.cursor() as cursor:
                query = f'insert into pokemon values ({pokemon["id"]}, \"{pokemon["name"]}\", {type_id}, {pokemon["height"]}, {pokemon["weight"]})'
                cursor.execute(query)
                connection.commit()
        insert_owners(pokemon['id'], pokemon['ownedBy'])
        
        
def insert_types():
    types = ["Normal", "Fire", "Water", "Grass", "Flying", "Fighting", "Poison", "Electric", "Ground", "Rock", "Psychic", "Ice", "Bug", "Ghost", "Steel", "Dragon", "Dark", "Fairy"]
    for type in types: 
        try:    
            with connection.cursor() as cursor:    
                query = f'insert into type values (null, \"{type}\")' 
                cursor.execute(query)
                connection.commit()

        except:
            print("DB error")


if __name__ == '__main__':
    insert_types()
    insert_data()