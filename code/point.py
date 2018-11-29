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


class Point():

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

		try:
			print(param_1, param_2, x, y)
		except:
			pass
		raise ValueError("Impossible de déduire des coordonnées.")


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
		return '<Point %s, %s >' % (str(self.x), str(self.y))


	def as_tuple(self):
		return self.x, self.y


	def as_dict(self):
		return {'x': self.x, 'y': self.y }


	def __eq__(self, other):
		point_other = Point(other)
		return self.x == point_other.x and self.y == point_other.y


# --- Direction operations ---

def cmp(a, b):
	# https://stackoverflow.com/questions/15556813/python-why-cmp-is-useful
	return (a > b) - (a < b)

def compute_direction(point_1, point_2):
	cmp_x = cmp(point_2.x, point_1.x)
	cmp_y = cmp(point_2.y, point_1.y)
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

