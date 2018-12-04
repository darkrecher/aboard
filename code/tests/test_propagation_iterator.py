# -*- coding: UTF-8 -*-

from aboard import Board
from propagation_iterator import BoardIteratorPropagation
from adjacency import AdjacencyEvaluatorCross
from iter_indicators import ItInd


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_propagation_simple():

	board = Board(15, 10)
	# TODO : il faudra faire une init du board from input. Pour que ce soit plus compréhensible.
	pos_walls = [
		(2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
		(6, 4), (6, 5), (6, 6),
		(5, 6), (4, 6),
		(4, 7), (4, 8),
		(3, 8), (2, 8),
		(2, 7), (2, 6), (2, 5), (2, 4),
	]
	for pos in pos_walls:
		board.get_tile(pos).data = '*'
	print(board.render())

	for point in BoardIteratorPropagation(board, (4, 4)):
		print(point)
		board.get_tile(point).data = 'o'
	print(board.render())

	render_result = """

		...............
		...............
		...............
		..*****........
		..*ooo*........
		..*ooo*........
		..*o***........
		..*o*..........
		..***..........
		...............

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_propagation_dist():

	board = Board(15, 10, class_adjacency=AdjacencyEvaluatorCross)

	def can_propag(source, dest):
		return any((
			dest.x < 7 and dest.y < 6,
			dest.y == 3,
			dest.x == 2
		))

	propag_iter = BoardIteratorPropagation(board, (4, 4), can_propag)

	for point in propag_iter:
		board.get_tile(point).data = propag_iter.propag_dist

	print(board.render())

	render_result = """

		8765456........
		7654345........
		6543234........
		543212345678911
		4321012........
		5432123........
		..4............
		..5............
		..6............
		..7............

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_propagation_dist_with_iter():

	board = Board(15, 10)

	def can_propag(source, dest):
		return any((
			dest.x < 7 and dest.y < 6,
			dest.y == 3,
			dest.x == 2
		))

	for propag_dist, point in BoardIteratorPropagation(board, (1, 3), can_propag).tell_indicators((ItInd.PROPAG_DIST, )):
		board.get_tile(point).data = propag_dist

	print(board.render())

	render_result = """

		3333345........
		2222345........
		1112345........
		101234567891111
		1112345........
		2222345........
		..3............
		..4............
		..5............
		..6............

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)

# TODO : test propagation montrant qu'on passe aussi en diagonale.
# TODO : test avec des adjacences toriques.
# TODO : test avec une condition de propagation plus compliquée. (impliquant source et dest).


