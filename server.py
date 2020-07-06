from flask import Flask, Response, request
import requests
import json

from insert import add_pokemon, insert_type, insert_owner_pokemon, get_pokemon_id
from exe2_find_by_type import find_by_type
from delete_pokemon_owner import delete_by_owner
from update_pokemon_owner import update_pokemon_owner
from exe4_find_roster import find_roster


app = Flask(__name__)


@app.route('/')
def welcome():
    return Response("Welcome to the Pokemon Game!!!")


@app.route('/pokemon/<trainer>')
def get_pokemon_by_trainer(trainer):
    pokemons = find_roster(trainer)
    return json.dumps({"trainer":trainer, "pokemons": pokemons})


@app.route('/pokemon', methods=["POST"])
def new_pokemon():
    pokemon = request.get_json()

    if not pokemon.get('id') or not pokemon.get('name') or not pokemon.get('height') or not pokemon.get('height') or not pokemon.get('types'):
        return Response("wrong data", 400)

    add_pokemon(pokemon)

    for type in pokemon['types']:
        insert_type(pokemon['id'], type)

    return Response(f"added {pokemon['name']} to pokemon table")


@app.route('/pokemon/<type>')
def get_pokemon_by_type(type):
    pokemons = find_by_type(type)
    return json.dumps({"found": pokemons})


@app.route('/pokemon_trainer/delete', methods=["DELETE"])
def delete_pokemon_by_trainer():
    data = request.get_json()

    if not data.get('owner_name') or not data.get('pokemon_name'):
        return Response("wrong data", 400)

    delete_by_owner(data['owner_name'], data['pokemon_name'])
    return Response(f"deleted pokemon: {data['pokemon_name']} which belongs to owner: {data['owner_name']}", 200)


def get_evolution_chain(url):
    data = requests.get(url).json()
    species_url = data['species']['url']
    info = requests.get(species_url).json()
    evolution_url = info['evolution_chain']['url']
    return requests.get(evolution_url).json()


def get_evolves_to(chain, pokemon_name):
    evolves_to = chain['chain']['evolves_to']
    species = chain['chain']['species']['name']
    name = None

    while len(evolves_to) > 0:
        if species == pokemon_name:
            name = evolves_to[0]['species']['name']
            break
        else:
            species =  evolves_to[0]['species']['name']
            evolves_to = evolves_to[0]['evolves_to']

    return name


def create_pokemon(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    data = requests.get(url).json()
    types = [type['type']['name'] for type in data['types']]
    pokemon = {'id': data['id'], 'name': pokemon_name, 'height': data['height'], 'types': types}
    add_pokemon(pokemon)


@app.route('/evolve/<trainer>/<pokemon_name>', methods=['PUT'])
def evolve(trainer, pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    chain = get_evolution_chain(url)
    name = get_evolves_to(chain, pokemon_name)

    if name:
        if not get_pokemon_id(name):
            create_pokemon(name)
        update_pokemon_owner(trainer, get_pokemon_id(pokemon_name), get_pokemon_id(name))
        
    return Response(f"pokemon: {pokemon_name} with owner: {trainer} evolved to {name}")


if __name__ == '__main__':
    app.run(port=3000)