import requests

def get_url(pokemon_name):
    return f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'


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