# -*- coding: UTF-8 -*-

# Version stand-alone de la librairie python aboard.
# https://github.com/darkrecher/aboard
# https://aboard.readthedocs.io/fr/latest/
#
# Date du build : 2019-01-02 10:12
# commit git : cedfdc9fe5cc177f36177701c46b3a17de5cd0b5


"""
On va faire simple.
C'est étonnant comme un truc aussi simple que le log peut devenir compliqué.
Dans tout un tas de cas.
Je veux juste écrire des conneries. C'est possible ou bien ?
"""

import sys

def log(*args):
	print(*args, file=sys.stderr)


# -*- coding: UTF-8 -*-

# TODO : Les directions, dans un autre fichier

from enum import IntEnum

class Direction(IntEnum):
	# C'est dans l'ordre du sens des aiguilles d'une montre, en commençant par le haut.
	# Classic
	UP = 0
	UP_RIGHT = 1
	RIGHT = 2
	DOWN_RIGHT = 3
	DOWN = 4
	DOWN_LEFT = 5
	LEFT = 6
	UP_LEFT = 7
	# Classic abbr.
	U = 0
	UR = 1
	R = 2
	DR = 3
	D = 4
	DL = 5
	L = 6
	UL = 7
	# Cardinal
	NORTH = 0
	NORTH_EAST = 1
	EAST = 2
	SOUTH_EAST = 3
	SOUTH = 4
	SOUTH_WEST = 5
	WEST = 6
	NORTH_WEST = 7
	# Cardinal abbr.
	N = 0
	NE = 1
	E = 2
	SE = 3
	S = 4
	SW = 5
	W = 6
	NW = 7
	# Numeric pad.
	PAD_8 = 0
	PAD_9 = 1
	PAD_6 = 2
	PAD_3 = 3
	PAD_2 = 4
	PAD_1 = 5
	PAD_4 = 6
	PAD_7 = 7

# Alias
Dir = Direction

DICT_DIR_FROM_STR = {
	# Box-drawing chars (https://en.wikipedia.org/wiki/Box-drawing_character)
	'┬': Dir.UP,
	'┐': Dir.UP_RIGHT,
	'┤': Dir.RIGHT,
	'┘': Dir.DOWN_RIGHT,
	'┴': Dir.DOWN,
	'└': Dir.DOWN_LEFT,
	'├': Dir.LEFT,
	'┌': Dir.UP_LEFT,
	# Arrows (ne marche pas complètement bien dans Sublime Text, mais c'est pas grave)
	'↑': Dir.UP,
	'↗': Dir.UP_RIGHT,
	'→': Dir.RIGHT,
	'↘': Dir.DOWN_RIGHT,
	'↓': Dir.DOWN,
	'↙': Dir.DOWN_LEFT,
	'←': Dir.LEFT,
	'↖': Dir.UP_LEFT,
	# Ascii arrows
	'^': Dir.UP,
	'>': Dir.RIGHT,
	'v': Dir.DOWN,
	'V': Dir.DOWN,
	'<': Dir.LEFT,
}

def dir_from_str(char):
	# FUTURE : raiser une exception spécifique si y'a pas le char dans dict.
	return DICT_DIR_FROM_STR[char]


