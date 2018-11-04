# -*- coding: UTF-8 -*-

from point import (
	Point, Direction,
	is_adjacent, compute_direction,
)


class BoardIteratorBase():

	def __init__(self, board):

		# jump : la coord précédente n'est pas adjacente
		# dir_change, la direction entre :
		#   (la coord précédente-précédente et la coord précédente)
		#   (la coord précédente et l'actuelle)
		# sont différentes.
		# Du coup, pour le jump, il faut se poser la question du type d'adjacence.
		# Diagonale ou pas diagonale ? (mais on a la fonction dans le board)

		self.board = board
		self.current_point = None
		self.prev_point = None
		self.prev_prev_point = None
		self.jumped = True
		# TODO : renommer ça pour que tout les indicateurs finissent par "ed"
		self.changed_direction = False
		self.both_coord_changed = True

	#def pouet(
	#	self, sense='┌ ┐ └ ┘', tell_main_coord_change=False,
	#	skip_lines=None, rect=None, poses=None,
	#	sliding_window=None, continuous_sliding_window=None
	#):
	#	pass

	def __iter__(self):
		return self


	def _update_indicators(self, new_point):

		self.prev_prev_point = self.prev_point
		self.prev_point = self.current_point
		self.current_point = new_point

		prev_prev_p = self.prev_prev_point
		prev_p = self.prev_point
		cur_p = self.current_point

		if prev_p is not None:

			self.jumped = not self.board.is_adjacent(prev_p, cur_p)

			if prev_prev_p is not None:
				prev_dir = compute_direction( prev_prev_p, prev_p)
				current_dir = compute_direction( prev_p, cur_p)
				self.changed_direction = prev_dir != current_dir

			self.both_coord_changed = (
				(cur_p.x != prev_p.x)
				and (cur_p.y != prev_p.y)
			)


	def __next__(self):
		"""
		Il faut définir le nouveau point, et appeler self._update_indicators().
		"""
		raise NotImplemented


class BoardIteratorPositions(BoardIteratorBase):

	def __init__(self, board, posis):
		super().__init__(board)
		# FUTURE : posis peut contenir des ellipsis.
		# TODO : on n'a peut-être pas besoin de tuplifier ça. Si on itère dessus c'est mieux.
		self.posis = tuple(posis)
		self.current_posis_index = -1


	def __next__(self):

		self.current_posis_index += 1

		if self.current_posis_index >= len(self.posis):
			raise StopIteration

		new_point = Point(self.posis[self.current_posis_index])
		self._update_indicators(new_point)
		return self.board.get_tile(self.current_point)


# TODO : dans un autre fichier ?
from enum import Enum

class Coord(Enum):
	X = 0
	Y = 1


def iter_from_slice(slice_):
	start = slice_.start or 0
	step = slice_.step or 1
	return iter(range(start, slice_.stop, step))


class BoardIteratorRect(BoardIteratorBase):
	# TODO : passer une liste de coord en param, à la place de slices.

	def __init__(self, board, slice_x, slice_y, id_coord_main=Coord.X):
		"""
		id_coord_main = Coord.X ou Coord.Y. La coordonnée principale sur laquelle on itère.
		Exemple : le sens de lecture (en alphabet latin), c'est : id_coord_main = Coord.X
		Parce qu'on itère d'abord sur le X (la coordonnée principale),
		puis on itère un peu le Y, et on re-itère sur le X. Etc.
		"""
		super().__init__(board)
		self.slice_x = slice_x
		self.slice_y = slice_y
		self.id_coord_main = id_coord_main
		self.val_coord_sub = None
		self.iter_x = iter_from_slice(slice_x)
		self.iter_y = iter_from_slice(slice_y)
		self.nb_sub_coord_to_skip = 1

		if self.id_coord_main == Coord.X:
			self.iter_main = None
			self.iter_sub = self.iter_y
		elif self.id_coord_main == Coord.Y:
			self.iter_main = None
			self.iter_sub = self.iter_x
		else:
			raise ValueError("id_coord_main doit valoir Coord.X ou Coord.Y")

		self._update_col_line_modification(None)


	def skip_sub_coord(self):
		self.nb_sub_coord_to_skip += 1


	def skip_line(self):
		self.skip_sub_coord()


	def skip_col(self):
		self.skip_sub_coord()


	def _apply_skip_sub_coord(self):

		if self.id_coord_main == Coord.X:
			self.iter_x = iter_from_slice(self.slice_x)
			self.iter_main = self.iter_x
		else:
			self.iter_y = iter_from_slice(self.slice_y)
			self.iter_main = self.iter_y

		self.val_coord_sub = next(self.iter_sub)


	def _update_col_line_modification(self, new_val):
		# TODO : useless ??
		self.changed_sub_coord = new_val
		self.changed_line = new_val
		self.changed_col = new_val


	def __next__(self):

		# TODO : crap
		#if self.must_init:
		#	x = next(self.iter_x)
		#	y = next(self.iter_y)
		#	self.current_point = Point(x, y)
		#	self.start_of_main = Point(x, y) # TODO : On aura peut-être jamais besoin de ça
		#	self._update_col_line_modification(True)
		#	self.must_init = False
		#	return self.current_point

		while self.nb_sub_coord_to_skip:
			self._apply_skip_sub_coord()
			self.nb_sub_coord_to_skip -= 1
			self._update_col_line_modification(True)

		try:
			val_coord_main = next(self.iter_main)
			must_change_sub = False
		except StopIteration:
			# Faut repartir à la "ligne" suivante.
			must_change_sub = True

		self._update_col_line_modification(must_change_sub)

		if must_change_sub:
			self._apply_skip_sub_coord()
			val_coord_main = next(self.iter_main)
			self._update_col_line_modification(True)

		if self.id_coord_main == Coord.X:
			x = val_coord_main
			y = self.val_coord_sub
		else:
			x = self.val_coord_sub
			y = val_coord_main

		new_point = Point(x, y)
		self._update_indicators(new_point)
		return self.board.get_tile(self.current_point)

