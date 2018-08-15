# -*- coding: UTF-8 -*-

from point import Point
from tile import Tile
from board_renderer import BoardRenderer
from positions_iterator import PositionsIterator
from board_iterator import BoardIterator


class Board():

	# TODO : on devrait pouvoir spécifier juste une classe héritée de Tile. Sans lambda.
	def __init__(
		self,
		w=1, h=1,
		tile_generator=lambda x, y: Tile(x, y),
		default_renderer=BoardRenderer(),
	):

		self.w = w
		self.h = h
		self._default_renderer = default_renderer

		self._tiles = [
			[ tile_generator(x, y) for x in range(w) ]
			for y in range(h)
		]


	def get_tile(self, *args, **kwargs):
		point = Point(*args, **kwargs)
		return self._tiles[point.y][point.x]


	def __getitem__(self, *args):
		try:
			point = Point(*args)
		except ValueError:
			point = None

		if point is not None:
			# TODO : raiser une exception si l'une des coords est out of bounds.
			return self._tiles[point.y][point.x]

		# TODO
		print("TODO")
		return args


	def render(self, renderer=None):
		if renderer is None:
			renderer = self._default_renderer
		return renderer.render(self)


	def iter_pos(
		self, *args, **kwargs):

		pos_iter = PositionsIterator(*args, **kwargs)
			#posis, step,
			#tell_jumps, tell_direction_changes,
			#sliding_window, continuous_sliding_window, adjacency)
		return BoardIterator(self, pos_iter)

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


	def iter_osef(self, sense='┌ ┐ └ ┘', tell_prime_coord_change=False, skip_lines=None, rect=None, poses=None):
		if skip_lines is None:
			skip_lines=lambda tile:False
		pass


	def iter_one_vector(self, sense='┌ └', prime_coord=None, x=None, y=None, dir='UPWARD, ...', rect=None):
		# cas particulier de la fonction ci-dessus.
		pass


	def iter_vectors(self, sense='(┌ ┐),(└ ┘)', rect=None):
		# ça va renvoyer des itérateurs, genre iter_one_vector.
		pass


	def iter_by_poses(self, poses):
		pass


	def sort_poses(self, poses, key):
		pass

	# Donc il faut un itérateur sur un rect.

	# Il faut aussi des itérateur de poses avec des ellipsis.
	# Genre : (1, 2), ... ,(5, 2), (1, 3), ..., (6, 3),

	# Une poses est une liste de position. C'est tout. On peut itérer dessus. Et filtrer.
	# Avec la fonction built-in filter().


# ----------------- tests des trucs en cours ------------------
# (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

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
	log(b[11, ...])
	log(b[..., 5])
	log(b[11:18:2])
	log(b[11:18:2, 1:33:5])
	log(b[11:, :33])
	log(b[:, ::5])

	log('Not End')

	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(8, 1) ]

	board = Board(10, 6)

	for index, point in enumerate(board.iter_pos(positions, step=2)):
		point.data = index

	print(board.render())

	print(board.get_tile(1, 4))
	print(board.get_tile(1, 4).data)
	print(board.get_tile(x=0, y=0).data)

	log('End')


if __name__ == '__main__':
	main()