class Pos():

	def __init__(self, param_1=None, param_2=None, x=None, y=None):

		if hasattr(param_1, 'x') and hasattr(param_1, 'y'):
			if self._compute_coords(param_1.x, param_1.y):
				return

		try:
			final_x = param_1['x']
			final_y = param_1['y']
		except TypeError:
			pass
		else:
			if self._compute_coords(final_x, final_y):
				return

		try:
			# FUTURE : il faudrait vérifier que param_1 est itérable,
			# et également ordonné.
			# Ce code fonctionne avec un objet "Set", mais de manière
			# non déterministe. On ne sait pas ce qui va dans x ni dans y.
			iter_param_1 = iter(param_1)
			final_x = next(iter_param_1)
			final_y = next(iter_param_1)
		except TypeError:
			pass
		except StopIteration:
			pass
		else:
			if self._compute_coords(final_x, final_y):
				return

		if self._compute_coords(param_1, param_2):
			return

		if self._compute_coords(x, y):
			return

		raise ValueError("Impossible de déduire des coordonnées de ces params : %s %s %s %s" % (param_1, param_2, x, y))


	def _compute_coords(self, final_x, final_y):
		try:
			int_final_x = int(final_x)
			int_final_y = int(final_y)
		except TypeError:
			return False
		except ValueError:
			return False
		else:
			self.x = int_final_x
			self.y = int_final_y
			return True


	def __str__(self):
		return '<Pos %s, %s >' % (str(self.x), str(self.y))


	def as_tuple(self):
		return self.x, self.y


	def as_dict(self):
		return {'x': self.x, 'y': self.y }


	# TODO : fonction à tester vite fait.
	def move(self, direction, dist=1):
		DICT_VECT_FROM_DIRS = {
			Dir.UP: (0, -1),
			Dir.UP_RIGHT: (+1, -1),
			Dir.RIGHT: (+1, 0),
			Dir.DOWN_RIGHT: (+1, +1),
			Dir.DOWN: (0, +1),
			Dir.DOWN_LEFT: (-1, +1),
			Dir.LEFT: (-1, 0),
			Dir.UP_LEFT: (-1, -1),
		}
		mov_x, mov_y = DICT_VECT_FROM_DIRS[direction]
		self.x += mov_x * dist
		self.y += mov_y * dist


	def __eq__(self, other):
		pos_other = Pos(other)
		return self.x == pos_other.x and self.y == pos_other.y


	def __hash__(self):
		return hash((self.x, self.y))


# --- Direction operations ---

def cmp(a, b):
	# https://stackoverflow.com/questions/15556813/python-why-cmp-is-useful
	return (a > b) - (a < b)

def compute_direction(pos_1, pos_2):
	cmp_x = cmp(pos_2.x, pos_1.x)
	cmp_y = cmp(pos_2.y, pos_1.y)
	cmps = (cmp_x, cmp_y)
	DICT_DIR_FROM_CMPS = {
		(0, 0): None,
		(0, -1): Dir.UP,
		(+1, -1): Dir.UP_RIGHT,
		(+1, 0): Dir.RIGHT,
		(+1, +1): Dir.DOWN_RIGHT,
		(0, +1): Dir.DOWN,
		(-1, +1): Dir.DOWN_LEFT,
		(-1, 0): Dir.LEFT,
		(-1, -1): Dir.UP_LEFT,
	}
	return DICT_DIR_FROM_CMPS[cmps]

# -*- coding: UTF-8 -*-


class AdjacencyEvaluator():

	def __init__(self, board):
		self.board = board

	def is_adjacent(self, pos_1, pos_2):
		raise NotImplemented

	def adjacent_tiles(self, pos):
		raise NotImplemented


class AdjacencyEvaluatorCross(AdjacencyEvaluator):

	def is_adjacent(self, pos_1, pos_2):
		if pos_1.x == pos_2.x:
			return pos_1.y-pos_2.y in (-1, 1)
		if pos_1.y == pos_2.y:
			return pos_1.x-pos_2.x in (-1, 1)
		return False

	def adjacent_positions(self, pos):
		# Il est conseillé de mettre dans le même ordre que l'ordre des Direction.
		# C'est à dire dans le sens des aiguilles d'une montre.
		# (Mais ce n'est pas tout le temps possible avec des fonctions d'adjacences tordues)
		offsets = [ (0, -1), (+1, 0), (0, +1), (-1, 0) ]
		for offset in offsets:
			x = pos.x + offset[0]
			y = pos.y + offset[1]
			# TODO : le check de inbounds devrait être dans la classe board, tellement c'est un truc basique.
			if (0 <= x < self.board.w) and (0 <= y < self.board.h):
				yield Pos(x, y)


