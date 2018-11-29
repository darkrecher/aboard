from point import Point
from aboard import Board
from positions_iterator import BoardIteratorRect, BoardIteratorPositions, ItInd


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


def test_sur_iter_tell_both_coord_changed():

	board = Board(3, 2)

	for both_coord_changed, tile in BoardIteratorRect(board).tell_indicators():
		if tile.x == 0:
			assert both_coord_changed == True
		else:
			assert both_coord_changed == False


def test_sur_iter_tell_everything():

	itind_everything = (
		ItInd.PREV_POINT,
		ItInd.PREV_PREV_POINT,
		ItInd.JUMPED,
		ItInd.CHANGED_DIRECTION,
		ItInd.BOTH_COORD_CHANGED,
	)

	board = Board(20, 20)
	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(9, 0) ]

	prev_positions = [ None ] + positions
	prev_prev_positions = [ None, None ] + positions

	for iter_everything in BoardIteratorPositions(board, positions).tell_indicators(itind_everything):

		print(iter_everything)

		(prev_point, prev_prev_point, jumped, changed_direction, both_coord_changed, tile) = iter_everything

		check_prev_point = prev_positions.pop(0)
		check_prev_prev_point = prev_prev_positions.pop(0)
		assert prev_point == check_prev_point
		assert prev_prev_point == check_prev_prev_point

		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)

		if point == (1, 2):
			assert jumped == True
			assert changed_direction == False
			assert both_coord_changed == True
		elif point == (2, 4):
			assert jumped == False
			assert changed_direction == True
			assert both_coord_changed == False
		elif point == (5, 4):
			assert jumped == True
			assert changed_direction == False
		elif point == (9, 0):
			assert jumped == True
			assert changed_direction == True
			assert both_coord_changed == True
		else:
			assert jumped == False
			assert changed_direction == False
			assert both_coord_changed == False


def test_sur_iter_group_by_simple():

	board = Board(5, 8)
	y_coord = 0

	for tile_group in BoardIteratorRect(board).group_by_subcoord():
		print(*map(str, tile_group))
		check_coords = [ (x, y_coord) for x in range(5) ]
		for tile, check_coord in zip(tile_group, check_coords):
			assert tile.point == check_coord
		y_coord += 1

	assert y_coord == 8


def test_sur_iter_groub_by_dir_changes():

	board = Board(10, 10)
	positions = [
		(1, 2), (1, 3), (1, 4), (1, 5),
		(2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
		(7, 6), (6, 7), (5, 8), (4, 9),
		(3, 8), (2, 7), (1, 6), (0, 5),
	 ]

	group_marker = 'a'

	for tile_group in BoardIteratorPositions(board, positions).group_by(lambda b:b.changed_direction):
		print(*map(str, tile_group))
		tile_group[0].data = group_marker.upper()
		for tile in tile_group[1:]:
			tile.data = group_marker
		group_marker = chr(ord(group_marker) + 1)

	render_result = """

		..........
		..........
		.A........
		.a........
		.a........
		daBbbbbbb.
		.d.....C..
		..d...c...
		...D.c....
		....c.....

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)


# TODO : tester un cas où la fonction de séparation renvoie True sur la dernière tile.
