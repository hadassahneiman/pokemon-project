from db import trainer
from db import pokemon
import json


def insert_owners(pokemon_id, owners):
    for owner in owners:
        if not trainer.isA(owner['name']):
            trainer.add(owner['name'], owner['town'])

        trainer.add_pokemon(owner['name'], pokemon_id)


def open_file():
    with open("setup/pokemon_data.json") as file:
        pokemon_data = json.load(file)
        return pokemon_data


def insert_data():
    pokemon_data = open_file()

    for object_ in pokemon_data:
        pokemon.add(object_)
        pokemon.add_type(object_['id'], object_['type'])
        insert_owners(object_['id'], object_['ownedBy'])
