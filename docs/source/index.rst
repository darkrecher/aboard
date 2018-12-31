.. aboard documentation master file, created by
   sphinx-quickstart on Thu Dec 27 10:28:19 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aboard's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   advanced

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

Accès à des lignes et des rectangles de tiles via des itérateurs.

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

Accès via le coin inférieur droit, par des coordonnées négatives.

>>> for point in [(-1, -1), (-1, 4), (-2, 4)]:
...     board[point].data = '.'
>>> print(board.render())
..|......
..|======
..|Z.....
..|......
..|####..
..|#####.

Itération par remplissage.

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

Vérification des coordonnées, déplacement d'un Point selon une direction.

TODO

Recherche du chemin le plus court. (En config par défaut : sans les diagonales).

TODO


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
