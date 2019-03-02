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

>>> for index, tile in enumerate(board[4::-1, ::-2]):
...     tile.data = index
>>> print(board.render())
......
98765.
......
43210.

Pour itérer en premier sur les colonnes, puis sur les lignes, ajouter le caractère "y" en troisième paramètre.

>>> for index, tile in enumerate(board[::, ::, 'y']):
...     tile.data = index if index < 10 else "."
>>> print(board.render())
048...
159...
26....
37....

Les slices renvoient un itérable, mais pas un indexable. On ne peut donc pas accéder directement à un élément en particulier. Mais on peut dérouler l'itérable dans une liste ou un tuple.

>>> board[2, ::]
<positions_iterator.BoardIteratorRect object at 0x00BA6590>
>>> list(board[2, ::])
[<Tile (2, 0): 8>, <Tile (2, 1): 9>, <Tile (2, 2): .>, <Tile (2, 3): .>]


Itérateurs par liste de positions
---------------------------------

Pour récupérer plusieurs Tiles à partir de positions arbitraires, il suffit d'itérer à partir d'une liste de coordonnées : ``for coord in [(0, 0), (2, 0), (3, 1)]: current_tile = board[coord]``.

La fonction ``Board.iter_positions`` permet la même chose, mais en itérant directement sur les Tiles. Voir chapitre suivant pour un exemple.


Indicateurs d'itérations
-------------------------

Les itérateurs de board possèdent des indicateurs mis à jour automatiquement :

 - prev_pos : position précédente (vaut None à la première itération).
 - jumped : vaut True si la position précédente et la position courante ne sont pas adjacentes.
 - changed_direction : vaut True si la direction de déplacement a changé lors de l'itération qui vient d'être effectuée.
 - both_coord_changed : vaut True si les deux coordonnées x et y de la position précédente et de la position courante sont différentes.

Pour les itérateurs par rectangle, l'indicateur ``both_coord_changed`` permet de savoir si on vient de changer de ligne.

>>> iter_board = board[:3, ::]
>>> for tile in iter_board:
...     print("pos:", tile.x, tile.y, "newline: ", iter_board.both_coord_changed)

>>> positions = [ (0, 0), (1, 0), (2, 0), (4, 0), (4, 1), (3, 3) ]
>>> iter_pos = board.iter_positions(positions)
>>> for tile in iter_pos:
...    print(
...        "pos:", tile.pos,
...        "prev:", iter_pos.prev_pos,
...        "indics:",
...        "jumped" * iter_pos.jumped,
...        "changed_dir" * iter_pos.changed_direction,
...        "both_changed" * iter_pos.both_coord_changed
...    )
pos: <Pos 0, 0 > prev: None        indics: jumped  both_changed
pos: <Pos 1, 0 > prev: <Pos 0, 0 > indics:
pos: <Pos 2, 0 > prev: <Pos 1, 0 > indics:
pos: <Pos 4, 0 > prev: <Pos 2, 0 > indics: jumped
pos: <Pos 4, 1 > prev: <Pos 4, 0 > indics:  changed_dir
pos: <Pos 3, 3 > prev: <Pos 4, 1 > indics: jumped changed_dir both_changed


Sur_iterators
=============

Les sur-itérateurs s'ajoutent après un itérateur de board.


``tell_indicators``
-----------------------------

Il permet de renvoyer directement des indicateurs, durant l'itération.

Les types d'indicateurs renvoyés doivent être spécifiés via des valeurs ``ItInd.*``.

from aboard import ItInd
indics = (ItInd.PREV_POS, ItInd.JUMPED)
>>> for prev_pos, jumped, tile in board.iter_positions(positions).tell_indicators(indics):
...    print(
...        "pos:", tile.pos,
...        "prev:", prev_pos,
...        "jumped:", jumped,
...    )
pos: <Pos 0, 0 > prev: None          jumped: True
pos: <Pos 1, 0 > prev: <Pos 0, 0 > jumped: False
pos: <Pos 2, 0 > prev: <Pos 1, 0 > jumped: False
pos: <Pos 4, 0 > prev: <Pos 2, 0 > jumped: True
pos: <Pos 4, 1 > prev: <Pos 4, 0 > jumped: False
pos: <Pos 3, 3 > prev: <Pos 4, 1 > jumped: True