class AdjacencyEvaluatorCrossDiag(AdjacencyEvaluator):

	def is_adjacent(self, pos_1, pos_2):
		abs_diff_x = abs(pos_1.x-pos_2.x)
		abs_diff_y = abs(pos_1.y-pos_2.y)
		return (
			(abs_diff_x, abs_diff_y) != (0, 0)
			and abs_diff_x <= 1
			and abs_diff_y <= 1
		)

	def adjacent_positions(self, pos):
		# Il est conseillé de mettre dans le même ordre que l'ordre des Direction.
		# C'est à dire dans le sens des aiguilles d'une montre.
		# (Mais ce n'est pas tout le temps possible avec des fonctions d'adjacences tordues)
		offsets = [
			(0, -1), (+1, -1), (+1, 0), (+1, +1),
			(0, +1), (-1, +1), (-1, 0), (-1, -1),
		]
		for offset in offsets:
			x = pos.x + offset[0]
			y = pos.y + offset[1]
			# TODO : le check de inbounds devrait être dans la classe board, tellement c'est un truc basique.
			if (0 <= x < self.board.w) and (0 <= y < self.board.h):
				yield Pos(x, y)


# TODO : les adjacences toriques. Avec les tests qui vont bien.
# TODO : tester les fonctions adjacent_positions.
# FUTURE : un itérateur qui renvoie des None sur les poss pas valides. (je sais pas si on en aura besoin)


class_default_adjacency = AdjacencyEvaluatorCross


def set_default_adjacency(new_class_default_adjacency):
	global class_default_adjacency
	class_default_adjacency = new_class_default_adjacency

def get_default_adjacency():
	global class_default_adjacency
	return class_default_adjacency
# -*- coding: UTF-8 -*-

from enum import IntEnum


class IterIndicator(IntEnum):
	PREV_POS = 0
	PREV_PREV_POS = 1
	JUMPED = 2
	CHANGED_DIRECTION = 3
	BOTH_COORD_CHANGED = 4
	PROPAG_DIST = 5

ItInd = IterIndicator

# -*- coding: UTF-8 -*-



class Tile():

	def __init__(self, x=None, y=None, board_father=None):
		# TODO : il faut accepter le même bazar de param que pour l'objet Pos. Ou pas.
		# TODO : renommer board_father en board_owner.
		self.x = x
		self.y = y
		# TODO : est-ce qu'on autorise des tiles sans coord, qui "flotte un peu dans les airs", ou pas ?
		try:
			self.pos = Pos(x, y)
		except:
			self.pos = None
		self.board_father = board_father
		self.data = '.'
		self.mobile_items = []


	def __str__(self):
		return '<Tile (%s, %s): %s>' % (self.x, self.y, self.data)


	def render(self, w=1, h=1):
		return str(self.data)[:w]


	def __eq__(self, other):
		return self.data == other.data


	# TODO WIP pas testé.
	def is_adjacent(self, other):
		if self.board_father is None:
			raise Exception("board_father must be defined.")
		# Ça va raiser des exceptions si le board_father n'est pas comme il faut
		# Osef, c'est ce qu'on veut.
		return self.board_father.is_adjacent(self, other)
# -*- coding: UTF-8 -*-



# BIG TODO : vu qu'on va afficher des tiles avec des mobitems dessus,
# il va carrément falloir un objet "Canvas / Surface / GraphicContext".
# Mais au lieu que ce soit des pixels, ce sera des chars.
# On fera simple, quand même.

