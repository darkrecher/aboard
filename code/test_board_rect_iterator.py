# -*- coding: UTF-8 -*-


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


def test_simple_iteration():

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


def test_both_coord_changed_on_rect_iter():

       my_board_renderer = BoardRenderer(
               tile_w=2,
               tile_padding_w=1, tile_padding_h=1,
               chr_fill_tile='.')
       board = Board(2, 4, default_renderer=my_board_renderer)
       board_iter_rect = BoardIteratorRect(board)

       for index, tile in enumerate(board_iter_rect):
               DICT_MARKERS = {
                       False: '_',
                       True: 'B',
               }
               both_coord_marker = DICT_MARKERS[board_iter_rect.both_coord_changed]
               tile.data = str(index) + both_coord_marker

       render_result = """

               0B 1_

               2B 3_

               4B 5_

               6B 7_

       """
       assert strip_multiline(board.render()) == strip_multiline(render_result)
