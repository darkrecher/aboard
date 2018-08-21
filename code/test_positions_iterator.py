# -*- coding: UTF-8 -*-

from positions_iterator import PositionsIterator


def test_simple_iteration():

	positions = [ (1, 2), (3, 4), (5, 6), (7, 8) ]

	for point_elem in PositionsIterator(positions):
		check_elem = positions.pop(0)
		assert point_elem == check_elem


def test_jumps_and_dir_changes():

	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(9, 0) ]

	pos_iterator = PositionsIterator(positions)

	for point in pos_iterator:
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

