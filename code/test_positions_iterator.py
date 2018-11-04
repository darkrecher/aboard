# -*- coding: UTF-8 -*-

from point import Point
from aboard import Board
from positions_iterator import BoardIteratorPositions


def test_simple_iteration():

	board = Board(20, 20)
	positions = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
	check_positions = list(positions)

	for tile in BoardIteratorPositions(board, positions):
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		check_pos = check_positions.pop(0)
		assert point == check_pos

	assert check_positions == []


def test_jumps_and_dir_changes():

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

