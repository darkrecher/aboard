# -*- coding: UTF-8 -*-

from aboard import Board
from propagation_iterator import BoardIteratorPropagation, BoardIteratorFindPath
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

	for pos in BoardIteratorPropagation(board, (4, 4)):
		print(pos)
		board.get_tile(pos).data = 'o'
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


def test_propagation_simple_2():

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

	for pos in board.get_by_propagation((4, 4)):
		print(pos)
		board.get_tile(pos).data = 'o'
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

	for pos in propag_iter:
		board.get_tile(pos).data = propag_iter.propag_dist

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

	for propag_dist, pos in BoardIteratorPropagation(board, (1, 3), can_propag).tell_indicators((ItInd.PROPAG_DIST, )):
		board.get_tile(pos).data = propag_dist

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


def test_find_path_simple():

	board = Board(15, 10, class_adjacency=AdjacencyEvaluatorCross)
	iter_find_path = BoardIteratorFindPath(board, (3, 2), (6, 9))

	for index, tile in enumerate(iter_find_path):
		tile.data = hex(index)[2]

	print(board.render())

	render_result = """

		...............
		...............
		...0123........
		......4........
		......5........
		......6........
		......7........
		......8........
		......9........
		......a........

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_find_path_simple_2():

	board = Board(15, 10, class_adjacency=AdjacencyEvaluatorCross)
	iter_find_path = board.get_by_pathfinding((3, 2), (6, 9))

	for index, tile in enumerate(iter_find_path):
		tile.data = hex(index)[2]

	print(board.render())

	render_result = """

		...............
		...............
		...0123........
		......4........
		......5........
		......6........
		......7........
		......8........
		......9........
		......a........

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_find_path_obstacle():

	board = Board(15, 10, class_adjacency=AdjacencyEvaluatorCross)

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
	pos_start = (5, 2)
	pos_end = (4, 9)

	for index, tile in enumerate(BoardIteratorFindPath(board, pos_start, pos_end)):
		tile.data = hex(index)[2]

	render_result = """

		...............
		...............
		.....012.......
		..*****3.......
		..*...*4.......
		..*...*5.......
		..*.***6.......
		..*.*987.......
		..***a.........
		....cb.........

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_find_path_no_path():

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
	pos_start = (5, 4)
	pos_end = (0, 9)

	path_found = True
	try:
		for index, tile in enumerate(BoardIteratorFindPath(board, pos_start, pos_end)):
			tile.data = 'o'
		print(board.render())
	except ValueError:
		path_found = False

	assert path_found == False

