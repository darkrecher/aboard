# -*- coding: UTF-8 -*-

# TODO : dans un autre fichier

from enum import Enum

class Direction(Enum):
	UP = 0
	UP_RIGHT = 1
	RIGHT = 2
	DOWN_RIGHT = 3
	DOWN = 4
	DOWN_LEFT = 5
	LEFT = 6
	UP_LEFT = 7
	# TODO etc
	NORTH = 0
	EAST = 2
	SOUTH = 4
	WEST = 6
	# re etc
	NE = 1
	# Avec PAD_8, PAD_9, etc.


def is_adjacent_cross(point_1, point_2):
	if point_1.x == point_2.x:
		return -1 <= point_1.y-point_2.y <= 1
	if point_1.y == point_2.y:
		return -1 <= point_1.x-point_2.x <= 1
	return False


def is_adjacent_diag(point_1, point_2):
	return -1 <= point_1.x-point_2.x <= 1 and -1 <= point_1.y-point_2.y <= 1


default_adjacency=is_adjacent_cross


def set_default_adjacency(new_default_adjacency):
	global default_adjacency
	default_adjacency = new_default_adjacency


def is_adjacent(point_1, point_2):
	return default_adjacency(point_1, point_2)


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