``group_by``
------------

Il permet de renvoyer les tiles par groupe, selon une fonction de groupement, à indiquer en paramètre.

La fonction a pour paramètre l'itérateur, elle doit renvoyer un booléen. Chaque fois qu'elle renvoie True, le sur-itérateur renvoie le groupe de tile accumulées.

>>> grouping_function = lambda iterator: (iterator.current_pos.x % 3) == 0
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

>>> from aboard import Tile
>>> class MyTile(Tile)
>>> board_with_my_tiles = Board(6, 4, class_tile=MyTile)

Les classes héritées peuvent utiliser d'autres attributs de données, en plus de tile.data.

Il est conseillé d'overrider les fonctions ``__str__`` et ``__repr__``. Les versions de base affichent uniquement tile.data.

La fonction ``__eq__`` peut être overridée. Elle devrait l'être si on utilise la classe ``IteratorGetDifferences`` (qui n'est pas encore documentée ici).

La fonction ``__eq__`` est supposée comparer uniquement les données à l'intérieur de la Tile, et non pas sa position (Tile.data, et non pas Tile.pos).

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


Règle d'adjacence
==================

La règle d'adjacence a pour but d'indiquer, pour deux Tiles d'un même Board, si elles sont adjacentes ou non.

Elle est utilisée dans les fonctions de pathfinding, de remplissage par propagation et pour les indicateurs d'itération (indicateur "jumped").


Sélection de la règle
----------------------

Un board possède dans ses variables membres une instance d'une classe ``AdjacencyEvaluator``, définissant sa règle d'adjacence. Par défaut, un board utilise ``AdjacencyEvaluatorCross``, qui considère que deux tiles sont adjacentes si elles sont côte à côte, sur la même ligne ou la même colonne, mais pas en diagonale.

Pour utiliser une autre règle d'adjacence, il faut la spécifier lors de la création du board.

>>> from adjacency import AdjacencyEvaluatorCrossDiag
>>> board_adj_diag = Board(4, 3, class_adjacency=AdjacencyEvaluatorCrossDiag)

La classe ``AdjacencyEvaluatorCrossDiag`` considère que deux tiles sont adjacente si elles sont côte à côte ou en diagonale.

>>> print([
...    str(tile)
...    for tile in board.get_by_pathfinding((0, 1), (1, 2))
... ])
['<Tile (0, 1): .>', '<Tile (1, 1): .>', '<Tile (1, 2): .>']
>>> print([
...    str(tile)
...    for tile in board_adj_diag.get_by_pathfinding((0, 1), (1, 2))
... ])
['<Tile (0, 1): .>', '<Tile (1, 2): .>']

Il est également possible de redéfinir l'adjacence par défaut, qui sera utilisée lors de la création de tous les prochains Boards.

>>> from adjacency import set_default_adjacency
>>> set_default_adjacency(AdjacencyEvaluatorCrossDiag)


Création d'une règle d'adjacence customisée
-------------------------------------------

Pour créer une autre règle d'adjacence, il faut hériter la classe ``AdjacencyEvaluator``, et surcharger deux de ses fonctions :

 - ``is_adjacent(self, pos_1, pos_2)`` : renvoie un booléen, indiquant si les deux positions passées en paramètre sont adjacentes.
 - ``adjacent_positions(self, pos):`` : renvoie un itérateur qui liste toutes les positions adjacentes à celle passée en paramètre.

La classe héritée possède un paramètre ``board``, correspondant au Board d'appartenance, sur lequel la règle d'adjacence doit s'appliquer.

Exemple de création d'une règle d'adjacence "torique". Cette règle considère que le Board est un tore. Lorsqu'on se déplace sur un bord, on est téléporté de l'autre côté. Les tiles tout à droite sont adjacentes avec celles tout à gauche, et les tiles tout en bas sont adjacentes avec celles tout en haut.

