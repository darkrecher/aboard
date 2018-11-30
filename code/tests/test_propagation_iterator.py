# -*- coding: UTF-8 -*-

from aboard import Board
from propagation_iterator import BoardIteratorPropagation


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


# TODO : test avec la distance de propagation à la tile de départ.