from point import Point
from aboard import Board
from positions_iterator import BoardIteratorRect, BoardIteratorPositions, ItInd


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

