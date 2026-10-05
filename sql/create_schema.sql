DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE ecommerce;
USE DATABASE ecommerce;

CREATE TABLE Client (
id_client INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nom VARCHAR(32),
prenom VARCHAR(32),
email VARCHAR(32),
ville VARCHAR(32),
date_creation DATETIME
);

CREATE TABLE Produit (
id_produit INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
nom VARCHAR(32),
categorie VARCHAR(32),
prix FLOAT,
stock_dispo INT
);

CREATE TABLE Commande (
id_commande INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
statut ENUM('payée', 'expédiée','livrée','annulée'),
date_cmd DATETIME,
id_client INT NOT NULL,
FOREIGN KEY (id_client) REFERENCES Client(id_client)
);

CREATE TABLE Ligne_commande (
id_commande INT,
id_produit INT,
quantite INT,
prix_unitaire FLOAT,
PRIMARY KEY (id_commande, id_produit),
FOREIGN KEY (id_commande) REFERENCES Commande(id_commande),
FOREIGN KEY (id_produit) REFERENCES Produit(id_produit);
);
