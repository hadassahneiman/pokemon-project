USE pokemon;

CREATE TABLE owner (
    name VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
);

CREATE TABLE type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20)
);

CREATE TABLE pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    type_id INT,
    height INT,
    weight INT,
    FOREIGN KEY(type_id) REFERENCES type(id)
);

CREATE TABLE owner_pokemon (
    owner_name VARCHAR(20),
    pokemon_id INT,
    PRIMARY KEY(owner_name, pokemon_id),
    FOREIGN KEY(owner_name) REFERENCES owner(name),
    FOREIGN key(pokemon_id) REFERENCES pokemon(id)
);


