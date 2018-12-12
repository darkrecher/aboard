# -*- coding: UTF-8 -*-

from point import Point
from adjacency import get_default_adjacency
from tile import Tile
from board_renderer import BoardRenderer
from positions_iterator import BoardIteratorRect, Coord


class BoardIndexError(IndexError):
	pass


class Board():

	# TODO : une fonction qui trouve un chemin passant par toutes les positions d'un
	# ensemble donné. (Si c'est possible).
	# Pour résoudre des problèmes "genre 4 elements".

	# TODO : on devrait pouvoir spécifier juste une classe héritée de Tile. Sans lambda.
	def __init__(
		self,
		w=1, h=1,
		tile_generator=lambda x, y: Tile(x, y),
		default_renderer=BoardRenderer(),
		class_adjacency=None,
	):
		self.w = w
		self.h = h
		self._default_renderer = default_renderer

		self.class_adjacency = (
			class_adjacency if class_adjacency is not None
			else get_default_adjacency())

		self.adjacency = self.class_adjacency(self)
		self.is_adjacent = self.adjacency.is_adjacent

		self._tiles = [
			[ tile_generator(x, y) for x in range(w) ]
			for y in range(h)
		]
		self.mobile_items = []
		# clé : un objet Point.
		# valeur : une liste de mobile items
		self.mobile_items_by_pos = {}


	def _indexify_mobi_add(mobile_item):
		# TODO WIP
		pass


	def _indexify_mobi_move(mobile_item):
		# TODO WIP
		pass


	def _indexify_mobi_del(mobile_item):
		# TODO WIP
		pass


	def get_tile(self, *args, **kwargs):
		point = Point(*args, **kwargs)

		# TODO : Dans une toute petite fonction "in_bounds"
		if any((
			point.x < 0,
			point.x >= self.w,
			point.y < 0,
			point.y >= self.h
		)):
			msg = "Coord not in board. coord : %s. board size : %s, %s."
			data = (str(point), self.w, self.h)
			raise BoardIndexError(msg % data)

		return self._tiles[point.y][point.x]


	def __getitem__(self, args):

		# TODO : accès à partir de la fin avec les index négatifs.
		#        aussi bien pour les itération que pour la récup d'un seul élément.

		if not args:
			return BoardIteratorRect(self)

		slice_x = None
		slice_y = None
		id_coord_main = Coord.X

		try:
			iter_on_args = iter(args)
			slice_x = next(iter_on_args)
			slice_y = next(iter_on_args)
			id_coord_main = next(iter_on_args)
		except TypeError:
			slice_x = args
		except StopIteration:
			pass

		if slice_x is None or slice_y is None or isinstance(slice_x, slice) or isinstance(slice_y, slice):

			# Mode itération
			if slice_x is None:
				slice_x = slice(None, None, None)
			if isinstance(slice_x, int):
				slice_x = slice(slice_x, slice_x+1, None)

			if slice_y is None:
				slice_y = slice(None, None, None)
			if isinstance(slice_y, int):
				slice_y = slice(slice_y, slice_y+1, None)

			dict_coord_from_str = {
				'X': Coord.X,
				'Y': Coord.Y,
			}
			if isinstance(id_coord_main, str):
				id_coord_main = id_coord_main.upper()
				if id_coord_main in dict_coord_from_str:
					id_coord_main = dict_coord_from_str[id_coord_main]

			return BoardIteratorRect(self, slice_x, slice_y, id_coord_main)

		try:
			point = Point(*args)
		except ValueError:
			point = None

		if point is not None:
			# Mode un seul élément
			# TODO : raiser une exception si l'une des coords est out of bounds.
			return self._tiles[point.y][point.x]

		# Mode fail
		raise Exception("TODO fail get item" + "".join(args))


	def render(self, renderer=None):
		if renderer is None:
			renderer = self._default_renderer
		return renderer.render(self)


	def set_data_from_string(self, data_lines, sep_line=None, sep_tiles=None):

		if sep_line is not None:
			data_lines = data_lines.split(sep_line)
		board_iter = BoardIteratorRect(self).group_by_subcoord()

		for data_line, board_line in zip(data_lines, board_iter):
			if sep_tiles is not None:
				data_line = data_line.split(sep_tiles)
			for data_tile, tile in zip(data_line, board_line):
				tile.data = data_tile


	# TODO : tout cela est un peu useless, mais je le laisse pour l'instant.
	# Pour de la doc et des réflexions de conception-tralala.

	#def iter_pos(
	#	self, *args, **kwargs):
	#
	#	pos_iter = PositionsIterator(*args, **kwargs)
	#		#posis, step,
	#		#tell_jumps, tell_direction_changes,
	#		#sliding_window, continuous_sliding_window, adjacency)
	#	return BoardPosIterator(self, pos_iter)

	# WIP : comment on va faire des itérateurs sur ce bazar ?
	# https://www.ibm.com/developerworks/library/l-pycon/
	# https://www.python.org/dev/peps/pep-0234/
	# https://wiki.python.org/moin/Iterator

	# On crée une autre classe qui va itérer (Positions).
	# Certaines fonctions de Board renvoient un itérable, mais sur le board.
	# Pas juste sur les positions.
	# Donc faudra encore une autre classe BoardIterator ou un truc du genre.
	# Et donc c'est elle qui itère, avec le Board, et une classe Positions.
	# Et qui renvoie les tiles, et etc.
	# Et juste pour le fun, la classe Board peut être itérable, mais avec une méthode
	# par défaut (de gauche à droite et de haut en bas). Et ça utilise un BoardIterator
	# interne.

	def iter_vectors(self, sense='(┌ ┐),(└ ┘)', rect=None):
		# ça va renvoyer des itérateurs, genre iter_one_vector.
		pass

	def sort_posis(self, posis, key):
		pass

	# TODO : Il faut des itérateur de posis avec des ellipsis.
	# Genre : (1, 2), ... ,(5, 2), (1, 3), ..., (6, 3),

	# Une posis est une liste de point. C'est tout. On peut itérer dessus. Et filtrer.
	# Avec la fonction built-in filter().


	def replace_tile(self, new_tile, pos):
		new_tile.x = pos.x
		new_tile.y = pos.y
		self._tiles[pos.y][pos.x] = new_tile


	def circular_permute_tiles(self, positions):
		# TODO : positions devrait pouvoir être un itérable.
		#        et donc si on pouvait faire des itérables sur les pos, et pas les tiles.
		#        puisque là on bouge les tiles, alors on n'est pas sûr de ce que ça peut donnéer d'itérer dessus en même temps.

		first_pos = positions.pop(0)
		first_tile = self._tiles[first_pos.y][first_pos.x]
		prev_pos = first_pos

		while positions:
			cur_pos = positions.pop(0)
			cur_tile = self._tiles[cur_pos.y][cur_pos.x]
			cur_tile.x = prev_pos.x
			cur_tile.y = prev_pos.y
			self._tiles[prev_pos.y][prev_pos.x] = cur_tile
			prev_pos = cur_pos

		first_tile.x = cur_pos.x
		first_tile.y = cur_pos.y
		self._tiles[cur_pos.y][cur_pos.x] = first_tile





# ----------------- tests des trucs en cours ------------------
# TODO : (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

def main():

	from my_log import debug, answer, log
	log('Hellow')

	# http://sametmax.com/implementer-une-fenetre-glissante-en-python-avec-un-deque/
	from collections import deque
	from itertools import islice

	def window(iterable, size=2):
		iterable = iter(iterable)
		d = deque(islice(iterable, size), size)
		yield d
		for x in iterable:
			d.append(x)
			yield d

	for x in window('azertyuiop', 3):
		log(x)

	b = Board(15, 15)
	log(b[11])
	log(b[11, 5])
	#log(b[11, ...])
	#log(b[..., 5])
	log(b[11:18:2])
	log(b[11:18:2, 1:33:5])
	log(b[11:, :33])
	log(b[:, ::5])

	log('End')