>>> from aboard import Pos
>>> class AdjacencyEvaluatorCrossTore(AdjacencyEvaluator):
...     def is_adjacent(self, pos_1, pos_2):
...         if pos_1.x == pos_2.x:
...             if (pos_1.y + 1) % self.board.h == pos_2.y:return True
...             if (pos_2.y + 1) % self.board.h == pos_1.y:return True
...         if pos_1.y == pos_2.y:
...             if (pos_1.x + 1) % self.board.w == pos_2.x:return True
...             if (pos_2.x + 1) % self.board.w == pos_1.x:return True
...         return False
...     def adjacent_positions(self, pos):
...         offsets = [ (0, -1), (+1, 0), (0, +1), (-1, 0) ]
...         for offset_x, offset_y in offsets:
...             x = (pos.x + offset_x + self.board.w) % self.board.w
...             y = (pos.y + offset_y + self.board.h) % self.board.h
...             yield Pos(x, y)
>>> board_adj_tore = Board(11, 3, class_adjacency=AdjacencyEvaluatorCrossTore)
>>> for tile in board_adj_tore.get_by_pathfinding((2, 1), (9, 1)):
...     tile.data = 'X'
>>> print(board_adj_tore.render())
...........
XXX......XX
...........

Avec cette règle, le chemin le plus court pour aller de (2, 1) à (9, 1) n'est pas un déplacement vers la droite, mais vers la gauche. On est téléporté du côté gauche vers le côté droit.


Fonction de remplissage par propagation
=======================================

La fonction ``Board.get_by_propagation`` effectue une itération à partir d'une tile initiale, et se propage petit à petit vers les tiles adjacentes remplissant la "condition de propagation". Par défaut, cette condition est vraie si la ``data`` de la tile vers laquelle on se propage vaut le caractère '.'. Il est possible de la redéfinir via le paramètre ``propag_condition``.

Il s'agit d'une fonction ayant deux paramètres : ``tile_source`` (la tile de départ actuelle), ``tile_dest`` (la tile vers laquelle on tente de se propager). Cette fonction doit renvoyer un booléen, indiquant si la propagation est possible ou non.

>>> def to_right_and_last_column(tile_source, tile_dest):
...     if tile_dest.x > tile_source.x:return True
...     if tile_dest.x == tile_dest.board_father.w-1:return True
...     return False
>>> board = Board(6, 5)
>>> for tile in board.get_by_propagation((1, 2), to_right_and_last_column):
...     tile.data = 'X'
>>> print(board.render())
.....X
.....X
.XXXXX
.....X
.....X

La propagation utilise la règle d'adjacence par défaut du board. L'ordre d'itération dépend de l'ordre des tiles renvoyées par la fonction ``adjacent_positions``.

>>> board = Board(6, 5)
>>> for index, tile in enumerate(
...    board.get_by_propagation((1, 2), to_right_and_last_column)
... ):
...     tile.data = index
>>> print(board.render())
.....7
.....5
.01234
.....6
.....8

Le changement de règle d'adjacence peut avoir des conséquences sur la propagation.

>>> board = Board(6, 5, class_adjacency=AdjacencyEvaluatorCrossDiag)
>>> for tile in board.get_by_propagation((1, 2), to_right_and_last_column):
...     tile.data = 'X'
>>> print(board.render())
...XXX
..XXXX
.XXXXX
..XXXX
...XXX

L'itérateur par propagation possède un indicateur spécifique : ``PROPAG_DIST``, indiquant la distance parcourue depuis la tile initiale jusqu'à la case courante.

>>> board = Board(6, 5)
>>> board_it = board.get_by_propagation((1, 2), to_right_and_last_column)
>>> for dist, tile in board_it.tell_indicators((ItInd.PROPAG_DIST, )):
...     tile.data = dist
>>> print(board.render())
.....6
.....5
.01234
.....5
.....6


Path-finding
============

La fonction ``Board.get_by_pathfinding`` recherche un chemin le plus court entre deux positions, et effectue une itération dessus, à partir de la tile de départ vers la tile d'arrivée.

Cette fonction utilise une "condition de déplacement", similaire à la condition de propagation. Par défaut, le déplacement est possible si la ``data`` de la tile vers laquelle on se propage vaut le caractère '.'. Il est possible de la redéfinir via le paramètre ``pass_through_condition``.

Le path-finding utilise les règles d'adjacence par défaut du board. Lorsqu'il existe plusieurs possibilités de chemin le plus court, la fonction en sélectionne un seul. Cette sélection dépend de l'ordre des tiles renvoyées par la fonction ``adjacent_positions``.

