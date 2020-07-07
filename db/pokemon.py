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

def add(pokemon):
    with connection.cursor() as cursor:
        query = f'insert into pokemon values ({pokemon["id"]}, \"{pokemon["name"]}\", {pokemon["height"]}, {pokemon["weight"]})'
        cursor.execute(query)
        connection.commit()


def add_type(pokemon_id, type_name):
    with connection.cursor() as cursor:
        query = f'insert into pokemon_type values ({pokemon_id}, \'{type_name}\')'
        cursor.execute(query)
        connection.commit()


def get_types(pokemon_name):
    with connection.cursor() as cursor:
        query = f"select type_name from pokemon_type where pokemon_id = (select id from pokemon where name = \'{pokemon_name}\')"
        cursor.execute(query)
        result = cursor.fetchall()
        return [x['type_name'] for x in result]


def get_id(name):
    with connection.cursor() as cursor:
        query = f"select id from pokemon where name=\"{name}\""
        cursor.execute(query)
        result = cursor.fetchone()
        return result['id'] if result else None


def filter_by_type(type_name):
    with connection.cursor() as cursor:
        query = f"select p.name from pokemon p join pokemon_type pt on pt.pokemon_id = p.id where pt.type_name=\'{type_name}\'"
        cursor.execute(query)
        res = cursor.fetchall()
        return [x['name'] for x in res]


def filter_by_trainer(name):
    with connection.cursor() as cursor:
        query = f"select p.name from pokemon p join owner_pokemon op on p.id = op.pokemon_id where op.owner_name = \"{name}\";"
        cursor.execute(query)
        res = cursor.fetchall()
        return [x['name'] for x in res]


def find_owners(name):
    with connection.cursor() as cursor:
        query = f"SELECT distinct op.owner_name from pokemon p join owner_pokemon op ON p.id = op.pokemon_id WHERE p.name = \"{name}\""
        cursor.execute(query)
        res = cursor.fetchall()
        return [x['owner_name'] for x in res]


def delete_by_owner(owner_name, pokemon_name):
    with connection.cursor() as cursor:
        query = f"delete from owner_pokemon where owner_name = \"{owner_name}\" and pokemon_id = (select id from pokemon where name = \"{pokemon_name}\");"
        cursor.execute(query)
        connection.commit()