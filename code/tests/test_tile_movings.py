# -*- coding: UTF-8 -*-


from point import Point
from tile import Tile
from aboard import Board
from board_renderer import BoardRenderer


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_replace_simple():

	board = Board(5, 3)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO')
	board.set_data_from_string(setting_data)
	new_tile = Tile()
	new_tile.data = 'Z'

	board.replace_tile(new_tile, Point(3, 1))
	print(board.render())

	assert new_tile.x == 3
	assert new_tile.y == 1
	assert board[3, 1].data == 'Z'

	render_result = """

		ABCDE
		FGHZJ
		KLMNO

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
	print(board.render())


def test_permute_simple():

	board = Board(5, 3)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO')
	board.set_data_from_string(setting_data)

	tile_with_c = board[2, 0]
	tile_with_n = board[3, 2]

	board.circular_permute_tiles([Point(2, 0), Point(3, 2)])
	print(board.render())

	assert tile_with_c.x == 3
	assert tile_with_c.y == 2
	assert tile_with_c.data == 'C'
	assert board[3, 2].data == 'C'

	assert tile_with_n.x == 2
	assert tile_with_n.y == 0
	assert tile_with_n.data == 'N'
	assert board[2, 0].data == 'N'

	render_result = """

		ABNDE
		FGHIJ
		KLMCO

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_permute_column():

	board = Board(5, 7)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY', '01234', '56789')
	board.set_data_from_string(setting_data)

	pos_lines = [ Point(tile.x, tile.y) for tile in board[2, :] ]

	board.circular_permute_tiles(pos_lines)
	print(board.render())

	render_result = """

		ABHDE
		FGMIJ
		KLRNO
		PQWST
		UV2XY
		01734
		56C89


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


# TODO : Test de push, dans les 4 directions. Parce qu'il le faut pour Xmas Rush.