class BoardRenderer():

	AUTHORIZED_ATTRIBUTES = {
		'tile_w': 1, 'tile_h': 1, 'chr_fill_tile': ' ',
		'word_wrap': False,
		'tile_padding_w': 0, 'tile_padding_h': 0,
		'chr_fill_tile_padding': ' ',
		'tile_border_vertic': False, 'tile_border_horiz': False,
		'chr_tile_border_vertic': '|', 'chr_tile_border_horiz': '-',
		'chr_tile_border_cross': '+',
		'deduce_board_style_from_tile_style': False,
		'board_padding_w': 0, 'board_padding_h': 0,
		'chr_fill_board_padding': ' ',
		'board_border_vertic': False, 'board_border_horiz': False,
		'chr_board_border_vertic': '|', 'chr_board_border_horiz': '-',
		'chr_board_border_cross': '+',
	}

	NOT_IMPLEMENTED = [
		'word_wrap',
		'tile_border_vertic', 'tile_border_horiz',
		'chr_tile_border_vertic', 'chr_tile_border_horiz',
		'chr_tile_border_cross',
		'deduce_board_style_from_tile_style',
		'board_padding_w', 'board_padding_h',
		'chr_fill_board_padding',
		'board_border_vertic', 'board_border_horiz',
		'chr_board_border_vertic', 'chr_board_border_horiz',
		'chr_board_border_cross',
	]

	def __init__(self, **kwargs):

		for key_attr in kwargs:
			if key_attr not in BoardRenderer.AUTHORIZED_ATTRIBUTES:
				raise ValueError("Paramètre inconnu : " + key_attr)
			if key_attr in BoardRenderer.NOT_IMPLEMENTED:
				raise ValueError("TODO : " + key_attr)

		dict_attrs = dict(BoardRenderer.AUTHORIZED_ATTRIBUTES)
		dict_attrs.update(kwargs)
		for key_attr, val_attr in dict_attrs.items():
			setattr(self, key_attr, val_attr)


	def _str_resized(self, value):
		w = self.tile_w
		return str(value).ljust(w, self.chr_fill_tile)[:w]


	def _render_tile(self, tile):
		"""
		Renvoie une liste de tile_h string, chacune ayant une taille tile_w.
		"""
		tile_res = tile.render(self.tile_w, self.tile_h)

		if isinstance(tile_res, str):
			process_as_string = True
		else:
			try:
				_ = iter(tile_res)
				process_as_string = False
			except TypeError:
				process_as_string = True

		if process_as_string:
			lines = [ self._str_resized(tile_res) ]
		else:
			lines = []
			for index, line in enumerate(tile_res):
				if index >= self.tile_h:
					break
				lines.append(self._str_resized(line))

		last_lines = [ self.chr_fill_tile*self.tile_w ] * (self.tile_h - 1)

		# Pour l'instant, on n'affiche que la première ligne des mobile_items. Osef.
		first_line = lines[0]
		for mobile_item in tile.mobile_items:
			line_mobitem = mobile_item.render()
			if line_mobitem is not None:
				first_line = line_mobitem + first_line[len(line_mobitem):]

		lines[0] = first_line[:self.tile_w]

		return lines + last_lines


	def render_iter_lines(self, board):
		# TODO : utiliser un itérateur de Board
		render_result = ''
		interval_tile_w = self.chr_fill_tile_padding * self.tile_padding_w
		interval_line_h = interval_tile_w.join((
			[ self.chr_fill_tile_padding*self.tile_w ] * board.w
		))

		for y in range(board.h):

			rendered_tiles = [
				self._render_tile(board.get_tile(x, y))
				for x in range(board.w)
			]

			for index_line in range(self.tile_h):

				yield interval_tile_w.join((
					rendered_tiles[x][index_line]
					for x in range(board.w)
				))

			if y < board.h-1:
				for index_interval in range(self.tile_padding_h):
					yield interval_line_h


	def render(self, board):
		return '\n'.join(self.render_iter_lines(board))
