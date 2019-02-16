# -*- coding: UTF-8 -*-


from position import Pos
from aboard import Board
from board_renderer import BoardRenderer
from positions_iterator import BoardIteratorPositions


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# plus lisiblement les strings des résultats attendus.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_simple_iteration_check_pos():

	board = Board(20, 20)
	positions = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
	check_positions = list(positions)

	for tile in BoardIteratorPositions(board, positions):
		# TODO : choper direct le pos à partir de la tile, quand ce sera possible.
		pos = Pos(tile.x, tile.y)
		print(pos)
		check_pos = check_positions.pop(0)
		assert pos == check_pos

	assert check_positions == []


def test_simple_iteration_render():

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


def test_both_coord_changed_render():

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


def test_jump_and_dir_change_check_indic():

	board = Board(20, 20)
	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(9, 0) ]

	pos_iterator = BoardIteratorPositions(board, positions)

	for tile in pos_iterator:
		# TODO : choper direct le pos à partir de la tile, quand ce sera possible.
		pos = Pos(tile.x, tile.y)
		if pos == (1, 2):
			assert pos_iterator.jumped == True
			assert pos_iterator.changed_direction == False
		elif pos == (2, 4):
			assert pos_iterator.jumped == False
			assert pos_iterator.changed_direction == True
		elif pos == (5, 4):
			assert pos_iterator.jumped == True
			assert pos_iterator.changed_direction == False
		elif pos == (9, 0):
			assert pos_iterator.jumped == True
			assert pos_iterator.changed_direction == True
		else:
			assert pos_iterator.jumped == False
			assert pos_iterator.changed_direction == False


def test_jump_and_dir_change_render():

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

