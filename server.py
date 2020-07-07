from flask import Flask, Response, request
import requests
import json
from pymysql import IntegrityError

from db import trainer, pokemon


app = Flask(__name__)


@app.route('/')
def welcome():
    return Response("Welcome to the Pokemon Game!!!")


@app.route('/pokemons/<pokemon_name>', methods=['PUT'])
def update_types(pokemon_name):
    pokemon_types = pokemon.get_types(pokemon_name)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    data = requests.get(url).json()
    types = [type['type']['name'] for type in data['types']]

    for type in types:
        if type not in pokemon_types:
           pokemon.insert_type(pokemon.get_id(pokemon_name), type)

    return Response(f"updated types for pokemon: {pokemon_name}")


@app.route('/pokemons')
def get_pokemons():
    pokemons = []

    if request.args.get('type'):
        pokemons = pokemon.filter_by_type(request.args.get('type'))

    elif request.args.get('trainer'):
        pokemons = pokemon.filter_by_trainer(request.args.get('trainer'))

    return Response(json.dumps(pokemons)), 200


# @app.route('/owners/<pokemon_name>')
# def get_owners_by_trainer(pokemon_name):
#     pokemons = find_owners(pokemon_name)
#     return json.dumps({"pokemon":pokemon_name, "trainers": pokemons})


@app.route('/pokemons', methods=["POST"])
def new_pokemon():
    data = request.get_json()

    if not data.get('id') or not data.get('name') or not data.get('height') or not data.get('height') or not data.get('types'):
        return Response("wrong data", 400)

    try:
        pokemon.add(data)

        for type in data['types']:
            pokemon.add_type(data['id'], type)

    except IntegrityError as e:
        return Response("pokemon already in db"), 202

    return Response(f"added {data['name']} to pokemon table"), 200


@app.route('/pokemon/<pokemon_name>/<trainer>', methods=["DELETE"])
def delete_pokemon_by_trainer(pokemon_name, trainer):
    pokemon.delete_by_owner(trainer, pokemon_name)
    return Response(f"deleted pokemon: {pokemon_name} which belongs to owner: {trainer}", 200)


def get_evolution_chain(url):
    data = requests.get(url,verify=False).json()
    species_url = data['species']['url']
    info = requests.get(species_url, verify=False).json()
    evolution_url = info['evolution_chain']['url']
    return requests.get(evolution_url,verify=False).json()


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
    data = requests.get(url, verify = False).json()
    types = [type['type']['name'] for type in data['types']]
    pokemon_to_add = {'id': data['id'], 'name': pokemon_name, 'height': data['height'], 'weight':data['weight'], 'types': types}
    pokemon.add(pokemon_to_add)


@app.route('/pokemons/evolve/<owner>/<pokemon_name>', methods=['PUT'])
def evolve(owner, pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    chain = get_evolution_chain(url)
    name = get_evolves_to(chain, pokemon_name)

    if name:
        if not pokemon.get_id(name):
            create_pokemon(name)
            
        try:
            trainer.update_pokemon(owner, pokemon.get_id(pokemon_name), pokemon.get_id(name))
        except IntegrityError as e:
            pass

    else: return Response(json.dumps(f"{pokemon_name} can not evolve")), 202
        
    return Response(json.dumps(f"pokemon: {pokemon_name} with owner: {owner} evolved to {name}")), 200


if __name__ == '__main__':
    app.run(port=3000)