# -*- coding: UTF-8 -*-


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
		Il faut définir le nouveau pos, appeler self._update_indicators(),
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
		# TODO : faut trouver le fonctionnement exact des slices.
		# Et factoriser ça dans une fonction de base, générique tools et tout ça.
		# Actuellement, un truc comme [1:-1] ne marchera pas.
		# Et y'a tellement de cas tordus qu'il faudra peut-être tester tous les cas possibles.
		# (start, stop, step) X (pos, neg, 0, indéfini).
		step = self.slice_x.step
		if step is None: step = 1

		start = self.slice_x.start
		stop = self.slice_x.stop
		if step > 0:
			if start is None: start = 0
			if stop is None: stop = self.board.w
		else:
			if start is None: start = self.board.w - 1
			if stop is None: stop = -1

		#print('TODO debug x', start, stop, step)
		return iter(range(start, stop, step))


	def _iter_from_slice_y(self):

		step = self.slice_y.step
		if step is None: step = 1

		start = self.slice_y.start
		stop = self.slice_y.stop
		if step > 0:
			if start is None: start = 0
			if stop is None: stop = self.board.h
		else:
			if start is None: start = self.board.h - 1
			if stop is None: stop = -1

		#print('TODO debug y', start, stop, step)
		return iter(range(start, stop, step))


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

# -*- coding: UTF-8 -*-



# TODO : un sur-itérateur renvoyant la distance de propagation.


propag_cond_default = lambda tile_source, tile_dest: tile_dest.data == '.'


class BoardIteratorPropagation(BoardIteratorBase):

	def __init__(self, board, pos_start, propag_condition=propag_cond_default):
		# TODO : avec plusieurs pos_start.
		super().__init__(board)
		self.propag_condition = propag_condition
		# Dict
		#  - clé : le pos propagé.
		#  - valeur : la distance depuis le pos de départ jusqu'au pos propagé.
		self.propagated_poss = {}
		# liste de tuple de 2 éléments : la distance et le pos propagé.
		self.to_propagate_poss = [ (0, Pos(pos_start)) ]


	def __iter__(self):
		return self


	def __next__(self):

		if self.to_propagate_poss:

			dist, new_pos = self.to_propagate_poss.pop(0)
			self.propagated_poss[new_pos] = dist

			to_propagate_only_poss = [
				o_pos for o_dist, o_pos
				in self.to_propagate_poss
			]
			for adj_pos in self.board.adjacency.adjacent_positions(new_pos):
				# TODO : mise en forme
				if all((
					adj_pos not in self.propagated_poss,
					adj_pos not in to_propagate_only_poss,
					self.propag_condition(self.board.get_tile(new_pos), self.board.get_tile(adj_pos))
				)):

					self.to_propagate_poss.append((dist+1, adj_pos))

			self.propag_dist = dist
			self._update_indicators(new_pos)
			return self.board.get_tile(new_pos)

		else:

			raise StopIteration


class BoardIteratorFindPath(BoardIteratorBase):

	def __init__(
		self, board,
		pos_start, pos_end,
		pass_through_condition=propag_cond_default
	):
	# FUTURE : pathfinding avec tous les shortest paths possibles.
	# pathfinding avec tous les paths possibles

		super().__init__(board)
		self.pass_through_condition = pass_through_condition
		pos_start = Pos(pos_start)
		pos_end = Pos(pos_end)
		self.pos_start = pos_start
		self.pos_end = pos_end

		iter_propag = BoardIteratorPropagation(
			self.board,
			self.pos_start,
			pass_through_condition)

		try:
			while pos_end not in iter_propag.propagated_poss:
				next(iter_propag)
		except StopIteration:
			self.path = None
			return

		propagated_poss = iter_propag.propagated_poss

		# Et maintenant, on parcourt la propagation à l'envers,
		# pour retrouver le chemin.
		pos_cur = pos_end
		dist_cur = propagated_poss[pos_cur]
		self.path = [ pos_cur ]

		while pos_cur != pos_start:

			advanced = False
			for adj_pos in self.board.adjacency.adjacent_positions(pos_cur):
				if (
					(propagated_poss.get(adj_pos, -2) == dist_cur - 1) and
					# TODO : faut vraiment s'affranchir de ce get_tile dégueulasse.
					pass_through_condition(self.board.get_tile(adj_pos), self.board.get_tile(pos_cur))
				):
					pos_cur = adj_pos
					dist_cur -= 1
					self.path.append(pos_cur)
					advanced = True
					break

			if not advanced:
				raise Exception("No adj pos with dist-1. Not supposed to happen")


	def __iter__(self):
		if self.path is None:
			# TODO : raiser une exception spécifique.
			# TODO : ou alors, faut signaler de manière moins violente que y'a pas de chemin.
			raise ValueError("Impossible de trouver un chemin")
		return self


	def __next__(self):
		if self.path:
			pos_path = self.path.pop()
			self._update_indicators(pos_path)
			# TODO : le __getitem__ doit pouvoir accepter des objets Pos.
			return self.board[pos_path.x, pos_path.y]
		else:
			raise StopIteration



