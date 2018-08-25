# -*- coding: UTF-8 -*-


from aboard import Board
from board_renderer import BoardRenderer
from positions_iterator import RectIterator, Coord
from board_iterator import BoardRectIterator


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_simple_iteration():

	board = Board(12, 6)
	board_rect_iterator = BoardRectIterator(
		board,
		RectIterator(slice(3, 7), slice(1, 7, 2)))

	for index, point in enumerate(board_rect_iterator):
		point.data = index

	render_result = """

		............
		...0123.....
		............
		...4567.....
		............
		...8911.....

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_iteration_rotated_and_reversed():

	board = Board(12, 6)
	board_rect_iterator = BoardRectIterator(
		board,
		RectIterator(slice(5, 1, -1), slice(None, 2, None), Coord.Y))

	for index, point in enumerate(board_rect_iterator):
		point.data = index

	render_result = """

		..6420......
		..7531......
		............
		............
		............
		............

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
