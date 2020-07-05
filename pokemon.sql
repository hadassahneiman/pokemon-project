USE pokemon;

CREATE TABLE owner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    town VARCHAR(20)
);

CREATE TABLE type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20)
);

CREATE TABLE pokemon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    type_id INT,
    height INT,
    weight INT,
    FOREIGN KEY(type_id) REFERENCES type(id)
);

CREATE TABLE owner_pokemon (
    owner_id INT,
    pokemon_id INT,
    PRIMARY KEY(owner_id, pokemon_id),
    FOREIGN KEY(owner_id) REFERENCES owner(id),
    FOREIGN key(pokemon_id) REFERENCES pokemon(id)
);