# -*- coding: UTF-8 -*-




class IteratorGetDifferences(BoardIteratorBase):

	def __init__(
		self,
		board_iterator_1, board_iterator_2,
		func_comparison=lambda tile_1,tile_2:tile_1 == tile_2,
		check_disposition = True, check_quantity = True
	):
		# TODO : il faudrait qu'on puisse itérer directement sur les boards.
		# Sans avoir besoin de mettre "[:]".
		self.board_iterator_1 = board_iterator_1
		self.board_iterator_2 = board_iterator_2
		self.func_comparison = func_comparison
		self.check_disposition = check_disposition
		self.check_quantity = check_quantity


	def __iter__(self):
		return self


	def __next__(self):

		while True:

			try:
				tile_1 = next(self.board_iterator_1)
				finished_iter_1 = False
			except StopIteration:
				finished_iter_1 = True

			try:
				tile_2 = next(self.board_iterator_2)
				finished_iter_2 = False
			except StopIteration:
				finished_iter_2 = True

			if finished_iter_1 or finished_iter_2:
				if (finished_iter_1 != finished_iter_2) and self.check_quantity:
					# TODO : une classe d'exception custom.
					raise Exception("Nombre de tile différentes entre les deux itérateurs de tiles.")
				else:
					raise StopIteration

			if (self.board_iterator_1.both_coord_changed != self.board_iterator_2.both_coord_changed) and self.check_disposition:
				# TODO : une classe d'exception custom.
				raise Exception("Les tiles ne sont pas disposées de la même manière.")

			if not self.func_comparison(tile_1, tile_2):
				return (tile_1, tile_2)




ItInd = IterIndicator


def _fetch_indicators(obj_source, obj_dest):
	obj_dest.prev_pos = obj_source.prev_pos
	obj_dest.prev_prev_pos = obj_source.prev_prev_pos
	obj_dest.jumped = obj_source.jumped
	obj_dest.changed_direction = obj_source.changed_direction
	obj_dest.both_coord_changed = obj_source.both_coord_changed
	obj_dest.propag_dist = obj_source.propag_dist
	obj_dest.iter_indicators = obj_source.iter_indicators


class SurIteratorTellIndicators():

	def __init__(
		self,
		board_iterator,
		id_indic_to_tell=(ItInd.BOTH_COORD_CHANGED, )):

		self.board_iterator = board_iterator
		self.id_indic_to_tell = id_indic_to_tell


	def __iter__(self):
		return self


	def __next__(self):

		next_tile = next(self.board_iterator)
		_fetch_indicators(self.board_iterator, self)

		returned_infos = [
			self.iter_indicators[id_ind]
			for id_ind in self.id_indic_to_tell ]

		returned_infos.append(next_tile)
		return tuple(returned_infos)


group_by_subcoord=lambda board_iterator:board_iterator.both_coord_changed

