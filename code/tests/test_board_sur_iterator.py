from positions_iterator import BoardIteratorRect, BoardIteratorPositions
from aboard import Board


def test_sur_iter_tell_both_coord_changed():

	board = Board(3, 2)

	for both_coord_changed, tile in BoardIteratorRect(board).tell_indicators():
		if tile.x == 0:
			assert both_coord_changed == True
		else:
			assert both_coord_changed == False


def test_sur_iter_tell_everything():

	# TODO
	assert False

	board = Board(20, 20)
	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(9, 0) ]

	pos_iterator = BoardIteratorPositions(board, positions)

	for tile in pos_iterator:
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		if point == (1, 2):
			assert pos_iterator.jumped == True
			assert pos_iterator.changed_direction == False
		elif point == (2, 4):
			assert pos_iterator.jumped == False
			assert pos_iterator.changed_direction == True
		elif point == (5, 4):
			assert pos_iterator.jumped == True
			assert pos_iterator.changed_direction == False
		elif point == (9, 0):
			assert pos_iterator.jumped == True
			assert pos_iterator.changed_direction == True
		else:
			assert pos_iterator.jumped == False
			assert pos_iterator.changed_direction == False
