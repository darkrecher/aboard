# -*- coding: UTF-8 -*-


from position import Point
from aboard import Board
from board_renderer import BoardRenderer
from positions_iterator import BoardIteratorRect, Coord


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_simple_iteration_main_x():

	board = Board(120, 120)
	slice_x = slice(1, 13, 3)
	slice_y = slice(15, 135, 30)

	positions_check = [
		(1, 15), (4, 15), (7, 15), (10, 15),
		(1, 45), (4, 45), (7, 45), (10, 45),
		(1, 75), (4, 75), (7, 75), (10, 75),
		(1, 105), (4, 105), (7, 105), (10, 105),
	]

	for tile in BoardIteratorRect(board, slice_x, slice_y):
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		position_check = positions_check.pop(0)
		assert point == position_check

	assert positions_check == []


def test_simple_iteration_main_y():

	board = Board(120, 120)
	slice_x = slice(1, 13, 3)
	slice_y = slice(15, 135, 30)

	positions_check = [
		(1, 15), (1, 45), (1, 75), (1, 105),
		(4, 15), (4, 45), (4, 75), (4, 105),
		(7, 15), (7, 45), (7, 75), (7, 105),
		(10, 15), (10, 45), (10, 75), (10, 105),
	]

	for tile in BoardIteratorRect(board, slice_x, slice_y, Coord.Y):
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		position_check = positions_check.pop(0)
		assert point == position_check

	assert positions_check == []


def test_iteration_all_board_render():

	board = Board(5, 2)

	for index, tile in enumerate(board):
		tile.data = index

	render_result = """

		01234
		56789

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_simple_iteration_render():

	board = Board(12, 6)
	board_iter_rect = BoardIteratorRect(board, slice(3, 7), slice(1, 7, 2))

	for index, tile in enumerate(board_iter_rect):
		tile.data = index

	render_result = """

		............
		...0123.....
		............
		...4567.....
		............
		...8911.....

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_iteration_all_board():

	board = Board(4, 5)
	board_iter_rect = BoardIteratorRect(board)

	for index, tile in enumerate(board_iter_rect):
		tile.data = chr(index+ord('A'))

	render_result = """

		ABCD
		EFGH
		IJKL
		MNOP
		QRST

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_iteration_rotated_and_reversed():

	board = Board(12, 6)
	board_iter_rect = BoardIteratorRect(
		board,
		slice(5, 1, -1),
		slice(None, 2, None),
		Coord.Y)

	for index, tile in enumerate(board_iter_rect):
		tile.data = index

	render_result = """

		..6420......
		..7531......
		............
		............
		............
		............

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_jump_and_dir_change():

	board = Board(10, 10)
	slice_x = slice(5)
	slice_y = slice(3)
	rect_iter = BoardIteratorRect(board, slice_x, slice_y)

	for tile in rect_iter:
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		if point == (0, 0):
			assert rect_iter.jumped == True
			assert rect_iter.changed_direction == False
			assert rect_iter.both_coord_changed == True
		elif point == (1, 0):
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == False
			assert rect_iter.both_coord_changed == False
		elif point.x == 0:
			assert rect_iter.jumped == True
			assert rect_iter.changed_direction == True
			assert rect_iter.both_coord_changed == True
		elif point.x == 1:
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == True
			assert rect_iter.both_coord_changed == False
		else:
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == False
			assert rect_iter.both_coord_changed == False


def test_both_coord_changed():

	my_board_renderer = BoardRenderer(
		tile_w=2,
		tile_padding_w=1, tile_padding_h=1,
		chr_fill_tile='.')
	board = Board(2, 4, default_renderer=my_board_renderer)
	board_iter_rect = BoardIteratorRect(board)

	DICT_MARKERS = {
		False: '_',
		True: 'B',
	}
	for index, tile in enumerate(board_iter_rect):
		both_coord_marker = DICT_MARKERS[board_iter_rect.both_coord_changed]
		tile.data = str(index) + both_coord_marker

	render_result = """

		0B 1_

		2B 3_

		4B 5_

		6B 7_

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_skip_lines():

	board = Board(10, 4)
	board_iter_rect = BoardIteratorRect(board)

	for index, tile in enumerate(board_iter_rect):
		char_data = chr(index+ord('A'))
		if char_data in ('D', 'V', 'Z'):
			board_iter_rect.skip_line()
		tile.data = char_data

	render_result = """

		ABCD......
		EFGHIJKLMN
		OPQRSTUV..
		WXYZ......

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