class SurIteratorGroupTiles():

	def __init__(
		self,
		board_iterator,
		grouping_separator=group_by_subcoord
	):
		self.board_iterator = board_iterator
		self.grouping_separator = grouping_separator
		self.current_group_tiles = []
		self.next_tile = None


	def __iter__(self):
		# FUTURE : il faut faire une première pré-itération.
		# Et à chaque renvoi d'un nouveau groupe, on a également une itération d'avance.
		# C'est un peu étrange et je me demande s'il n'y aurait pas moyen de faire plus simple.
		self.next_tile = next(self.board_iterator)
		return self


	def __next__(self):

		if self.next_tile is None:
			raise StopIteration

		self.current_group_tiles.append(self.next_tile)
		finished_iterator = False

		try:
			self.next_tile = next(self.board_iterator)
		except StopIteration:
			finished_iterator = True

		while not self.grouping_separator(self.board_iterator) and not finished_iterator:
			self.current_group_tiles.append(self.next_tile)
			try:
				self.next_tile = next(self.board_iterator)
			except StopIteration:
				finished_iterator = True

		# TODO : à factoriser, mais après avoir testé le cas qui reste, à faire dans test_board_sur_iterator.
		if finished_iterator:
			self.next_tile = None
			returned_group_tiles = self.current_group_tiles
			self.current_group_tiles = []
			return returned_group_tiles
		else:
			returned_group_tiles = self.current_group_tiles
			self.current_group_tiles = []
			return returned_group_tiles


# autre sur_itérateur : emmagasiner toutes les tiles, jusqu'à répondre à une certaine condition.
# Quand ça arrive, ressortir les tiles emmagasinées, et ainsi de suite.
# (On les ressort sous forme d'un itérateur, ou d'une liste ? On va dire une liste)
# TODO : sortir les groupes de tile sous forme d'itérateur. Sans pré-itérer au départ.
# La "certaine condition", ce serait both_coord_changed. Mais on peut mettre autre chose, une lambda, etc.



class MobileItem():

	# TODO : les params, c'est totalement nawak. Faut arranger ça autrement.

	def __init__(
		self,
		board_owner=None, tile_owner=None, z_index=None,
		*args, **kwargs
	):
		self.tile_owner = None
		self.data = '#'
		self.move(board_owner, tile_owner, z_index, *args, **kwargs)


	def move(
		self,
		board_owner=None, tile_owner=None, z_index=None,
		*args, **kwargs
	):
		"""
		Param prioritaire : tile_owner.
		Sinon : les autres params.
		"""
		# FUTURE : j'ai plein de fonctions qui crée un pos à partir de args et kwargs.
		# Y'aurait peut-être moyen de le factoriser avec un décorateur.

		if self.tile_owner is not None:
			# --- suppression du mobitem de la tile où il était avant ---
			# Si self n'est pas mobile_items, ça va raiser une exception.
			# C'est ce qu'on veut, parce que not supposed to happen.
			index_myself = self.tile_owner.mobile_items.index(self)
			del self.tile_owner.mobile_items[index_myself]
			# --- définition éventuelle de board_owner, à partir de l'actuel board_owner ---
			if board_owner is None:
				board_owner = self.tile_owner.board_father

		# --- définition éventuelle de board_owner, à partir du nouveau tile_owner ---
		if tile_owner is not None:
			board_owner = tile_owner.board_father

		# --- définition éventuelle de tile_owner, à partir de board_owner et des param de pos ---
		if tile_owner is None and board_owner is not None:
			try:
				pos = Pos(*args, **kwargs)
				tile_owner = board_owner[pos]
			except:
				tile_owner = None

		# --- Enregistrement dans le nouveau tile_owner, si défini ---
		if tile_owner is not None:
			self.tile_owner = tile_owner
			if z_index is None:
				tile_owner.mobile_items.append(self)
			else:
				tile_owner.mobile_items.insert(z_index, self)


	def unlink(self):
		pass
		# TODO : c'est comme un move, mais avec tout à None.


	def render(self, w=1, h=1, chr_transparency=" "):
		return str(self.data)[:w]

