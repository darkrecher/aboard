**********************************
Doc détaillée
**********************************

Objets de base, lecture/écriture simple
=======================================

Un Board est un tableau à deux dimensions contenant des objets Tile.

La taille (largeur, hauteur) est à spécifier à la création.

>>> from aboard import Board
>>> board = Board(7, 4)

 - coordonnées (0, 0) : Tile en haut à gauche,
 - coordonnées (1, 0) : Tile juste à droite,
 - etc.
 - coordonnées (largeur-1, hauteur-1) : dernière Tile tout en bas à droite.

Une Tile possède les attributs suivants :

 - board_father : référence vers l'objet Board contenant la Tile.
 - x, y : position de la Tile dans le Board conteneur.
 - data : string. Donnée quelconque. Initialisée au caractère "." (un point).

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

Avec l'opérateur "[]", remplacez l'une ou les deux coordonnées par un slice, pour faire une itération sur une ligne, une colonne, un sous-rectangle, avec une ligne sur deux, de gauche à droite, ...

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
[<tile.Tile object at 0x00BE6DD0>, <tile.Tile object at 0x00BF1050>, <tile.Tile object at 0x00BF11D0>, <tile.Tile object at 0x00BF1350>]

TODO : et faut que je rajoute un "repr" propre pour les Tile.


Itérateurs par liste de positions
---------------------------------

TODO. Bon c'est moche. Faut pouvoir appeler cet itérateur directement depuis le board.

Pour récupérer plusieurs Tiles à partir de positions arbitraires, il suffit d'itérer à partir d'une liste de coordonnées : ``for coord in [(0, 0), (2, 0), (3, 1)]: current_tile = board[coord]``.

L'itérateur ``BoardIteratorPositions`` permet la même chose, mais renvoie directement les Tiles. Voir chapitre suivant pour un exemple.


Indicateurs d'itérations
-------------------------

Les itérateurs de board possèdent des indicateurs mis à jour automatiquement :

 - prev_point : position précédente (vaut None à la première itération).
 - jumped : vaut True si la position précédente et la position courante ne sont pas adjacentes.
 - changed_direction : vaut True si la direction de déplacement a changé lors de l'itération qui vient d'être effectuée.
 - both_coord_changed : vaut True si les deux coordonnées x et y de la position précédente et de la position courante sont différentes.

Pour les itérateurs par rectangle, l'indicateur ``both_coord_changed`` permet de savoir si on vient de changer de ligne.

>>> iter_board = board[:3, ::]
>>> for tile in iter_board:
...     print("pos:", tile.x, tile.y, "newline: ", iter_board.both_coord_changed)

TODO : ce sera prev_pos. Et aussi tile.pos, et non pas Point(tile.x et tile.y).

>>> positions = [ (0, 0), (1, 0), (2, 0), (4, 0), (4, 1), (3, 3) ]
>>> iter_pos = BoardIteratorPositions(board, positions)
>>> for tile in iter_pos:
...    print(
...        "pos:", Point(tile.x, tile.y),
...        "prev:", iter_pos.prev_point,
...        "indics:",
...        "jumped" * iter_pos.jumped,
...        "changed_dir" * iter_pos.changed_direction,
...        "both_changed" * iter_pos.both_coord_changed
...    )
pos: <Point 0, 0 > prev: None          indics: jumped  both_changed
pos: <Point 1, 0 > prev: <Point 0, 0 > indics:
pos: <Point 2, 0 > prev: <Point 1, 0 > indics:
pos: <Point 4, 0 > prev: <Point 2, 0 > indics: jumped
pos: <Point 4, 1 > prev: <Point 4, 0 > indics:  changed_dir
pos: <Point 3, 3 > prev: <Point 4, 1 > indics: jumped changed_dir both_changed


Sur_iterators
=============

Les sur-itérateurs s'ajoutent après un itérateur de board.


``tell_indicators``
-----------------------------

Il permet de renvoyer directement des indicateurs, durant l'itération.

Les types d'indicateurs renvoyés doivent être spécifiés via des valeurs ``ItInd.*``.

TODO : ItInd doit être accessible depuis aboard.
Re TODO. Bon c'est moche. Faut pouvoir appeler l'itérateur de pos directement depuis le board.

from positions_iterator import ItInd
indics = (ItInd.PREV_POINT, ItInd.JUMPED)
>>> for prev_point, jumped, tile in BoardIteratorPositions(board, positions).tell_indicators(indics):
...    print(
...        "pos:", Point(tile.x, tile.y),
...        "prev:", prev_point,
...        "jumped:", jumped,
...    )
pos: <Point 0, 0 > prev: None          jumped: True
pos: <Point 1, 0 > prev: <Point 0, 0 > jumped: False
pos: <Point 2, 0 > prev: <Point 1, 0 > jumped: False
pos: <Point 4, 0 > prev: <Point 2, 0 > jumped: True
pos: <Point 4, 1 > prev: <Point 4, 0 > jumped: False
pos: <Point 3, 3 > prev: <Point 4, 1 > jumped: True


``group_by``
------------

Il permet de renvoyer les tiles par groupe, selon une fonction de groupement, à indiquer en paramètre.

La fonction a pour paramètre l'itérateur, elle doit renvoyer un booléen. Chaque fois qu'elle renvoie True, le sur-itérateur renvoie le groupe de tile accumulées.

TODO : or donc, current_pos, n'est-ce pas ?

