# -*- coding: UTF-8 -*-


from aboard import Board
from board_renderer import BoardRenderer
from positions_iterator import PositionsIterator
from board_iterator import BoardIterator


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_simple_iteration():

	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(8, 1) ]

	board = Board(10, 6)
	board_iterator = BoardIterator(
		board,
		PositionsIterator(positions))

	for index, point in enumerate(board_iterator):
		point.data = index

	render_result = """

		..........
		........7.
		.0........
		.1........
		.234.56...
		..........

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_iteration_jumped_changed_directions():

	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(8, 1) ]

	my_board_renderer = BoardRenderer(
		tile_w=2,
		tile_padding_w=1, tile_padding_h=1,
		chr_fill_tile='.')
	board = Board(10, 6, default_renderer=my_board_renderer)
	board_iterator = BoardIterator(
		board,
		PositionsIterator(positions))

	for index, point in enumerate(board_iterator):
		DICT_JUMP_DIR = {
			(False, False): '_',
			(True, False): 'J',
			(False, True): 'D',
			(True, True): 'X',
		}
		jump_dir_marker = DICT_JUMP_DIR[ (
			board_iterator.jumped,
			board_iterator.changed_direction) ]
		point.data = str(index) + jump_dir_marker

	render_result = """

		.. .. .. .. .. .. .. .. .. ..

		.. .. .. .. .. .. .. .. 7X ..

		.. 0J .. .. .. .. .. .. .. ..

		.. 1_ .. .. .. .. .. .. .. ..

		.. 2_ 3D 4_ .. 5J 6_ .. .. ..

		.. .. .. .. .. .. .. .. .. ..


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)

