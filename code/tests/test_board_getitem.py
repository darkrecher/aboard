# -*- coding: UTF-8 -*-


from aboard import Board, BoardIndexError
from point import Point
from board_renderer import BoardRenderer


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_getitem_one_elem():

	board = Board(9, 5)
	board[0, 0].data = '\\'
	board[4, 0].data = '^'
	board[8, 0].data = '/'
	board[0, 2].data = '<'
	board[4, 2].data = '+'
	board[8, 2].data = '>'
	board[0, 4].data = 'L'
	board[4, 4].data = 'V'
	board[8, 4].data = 'J'

	render_result = """

		\...^.../
		.........
		<...+...>
		.........
		L...V...J

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_one_elem_negative_coords():

	board = Board(9, 5)
	board[-9, -5].data = '{'
	board[-8, -5].data = '('
	board[-9, -4].data = '['
	board[-1, 0].data = '"'
	board[0, -1].data = '\''
	board[-5, 2].data = '#'
	board[-1, -2].data = ']'
	board[-2, -1].data = ')'
	board[-1, -1].data = '}'

	render_result = """

		{(......"
		[........
		....#....
		........]
		'......)}

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_point():

	board = Board(3, 3)
	p = Point(1, 0)
	board[p].data = '|'
	board[Point(0, -2)].data = '-'
	board[Point(-2, 1)].data = '*'
	board[Point(-1, -2)].data = '~'
	board[{'x':1, 'y':2}].data = 'I'

	render_result = """

		.|.
		-*~
		.I.

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_fail():

	board = Board(5, 14)
	failed_at_failing = False

	try:
		a = board[0, 14]
		failed_at_failing = True
	except BoardIndexError as e:
		print(e)
	try:
		p=Point(5, 0)
		a = board[p]
		failed_at_failing = True
	except BoardIndexError as e:
		print(e)
	try:
		a = board[0, -15]
		failed_at_failing = True
	except BoardIndexError as e:
		print(e)
	try:
		p=Point(-6, 0)
		a = board[p]
		failed_at_failing = True
	except BoardIndexError as e:
		print(e)

	assert failed_at_failing == False


def test_getitem_square():

	board = Board(10, 6)

	for index, tile in enumerate(board[3:7,2:5]):
		tile.data = hex(index)[2]

	render_result = """

		..........
		..........
		...0123...
		...4567...
		...89ab...
		..........

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_stepped():

	board = Board(8, 13)

	for index, tile in enumerate(board[::3,::4]):
		tile.data = hex(index)[2]

	render_result = """

		0..1..2.
		........
		........
		........
		3..4..5.
		........
		........
		........
		6..7..8.
		........
		........
		........
		9..a..b.

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_all():

	board = Board(2, 3)

	for index, tile in enumerate(board[:]):
		tile.data = hex(index)[2]

	render_result = """

		01
		23
		45

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_all_on_y():

	board = Board(5, 3)

	for index, tile in enumerate(board[:,:,'y']):
		tile.data = hex(index)[2]

	render_result = """

		0369c
		147ad
		258be

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_one_line():

	board = Board(8, 8)

	for index, tile in enumerate(board[:,6]):
		tile.data = hex(index)[2]

	render_result = """

		........
		........
		........
		........
		........
		........
		01234567
		........

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_one_column():

	board = Board(8, 8)

	for index, tile in enumerate(board[5]):
		tile.data = hex(index)[2]

	render_result = """

		.....0..
		.....1..
		.....2..
		.....3..
		.....4..
		.....5..
		.....6..
		.....7..

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_square_reversed_stepped_on_y():

	board = Board(12, 13)

	for index, tile in enumerate(board[ 9:2:-3, 11:3:-2, 'y' ]):
		tile.data = hex(index)[2]

	render_result = """

		............
		............
		............
		............
		............
		...b..7..3..
		............
		...a..6..2..
		............
		...9..5..1..
		............
		...8..4..0..
		............

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_square_reversed_stepped_on_y_grouped():

	my_board_renderer = BoardRenderer(tile_w=2)

	board = Board(12, 13, default_renderer=my_board_renderer)

	for group_index, column in enumerate(board[ 9:2:-3, 11:3:-2, 'y' ].group_by_subcoord()):
		for index, tile in enumerate(column):
			tile.data = chr(group_index + ord('A')) + str(index)

	render_result = """

		. . . . . . . . . . . .
		. . . . . . . . . . . .
		. . . . . . . . . . . .
		. . . . . . . . . . . .
		. . . . . . . . . . . .
		. . . C3. . B3. . A3. .
		. . . . . . . . . . . .
		. . . C2. . B2. . A2. .
		. . . . . . . . . . . .
		. . . C1. . B1. . A1. .
		. . . . . . . . . . . .
		. . . C0. . B0. . A0. .
		. . . . . . . . . . . .

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_square_neg_coords():

	board = Board(8, 8)

	for index, tile in enumerate(board[-5:-2, -7:-3]):
		tile.data = hex(index)[2]

	render_result = """

		........
		...012..
		...345..
		...678..
		...9ab..
		........
		........
		........

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_square_reversed_all():

	board = Board(3, 2)

	for index, tile in enumerate(board[::-1, ::-1]):
		tile.data = hex(index)[2]

	render_result = """

		543
		210

	"""
	print(board.render())
	assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_getitem_fail_step_zero():

	board = Board(1, 1)
	failed_at_failing = False
	try:
		for t in board[::0]:pass
		failed_at_failing = True
	except ValueError as e:
		print(e)
	try:
		for t in board[:, ::0]:pass
		failed_at_failing = True
	except ValueError as e:
		print(e)
	assert failed_at_failing == False

