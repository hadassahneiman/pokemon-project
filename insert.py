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


def is_owner(name):
    with connection.cursor() as cursor:
        query = f"select name from owner where name=\"{name}\""
        cursor.execute(query)
        result = cursor.fetchone()
        return True if result else False


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


def insert_data():
    pokemon_data = open_file("pokemon_data.json")

    for pokemon in pokemon_data:
        type_id = find_id_type(pokemon['type'])

        if type_id:
            with connection.cursor() as cursor:
                query = f'insert into pokemon values ({pokemon["id"]}, \"{pokemon["name"]}\", {type_id}, {pokemon["height"]}, {pokemon["weight"]})'
                cursor.execute(query)
                connection.commit()
        else: print("Wrong type")

        insert_owners(pokemon['id'], pokemon['ownedBy'])
        
        
def insert_types():
    types = ["Normal", "Fire", "Water", "Grass", "Flying", "Fighting", "Poison", "Electric", "Ground", "Rock", "Psychic", "Ice", "Bug", "Ghost", "Steel", "Dragon", "Dark", "Fairy"]
    for type in types:   
        with connection.cursor() as cursor:    
            query = f'insert into type values (null, \"{type}\")' 
            cursor.execute(query)
            connection.commit()



if __name__ == '__main__':
    # insert_types()
    insert_data()