>>> grouping_function = lambda iterator: (iterator.current_point.x % 3) == 0
>>> for tile_group in board[:].group_by(grouping_function):
...     print([(tile.x, tile.y) for tile in tile_group])
[(0, 0), (1, 0), (2, 0)]
[(3, 0), (4, 0), (5, 0)]
[(0, 1), (1, 1), (2, 1)]
[(3, 1), (4, 1), (5, 1)]
[(0, 2), (1, 2), (2, 2)]
[(3, 2), (4, 2), (5, 2)]
[(0, 3), (1, 3), (2, 3)]
[(3, 3), (4, 3), (5, 3)]


``group_by_subcoord``
---------------------

Sur-itérateur de type ``group_by```, dont la fonction de groupement se base sur ``both_coord_changed``. Il permet de récupérer les tiles par groupe de lignes ou de colonnes, à partir d'un itérateur par rectangle.

>>> for tile_group_column in board[:, :, 'y'].group_by_subcoord():
...     print(*map(str, tile_group_column))
<Tile (0, 0): .> <Tile (0, 1): .> <Tile (0, 2): .> <Tile (0, 3): .>
<Tile (1, 0): .> <Tile (1, 1): .> <Tile (1, 2): .> <Tile (1, 3): .>
<Tile (2, 0): .> <Tile (2, 1): .> <Tile (2, 2): .> <Tile (2, 3): .>
<Tile (3, 0): .> <Tile (3, 1): .> <Tile (3, 2): .> <Tile (3, 3): .>
<Tile (4, 0): .> <Tile (4, 1): .> <Tile (4, 2): .> <Tile (4, 3): .>
<Tile (5, 0): .> <Tile (5, 1): .> <Tile (5, 2): .> <Tile (5, 3): .>

Il n'est pas possible d'enchaîner les sur-itérateurs. ``board[:].tell_indicators(x).group_by(y)`` ne fonctionne pas.


Héritage de la classe Tile
==========================

Il est possible de créer des classes héritées de la classe Tile, et de s'en servir pour créer un board.

>>> class MyTile(Tile)
>>> board_with_my_tiles = Board(6, 4, class_tile=MyTile)

TODO : virer le __eq__ de la class Tile, car on ne sait pas ce que ça devrait faire.

Les classes héritées peuvent utiliser d'autres attributs de données, en plus de tile.data.

Il est conseillé d'overrider les fonctions ``__str__`` et ``__repr__``. Les versions de base affichent uniquement tile.data.


Fonction ``Tile.render``
------------------------

Cette fonction peut être overridée. Elle est censée renvoyer une string ou une liste de string, qui est ensuite transmise à la fonction ``board.render``.

Par défaut, chaque tile est rendue sur un seul caractère. Même si ``Tile.render`` en renvoie plus, seul le premier sera utilisé. Il est possible de configurer un renderer pour le faire afficher des tiles sur des rectangles de caractères (voir plus loin).

Lorsque la fonction ``tile.render`` est appelée, deux paramètres ``w`` et ``h`` lui sont indiqués, représentant la taille du rectangle de rendu. La fonction est alors censée renvoyer une liste de ``h`` éléments, chacun d'eux devant être une string de ``w`` caractères.

Si ce n'est pas exactement cette structure de données qui est renvoyée, le renderer la remet en forme. Il coupe des éléments de la liste et des caractères, et ajoute des espaces, de façon à avoir un rectangle de rendu correct.


Objet BoardRenderer
===================

Utilisation
-----------

Il s'agit d'un objet utilisant les données d'un Board, pour générer la string de rendu.

Tous les objets Board possèdent en variable membre un objet BoardRenderer par défaut, qui est utilisé lors de l'appel à ``Board.render()``.

Il est possible de créer un autre BoardRenderer doté d'une configuration spécifique, et de les utiliser pour générer des strings de rendu différentes.

>>> from aboard import BoardRenderer
>>> board = Board(4, 3)
>>> board[1, 1].data = ("ABZZ", "CDZZ", "XXZZ")
>>> my_renderer = BoardRenderer(
...     tile_w=2, tile_h=2, chr_fill_tile='_',
...     tile_padding_w=1, tile_padding_h=0)
>>> print(board.render(renderer=my_renderer))
._ ._ ._ ._
__ __ __ __
._ AB ._ ._
__ CD __ __
._ ._ ._ ._
__ __ __ __

# TODO : faut corriger le renderer de la tile par défaut. return self.data. Tout simplement.

Il est également possible de définir le renderer dès l'instanciation du board.

>>> my_renderer = BoardRenderer(tile_w=2, tile_h=2)
>>> board = Board(4, 3, default_renderer=my_renderer)


Paramètres du renderer
----------------------

Les paramètres sont à indiquer lors de l'instanciation du BoardRenderer. Ils ont tous une valeur par défaut, correspondant à celle du renderer par défaut inclus dans chaque Board.

 - tile_w, tile_h : largeur et hauteur des tiles
 - chr_fill_tile : caractère utilisé pour compléter les rectangles des Tiles, lorsque la fonction ``Tile.render`` ne renvoie pas suffisamment de caractères.
 - tile_padding_w, tile_padding_h : nombre de caractère d'espacement entre chaque Tile, horizontal et vertical. Par défaut : 0.
 - chr_fill_tile_padding : caractère utilisé pour écrire les paddings horizontaux et verticaux. Par défaut : ' ' (espace).


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