# -*- coding: UTF-8 -*-



class BoardIndexError(IndexError):
	pass


class Board():

	# TODO : une fonction qui trouve un chemin passant par toutes les positions d'un
	# ensemble donné. (Si c'est possible).
	# Pour résoudre des problèmes "genre 4 elements".

	def __init__(
		self,
		w=1, h=1,
		class_tile=Tile,
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
			[ class_tile(x, y, self) for x in range(w) ]
			for y in range(h)
		]


	def _get_tile(self, x, y):
		try:
			return self._tiles[y][x]
		except IndexError:
			msg = "Coord not in board. coord : %s, %s. board size : %s, %s."
			data = (x, y, self.w, self.h)
			raise BoardIndexError(msg % data)


	def get_tile(self, *args, **kwargs):
		pos = Pos(*args, **kwargs)
		return self._get_tile(pos.x, pos.y)


	def __getitem__(self, args):
		# FUTURE : on a le droit de faire du *args, **kwargs avec getitem ?
		# Et ça donne quoi si on le fait ? À tester.

		if not args:
			return BoardIteratorRect(self)

		try:
			pos = Pos(args)
		except ValueError:
			pos = None

		if pos is not None:
			# Mode un seul élément
			return self._get_tile(pos.x, pos.y)

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

		# Mode fail
		raise Exception("TODO fail get item" + "".join(args))


	def __iter__(self):
		return BoardIteratorRect(self)


	def render(self, renderer=None):
		if renderer is None:
			renderer = self._default_renderer
		return renderer.render(self)


	def get_by_propagation(self, pos_start, propag_condition=propag_cond_default):
		return BoardIteratorPropagation(self, pos_start, propag_condition)


	def get_by_pathfinding(self, pos_start, pos_end, pass_through_condition=propag_cond_default):
		return BoardIteratorFindPath(self, pos_start, pos_end, pass_through_condition)


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

	# Une posis est une liste de pos. C'est tout. On peut itérer dessus. Et filtrer.
	# Avec la fonction built-in filter().


	def replace_tile(self, new_tile, pos):
		new_tile.x = pos.x
		new_tile.y = pos.y
		self._tiles[pos.y][pos.x] = new_tile


	def circular_permute_tiles(self, positions):
		"""
		positions est un itérable.
		"""

		made_first_iteration = False

		for pos in positions:
			if made_first_iteration:
				cur_pos = pos
				cur_tile = self._tiles[cur_pos.y][cur_pos.x]
				cur_tile.x = prev_pos.x
				cur_tile.y = prev_pos.y
				self._tiles[prev_pos.y][prev_pos.x] = cur_tile
				prev_pos = cur_pos
			else:
				first_pos = pos
				first_tile = self._tiles[first_pos.y][first_pos.x]
				prev_pos = first_pos
				made_first_iteration = True

		first_tile.x = pos.x
		first_tile.y = pos.y
		self._tiles[pos.y][pos.x] = first_tile


# ----------------- tests des trucs en cours ------------------
# TODO : (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

def main():


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

	b = Board(10, 10)
	mob = MobileItem(b, None, None, (3, 5))
	#log(b[11])
	#b[11, 5].data = 'Z'
	##log(b[11, ...])
	##log(b[..., 5])
	#log(b[11:18:2])
	#log(b[11:18:2, 1:33:5])
	#log(b[11:, :33])
	#log(b[:, ::5])
	#a=Pos(3, 4)
	#b[a].data = 'Y'
	log(b.render())
	log('-' * 40)
	print("before move")
	mob.move(None, None, None, (7, 4))
	log(b.render())

	log('End')


if __name__ == '__main__':
	main()

