# -*- coding: UTF-8 -*-

import point
import adjacency
from tile import Tile
from board_renderer import BoardRenderer
from positions_iterator import BoardIteratorRect, Coord

Point = point.Point


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
			else adjacency.class_default_adjacency)

		self.adjacency = self.class_adjacency(self)
		self.is_adjacent = self.adjacency.is_adjacent

		self._tiles = [
			[ tile_generator(x, y) for x in range(w) ]
			for y in range(h)
		]


	def get_tile(self, *args, **kwargs):
		point = Point(*args, **kwargs)

		# Dans une toute petite fonction "in_bounds"
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


if __name__ == '__main__':
	main()
