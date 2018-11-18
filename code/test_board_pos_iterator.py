# -*- coding: UTF-8 -*-


from aboard import Board
from board_renderer import BoardRenderer
from positions_iterator import BoardIteratorPositions


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
	board_iter_positions = BoardIteratorPositions(board, positions)

	for index, tile in enumerate(board_iter_positions):
		tile.data = index

	render_result = """

		..........
		........7.
		.0........
		.1........
		.234.56...
		..........

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_both_coord_changed():

	positions = [
		(0, 0), (0, 2), (2, 2),
		(1, 1), (1, 0),
		(3, 3), (0, 3) ]

	my_board_renderer = BoardRenderer(
		tile_w=2,
		tile_padding_w=1, tile_padding_h=1,
		chr_fill_tile='.')
	board = Board(4, 5, default_renderer=my_board_renderer)
	board_iter_positions = BoardIteratorPositions(board, positions)

	for index, tile in enumerate(board_iter_positions):
		DICT_MARKERS = {
			False: '_',
			True: 'B',
		}
		both_coord_marker = DICT_MARKERS[board_iter_positions.both_coord_changed]
		tile.data = str(index) + both_coord_marker

	# Pour la toute première itération, both_coord_changed est à True.
	# On considère que le curseur passe de (rien, rien) à (0, 0), et que les deux coords changent.
	render_result = """

		0B 4_ .. ..

		.. 3B .. ..

		1_ .. 2_ ..

		6_ .. .. 5B

		.. .. .. ..

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
	board_iter_positions = BoardIteratorPositions(board, positions)

	for index, tile in enumerate(board_iter_positions):
		DICT_JUMP_DIR = {
			(False, False): '_',
			(True, False): 'J',
			(False, True): 'D',
			(True, True): 'X',
		}
		jump_dir_marker = DICT_JUMP_DIR[ (
			board_iter_positions.jumped,
			board_iter_positions.changed_direction) ]
		tile.data = str(index) + jump_dir_marker

	render_result = """

		.. .. .. .. .. .. .. .. .. ..

		.. .. .. .. .. .. .. .. 7X ..

		.. 0J .. .. .. .. .. .. .. ..

		.. 1_ .. .. .. .. .. .. .. ..

		.. 2_ 3D 4_ .. 5J 6_ .. .. ..

		.. .. .. .. .. .. .. .. .. ..


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)

