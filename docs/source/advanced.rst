**********************************
Doc détaillée
**********************************

Objets de base, lecture/écriture simple
=======================================

Un Board est un tableau à deux dimensions contenant des objets Tile.

La taille (largeur, hauteur) est à spécifier à la création.

>>> board = Board(7, 4)

La Tile en haut à gauche correspond à la coordonnée (0, 0), celle à sa droite à la coordonnée (1, 0), etc.

La dernière Tile en bas à droite a pour coordonnée (largeur-1, hauteur-1).

Une Tile possède les attributs suivants :

 - board_father : référence vers l'objet Board contenant la Tile.
 - x, y : position de la Tile dans le Board conteneur.
 - data : string. Donnée stockée. Initialisée au caractère "." (un point).

``board_father``, ``x`` et ``y`` peuvent être lus, mais ne devraient jamais être directement modifiés.

``data`` peut être lu et modifié.

Pour accéder à une Tile dans un Board, utilisez l'opérateur "[]" (``__getitem__``), en spécifiant les coordonnées x et y.

>>> tile = board[3, 2]
>>> print(tile.x)
3
>>> print(tile.y)
2
>>> print(tile.data)
.
>>> tile.data = "ABCD"

La fonction `Board.render()` renvoie une string multi-ligne (séparateur : "\\n"), représentant le Board.

Dans la configuration de rendering par défaut, chaque Tile est représentée par un seul caractère, égal au premier caractère de l'attribut data.

>>> print(board.render())
.......
.......
...A...
.......


Itérateurs
==========

Itérateurs par rectangle
------------------------

Avec l'opérateur "[]", remplacez une ou les deux coordonnées, par un slice, pour faire une itération sur une ligne, une colonne, un sous-rectangle, avec une ligne sur deux, de gauche à droite, ...

Exemple :

>>> board = Board(6, 4)
>>> for tile in board[1:4, 1]:
...     tile.data = "#"
>>> print(board.render())
......
.###..
......
......

>>> for index, tile in enumerate(board[4::-1, :-1:-2]):
...     tile.data = index
>>> print(board.render())
......
98765.
......
43210.

Attention. Pour l'instant : board[1:-1] ne fonctione pas. TODO : Dans le code, il suffit de faire range(self.w)[param_slice], et tout marche tout seul.

Pour itérer en premier sur les colonnes, puis sur les lignes, ajouter le caractère "y" en troisième paramètre.

>>> for index, tile in enumerate(board[::, ::, 'y']):
...     tile.data = index if index < 10 else "A"
>>> print(board.render())
048AAA
159AAA
26AAAA
37AAAA


Itérateurs par liste de points
------------------------------

Informations d'itérations
-------------------------

override class tiles
====================

rendering
=========

sur_iterators
=============

Adjacency
=========

specific fill et path-finding
=============================

build pour codingame
====================

mobile item (en construction)
=============================

exemple complet
===============

Jeu de plateau "Labyrinthe".
