# -*- coding: UTF-8 -*-


from position import Pos
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

	board.replace_tile(new_tile, Pos(3, 1))

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

	board.circular_permute_tiles([Pos(2, 0), Pos(3, 2)])
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

	pos_to_permute = [ Pos(tile.x, tile.y) for tile in board[2, :] ]
	assert len(pos_to_permute) == 7

	board.circular_permute_tiles(pos_to_permute)
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
	# Pour vérifier que la fonction de permutation ne vide pas la liste.
	# Ça le faisait avant, et c'était mal.
	assert len(pos_to_permute) == 7


def test_push_cols_lines():
	"""
	Test de déplacement de toutes les tiles d'une ligne ou d'une colonne,
	en ajoutant une nouvelle tile qui va pousser les autres.
	Comme dans le jeu de plateau 'Labyrinthe', et dans le challenge CodinGame 'Xmas Rush'
	"""

	# PUSH 3 RIGHT

	board = Board(5, 7)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY', '01234', '56789')
	board.set_data_from_string(setting_data)

	added_tile = Tile()
	added_tile.data = '#'
	pos_to_permute = [ Pos(tile.x, tile.y) for tile in board[::-1, 3] ]

	board.circular_permute_tiles(pos_to_permute)
	removed_tile = board[0, 3]
	board.replace_tile(added_tile, Pos(0, 3))
	print(board.render())

	assert removed_tile.data == 'T'

	render_result = """

		ABCDE
		FGHIJ
		KLMNO
		#PQRS
		UVWXY
		01234
		56789


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
	print("")

	# PUSH 0 LEFT

	board = Board(5, 7)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY', '01234', '56789')
	board.set_data_from_string(setting_data)

	added_tile = Tile()
	added_tile.data = '#'
	pos_to_permute = [ Pos(tile.x, tile.y) for tile in board[:, 0] ]

	board.circular_permute_tiles(pos_to_permute)
	removed_tile = board[4, 0]
	board.replace_tile(added_tile, Pos(4, 0))
	print(board.render())

	assert removed_tile.data == 'A'

	render_result = """

		BCDE#
		FGHIJ
		KLMNO
		PQRST
		UVWXY
		01234
		56789


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
	print("")

	# PUSH 4 DOWN

	board = Board(5, 7)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY', '01234', '56789')
	board.set_data_from_string(setting_data)

	added_tile = Tile()
	added_tile.data = '#'
	pos_to_permute = [ Pos(tile.x, tile.y) for tile in board[4, ::-1] ]

	board.circular_permute_tiles(pos_to_permute)
	removed_tile = board[4, 0]
	board.replace_tile(added_tile, Pos(4, 0))
	print(board.render())

	assert removed_tile.data == '9'

	render_result = """

		ABCD#
		FGHIE
		KLMNJ
		PQRSO
		UVWXT
		0123Y
		56784


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
	print("")

	# PUSH 1 UP

	board = Board(5, 7)
	setting_data = ('ABCDE', 'FGHIJ', 'KLMNO', 'PQRST', 'UVWXY', '01234', '56789')
	board.set_data_from_string(setting_data)

	added_tile = Tile()
	added_tile.data = '#'
	pos_to_permute = [ Pos(tile.x, tile.y) for tile in board[1, :] ]

	board.circular_permute_tiles(pos_to_permute)
	removed_tile = board[1, board.h-1]
	board.replace_tile(added_tile, Pos(1, board.h-1))
	print(board.render())

	assert removed_tile.data == 'B'

	render_result = """

		AGCDE
		FLHIJ
		KQMNO
		PVRST
		U1WXY
		06234
		5#789


	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)
	print("")


