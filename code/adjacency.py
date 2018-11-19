# -*- coding: UTF-8 -*-

class AdjacencyEvaluator():

	def __init__(self, board):
		self.board = board

	def is_adjacent(self, point_1, point_2):
		raise NotImplemented


class AdjacencyEvaluatorCross(AdjacencyEvaluator):

	def is_adjacent(self, point_1, point_2):
		if point_1.x == point_2.x:
			return point_1.y-point_2.y in (-1, 1)
		if point_1.y == point_2.y:
			return point_1.x-point_2.x in (-1, 1)
		return False


class AdjacencyEvaluatorCrossDiag(AdjacencyEvaluator):

	def is_adjacent(self, point_1, point_2):
		abs_diff_x = abs(point_1.x-point_2.x)
		abs_diff_y = abs(point_1.y-point_2.y)
		return (
			(abs_diff_x, abs_diff_y) != (0, 0)
			and abs_diff_x <= 1
			and abs_diff_y <= 1
		)


# TODO : les adjacences toriques. Avec les tests qui vont bien.
# TODO : un itérateur dans chaque classe, renvoyant les point adjacents au point passés en paramètre.
#        (et faudrait checker en même temps si les points sont valides. Vu qu'on a le board, autant le faire ici).
#        (un itérateur qui renvoie que les valides, et un qui renvoie des None sur les pas valides).


class_default_adjacency = AdjacencyEvaluatorCross


def set_default_adjacency(new_class_default_adjacency):
	global class_default_adjacency
	class_default_adjacency = new_class_default_adjacency
