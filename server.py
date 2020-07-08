from flask import Flask, Response, request, url_for, redirect, render_template
import requests
import json
from pymysql import IntegrityError

from db import trainer, pokemon
from external_API import pokeApi, imagesApi


app = Flask(__name__, static_url_path='', static_folder='frontend', template_folder='frontend')


@app.route('/')
def welcome():
    return redirect('/home_page.html')


@app.route('/<file_path>')
def serve_static_file(file_path):
    return app.send_static_file(file_path)


@app.route('/pic', methods=['GET'])
def get_picture():
    pokemon_name = request.args.get('pokemon')
    pokemon_id = pokemon.get_id(pokemon_name)
    if pokemon_id:
        return render_template('/view_pok.html', name= pokemon_name, the_url= imagesApi.get_url(pokemon_id))
    return render_template('/view_pok.html', name= pokemon_name, the_url= '')
 

@app.route('/evolve/pic')
def evolve_pic():
    pokemon_name = request.args.get('pokemon')
    owner_name = request.args.get('owner')
    
    url = pokeApi.get_url(pokemon_name)
    chain = pokeApi.get_evolution_chain(url)
    name = pokeApi.get_evolves_to(chain, pokemon_name)
 
    if name:
        return render_template("/evolve_render.html", name= pokemon_name, old_url= imagesApi.get_url(pokemon.get_id(pokemon_name)), new_url= imagesApi.get_url(pokemon.get_id(name)))
    else :
        return render_template("/evolve_render.html", name= pokemon_name, old_url= imagesApi.get_url(pokemon.get_id(pokemon_name)), new_url= imagesApi.get_url(pokemon.get_id(pokemon_name)))


@app.route('/pokemons')
def get_pokemons():
    pokemons = []

    if request.args.get('type'):
        pokemons = pokemon.filter_by_type(request.args.get('type'))

    elif request.args.get('trainer'):
        pokemons = pokemon.filter_by_trainer(request.args.get('trainer'))

    return Response(json.dumps(pokemons)), 200


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


@app.route('/pokemons/<pokemon_name>', methods=['PUT'])
def update_types(pokemon_name):
    pokemon_types = pokemon.get_types(pokemon_name)
    url = pokeApi.get_url(pokemon_name)
    data = requests.get(url).json()
    types = [type['type']['name'] for type in data['types']]

    for type in types:
        if type not in pokemon_types:
           pokemon.insert_type(pokemon.get_id(pokemon_name), type)

    return Response(f"updated types for pokemon: {pokemon_name}")


@app.route('/pokemon/<pokemon_name>/<trainer>', methods=["DELETE"])
def delete_pokemon_by_trainer(pokemon_name, trainer):
    pokemon.delete_by_owner(trainer, pokemon_name)
    return Response(f"deleted pokemon: {pokemon_name} which belongs to owner: {trainer}", 200)


def create_pokemon(pokemon_name):
    url = pokeApi.get_url(pokemon_name)
    data = requests.get(url, verify = False).json()
    types = [type['type']['name'] for type in data['types']]
    pokemon_to_add = {'id': data['id'], 'name': pokemon_name, 'height': data['height'], 'weight':data['weight'], 'types': types}
    pokemon.add(pokemon_to_add)


@app.route('/pokemons/evolve/<owner>/<pokemon_name>', methods=['PUT'])
def evolve(owner, pokemon_name):
    url = pokeApi.get_url(pokemon_name)
    chain = pokeApi.get_evolution_chain(url)
    name = pokeApi.get_evolves_to(chain, pokemon_name)

    if name:
        if not pokemon.get_id(name):
            create_pokemon(name)

        try:
            trainer.update_pokemon(owner, pokemon.get_id(pokemon_name), pokemon.get_id(name))
        except IntegrityError as e:
            pass

    else: return Response(json.dumps(f"{pokemon_name} can not evolve")), 202
        
    return Response(json.dumps({'pokemon': pokemon_name, 'owner': owner, 'evolved_to': name})), 200


if __name__ == '__main__':
    app.run(port=3001)