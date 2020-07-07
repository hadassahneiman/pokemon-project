DROP Database pokemon;
CREATE DATABASE pokemon;

USE pokemon;

CREATE TABLE owner (
    name VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
);

CREATE TABLE pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    height INT,
    weight INT
);

CREATE TABLE  pokemon_type (
    pokemon_id INT,
    type_name VARCHAR(20),
    PRIMARY KEY(type_name, pokemon_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
);

CREATE TABLE owner_pokemon (
    owner_name VARCHAR(20),
    pokemon_id INT,
    PRIMARY KEY(owner_name, pokemon_id),
    FOREIGN KEY(owner_name) REFERENCES owner(name),
    FOREIGN key(pokemon_id) REFERENCES pokemon(id)
);