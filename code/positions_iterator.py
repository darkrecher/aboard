# -*- coding: UTF-8 -*-

from point import (
	Point, Direction,
	is_adjacent, compute_direction,
)


class PositionsIterator():

	def __init__(
		self,
		posis,
		step=1,
		tell_jumps=False,
		tell_direction_changes=False,
		sliding_window=None,
		continuous_sliding_window=None,
		adjacency=None,
	):

		# jump : la coord précédente n'est pas adjacente
		# dir_change, la direction entre :
		#   (la coord précédente-précédente et la coord précédente)
		#   (la coord précédente et l'actuelle)
		# sont différentes.
		# Du coup, pour le jump, il faut se poser la question du type d'adjacence.
		# Diagonale ou pas diagonale ?

		if sliding_window is not None or continuous_sliding_window is not None:
			raise ValueError("TODO sliding_window continuous_sliding_window")

		if tell_jumps or tell_direction_changes:
			raise ValueError("TODO tell_jumps tell_direction_changes")

		# FUTURE : posis peut contenir des ellipsis.
		self.posis = tuple(posis)
		self.step = step
		if self.step > 0:
			self.next_index = 0
		elif self.step < 0:
			self.next_index = len(self.posis) - 1
		else:
			raise ValueError("Le step doit être différent de 0.")

		self.is_adjacent = adjacency or is_adjacent
		self.current_point = None
		self.prev_point = None
		self.prev_prev_point = None
		self.jumped = True
		self.changed_direction = False

	#def pouet(
	#	self, sense='┌ ┐ └ ┘', tell_main_coord_change=False,
	#	skip_lines=None, rect=None, poses=None,
	#	sliding_window=None, continuous_sliding_window=None
	#):
	#	pass

	def __iter__(self):
		return self


	def __next__(self):

		if self.next_index <= -1 or self.next_index >= len(self.posis):
			raise StopIteration

		self.prev_prev_point = self.prev_point
		self.prev_point = self.current_point
		self.current_point = Point(self.posis[self.next_index])

		self.jumped = (
			self.prev_point is None
			or not self.is_adjacent(self.prev_point, self.current_point))

		if self.prev_prev_point is not None and self.prev_point is not None:
			prev_dir = compute_direction(self.prev_prev_point, self.prev_point)
			current_dir = compute_direction(self.prev_point, self.current_point)
			self.changed_direction = prev_dir != current_dir

		self.next_index += self.step
		return self.current_point


# TODO : dans un autre fichier ?
from enum import Enum

class Coord(Enum):
	X = 0
	Y = 1


def iter_from_slice(slice_):
	start = slice_.start or 0
	step = slice_.step or 1
	return iter(range(start, slice_.stop, step))

class RectIterator(PositionsIterator):
	# Retenir la position au "début de la ligne". (TODO : ou pas)
	# TODO : Un moyen de savoir (en consultant le x ou le y) si on est au début d'une ligne ou pas.
	# jumped et changed dir ne suffit pas. Si on itère sur un rect de 2*x, avec adj=diag,
	# on aura des true tout le temps.

	def __init__(self, slice_x, slice_y, main_coord=Coord.Y, adjacency=None):
		"""
		main_coord = Coord.X ou Coord.Y. La coordonnée principale sur laquelle on itère.
		Exemple : le sens de lecture (en alphabet latin), c'est : main_coord = Coord.Y
		Parce qu'on fait varier le X (le Y ne change pas, c'est le principal),
		puis on fait varier un peu le Y, et on fait revarier le X. Etc.
		"""
		self.slice_x = slice_x
		self.slice_y = slice_y
		self.main_coord = main_coord
		self.iter_x = iter_from_slice(slice_x)
		self.iter_y = iter_from_slice(slice_y)
		self.must_init = True

		if self.main_coord == Coord.X:
			self.iter_main = self.iter_x
			self.iter_sub = self.iter_y
		elif self.main_coord == Coord.Y:
			self.iter_main = self.iter_y
			self.iter_sub = self.iter_x
		else:
			raise ValueError("main_coord doit valoir Coord.X ou Coord.Y")

		# TODO : à factoriser, ou pas.
		self.is_adjacent = adjacency or is_adjacent
		self.current_point = None
		self.prev_point = None
		self.prev_prev_point = None
		self.jumped = True
		self.changed_direction = False


	def __iter__(self):
		return self


	def __next__(self):

		if self.must_init:
			x = next(self.iter_x)
			y = next(self.iter_y)
			self.current_point = Point(x, y)
			self.start_of_main = Point(x, y) # TODO : On aura peut-être jamais besoin de ça
			self.must_init = False
			return self.current_point

		# TODO : jumped et changed dir, à factoriser.
		self.prev_prev_point = self.prev_point
		self.prev_point = self.current_point

		try:
			coord_sub = next(self.iter_sub)
			must_change_main = False
		except StopIteration:
			# Faut repartir à la "ligne" suivante.
			must_change_main = True

		if must_change_main:
			# Attention c'est inversé, c'est normal. On réinitialise le sub.
			if self.main_coord == Coord.X:
				self.iter_y = iter_from_slice(self.slice_y)
				self.iter_sub = self.iter_y
			else:
				self.iter_x = iter_from_slice(self.slice_x)
				self.iter_sub = self.iter_x
			x = next(self.iter_x)
			y = next(self.iter_y)
			self.current_point = Point(x, y)

		else:
			# Attention c'est inversé aussi, c'est normal. On fait varier le sub.
			if self.main_coord == Coord.X:
				x = self.current_point.x
				y = coord_sub
			else:
				x = coord_sub
				y = self.current_point.y
			self.current_point = Point(x, y)

		# TODO : jumped et changed dir, à factoriser.
		self.jumped = (
			self.prev_point is None
			or not self.is_adjacent(self.prev_point, self.current_point))

		if self.prev_prev_point is not None and self.prev_point is not None:
			prev_dir = compute_direction(self.prev_prev_point, self.prev_point)
			current_dir = compute_direction(self.prev_point, self.current_point)
			self.changed_direction = prev_dir != current_dir

		return self.current_point


# ----------------- tests des trucs en cours ------------------

def main():

	p = PositionsIterator(((1, 2), (3, 4), (5, 6), (7, 8)))

	for elem in p:
		print(elem)


if __name__ == '__main__':
	main()
