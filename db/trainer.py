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


def add(name, town):
    with connection.cursor() as cursor:
        query = f"insert into owner values (\"{name}\", \"{town}\")"
        cursor.execute(query)
        connection.commit()


def isA(name):
    with connection.cursor() as cursor:
        query = f"select name from owner where name=\"{name}\""
        cursor.execute(query)
        result = cursor.fetchone()
        return True if result else False


def add_pokemon(owner_name, pokemon_id):
     with connection.cursor() as cursor:
        query = f"insert into owner_pokemon values (\'{owner_name}\', {pokemon_id})"
        cursor.execute(query)
        connection.commit()


def update_pokemon(owner_name, pokemon_id, new_id):
    with connection.cursor() as cursor:
        query = f"update owner_pokemon set pokemon_id = {new_id} where owner_name = \'{owner_name}\';"
        cursor.execute(query)
        connection.commit()