La fonction ``pass_through_condition`` fonctionne de la même manière que ``propag_condition``. Elle possède deux paramètres : ``tile_source`` (la tile de départ actuelle), ``tile_dest`` (la tile vers laquelle on tente de se déplacer), et doit renvoyer un booléen, indiquant si le déplacement est possible ou non.

Le path-finding déclenche une exception ``ValueError`` si il n'existe aucun chemin possible.

>>> board = Board(9, 7)
>>> for tile in board[2:7, 2]:tile.data = '#'
>>> for tile in board[2, 3:6]:tile.data = '#'
>>> for tile in board[6, 3:6]:tile.data = '>'
>>> for tile in board[2:7, 5]:tile.data = '#'
>>> print(board.render())
.........
.........
..#####..
..#...>..
..#...>..
..#####..
.........

>>> for tile in board.get_by_pathfinding((3, 4), (0, 0)):
...     if tile.data != '>': tile.data = '*'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/path/to/git/aboard/code/propagation_iterator.py", line 121, in __iter__
    raise ValueError("Impossible de trouver un chemin")
ValueError: Impossible de trouver un chemin

>>> def my_pass_through_condition(tile_source, tile_dest):
...     tile_datas = (tile_source.data, tile_dest.data)
...     if tile_datas == ('.', '.'):return True
...     if tile_datas in (('.', '>'), ('>', '.')):
...         return tile_source.x <= tile_dest.x
...     return False

>>> for tile in board.get_by_pathfinding((3, 4), (0, 0), my_pass_through_condition):
...     if tile.data != '>': tile.data = '*'
>>> print(board.render())
********.
.......*.
..#####*.
..#...>*.
..#***>*.
..#####..
.........

Le chemin aurait été un peu différent avec une règle d'adjacence autorisant les diagonales.


Échanges et permutations circulaires de tiles
=============================================

Chaque case d'un Board ne doit contenir rien d'autre qu'une Tile (pas de None, pas de liste de Tile, etc.). Les Tiles ne sont pas supposées se déplacer dans le Board. Pour représenter des éléments qui se déplacent d'une case à l'autre, il faut modifier la variable ``tile.data``, ou utiliser des ``MobileItems`` (voir plus loin).

Cependant, comme cette fonctionnalité pourrait être utile, et que les ``MobileItem`` ne sont pas terminés, il est possible d'utiliser la fonction ``board.replace_tile``. Celle-ci met à jour automatiquement les variables ``tile.x`` et ``tile.y``.

>>> board = Board(3, 2)
>>> new_t = Tile()
>>> new_t.data = 'A'
>>> print(new_t)
<Tile (None, None): A>
>>> board.replace_tile(new_t, Pos(0, 1))
>>> print(board.render())
...
A..
>>> print(new_t)
<Tile (0, 1): A>

Pour déplacer plusieurs tiles en une seule opération de permutation circulaire, utiliser la fonction ``board.circular_permute_tiles``.

>>> board = Board(6, 3)
>>> for index, tile in enumerate(board[:, 1]):
...     tile.data = index
>>> positions = [ Pos(tile) for tile in board[1:5, 1] ]
>>> board.circular_permute_tiles(positions)
>>> print(board.render())
......
023415
......


build pour codingame
====================

La librairie aboard est compilée en un seul fichier de code : ``code/builder/aboard_standalone.py``. Ce fichier permet une utilisation de la librairie dans des contextes spécifiques. Par exemple, il est possible de copier-coller son contenu dans un puzzle ou un challenge du site codingame.com.

Le début du fichier stand-alone indique la version et le commit git qui ont été utilisés pour le générer.

Le script ``code/builder/builder.py`` permet de regénérer manuellement ce fichier à partir du code actuel.


Mobile Items (en construction)
=============================

Ça fonctionne mais ce n'est vraiment pas pratique et il n'y a pas beaucoup de fonctions pour les manipuler, les déplacer, etc.

Cette partie sera détaillé plus tard.

>>> from mobitem import MobileItem
>>> board = Board(2, 2)
>>> mobitem = MobileItem(tile_owner=board[0, 0])
>>> print(board.render())
..
.#
>>> mobitem.move(x=1, y=0)
>>> mobitem.data = 'M'
>>> print(board.render())
.M
..


