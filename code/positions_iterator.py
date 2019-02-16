# -*- coding: UTF-8 -*-

from position import Pos, Direction, compute_direction
from iter_indicators import IterIndicator
from sur_iterators import SurIteratorTellIndicators, SurIteratorGroupTiles

ItInd = IterIndicator


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
		self.current_pos = None
		self.prev_pos = None
		self.prev_prev_pos = None
		self.jumped = True
		self.changed_direction = False
		self.both_coord_changed = True
		self.propag_dist = None

	# TODO crap.
	#def pouet(
	#	self, sense='┌ ┐ └ ┘', tell_main_coord_change=False,
	#	skip_lines=None, rect=None, poses=None,
	#	sliding_window=None, continuous_sliding_window=None
	#):
	#	pass

	def __iter__(self):
		return self


	def _update_indicators(self, new_pos):

		self.prev_prev_pos = self.prev_pos
		self.prev_pos = self.current_pos
		self.current_pos = new_pos

		prev_prev_p = self.prev_prev_pos
		prev_p = self.prev_pos
		cur_p = self.current_pos

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

		self.iter_indicators = {
			ItInd.PREV_POS: self.prev_pos,
			ItInd.PREV_PREV_POS: self.prev_prev_pos,
			ItInd.JUMPED: self.jumped,
			ItInd.CHANGED_DIRECTION: self.changed_direction,
			ItInd.BOTH_COORD_CHANGED: self.both_coord_changed,
			ItInd.PROPAG_DIST : self.propag_dist,
		}


	def __next__(self):
		"""
		Il faut définir la nouvelle pos, appeler self._update_indicators(),
		et renvoyer la tile correspondante.
		"""
		raise NotImplemented


	def tell_indicators(self, indic_to_tell=(ItInd.BOTH_COORD_CHANGED, )):
		return SurIteratorTellIndicators(self, indic_to_tell)


	def group_by_subcoord(self):
		return SurIteratorGroupTiles(self)


	def group_by(self, grouping_separator):
		return SurIteratorGroupTiles(self, grouping_separator)


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

		new_pos = Pos(self.posis[self.current_posis_index])
		self._update_indicators(new_pos)
		return self.board.get_tile(self.current_pos)


# TODO : dans un autre fichier ?
from enum import Enum

class Coord(Enum):
	X = 0
	Y = 1


class BoardIteratorRect(BoardIteratorBase):
	# TODO : passer une liste de coord en param, à la place de slices.

	def __init__(
		self, board,
		slice_x=slice(None, None, None), slice_y=slice(None, None, None),
		id_coord_main=Coord.X
	):
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
		self.iter_x = self._iter_from_slice_x()
		self.iter_y = self._iter_from_slice_y()
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


	def _iter_from_slice_x(self):
		# TODO : Dans les tests, ajouter un test avec un slice [1:-1].
		# Normalement ça devrait marcher maintenant.
		# Et y'a tellement de cas tordus qu'il faudra peut-être tester tous les cas possibles.
		# (start, stop, step) X (pos, neg, 0, indéfini).
		# pareil pour le slice_y.
		return iter(range(self.board.w)[self.slice_x])


	def _iter_from_slice_y(self):
		return iter(range(self.board.h)[self.slice_y])


	def skip_sub_coord(self):
		self.nb_sub_coord_to_skip += 1


	def skip_line(self):
		self.skip_sub_coord()


	def skip_col(self):
		self.skip_sub_coord()


	def _apply_skip_sub_coord(self):

		if self.id_coord_main == Coord.X:
			self.iter_x = self._iter_from_slice_x()
			self.iter_main = self.iter_x
		else:
			self.iter_y = self._iter_from_slice_y()
			self.iter_main = self.iter_y

		self.val_coord_sub = next(self.iter_sub)


	def _update_col_line_modification(self, new_val):
		# TODO : useless ??
		self.changed_sub_coord = new_val
		self.changed_line = new_val
		self.changed_col = new_val


	def __next__(self):

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

		new_pos = Pos(x, y)
		self._update_indicators(new_pos)
		return self.board.get_tile(self.current_pos)

