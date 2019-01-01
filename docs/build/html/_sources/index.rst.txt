.. aboard documentation master file, created by
   sphinx-quickstart on Thu Dec 27 10:28:19 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aboard
======

Lib Python 3 de gestion de quadrillages en 2D, avec des opérations de base permettant d'implémenter une game logic ou des bots pour des jeux de plateaux.

Pas de "pip install" pour l'instant. Il faut copier manuellement les fichiers de code dans votre projet, et éventuellement modifier votre PYTHONPATH.

Le fichier "aboard_standalone.py" est généré avec tout le code de la lib. Il est possible de copier-coller son contenu, pour l'utiliser dans n'importe quel contexte (par exemple, un puzzle ou un challenge du site codingame).


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
>>> board[3,2].data = 'Z'
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

Remplissage par propagation.

>>> from propagation_iterator import BoardIteratorPropagation
>>> for tile in BoardIteratorPropagation(board, (6, 3)):
...     tile.data = '/'
>>> print(board.render())
..|......
..|======
..|Z/////
..|//////
..|####//
..|#####/

Vérification des coordonnées, déplacement selon une direction.

>>> from aboard import BoardIndexError
>>> from point import Point, Dir
>>> point = Point(9, 0)
>>> try:
...     board[point]
... except BoardIndexError as e:
...     print(e)
Coord not in board. coord : 9 0. board size : 9, 6.
TODO : il manque une virgule.
>>> point.move(Dir.LEFT, 7)
>>> board[point].data = '.'
>>> point.move(Dir.DOWN)
>>> board[point].data = '.'
>>> print(board.render())
.........
...======
..|Z/////
..|//////
..|####//
..|#####/

Recherche du chemin le plus court. (La configuration par défaut n'autorise pas les mouvements en diagonale, mais c'est modifiable).

>>> from propagation_iterator import BoardIteratorFindPath
>>> for idx,tile in enumerate(BoardIteratorFindPath(board, (1,3), (6,0))):
...    tile.data = idx
>>> print(board.render())
..45678..
.23======
.1|Z/////
.0|//////
..|####//
..|#####/


