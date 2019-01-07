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

L'opérateur "[]" accepte également les tuples ``board[(3, 2)]``, ainsi que les objets ``Pos``. (Voir plus loin).

TODO : et donc on va renommer la classe Point en Pos, car c'est plus clair comme ça.

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

Les slices renvoient un itérable, mais pas un indexable. On ne peut donc pas accéder directement à un élément en particulier. Mais on peut dérouler l'itérable dans une liste ou un tuple.

>>> board[2, ::]
<positions_iterator.BoardIteratorRect object at 0x00BA6590>
>>> list(board[2, ::])
[<tile.Tile object at 0x00BE6DD0>, <tile.Tile object at 0x00BF1050>, <tile.Tile
object at 0x00BF11D0>, <tile.Tile object at 0x00BF1350>]

TODO : et faut que je rajoute un "repr" propre pour les Tile.


Itérateurs par liste de positions
---------------------------------

TODO. Bon c'est moche. Faut pouvoir appeler cet itérateur directement depuis le board.

Pour récupérer plusieurs Tiles à partir de positions arbitraires, il suffit d'itérer à partir d'une liste de tuple de coordonnées : ``for coord in [(0, 0), (2, 0), (3, 1)]: current_tile = board[coord]``.

L'itérateur ``BoardIteratorPositions`` permet la même chose, mais renvoie directement les Tiles. Voir chapitre suivant pour un exemple.


Informations d'itérations
-------------------------

Les itérateurs possèdent des indicateurs mis à jour automatiquement :

 - prev_point : position précédente (vaut None à la première itération)
 - jumped : vaut True si la position précédente et la position courante ne sont pas adjacentes
 - changed_direction : vaut True si la direction de déplacement a changé lors de l'itération qui vient d'être effectuée
 - both_coord_changed : vaut True si les deux coordonnées x et y de la position précédente et de la position courante sont différentes.

Pour les itérateurs par rectangle, l'indicateur ``both_coord_changed`` permet de savoir si on vient de changer de colonne ou de ligne.

>>> iter_board = board[:3, ::]
>>> for tile in iter_board:
...     print("pos:", tile.x, tile.y, "newline: ", iter_board.both_coord_changed)

TODO : ce sera prev_pos. Et aussi tile.pos, et non pas tile.x et tile.y.

>>> positions = [ (0, 0), (1, 0), (2, 0), (4, 0), (4, 1), (3, 3) ]
>>> iter_pos = BoardIteratorPositions(board, positions)
>>> for tile in iter_pos:
...    print(
...        "pos:", tile.x, tile.y,
...        "prev:", iter_pos.prev_point,
...        "jumped:", iter_pos.jumped,
...        "changed_dir:", iter_pos.changed_direction,
...        "both_changed:", iter_pos.both_coord_changed
...    )
pos: 0 0 prev: None jumped: True changed_dir: False both_changed: True
pos: 1 0 prev: <Point 0, 0 > jumped: False changed_dir: False both_changed: False
pos: 2 0 prev: <Point 1, 0 > jumped: False changed_dir: False both_changed: False
pos: 4 0 prev: <Point 2, 0 > jumped: True changed_dir: False both_changed: False
pos: 4 1 prev: <Point 4, 0 > jumped: False changed_dir: True both_changed: False
pos: 3 3 prev: <Point 4, 1 > jumped: True changed_dir: True both_changed: True



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
