.. aboard documentation master file, created by
   sphinx-quickstart on Thu Dec 27 10:28:19 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aboard
======

Lib Python 3 de gestion de quadrillages en 2D, avec des opérations de base permettant d'implémenter une game logic ou des bots pour des jeux de plateaux.

Pas de "pip install" pour l'instant. Il faut copier manuellement les fichiers de code dans votre projet.

Le fichier "aboard_standalone.py" est généré avec tout le code de la lib. Son contenu peut être copié-collé dans n'importe quel contexte (par exemple, un puzzle ou un challenge du site codingame).


Sommaire
========

.. toctree::
   :maxdepth: 2

   advanced

* :ref:`search`


Quickstart
==========

Création, accès aux tiles, affichage.

>>> from aboard import Board
>>> board = Board(9, 6)
>>> board[3, 2].data = 'Z'
>>> print(board.render())
.........
.........
...Z.....
.........
.........
.........

Accès à des lignes, colonnes, rectangles de tiles via des itérateurs.

>>> for tile in board[2, :]:
...     tile.data = '|'
>>> for tile in board[3:, 1]:
...     tile.data = '='
>>> for tile in board[3:, 4:6]:
...     tile.data = '#'
>>> print(board.render())
..|......
..|======
..|Z.....
..|......
..|######
..|######

Accès à partir du coin inférieur droit, avec des coordonnées négatives.

>>> for coord in [(-1, -1), (-1, 4), (-2, 4)]:
...     board[coord].data = '.'
>>> print(board.render())
..|......
..|======
..|Z.....
..|......
..|####..
..|#####.

Remplissage par propagation, à partir d'une position donnée.

>>> for tile in board.get_by_propagation((6, 3)):
...     tile.data = '/'
>>> print(board.render())
..|......
..|======
..|Z/////
..|//////
..|####//
..|#####/

Vérification des coordonnées, déplacement selon une direction.

>>> from aboard import BoardIndexError, Pos, Dir
>>> pos = Pos(9, 0)
>>> try:
...     board[pos]
... except BoardIndexError as e:
...     print(e)
Coord not in board. coord : 9, 0. board size : 9, 6.
>>> pos.move(Dir.LEFT, 7)
>>> board[pos].data = '.'
>>> pos.move(Dir.DOWN)
>>> board[pos].data = '.'
>>> print(board.render())
.........
...======
..|Z/////
..|//////
..|####//
..|#####/

Recherche du chemin le plus court. (La configuration par défaut n'autorise pas les mouvements en diagonale, mais c'est modifiable).

>>> for idx, tile in enumerate(board.get_by_pathfinding((1, 3), (6, 0))):
...    tile.data = idx
>>> print(board.render())
..45678..
.23======
.1|Z/////
.0|//////
..|####//
..|#####/