exemple complet
===============

Exemple inspiré du challenge codingame "Xmas Rush", lui-même inspiré du jeu de plateau "Labyrinthe".

Chaque Tile possède duex attributs spécifiques :

 - ``mid_marker`` : une string (ou l'équivalent), dont seul le premier caractère est utilisé.
 - ``roads`` : dictionnaire contenant 4 éléments, les clés étant les 4 directions. La valeur de chaque clé est un booléen, indiquant si la tile possède une ouverture dans la direction donnée.

Une Tile est rendu sur un carré de 3*3 caractères, avec l'affichage des chemins, et le ``mid_marker`` écrit au milieu.

La règle d'adjacence est celle par défaut : les 4 directions, mais pas de diagonale.

L'initialisation du board est effectuée par un tableau de caractère, chacun d'eux permet de déduire le contenu du ``roads`` de la Tile concernée.


```

from aboard import Board, Tile, Dir, BoardRenderer, compute_direction

class XmasTile(Tile):

	DICT_ROADFUL_DIRS_FROM_CHAR = {
		'-': (Dir.LEFT, Dir.RIGHT),
		'|': (Dir.UP, Dir.DOWN),
		'L': (Dir.UP, Dir.RIGHT),
		'F': (Dir.DOWN, Dir.RIGHT),
		'7': (Dir.DOWN, Dir.LEFT),
		'J': (Dir.UP, Dir.LEFT),
		'+': (Dir.LEFT, Dir.RIGHT, Dir.UP, Dir.DOWN),
		' ': (),
	}


	def __init__(self, x=None, y=None, board_father=None):
		super().__init__(x, y, board_father)
		self.roads = {
			Dir.UP: False,
			Dir.RIGHT: False,
			Dir.DOWN: False,
			Dir.LEFT: False,
		}
		self.mid_marker = ' '


	def dirs_from_input(self, char_roadful):
		for dir_ in XmasTile.DICT_ROADFUL_DIRS_FROM_CHAR[char_roadful]:
			self.roads[dir_] = True


	def render(self, w=3, h=3):

		path_up = '|' if self.roads[Dir.UP] else ' '
		path_left = '-' if self.roads[Dir.LEFT] else ' '
		path_right = '-' if self.roads[Dir.RIGHT] else ' '
		path_down = '|' if self.roads[Dir.DOWN] else ' '
		template = " %s \n%s%s%s\n %s "

		data = (
			path_up,
			path_left,
			self.mid_marker[:1].rjust(1),
			path_right,
			path_down,
		)

		str_result = template % data
		# Will return something weird if self.mid_marker contains a newline.
		# Not supposed to happen.
		return str_result.split('\n')

renderer = BoardRenderer(
	tile_w=3, tile_h=3,
	tile_padding_w=1, tile_padding_h=1, chr_fill_tile_padding=' ')

board = Board(
	6, 5, class_tile=XmasTile,
	default_renderer=renderer,
)

BOARD_MAP = """
 F---7
F+7  |
||   |
L----J
"""

board_map = BOARD_MAP.replace('\n', '')

for tile, char_roadful in zip(board, board_map):
	tile.dirs_from_input(char_roadful)

def pass_through_xmas(tile_source, tile_dest):
	dir_ = compute_direction(tile_source, tile_dest)
	roads_to_check = {
		Dir.UP:(Dir.UP, Dir.DOWN),
		Dir.DOWN:(Dir.DOWN, Dir.UP),
		Dir.LEFT:(Dir.LEFT, Dir.RIGHT),
		Dir.RIGHT:(Dir.RIGHT, Dir.LEFT),
	}
	road_to_check = roads_to_check.get(dir_)
	if road_to_check is None:
		# Not supposed to happen
		return False
	road_source, road_dest = road_to_check
	return tile_source.roads[road_source] and tile_dest.roads[road_dest]


for index, tile in enumerate(board.get_by_pathfinding((0, 3), (2, 0), pass_through_xmas)):
	tile.mid_marker = str(index)


print(board.render())

     4- -5- - - - - -
     |               |

     |               |
 2- -3- -
 |   |   |           |

 |   |               |
 1
 |   |               |

 |                   |
 0- - - - - - - - - -


```

